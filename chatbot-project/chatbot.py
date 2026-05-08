#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║          ███╗   ███╗██╗   ██╗     █████╗ ██╗                                    ║
║          ████╗ ████║╚██╗ ██╔╝    ██╔══██╗██║                                    ║
║          ██╔████╔██║ ╚████╔╝     ███████║██║                                    ║
║          ██║╚██╔╝██║  ╚██╔╝      ██╔══██║██║                                    ║
║          ██║ ╚═╝ ██║   ██║       ██║  ██║██║                                    ║
║          ╚═╝     ╚═╝   ╚═╝       ╚═╝  ╚═╝╚═╝                                    ║
║                                                                                  ║
║                    ██████╗██╗  ██╗ █████╗ ████████╗██████╗  ██████╗ ████████╗  ║
║                   ██╔════╝██║  ██║██╔══██╗╚══██╔══╝██╔══██╗██╔═══██╗╚══██╔══╝  ║
║                   ██║     ███████║███████║   ██║   ██████╔╝██║   ██║   ██║     ║
║                   ██║     ██╔══██║██╔══██║   ██║   ██╔══██╗██║   ██║   ██║     ║
║                   ╚██████╗██║  ██║██║  ██║   ██║   ██████╔╝╚██████╔╝   ██║     ║
║                    ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═════╝  ╚═════╝    ╚═╝     ║
║                                                                                  ║
║                         A Fully-Featured AI Chatbot Engine                      ║
║                              Built with ❤️  by You                               ║
║                                   Version 3.0.0                                 ║
╚══════════════════════════════════════════════════════════════════════════════════╝

FEATURES:
  ✦ Multi-provider AI support (OpenAI, Anthropic Claude, Google Gemini, Cohere, Ollama)
  ✦ Persistent memory & long-term conversation history (SQLite)
  ✦ Rich persona system with custom AI personalities
  ✦ Plugin architecture for extensible commands
  ✦ Real-time streaming responses
  ✦ File & image input support
  ✦ Token usage tracking & cost estimation
  ✦ Conversation export (JSON, Markdown, PDF-ready HTML)
  ✦ Context window management & summarization
  ✦ Rate limiting & retry logic
  ✦ Colorized terminal UI with rich formatting
  ✦ Web search tool integration (optional)
  ✦ Voice output support (optional TTS)
  ✦ Session management (save, load, fork)
  ✦ Moderation & safety filters
  ✦ Async-ready architecture

REQUIREMENTS (install via pip):
  pip install openai anthropic google-generativeai cohere rich prompt_toolkit
  pip install requests tiktoken colorama aiohttp tenacity pydantic

OPTIONAL:
  pip install gtts pygame  # for text-to-speech
  pip install pillow       # for image handling
"""

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import asyncio
import base64
import datetime
import hashlib
import inspect
import io
import json
import logging
import math
import mimetypes
import os
import platform
import re
import shutil
import signal
import sqlite3
import sys
import tempfile
import textwrap
import threading
import time
import traceback
import uuid
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from contextlib import contextmanager, suppress
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import lru_cache, wraps
from pathlib import Path
from typing import (
    Any, AsyncGenerator, Callable, Dict, Generator,
    Iterator, List, Optional, Sequence, Tuple, Type, Union
)

# ─────────────────────────────────────────────────────────────────────────────
# OPTIONAL DEPENDENCY HANDLING
# ─────────────────────────────────────────────────────────────────────────────

def _try_import(module_name: str, package_name: Optional[str] = None):
    """Gracefully attempt to import a module, returning None on failure."""
    try:
        import importlib
        return importlib.import_module(module_name)
    except ImportError:
        pkg = package_name or module_name
        logging.debug(f"Optional dependency '{pkg}' not installed. Some features disabled.")
        return None

rich        = _try_import("rich")
openai_mod  = _try_import("openai")
anthropic_m = _try_import("anthropic")
genai       = _try_import("google.generativeai", "google-generativeai")
cohere_mod  = _try_import("cohere")
tiktoken    = _try_import("tiktoken")
requests    = _try_import("requests")
tenacity    = _try_import("tenacity")
pydantic    = _try_import("pydantic")
gtts_mod    = _try_import("gtts")
pygame_mod  = _try_import("pygame")

# Rich console setup
if rich:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.prompt import Prompt, Confirm
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.syntax import Syntax
    from rich.live import Live
    from rich.columns import Columns
    from rich import box
    console = Console()
else:
    # Minimal fallback console
    class _FallbackConsole:
        def print(self, *args, **kwargs): print(*args)
        def rule(self, *args, **kwargs): print("─" * 60)
        def log(self, *args, **kwargs): print(*args)
    console = _FallbackConsole()

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION & CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

APP_NAME        = "My AI Chatbot"
APP_VERSION     = "3.0.0"
APP_AUTHOR      = "You"
APP_DESCRIPTION = "A powerful, feature-rich AI chatbot built from scratch."

# Default config path
CONFIG_DIR  = Path.home() / ".my_ai_chatbot"
CONFIG_FILE = CONFIG_DIR / "config.json"
DB_FILE     = CONFIG_DIR / "history.db"
LOG_FILE    = CONFIG_DIR / "chatbot.log"
EXPORT_DIR  = CONFIG_DIR / "exports"
PLUGIN_DIR  = CONFIG_DIR / "plugins"

# Ensure dirs exist
for _dir in [CONFIG_DIR, EXPORT_DIR, PLUGIN_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)

# Pricing per 1K tokens (approximate, USD) — update as needed
PRICING_TABLE: Dict[str, Dict[str, float]] = {
    "gpt-4o":                  {"input": 0.005,  "output": 0.015},
    "gpt-4o-mini":             {"input": 0.00015,"output": 0.0006},
    "gpt-4-turbo":             {"input": 0.01,   "output": 0.03},
    "gpt-3.5-turbo":           {"input": 0.0005, "output": 0.0015},
    "claude-opus-4-20250514":      {"input": 0.015,  "output": 0.075},
    "claude-sonnet-4-20250514":    {"input": 0.003,  "output": 0.015},
    "claude-haiku-4-5-20251001": {"input": 0.00025,"output": 0.00125},
    "gemini-1.5-pro":          {"input": 0.00125,"output": 0.005},
    "gemini-1.5-flash":        {"input": 0.000075,"output":0.0003},
    "command-r-plus":          {"input": 0.003,  "output": 0.015},
}

# Context window limits (tokens)
CONTEXT_LIMITS: Dict[str, int] = {
    "gpt-4o":                  128_000,
    "gpt-4o-mini":             128_000,
    "gpt-4-turbo":             128_000,
    "gpt-3.5-turbo":            16_000,
    "claude-opus-4-20250514":      200_000,
    "claude-sonnet-4-20250514":    200_000,
    "claude-haiku-4-5-20251001": 200_000,
    "gemini-1.5-pro":        1_000_000,
    "gemini-1.5-flash":      1_000_000,
    "command-r-plus":          128_000,
    "ollama/llama3":             8_192,
    "ollama/mistral":            8_192,
    "ollama/phi3":               4_096,
}

# ─────────────────────────────────────────────────────────────────────────────
# ENUMS & DATA STRUCTURES
# ─────────────────────────────────────────────────────────────────────────────

class Role(str, Enum):
    SYSTEM    = "system"
    USER      = "user"
    ASSISTANT = "assistant"
    TOOL      = "tool"

class Provider(str, Enum):
    OPENAI    = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE    = "google"
    COHERE    = "cohere"
    OLLAMA    = "ollama"
    MOCK      = "mock"  # for testing without API keys

class ExportFormat(str, Enum):
    JSON     = "json"
    MARKDOWN = "markdown"
    HTML     = "html"
    TEXT     = "text"

class MessageStatus(str, Enum):
    PENDING  = "pending"
    COMPLETE = "complete"
    ERROR    = "error"
    FILTERED = "filtered"

@dataclass
class TokenUsage:
    prompt_tokens:     int = 0
    completion_tokens: int = 0
    total_tokens:      int = 0

    @property
    def cost_usd(self) -> float:
        return getattr(self, "_cost", 0.0)

    def set_cost(self, model: str) -> None:
        pricing = PRICING_TABLE.get(model, {"input": 0.0, "output": 0.0})
        cost = (self.prompt_tokens / 1000 * pricing["input"] +
                self.completion_tokens / 1000 * pricing["output"])
        object.__setattr__(self, "_cost", cost) if False else setattr(self, "_cost", cost)

    def __add__(self, other: "TokenUsage") -> "TokenUsage":
        return TokenUsage(
            self.prompt_tokens     + other.prompt_tokens,
            self.completion_tokens + other.completion_tokens,
            self.total_tokens      + other.total_tokens,
        )


@dataclass
class Attachment:
    """Represents a file or image attached to a message."""
    filename:   str
    mime_type:  str
    data:       bytes
    description: Optional[str] = None

    @classmethod
    def from_path(cls, path: Union[str, Path]) -> "Attachment":
        p = Path(path)
        mime, _ = mimetypes.guess_type(str(p))
        mime = mime or "application/octet-stream"
        return cls(filename=p.name, mime_type=mime, data=p.read_bytes())

    @property
    def base64_data(self) -> str:
        return base64.b64encode(self.data).decode()

    @property
    def is_image(self) -> bool:
        return self.mime_type.startswith("image/")

    @property
    def is_text(self) -> bool:
        return self.mime_type.startswith("text/")

    def as_text(self) -> str:
        if self.is_text:
            return self.data.decode("utf-8", errors="replace")
        return f"[Binary file: {self.filename} ({self.mime_type})]"


@dataclass
class Message:
    """A single chat message with full metadata."""
    id:          str          = field(default_factory=lambda: str(uuid.uuid4()))
    role:        Role         = Role.USER
    content:     str          = ""
    timestamp:   datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    model:       Optional[str] = None
    usage:       Optional[TokenUsage] = None
    status:      MessageStatus = MessageStatus.COMPLETE
    attachments: List[Attachment] = field(default_factory=list)
    metadata:    Dict[str, Any]   = field(default_factory=dict)
    parent_id:   Optional[str]    = None  # for branching conversations

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":        self.id,
            "role":      self.role.value,
            "content":   self.content,
            "timestamp": self.timestamp.isoformat(),
            "model":     self.model,
            "metadata":  self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Message":
        return cls(
            id        = d.get("id", str(uuid.uuid4())),
            role      = Role(d["role"]),
            content   = d["content"],
            timestamp = datetime.datetime.fromisoformat(d.get("timestamp", datetime.datetime.utcnow().isoformat())),
            model     = d.get("model"),
            metadata  = d.get("metadata", {}),
        )

    def word_count(self) -> int:
        return len(self.content.split())

    def char_count(self) -> int:
        return len(self.content)

    def estimated_tokens(self) -> int:
        # Rough estimate: ~4 chars per token
        return math.ceil(len(self.content) / 4)


@dataclass
class Session:
    """A conversation session with full history."""
    id:          str   = field(default_factory=lambda: str(uuid.uuid4()))
    name:        str   = "Untitled Session"
    created_at:  datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    updated_at:  datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    messages:    List[Message]     = field(default_factory=list)
    persona_id:  Optional[str]     = None
    model:       Optional[str]     = None
    provider:    Optional[str]     = None
    total_usage: TokenUsage        = field(default_factory=TokenUsage)
    tags:        List[str]         = field(default_factory=list)
    summary:     Optional[str]     = None
    is_archived: bool              = False

    def add_message(self, msg: Message) -> None:
        self.messages.append(msg)
        self.updated_at = datetime.datetime.utcnow()
        if msg.usage:
            self.total_usage = self.total_usage + msg.usage

    def get_context_messages(self, max_tokens: int = 4000) -> List[Message]:
        """Return recent messages fitting within a token budget."""
        selected = []
        token_count = 0
        for msg in reversed(self.messages):
            est = msg.estimated_tokens()
            if token_count + est > max_tokens and selected:
                break
            selected.insert(0, msg)
            token_count += est
        return selected

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":         self.id,
            "name":       self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "messages":   [m.to_dict() for m in self.messages],
            "persona_id": self.persona_id,
            "model":      self.model,
            "provider":   self.provider,
            "tags":       self.tags,
            "summary":    self.summary,
        }

    def message_count(self) -> int:
        return len(self.messages)

    def user_message_count(self) -> int:
        return sum(1 for m in self.messages if m.role == Role.USER)

    def duration_str(self) -> str:
        delta = self.updated_at - self.created_at
        secs = int(delta.total_seconds())
        if secs < 60: return f"{secs}s"
        if secs < 3600: return f"{secs//60}m {secs%60}s"
        return f"{secs//3600}h {(secs%3600)//60}m"


@dataclass
class Persona:
    """An AI personality/character configuration."""
    id:            str
    name:          str
    description:   str
    system_prompt: str
    avatar:        str  = "🤖"
    voice:         Optional[str] = None
    temperature:   float = 0.7
    max_tokens:    int   = 2048
    tags:          List[str] = field(default_factory=list)

    # Built-in personas
    @classmethod
    def default_personas(cls) -> List["Persona"]:
        return [
            cls(
                id="default",
                name="Assistant",
                description="A helpful, harmless, and honest AI assistant.",
                system_prompt=(
                    "You are a helpful, harmless, and honest AI assistant. "
                    "You answer questions clearly, truthfully, and concisely. "
                    "If you don't know something, you say so."
                ),
                avatar="🤖",
                temperature=0.7,
            ),
            cls(
                id="coder",
                name="Code Wizard",
                description="Expert programmer across all languages and frameworks.",
                system_prompt=(
                    "You are Code Wizard, an expert software engineer with deep knowledge "
                    "of Python, JavaScript, TypeScript, Rust, Go, C++, and many other languages. "
                    "You write clean, efficient, well-documented code. You explain your reasoning "
                    "clearly and suggest best practices. Always include error handling. "
                    "Format code blocks with proper syntax highlighting."
                ),
                avatar="🧙‍♂️",
                temperature=0.3,
                tags=["coding", "technical"],
            ),
            cls(
                id="tutor",
                name="Professor",
                description="Patient, thorough educator who explains complex topics simply.",
                system_prompt=(
                    "You are Professor, a brilliant and patient educator. You excel at breaking "
                    "down complex topics into simple, digestible explanations. You use analogies, "
                    "examples, and real-world applications. You ask clarifying questions and "
                    "tailor your explanations to the student's level. You encourage curiosity."
                ),
                avatar="🎓",
                temperature=0.6,
                tags=["education", "learning"],
            ),
            cls(
                id="creative",
                name="Muse",
                description="Creative writing partner, storyteller, and idea generator.",
                system_prompt=(
                    "You are Muse, a wildly creative writing partner with an expansive imagination. "
                    "You help with stories, poems, scripts, worldbuilding, and brainstorming. "
                    "You're evocative, descriptive, and emotionally resonant. You push creative "
                    "boundaries while respecting the user's vision. You offer multiple creative "
                    "directions and aren't afraid to be unconventional."
                ),
                avatar="🎨",
                temperature=0.95,
                tags=["creative", "writing"],
            ),
            cls(
                id="analyst",
                name="Analyst",
                description="Data-driven, analytical thinker for research and problem solving.",
                system_prompt=(
                    "You are Analyst, a rigorous and methodical thinker. You approach problems "
                    "with structured reasoning, evidence-based thinking, and clear logic. You excel "
                    "at research synthesis, pro/con analysis, decision frameworks, and identifying "
                    "assumptions. You're direct, precise, and cite sources when possible. "
                    "You use numbered lists, tables, and clear structure in your responses."
                ),
                avatar="📊",
                temperature=0.2,
                tags=["analysis", "research"],
            ),
            cls(
                id="therapist",
                name="Sage",
                description="Empathetic listener and supportive conversational companion.",
                system_prompt=(
                    "You are Sage, a warm, empathetic, and non-judgmental conversational companion. "
                    "You listen deeply, reflect back what you hear, and offer gentle perspectives. "
                    "You validate emotions and help people feel heard. You ask thoughtful questions. "
                    "Important: you are NOT a licensed therapist. For serious mental health concerns, "
                    "always encourage professional help. You provide emotional support, not medical advice."
                ),
                avatar="🌿",
                temperature=0.8,
                tags=["wellness", "support"],
            ),
            cls(
                id="debater",
                name="Socrates",
                description="Challenges ideas through Socratic questioning and rigorous debate.",
                system_prompt=(
                    "You are Socrates, a sharp intellectual who engages in rigorous debate and "
                    "Socratic questioning. You challenge assumptions, probe for inconsistencies, "
                    "steelman opposing views, and help people think more critically. You're direct, "
                    "intellectually honest, and willing to take controversial positions to advance "
                    "the argument. You cite historical examples and philosophical precedents."
                ),
                avatar="⚖️",
                temperature=0.75,
                tags=["debate", "philosophy"],
            ),
        ]


# ─────────────────────────────────────────────────────────────────────────────
# DATABASE LAYER
# ─────────────────────────────────────────────────────────────────────────────

class Database:
    """SQLite persistence layer for sessions, messages, and settings."""

    SCHEMA = """
    CREATE TABLE IF NOT EXISTS sessions (
        id          TEXT PRIMARY KEY,
        name        TEXT NOT NULL,
        created_at  TEXT NOT NULL,
        updated_at  TEXT NOT NULL,
        persona_id  TEXT,
        model       TEXT,
        provider    TEXT,
        tags        TEXT DEFAULT '[]',
        summary     TEXT,
        is_archived INTEGER DEFAULT 0,
        metadata    TEXT DEFAULT '{}'
    );

    CREATE TABLE IF NOT EXISTS messages (
        id              TEXT PRIMARY KEY,
        session_id      TEXT NOT NULL,
        role            TEXT NOT NULL,
        content         TEXT NOT NULL,
        timestamp       TEXT NOT NULL,
        model           TEXT,
        status          TEXT DEFAULT 'complete',
        prompt_tokens   INTEGER DEFAULT 0,
        completion_tokens INTEGER DEFAULT 0,
        total_tokens    INTEGER DEFAULT 0,
        cost_usd        REAL DEFAULT 0.0,
        metadata        TEXT DEFAULT '{}',
        parent_id       TEXT,
        FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS personas (
        id             TEXT PRIMARY KEY,
        name           TEXT NOT NULL,
        description    TEXT,
        system_prompt  TEXT NOT NULL,
        avatar         TEXT DEFAULT '🤖',
        temperature    REAL DEFAULT 0.7,
        max_tokens     INTEGER DEFAULT 2048,
        tags           TEXT DEFAULT '[]',
        created_at     TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS settings (
        key   TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS token_stats (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        date            TEXT NOT NULL,
        model           TEXT NOT NULL,
        prompt_tokens   INTEGER DEFAULT 0,
        completion_tokens INTEGER DEFAULT 0,
        cost_usd        REAL DEFAULT 0.0
    );

    CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id);
    CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);
    CREATE INDEX IF NOT EXISTS idx_sessions_updated ON sessions(updated_at);
    CREATE INDEX IF NOT EXISTS idx_token_stats_date ON token_stats(date);
    """

    def __init__(self, db_path: Union[str, Path] = DB_FILE):
        self.db_path = str(db_path)
        self._local = threading.local()
        self._init_db()

    @property
    def conn(self) -> sqlite3.Connection:
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = sqlite3.connect(self.db_path)
            self._local.conn.row_factory = sqlite3.Row
            self._local.conn.execute("PRAGMA journal_mode=WAL")
            self._local.conn.execute("PRAGMA foreign_keys=ON")
        return self._local.conn

    def _init_db(self) -> None:
        with self.conn:
            self.conn.executescript(self.SCHEMA)

    def close(self) -> None:
        if hasattr(self._local, "conn") and self._local.conn:
            self._local.conn.close()
            self._local.conn = None

    # ── Session CRUD ──────────────────────────────────────────────────────────

    def save_session(self, session: Session) -> None:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO sessions
                (id, name, created_at, updated_at, persona_id, model, provider,
                 tags, summary, is_archived)
                VALUES (?,?,?,?,?,?,?,?,?,?)
            """, (
                session.id, session.name,
                session.created_at.isoformat(), session.updated_at.isoformat(),
                session.persona_id, session.model, session.provider,
                json.dumps(session.tags), session.summary, int(session.is_archived),
            ))

    def load_session(self, session_id: str) -> Optional[Session]:
        row = self.conn.execute(
            "SELECT * FROM sessions WHERE id=?", (session_id,)
        ).fetchone()
        if not row:
            return None
        session = Session(
            id         = row["id"],
            name       = row["name"],
            created_at = datetime.datetime.fromisoformat(row["created_at"]),
            updated_at = datetime.datetime.fromisoformat(row["updated_at"]),
            persona_id = row["persona_id"],
            model      = row["model"],
            provider   = row["provider"],
            tags       = json.loads(row["tags"] or "[]"),
            summary    = row["summary"],
            is_archived= bool(row["is_archived"]),
        )
        session.messages = self.load_messages(session_id)
        return session

    def list_sessions(self, archived: bool = False, limit: int = 50) -> List[Dict]:
        rows = self.conn.execute("""
            SELECT s.*, COUNT(m.id) as msg_count
            FROM sessions s
            LEFT JOIN messages m ON m.session_id = s.id
            WHERE s.is_archived = ?
            GROUP BY s.id
            ORDER BY s.updated_at DESC
            LIMIT ?
        """, (int(archived), limit)).fetchall()
        return [dict(r) for r in rows]

    def delete_session(self, session_id: str) -> bool:
        with self.conn:
            self.conn.execute("DELETE FROM sessions WHERE id=?", (session_id,))
        return True

    def search_sessions(self, query: str) -> List[Dict]:
        rows = self.conn.execute("""
            SELECT DISTINCT s.id, s.name, s.updated_at
            FROM sessions s
            JOIN messages m ON m.session_id = s.id
            WHERE m.content LIKE ? OR s.name LIKE ?
            ORDER BY s.updated_at DESC
            LIMIT 20
        """, (f"%{query}%", f"%{query}%")).fetchall()
        return [dict(r) for r in rows]

    # ── Message CRUD ──────────────────────────────────────────────────────────

    def save_message(self, session_id: str, msg: Message) -> None:
        usage = msg.usage or TokenUsage()
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO messages
                (id, session_id, role, content, timestamp, model, status,
                 prompt_tokens, completion_tokens, total_tokens, cost_usd, metadata, parent_id)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                msg.id, session_id, msg.role.value, msg.content,
                msg.timestamp.isoformat(), msg.model, msg.status.value,
                usage.prompt_tokens, usage.completion_tokens, usage.total_tokens,
                getattr(usage, "_cost", 0.0),
                json.dumps(msg.metadata), msg.parent_id,
            ))

    def load_messages(self, session_id: str) -> List[Message]:
        rows = self.conn.execute("""
            SELECT * FROM messages WHERE session_id=? ORDER BY timestamp ASC
        """, (session_id,)).fetchall()
        messages = []
        for row in rows:
            usage = TokenUsage(
                prompt_tokens=row["prompt_tokens"],
                completion_tokens=row["completion_tokens"],
                total_tokens=row["total_tokens"],
            )
            msg = Message(
                id        = row["id"],
                role      = Role(row["role"]),
                content   = row["content"],
                timestamp = datetime.datetime.fromisoformat(row["timestamp"]),
                model     = row["model"],
                status    = MessageStatus(row["status"]),
                usage     = usage,
                metadata  = json.loads(row["metadata"] or "{}"),
                parent_id = row["parent_id"],
            )
            messages.append(msg)
        return messages

    def search_messages(self, query: str, session_id: Optional[str] = None) -> List[Dict]:
        if session_id:
            rows = self.conn.execute("""
                SELECT m.*, s.name as session_name FROM messages m
                JOIN sessions s ON s.id = m.session_id
                WHERE m.content LIKE ? AND m.session_id = ?
                ORDER BY m.timestamp DESC LIMIT 50
            """, (f"%{query}%", session_id)).fetchall()
        else:
            rows = self.conn.execute("""
                SELECT m.*, s.name as session_name FROM messages m
                JOIN sessions s ON s.id = m.session_id
                WHERE m.content LIKE ?
                ORDER BY m.timestamp DESC LIMIT 50
            """, (f"%{query}%",)).fetchall()
        return [dict(r) for r in rows]

    # ── Settings ──────────────────────────────────────────────────────────────

    def get_setting(self, key: str, default: Any = None) -> Any:
        row = self.conn.execute(
            "SELECT value FROM settings WHERE key=?", (key,)
        ).fetchone()
        if row:
            try:
                return json.loads(row["value"])
            except (json.JSONDecodeError, TypeError):
                return row["value"]
        return default

    def set_setting(self, key: str, value: Any) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO settings (key, value) VALUES (?,?)",
                (key, json.dumps(value))
            )

    def get_all_settings(self) -> Dict[str, Any]:
        rows = self.conn.execute("SELECT key, value FROM settings").fetchall()
        result = {}
        for row in rows:
            try:
                result[row["key"]] = json.loads(row["value"])
            except (json.JSONDecodeError, TypeError):
                result[row["key"]] = row["value"]
        return result

    # ── Token Stats ───────────────────────────────────────────────────────────

    def record_usage(self, model: str, usage: TokenUsage) -> None:
        today = datetime.date.today().isoformat()
        cost  = getattr(usage, "_cost", 0.0)
        with self.conn:
            self.conn.execute("""
                INSERT INTO token_stats (date, model, prompt_tokens, completion_tokens, cost_usd)
                VALUES (?,?,?,?,?)
            """, (today, model, usage.prompt_tokens, usage.completion_tokens, cost))

    def get_usage_summary(self, days: int = 30) -> List[Dict]:
        cutoff = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
        rows = self.conn.execute("""
            SELECT date, model,
                   SUM(prompt_tokens) as prompt_tokens,
                   SUM(completion_tokens) as completion_tokens,
                   SUM(cost_usd) as cost_usd
            FROM token_stats
            WHERE date >= ?
            GROUP BY date, model
            ORDER BY date DESC
        """, (cutoff,)).fetchall()
        return [dict(r) for r in rows]

    def get_total_cost(self) -> float:
        row = self.conn.execute(
            "SELECT SUM(cost_usd) as total FROM token_stats"
        ).fetchone()
        return float(row["total"] or 0)

    # ── Personas ──────────────────────────────────────────────────────────────

    def save_persona(self, persona: Persona) -> None:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO personas
                (id, name, description, system_prompt, avatar, temperature, max_tokens, tags, created_at)
                VALUES (?,?,?,?,?,?,?,?,?)
            """, (
                persona.id, persona.name, persona.description,
                persona.system_prompt, persona.avatar, persona.temperature,
                persona.max_tokens, json.dumps(persona.tags),
                datetime.datetime.utcnow().isoformat(),
            ))

    def load_persona(self, persona_id: str) -> Optional[Persona]:
        row = self.conn.execute(
            "SELECT * FROM personas WHERE id=?", (persona_id,)
        ).fetchone()
        if not row:
            return None
        return Persona(
            id=row["id"], name=row["name"], description=row["description"],
            system_prompt=row["system_prompt"], avatar=row["avatar"],
            temperature=row["temperature"], max_tokens=row["max_tokens"],
            tags=json.loads(row["tags"] or "[]"),
        )

    def list_personas(self) -> List[Dict]:
        rows = self.conn.execute("SELECT * FROM personas ORDER BY name ASC").fetchall()
        return [dict(r) for r in rows]


# ─────────────────────────────────────────────────────────────────────────────
# AI PROVIDER BACKENDS
# ─────────────────────────────────────────────────────────────────────────────

class AIBackend(ABC):
    """Abstract base class for all AI provider backends."""

    def __init__(self, model: str, api_key: Optional[str] = None):
        self.model   = model
        self.api_key = api_key

    @abstractmethod
    def complete(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = False,
        **kwargs,
    ) -> Union[Message, Generator[str, None, None]]:
        """Send messages and return a response (or stream tokens)."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if this backend is configured and usable."""
        ...

    def format_messages(self, messages: List[Message]) -> List[Dict]:
        """Default: convert Message list to API-standard dicts."""
        return [{"role": m.role.value, "content": m.content} for m in messages]

    @property
    def provider_name(self) -> str:
        return self.__class__.__name__.replace("Backend", "")


class MockBackend(AIBackend):
    """A local mock backend for testing without API keys."""

    RESPONSES = [
        "That's a fascinating question! Let me think about it...\n\nBased on my analysis, I'd say the answer involves multiple factors. First, we need to consider the context. Second, let's examine the underlying assumptions. In conclusion, the most likely explanation is that this depends heavily on your specific situation.",
        "Great point! Here's what I know about this topic:\n\n1. **Key insight one**: This is fundamental to understanding the problem.\n2. **Key insight two**: This often gets overlooked but is critically important.\n3. **Key insight three**: Putting these together gives us a complete picture.\n\nDoes that help clarify things?",
        "I understand what you're asking. This is actually a well-studied area!\n\nThe short answer is: it depends. The long answer requires understanding that there are trade-offs involved. The best approach typically balances efficiency with clarity, and practicality with idealism.\n\nWhat aspect would you like me to elaborate on?",
        "Interesting! Let me give you a thorough response.\n\n```python\ndef example():\n    # Here's how you might approach this programmatically\n    result = process_input(data)\n    return result\n```\n\nThis pattern is commonly used because it's both readable and efficient.",
        "I appreciate you sharing that with me. Here's my perspective:\n\nThe topic you've raised touches on some deep questions. Historically, people have approached this in several ways. Modern thinking suggests a more nuanced view that takes into account individual context and systemic factors.\n\nWould you like to explore any particular angle further?",
    ]

    def __init__(self, model: str = "mock-model", **kwargs):
        super().__init__(model)
        self._response_index = 0

    def is_available(self) -> bool:
        return True

    def complete(self, messages, system_prompt=None, temperature=0.7,
                 max_tokens=2048, stream=False, **kwargs):
        # Simulate a small delay
        time.sleep(0.3)
        last_user = next(
            (m.content for m in reversed(messages) if m.role == Role.USER), ""
        )
        # Echo-style responses for specific inputs
        if any(kw in last_user.lower() for kw in ["hello", "hi", "hey"]):
            text = "Hello! I'm your AI assistant (running in mock mode — no API key needed). How can I help you today?"
        elif "?" in last_user:
            text = self.RESPONSES[self._response_index % len(self.RESPONSES)]
            self._response_index += 1
        else:
            text = f"I received your message: \"{last_user[:80]}{'...' if len(last_user)>80 else ''}\"\n\nIn mock mode, I echo back a simulated response. Configure a real API key to get actual AI responses!"

        usage = TokenUsage(
            prompt_tokens=sum(m.estimated_tokens() for m in messages),
            completion_tokens=len(text.split()),
            total_tokens=sum(m.estimated_tokens() for m in messages) + len(text.split()),
        )
        if stream:
            def _gen():
                for word in text.split(" "):
                    yield word + " "
                    time.sleep(0.02)
            return _gen()

        msg = Message(role=Role.ASSISTANT, content=text, model=self.model, usage=usage)
        return msg


class OpenAIBackend(AIBackend):
    """OpenAI GPT backend (GPT-4o, GPT-4-turbo, GPT-3.5-turbo, etc.)"""

    def __init__(self, model: str = "gpt-4o", api_key: Optional[str] = None):
        super().__init__(model, api_key or os.getenv("OPENAI_API_KEY"))
        self._client = None

    def _get_client(self):
        if self._client is None:
            if openai_mod is None:
                raise ImportError("openai package not installed. Run: pip install openai")
            self._client = openai_mod.OpenAI(api_key=self.api_key)
        return self._client

    def is_available(self) -> bool:
        return bool(self.api_key) and openai_mod is not None

    def complete(self, messages, system_prompt=None, temperature=0.7,
                 max_tokens=2048, stream=False, **kwargs):
        client = self._get_client()
        api_messages = []
        if system_prompt:
            api_messages.append({"role": "system", "content": system_prompt})
        for m in messages:
            if m.attachments and any(a.is_image for a in m.attachments):
                content = [{"type": "text", "text": m.content}]
                for att in m.attachments:
                    if att.is_image:
                        content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{att.mime_type};base64,{att.base64_data}"
                            }
                        })
                api_messages.append({"role": m.role.value, "content": content})
            else:
                api_messages.append({"role": m.role.value, "content": m.content})

        if stream:
            def _stream_gen():
                resp = client.chat.completions.create(
                    model=self.model, messages=api_messages,
                    temperature=temperature, max_tokens=max_tokens, stream=True,
                )
                for chunk in resp:
                    delta = chunk.choices[0].delta
                    if delta.content:
                        yield delta.content
            return _stream_gen()

        resp = client.chat.completions.create(
            model=self.model, messages=api_messages,
            temperature=temperature, max_tokens=max_tokens,
        )
        choice = resp.choices[0]
        usage  = TokenUsage(
            prompt_tokens=resp.usage.prompt_tokens,
            completion_tokens=resp.usage.completion_tokens,
            total_tokens=resp.usage.total_tokens,
        )
        usage.set_cost(self.model)
        return Message(
            role=Role.ASSISTANT,
            content=choice.message.content,
            model=self.model,
            usage=usage,
        )


class AnthropicBackend(AIBackend):
    """Anthropic Claude backend."""

    def __init__(self, model: str = "claude-sonnet-4-20250514", api_key: Optional[str] = None):
        super().__init__(model, api_key or os.getenv("ANTHROPIC_API_KEY"))
        self._client = None

    def _get_client(self):
        if self._client is None:
            if anthropic_m is None:
                raise ImportError("anthropic package not installed. Run: pip install anthropic")
            self._client = anthropic_m.Anthropic(api_key=self.api_key)
        return self._client

    def is_available(self) -> bool:
        return bool(self.api_key) and anthropic_m is not None

    def complete(self, messages, system_prompt=None, temperature=0.7,
                 max_tokens=2048, stream=False, **kwargs):
        client = self._get_client()
        api_messages = []
        for m in messages:
            if m.role == Role.SYSTEM:
                continue  # Claude uses system param separately
            if m.attachments:
                content = [{"type": "text", "text": m.content}]
                for att in m.attachments:
                    if att.is_image:
                        content.append({
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": att.mime_type,
                                "data": att.base64_data,
                            }
                        })
                api_messages.append({"role": m.role.value, "content": content})
            else:
                api_messages.append({"role": m.role.value, "content": m.content})

        kwargs_extra = {}
        if system_prompt:
            kwargs_extra["system"] = system_prompt

        if stream:
            def _stream_gen():
                with client.messages.stream(
                    model=self.model, messages=api_messages,
                    temperature=temperature, max_tokens=max_tokens, **kwargs_extra,
                ) as s:
                    for text in s.text_stream:
                        yield text
            return _stream_gen()

        resp = client.messages.create(
            model=self.model, messages=api_messages,
            temperature=temperature, max_tokens=max_tokens, **kwargs_extra,
        )
        content = resp.content[0].text if resp.content else ""
        usage = TokenUsage(
            prompt_tokens=resp.usage.input_tokens,
            completion_tokens=resp.usage.output_tokens,
            total_tokens=resp.usage.input_tokens + resp.usage.output_tokens,
        )
        usage.set_cost(self.model)
        return Message(role=Role.ASSISTANT, content=content, model=self.model, usage=usage)


class GoogleBackend(AIBackend):
    """Google Gemini backend."""

    def __init__(self, model: str = "gemini-1.5-flash", api_key: Optional[str] = None):
        super().__init__(model, api_key or os.getenv("GOOGLE_API_KEY"))
        self._model_obj = None

    def _get_model(self):
        if self._model_obj is None:
            if genai is None:
                raise ImportError("google-generativeai not installed. Run: pip install google-generativeai")
            genai.configure(api_key=self.api_key)
            self._model_obj = genai.GenerativeModel(self.model)
        return self._model_obj

    def is_available(self) -> bool:
        return bool(self.api_key) and genai is not None

    def complete(self, messages, system_prompt=None, temperature=0.7,
                 max_tokens=2048, stream=False, **kwargs):
        model = self._get_model()
        # Build conversation history
        history = []
        for m in messages[:-1]:
            if m.role == Role.SYSTEM:
                continue
            role = "user" if m.role == Role.USER else "model"
            history.append({"role": role, "parts": [m.content]})
        last_msg = messages[-1].content if messages else ""
        chat = model.start_chat(history=history)
        gen_cfg = {"temperature": temperature, "max_output_tokens": max_tokens}

        if stream:
            resp = chat.send_message(last_msg, generation_config=gen_cfg, stream=True)
            def _gen():
                for chunk in resp:
                    if chunk.text:
                        yield chunk.text
            return _gen()

        resp = chat.send_message(last_msg, generation_config=gen_cfg)
        text = resp.text
        # Gemini doesn't provide detailed token counts in basic API
        approx_tokens = len(text.split()) + sum(len(m.content.split()) for m in messages)
        usage = TokenUsage(prompt_tokens=approx_tokens//2, completion_tokens=len(text.split()),
                           total_tokens=approx_tokens)
        return Message(role=Role.ASSISTANT, content=text, model=self.model, usage=usage)


class OllamaBackend(AIBackend):
    """Ollama local model backend (runs models locally)."""

    def __init__(self, model: str = "llama3", base_url: str = "http://localhost:11434"):
        super().__init__(model)
        self.base_url = base_url

    def is_available(self) -> bool:
        if requests is None:
            return False
        try:
            r = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return r.status_code == 200
        except Exception:
            return False

    def complete(self, messages, system_prompt=None, temperature=0.7,
                 max_tokens=2048, stream=False, **kwargs):
        if requests is None:
            raise ImportError("requests package not installed.")
        api_msgs = []
        if system_prompt:
            api_msgs.append({"role": "system", "content": system_prompt})
        api_msgs.extend({"role": m.role.value, "content": m.content} for m in messages)

        payload = {
            "model": self.model,
            "messages": api_msgs,
            "stream": stream,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }
        if stream:
            resp = requests.post(f"{self.base_url}/api/chat", json=payload, stream=True, timeout=120)
            def _gen():
                for line in resp.iter_lines():
                    if line:
                        data = json.loads(line)
                        if "message" in data and "content" in data["message"]:
                            yield data["message"]["content"]
            return _gen()

        resp = requests.post(f"{self.base_url}/api/chat", json=payload, timeout=120)
        data = resp.json()
        text = data.get("message", {}).get("content", "")
        usage = TokenUsage(
            prompt_tokens=data.get("prompt_eval_count", 0),
            completion_tokens=data.get("eval_count", 0),
            total_tokens=data.get("prompt_eval_count", 0) + data.get("eval_count", 0),
        )
        return Message(role=Role.ASSISTANT, content=text, model=f"ollama/{self.model}", usage=usage)


# ─────────────────────────────────────────────────────────────────────────────
# PLUGIN SYSTEM
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class CommandResult:
    """The result of executing a chatbot command."""
    output:    str  = ""
    success:   bool = True
    exit_chat: bool = False
    new_session: bool = False

class Plugin(ABC):
    """Base class for all chatbot plugins/commands."""

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def description(self) -> str: ...

    @property
    def aliases(self) -> List[str]:
        return []

    @property
    def usage(self) -> str:
        return f"/{self.name}"

    @abstractmethod
    def execute(self, args: str, chatbot: "Chatbot") -> CommandResult: ...


class HelpPlugin(Plugin):
    name        = "help"
    description = "Show all available commands"
    aliases     = ["h", "?"]
    usage       = "/help [command]"

    def execute(self, args: str, chatbot: "Chatbot") -> CommandResult:
        if args:
            plugin = chatbot.plugin_manager.get(args.strip().lstrip("/"))
            if plugin:
                return CommandResult(output=f"**/{plugin.name}** — {plugin.description}\nUsage: `{plugin.usage}`")
            return CommandResult(output=f"Unknown command: {args}", success=False)
        lines = ["## Available Commands\n"]
        for p in sorted(chatbot.plugin_manager.plugins.values(), key=lambda x: x.name):
            aliases = f" (aliases: {', '.join('/' + a for a in p.aliases)})" if p.aliases else ""
            lines.append(f"  `{p.usage}` — {p.description}{aliases}")
        return CommandResult(output="\n".join(lines))


class NewSessionPlugin(Plugin):
    name        = "new"
    description = "Start a new conversation session"
    aliases     = ["n", "clear"]
    usage       = "/new [session name]"

    def execute(self, args: str, chatbot: "Chatbot") -> CommandResult:
        chatbot._save_current_session()
        chatbot.session = Session(
            name    = args.strip() or f"Session {datetime.datetime.now().strftime('%b %d %H:%M')}",
            model   = chatbot.current_model,
            persona_id = chatbot.current_persona.id if chatbot.current_persona else None,
        )
        return CommandResult(output=f"✨ New session started: **{chatbot.session.name}**", new_session=True)


class ExitPlugin(Plugin):
    name        = "exit"
    description = "Exit the chatbot"
    aliases     = ["quit", "q", "bye"]
    usage       = "/exit"

    def execute(self, args: str, chatbot: "Chatbot") -> CommandResult:
        return CommandResult(output="Goodbye! 👋", exit_chat=True)


class HistoryPlugin(Plugin):
    name        = "history"
    description = "Show conversation history"
    aliases     = ["hist"]
    usage       = "/history [n]"

    def execute(self, args: str, chatbot: "Chatbot") -> CommandResult:
        n = int(args.strip()) if args.strip().isdigit() else 10
        msgs = chatbot.session.messages[-n:]
        if not msgs:
            return CommandResult(output="No messages in this session.")
        lines = [f"## Last {min(n, len(msgs))} messages\n"]
        for m in msgs:
            ts   = m.timestamp.strftime("%H:%M:%S")
            role = m.role.value.upper()
            preview = m.content[:200].replace("\n", " ")
            if len(m.content) > 200:
                preview += "..."
            lines.append(f"[{ts}] **{role}**: {preview}")
        return CommandResult(output="\n".join(lines))


class SessionsPlugin(Plugin):
    name        = "sessions"
    description = "List all saved sessions"
    aliases     = ["ls", "list"]
    usage       = "/sessions"

    def execute(self, args: str, chatbot: "Chatbot") -> CommandResult:
        sessions = chatbot.db.list_sessions()
        if not sessions:
            return CommandResult(output="No saved sessions found.")
        lines = ["## Saved Sessions\n"]
        for s in sessions:
            updated = datetime.datetime.fromisoformat(s["updated_at"]).strftime("%b %d, %Y %H:%M")
            lines.append(f"  • `{s['id'][:8]}` **{s['name']}** — {s['msg_count']} msgs — {updated}")
        return CommandResult(output="\n".join(lines))


class LoadSessionPlugin(Plugin):
    name        = "load"
    description = "Load a previous session by ID or name"
    usage       = "/load <session_id_prefix>"

    def execute(self, args: str, chatbot: "Chatbot") -> CommandResult:
        if not args.strip():
            return CommandResult(output="Usage: /load <session_id_prefix>", success=False)
        sessions = chatbot.db.list_sessions()
        prefix   = args.strip().lower()
        match    = next(
            (s for s in sessions if s["id"].startswith(prefix) or
             prefix in s["name"].lower()),
            None
        )
        if not match:
            return CommandResult(output=f"No session found matching '{prefix}'", success=False)
        chatbot._save_current_session()
        loaded = chatbot.db.load_session(match["id"])
        if loaded:
            chatbot.session = loaded
            return CommandResult(
                output=f"✅ Loaded session: **{loaded.name}** ({loaded.message_count()} messages)",
                new_session=True,
            )
        return CommandResult(output="Failed to load session.", success=False)


class ExportPlugin(Plugin):
    name        = "export"
    description = "Export current session to a file"
    aliases     = ["save"]
    usage       = "/export [json|markdown|html|text]"

    def execute(self, args: str, chatbot: "Chatbot") -> CommandResult:
        fmt_str = args.strip().lower() or "markdown"
        try:
            fmt = ExportFormat(fmt_str)
        except ValueError:
            return CommandResult(output=f"Invalid format. Use: {', '.join(f.value for f in ExportFormat)}", success=False)

        exporter = ConversationExporter(chatbot.session)
        path     = exporter.export(fmt, EXPORT_DIR)
        return CommandResult(output=f"✅ Exported to: `{path}`")


class PersonaPlugin(Plugin):
    name        = "persona"
    description = "Switch AI persona/personality"
    aliases     = ["p", "char"]
    usage       = "/persona [persona_id | list]"

    def execute(self, args: str, chatbot: "Chatbot") -> CommandResult:
        args = args.strip().lower()
        if not args or args == "list":
            lines = ["## Available Personas\n"]
            for p in chatbot.personas.values():
                active = " ← active" if chatbot.current_persona and chatbot.current_persona.id == p.id else ""
                lines.append(f"  {p.avatar} **{p.name}** (`{p.id}`) — {p.description}{active}")
            return CommandResult(output="\n".join(lines))

        if args not in chatbot.personas:
            return CommandResult(output=f"Unknown persona: {args}. Use /persona list to see options.", success=False)
        chatbot.current_persona = chatbot.personas[args]
        chatbot.session.persona_id = args
        p = chatbot.current_persona
        return CommandResult(output=f"{p.avatar} Switched to **{p.name}**: {p.description}")


class ModelPlugin(Plugin):
    name        = "model"
    description = "Switch AI model"
    aliases     = ["m"]
    usage       = "/model [model_name | list]"

    def execute(self, args: str, chatbot: "Chatbot") -> CommandResult:
        if not args or args.strip() == "list":
            available = chatbot.backend_factory.available_models()
            lines = ["## Available Models\n"]
            for provider, models in available.items():
                lines.append(f"**{provider}:**")
                for m in models:
                    active = " ← active" if m == chatbot.current_model else ""
                    lines.append(f"  • `{m}`{active}")
            return CommandResult(output="\n".join(lines))

        new_model = args.strip()
        backend   = chatbot.backend_factory.get_backend(new_model)
        if backend and backend.is_available():
            chatbot.current_model   = new_model
            chatbot.current_backend = backend
            chatbot.session.model   = new_model
            return CommandResult(output=f"✅ Switched to model: **{new_model}**")
        return CommandResult(output=f"Model '{new_model}' is not available. Check your API keys.", success=False)


class StatsPlugin(Plugin):
    name        = "stats"
    description = "Show token usage and cost statistics"
    usage       = "/stats [days]"

    def execute(self, args: str, chatbot: "Chatbot") -> CommandResult:
        days  = int(args.strip()) if args.strip().isdigit() else 30
        stats = chatbot.db.get_usage_summary(days)
        total_cost = chatbot.db.get_total_cost()

        session_usage = chatbot.session.total_usage
        lines = [
            f"## Usage Statistics (last {days} days)\n",
            f"**Current Session:**",
            f"  • Prompt tokens:     {session_usage.prompt_tokens:,}",
            f"  • Completion tokens: {session_usage.completion_tokens:,}",
            f"  • Total tokens:      {session_usage.total_tokens:,}",
            f"\n**All-Time Total Cost:** ${total_cost:.4f}",
        ]
        if stats:
            lines.append(f"\n**Daily Breakdown:**")
            daily: Dict[str, Dict] = defaultdict(lambda: {"pt": 0, "ct": 0, "cost": 0.0})
            for row in stats:
                d = row["date"]
                daily[d]["pt"]   += row["prompt_tokens"]
                daily[d]["ct"]   += row["completion_tokens"]
                daily[d]["cost"] += row["cost_usd"]
            for date in sorted(daily.keys(), reverse=True)[:7]:
                d = daily[date]
                lines.append(f"  {date}: {d['pt']+d['ct']:,} tokens | ${d['cost']:.4f}")
        return CommandResult(output="\n".join(lines))


class SearchPlugin(Plugin):
    name        = "search"
    description = "Search through conversation history"
    usage       = "/search <query>"

    def execute(self, args: str, chatbot: "Chatbot") -> CommandResult:
        if not args.strip():
            return CommandResult(output="Usage: /search <query>", success=False)
        results = chatbot.db.search_messages(args.strip())
        if not results:
            return CommandResult(output=f"No messages found matching '{args}'")
        lines = [f"## Search results for '{args}'\n"]
        for r in results[:10]:
            ts      = datetime.datetime.fromisoformat(r["timestamp"]).strftime("%b %d %H:%M")
            preview = r["content"][:150].replace("\n", " ")
            lines.append(f"  [{ts}] **{r['role'].upper()}** (in _{r['session_name']}_): {preview}...")
        return CommandResult(output="\n".join(lines))


class SummarizePlugin(Plugin):
    name        = "summarize"
    description = "Summarize the current conversation"
    usage       = "/summarize"

    def execute(self, args: str, chatbot: "Chatbot") -> CommandResult:
        if not chatbot.session.messages:
            return CommandResult(output="No messages to summarize.")
        context = "\n".join(
            f"{m.role.value.upper()}: {m.content[:500]}"
            for m in chatbot.session.messages[-20:]
        )
        summary_prompt = f"Please provide a concise 3-5 sentence summary of the following conversation:\n\n{context}"
        summary_msg    = Message(role=Role.USER, content=summary_prompt)

        try:
            response = chatbot.current_backend.complete(
                messages=[summary_msg],
                temperature=0.3, max_tokens=300,
            )
            chatbot.session.summary = response.content
            return CommandResult(output=f"## Conversation Summary\n\n{response.content}")
        except Exception as e:
            return CommandResult(output=f"Failed to summarize: {e}", success=False)


class SystemPromptPlugin(Plugin):
    name        = "system"
    description = "View or set a custom system prompt"
    usage       = "/system [prompt text]"

    def execute(self, args: str, chatbot: "Chatbot") -> CommandResult:
        if not args.strip():
            current = chatbot.custom_system_prompt or (
                chatbot.current_persona.system_prompt if chatbot.current_persona else "None"
            )
            return CommandResult(output=f"**Current system prompt:**\n\n{current}")
        chatbot.custom_system_prompt = args.strip()
        return CommandResult(output=f"✅ System prompt updated ({len(args.split())} words).")


class TemperaturePlugin(Plugin):
    name        = "temp"
    description = "Set the AI temperature (creativity level)"
    usage       = "/temp <0.0-2.0>"

    def execute(self, args: str, chatbot: "Chatbot") -> CommandResult:
        try:
            t = float(args.strip())
            if not 0.0 <= t <= 2.0:
                raise ValueError("Out of range")
            chatbot.temperature = t
            label = "precise" if t < 0.3 else "balanced" if t < 0.7 else "creative" if t < 1.2 else "wild"
            return CommandResult(output=f"✅ Temperature set to **{t}** ({label})")
        except (ValueError, TypeError):
            return CommandResult(output="Usage: /temp <0.0-2.0>  (e.g., /temp 0.7)", success=False)


class RenamePlugin(Plugin):
    name        = "rename"
    description = "Rename the current session"
    usage       = "/rename <new name>"

    def execute(self, args: str, chatbot: "Chatbot") -> CommandResult:
        if not args.strip():
            return CommandResult(output="Usage: /rename <new name>", success=False)
        old_name = chatbot.session.name
        chatbot.session.name = args.strip()
        return CommandResult(output=f"✅ Renamed: _{old_name}_ → **{chatbot.session.name}**")


class InfoPlugin(Plugin):
    name        = "info"
    description = "Show current session information"
    usage       = "/info"

    def execute(self, args: str, chatbot: "Chatbot") -> CommandResult:
        s = chatbot.session
        p = chatbot.current_persona
        lines = [
            "## Current Session Info",
            f"  **Name:**      {s.name}",
            f"  **ID:**        {s.id}",
            f"  **Model:**     {chatbot.current_model}",
            f"  **Persona:**   {p.avatar + ' ' + p.name if p else 'None'}",
            f"  **Temperature:** {chatbot.temperature}",
            f"  **Messages:**  {s.message_count()} ({s.user_message_count()} from you)",
            f"  **Duration:**  {s.duration_str()}",
            f"  **Tokens:**    {s.total_usage.total_tokens:,}",
            f"  **Created:**   {s.created_at.strftime('%b %d, %Y %H:%M')}",
        ]
        if s.summary:
            lines.append(f"\n**Summary:** {s.summary}")
        return CommandResult(output="\n".join(lines))


class DeletePlugin(Plugin):
    name        = "delete"
    description = "Delete a session by ID prefix"
    usage       = "/delete <session_id_prefix>"

    def execute(self, args: str, chatbot: "Chatbot") -> CommandResult:
        prefix = args.strip()
        if not prefix:
            return CommandResult(output="Usage: /delete <session_id_prefix>", success=False)
        sessions = chatbot.db.list_sessions()
        match    = next((s for s in sessions if s["id"].startswith(prefix)), None)
        if not match:
            return CommandResult(output=f"No session found with ID starting with '{prefix}'", success=False)
        chatbot.db.delete_session(match["id"])
        return CommandResult(output=f"🗑️ Deleted session: **{match['name']}**")


class PluginManager:
    """Registry and dispatcher for all plugins."""

    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}

    def register(self, plugin: Plugin) -> None:
        self.plugins[plugin.name] = plugin
        for alias in plugin.aliases:
            self.plugins[alias] = plugin

    def get(self, name: str) -> Optional[Plugin]:
        return self.plugins.get(name.lower().lstrip("/"))

    def dispatch(self, raw_input: str, chatbot: "Chatbot") -> Optional[CommandResult]:
        """Check if input is a command; dispatch if so. Return None if not a command."""
        stripped = raw_input.strip()
        if not stripped.startswith("/"):
            return None
        parts   = stripped[1:].split(maxsplit=1)
        cmd     = parts[0].lower()
        args    = parts[1] if len(parts) > 1 else ""
        plugin  = self.get(cmd)
        if plugin:
            try:
                return plugin.execute(args, chatbot)
            except Exception as e:
                return CommandResult(output=f"Command error: {e}", success=False)
        return CommandResult(output=f"Unknown command: /{cmd}. Type /help for available commands.", success=False)

    def register_defaults(self):
        for cls in [
            HelpPlugin, NewSessionPlugin, ExitPlugin, HistoryPlugin,
            SessionsPlugin, LoadSessionPlugin, ExportPlugin, PersonaPlugin,
            ModelPlugin, StatsPlugin, SearchPlugin, SummarizePlugin,
            SystemPromptPlugin, TemperaturePlugin, RenamePlugin, InfoPlugin,
            DeletePlugin,
        ]:
            self.register(cls())


# ─────────────────────────────────────────────────────────────────────────────
# BACKEND FACTORY
# ─────────────────────────────────────────────────────────────────────────────

class BackendFactory:
    """Creates and caches AI backends based on model names."""

    PROVIDER_MAP: Dict[str, Provider] = {
        "gpt":     Provider.OPENAI,
        "claude":  Provider.ANTHROPIC,
        "gemini":  Provider.GOOGLE,
        "command": Provider.COHERE,
        "ollama/": Provider.OLLAMA,
        "mock":    Provider.MOCK,
    }

    def __init__(self):
        self._cache: Dict[str, AIBackend] = {}

    def get_backend(self, model: str) -> AIBackend:
        if model in self._cache:
            return self._cache[model]
        backend = self._create_backend(model)
        self._cache[model] = backend
        return backend

    def _create_backend(self, model: str) -> AIBackend:
        model_lower = model.lower()
        if model_lower.startswith("mock"):
            return MockBackend(model)
        if model_lower.startswith("gpt"):
            return OpenAIBackend(model)
        if model_lower.startswith("claude"):
            return AnthropicBackend(model)
        if model_lower.startswith("gemini"):
            return GoogleBackend(model)
        if model_lower.startswith("ollama/"):
            return OllamaBackend(model.split("/", 1)[1])
        # Default: try OpenAI-compatible
        return OpenAIBackend(model)

    def available_models(self) -> Dict[str, List[str]]:
        result = {}
        candidates = {
            "OpenAI":    (["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"], OpenAIBackend),
            "Anthropic": (["claude-opus-4-20250514", "claude-sonnet-4-20250514", "claude-haiku-4-5-20251001"], AnthropicBackend),
            "Google":    (["gemini-1.5-pro", "gemini-1.5-flash"], GoogleBackend),
            "Ollama":    (["ollama/llama3", "ollama/mistral", "ollama/phi3"], OllamaBackend),
            "Mock":      (["mock-model"], MockBackend),
        }
        for provider, (models, cls) in candidates.items():
            test_backend = cls(models[0]) if cls != MockBackend else MockBackend()
            if test_backend.is_available():
                result[provider] = models
        return result

    def detect_best_backend(self) -> str:
        """Auto-detect and return the best available model."""
        priority = [
            ("claude-sonnet-4-20250514", AnthropicBackend),
            ("gpt-4o", OpenAIBackend),
            ("gemini-1.5-flash", GoogleBackend),
            ("ollama/llama3", OllamaBackend),
            ("mock-model", MockBackend),
        ]
        for model, cls in priority:
            backend = cls(model) if cls != MockBackend else MockBackend()
            if backend.is_available():
                return model
        return "mock-model"


# ─────────────────────────────────────────────────────────────────────────────
# CONVERSATION EXPORT
# ─────────────────────────────────────────────────────────────────────────────

class ConversationExporter:
    """Exports a Session to various file formats."""

    def __init__(self, session: Session):
        self.session = session

    def export(self, fmt: ExportFormat, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        safe_name = re.sub(r'[^\w\-_]', '_', self.session.name)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_name}_{ts}.{fmt.value}"
        path = output_dir / filename

        dispatch = {
            ExportFormat.JSON:     self._to_json,
            ExportFormat.MARKDOWN: self._to_markdown,
            ExportFormat.HTML:     self._to_html,
            ExportFormat.TEXT:     self._to_text,
        }
        content = dispatch[fmt]()
        path.write_text(content, encoding="utf-8")
        return path

    def _to_json(self) -> str:
        return json.dumps(self.session.to_dict(), indent=2, ensure_ascii=False)

    def _to_markdown(self) -> str:
        lines = [
            f"# {self.session.name}",
            f"",
            f"> **Session ID:** {self.session.id}  ",
            f"> **Created:** {self.session.created_at.strftime('%B %d, %Y %H:%M')}  ",
            f"> **Model:** {self.session.model or 'Unknown'}  ",
            f"> **Messages:** {self.session.message_count()}  ",
            f"",
        ]
        if self.session.summary:
            lines += [f"## Summary", f"", self.session.summary, f""]
        lines.append("## Conversation")
        lines.append("")
        for msg in self.session.messages:
            ts   = msg.timestamp.strftime("%H:%M:%S")
            role = msg.role.value.title()
            lines.append(f"### {role} _{ts}_")
            lines.append("")
            lines.append(msg.content)
            lines.append("")
        return "\n".join(lines)

    def _to_html(self) -> str:
        def escape(s): return (s.replace("&","&amp;").replace("<","&lt;")
                                .replace(">","&gt;").replace('"',"&quot;"))
        msg_html = ""
        for msg in self.session.messages:
            role_class = "user" if msg.role == Role.USER else "assistant"
            ts = msg.timestamp.strftime("%H:%M:%S")
            content_escaped = escape(msg.content).replace("\n", "<br>")
            msg_html += f"""
        <div class="message {role_class}">
          <div class="meta">{msg.role.value.title()} · {ts}</div>
          <div class="content">{content_escaped}</div>
        </div>"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(self.session.name)}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f0f2f5; padding: 20px; color: #1a1a1a; }}
    h1 {{ text-align: center; padding: 20px 0; color: #333; font-size: 1.6rem; }}
    .meta-bar {{ text-align:center; font-size:0.85rem; color:#666; margin-bottom:20px; }}
    .message {{ max-width: 720px; margin: 12px auto; padding: 14px 18px;
                border-radius: 12px; line-height: 1.6; }}
    .user {{ background: #0071e3; color: white; margin-left: auto; text-align: left; }}
    .assistant {{ background: white; box-shadow: 0 1px 4px rgba(0,0,0,0.1); }}
    .meta {{ font-size: 0.75rem; opacity: 0.7; margin-bottom: 6px; font-weight: 600; }}
    .content {{ white-space: pre-wrap; word-wrap: break-word; }}
  </style>
</head>
<body>
  <h1>💬 {escape(self.session.name)}</h1>
  <div class="meta-bar">
    {escape(self.session.created_at.strftime('%B %d, %Y'))} ·
    {self.session.message_count()} messages ·
    {escape(self.session.model or 'Unknown')}
  </div>
  {msg_html}
</body>
</html>"""

    def _to_text(self) -> str:
        lines = [
            f"=== {self.session.name} ===",
            f"Created: {self.session.created_at.strftime('%B %d, %Y %H:%M')}",
            f"Model: {self.session.model or 'Unknown'}",
            f"Messages: {self.session.message_count()}",
            "",
            "─" * 60,
            "",
        ]
        for msg in self.session.messages:
            ts   = msg.timestamp.strftime("%H:%M:%S")
            role = msg.role.value.upper()
            lines.append(f"[{ts}] {role}:")
            lines.append(textwrap.fill(msg.content, width=80))
            lines.append("")
        return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# TEXT-TO-SPEECH
# ─────────────────────────────────────────────────────────────────────────────

class TTSEngine:
    """Optional text-to-speech output using gTTS."""

    def __init__(self, lang: str = "en", enabled: bool = False):
        self.lang    = lang
        self.enabled = enabled and gtts_mod is not None and pygame_mod is not None
        self._lock   = threading.Lock()
        if self.enabled:
            pygame_mod.mixer.init()

    def speak(self, text: str) -> None:
        if not self.enabled:
            return
        def _run():
            with self._lock:
                try:
                    clean = re.sub(r'[#*`_\[\]()>]', '', text)[:500]
                    tts   = gtts_mod.gTTS(text=clean, lang=self.lang, slow=False)
                    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                        tts.save(f.name)
                        pygame_mod.mixer.music.load(f.name)
                        pygame_mod.mixer.music.play()
                        while pygame_mod.mixer.music.get_busy():
                            time.sleep(0.1)
                        os.unlink(f.name)
                except Exception as e:
                    logging.debug(f"TTS error: {e}")
        threading.Thread(target=_run, daemon=True).start()


# ─────────────────────────────────────────────────────────────────────────────
# SAFETY & MODERATION
# ─────────────────────────────────────────────────────────────────────────────

class SafetyFilter:
    """Basic content moderation and safety checks."""

    # Simple keyword blocklist — extend or replace with API-based moderation
    BLOCKED_PATTERNS: List[str] = []

    def check_input(self, text: str) -> Tuple[bool, str]:
        """Return (is_safe, reason). Override for custom moderation."""
        text_lower = text.lower()
        for pattern in self.BLOCKED_PATTERNS:
            if pattern in text_lower:
                return False, f"Content policy violation detected."
        if len(text) > 32_000:
            return False, "Message too long (max 32,000 characters)."
        return True, ""

    def check_output(self, text: str) -> Tuple[bool, str]:
        return True, ""


# ─────────────────────────────────────────────────────────────────────────────
# RATE LIMITER
# ─────────────────────────────────────────────────────────────────────────────

class RateLimiter:
    """Token bucket rate limiter for API calls."""

    def __init__(self, requests_per_minute: int = 60):
        self.rpm        = requests_per_minute
        self._tokens    = float(requests_per_minute)
        self._max       = float(requests_per_minute)
        self._last_tick = time.monotonic()
        self._lock      = threading.Lock()

    def acquire(self, block: bool = True) -> bool:
        with self._lock:
            now    = time.monotonic()
            delta  = now - self._last_tick
            self._tokens = min(self._max, self._tokens + delta * (self.rpm / 60))
            self._last_tick = now
            if self._tokens >= 1.0:
                self._tokens -= 1.0
                return True
            if block:
                wait = (1.0 - self._tokens) / (self.rpm / 60)
                time.sleep(wait)
                self._tokens = 0.0
                return True
            return False


# ─────────────────────────────────────────────────────────────────────────────
# DISPLAY / UI LAYER
# ─────────────────────────────────────────────────────────────────────────────

class ChatUI:
    """Handles all terminal display logic."""

    BANNER = r"""
  ╔════════════════════════════════════════╗
  ║         MY AI CHATBOT  v3.0.0         ║
  ║         Built with ❤️  by You          ║
  ╚════════════════════════════════════════╝
"""

    def __init__(self, use_rich: bool = True):
        self.use_rich = use_rich and rich is not None

    def banner(self) -> None:
        if self.use_rich:
            console.print(Panel.fit(
                Text.from_markup(
                    "[bold cyan]MY AI CHATBOT[/bold cyan] [dim]v3.0.0[/dim]\n"
                    "[dim]Built with [red]❤️[/red] by [bold]You[/bold][/dim]"
                ),
                border_style="bright_blue",
                padding=(1, 4),
            ))
        else:
            print(self.BANNER)

    def session_header(self, session: Session, persona: Optional[Persona],
                        model: str) -> None:
        if self.use_rich:
            persona_str = f"{persona.avatar} {persona.name}" if persona else "None"
            console.print(
                f"[dim]Session:[/dim] [bold]{session.name}[/bold]  "
                f"[dim]│[/dim]  [dim]Model:[/dim] [cyan]{model}[/cyan]  "
                f"[dim]│[/dim]  [dim]Persona:[/dim] {persona_str}  "
                f"[dim]│[/dim]  [dim]Type[/dim] [bold yellow]/help[/bold yellow] [dim]for commands[/dim]"
            )
            console.rule(style="dim")
        else:
            print(f"\nSession: {session.name} | Model: {model}")
            print("-" * 60)

    def user_prompt(self, persona_avatar: str = "") -> str:
        if self.use_rich:
            return Prompt.ask(f"\n[bold green]You[/bold green]")
        else:
            return input("\nYou: ")

    def show_thinking(self) -> Any:
        """Context manager that shows a spinner while AI is thinking."""
        if self.use_rich:
            return Progress(
                SpinnerColumn("dots"),
                TextColumn("[dim]Thinking...[/dim]"),
                transient=True,
            )
        return _NullContext()

    def display_response(self, content: str, persona: Optional[Persona],
                          model: str, usage: Optional[TokenUsage] = None) -> None:
        name  = persona.name if persona else "Assistant"
        emoji = persona.avatar if persona else "🤖"
        if self.use_rich:
            header = f"\n[bold magenta]{emoji} {name}[/bold magenta] [dim]({model})[/dim]"
            console.print(header)
            try:
                console.print(Markdown(content))
            except Exception:
                console.print(content)
            if usage and usage.total_tokens:
                cost = f"${getattr(usage, '_cost', 0.0):.4f}" if getattr(usage, '_cost', 0) > 0 else ""
                console.print(
                    f"  [dim]▸ {usage.prompt_tokens}↑ {usage.completion_tokens}↓ "
                    f"= {usage.total_tokens} tokens {cost}[/dim]"
                )
        else:
            print(f"\n{emoji} {name}: {content}")
            if usage:
                print(f"  [{usage.total_tokens} tokens]")

    def display_streaming(self, stream: Generator, persona: Optional[Persona],
                           model: str) -> str:
        """Stream response tokens to terminal, return full text."""
        name  = persona.name if persona else "Assistant"
        emoji = persona.avatar if persona else "🤖"
        if self.use_rich:
            console.print(f"\n[bold magenta]{emoji} {name}[/bold magenta] [dim]({model})[/dim]")
        else:
            print(f"\n{emoji} {name}: ", end="", flush=True)

        buffer = []
        try:
            for token in stream:
                buffer.append(token)
                print(token, end="", flush=True)
        except KeyboardInterrupt:
            print("\n[interrupted]")
        print()  # newline after stream
        return "".join(buffer)

    def display_command_result(self, result: CommandResult) -> None:
        if self.use_rich:
            style = "green" if result.success else "red"
            try:
                console.print(Markdown(result.output))
            except Exception:
                console.print(result.output, style=style)
        else:
            print(result.output)

    def error(self, msg: str) -> None:
        if self.use_rich:
            console.print(f"[bold red]Error:[/bold red] {msg}")
        else:
            print(f"Error: {msg}")

    def info(self, msg: str) -> None:
        if self.use_rich:
            console.print(f"[dim]{msg}[/dim]")
        else:
            print(msg)

    def success(self, msg: str) -> None:
        if self.use_rich:
            console.print(f"[bold green]✓[/bold green] {msg}")
        else:
            print(f"✓ {msg}")


@contextmanager
def _NullContext():
    yield None


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION MANAGER
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ChatbotConfig:
    """All user-configurable settings."""
    default_model:     str   = "mock-model"
    default_persona:   str   = "default"
    temperature:       float = 0.7
    max_tokens:        int   = 2048
    stream_responses:  bool  = True
    context_messages:  int   = 20       # how many past msgs to include
    auto_save:         bool  = True
    show_token_usage:  bool  = True
    use_rich:          bool  = True
    tts_enabled:       bool  = False
    tts_language:      str   = "en"
    requests_per_min:  int   = 60
    log_level:         str   = "WARNING"
    custom_system_prompt: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items()}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ChatbotConfig":
        valid = {f for f in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in d.items() if k in valid})

    @classmethod
    def load(cls) -> "ChatbotConfig":
        if CONFIG_FILE.exists():
            try:
                return cls.from_dict(json.loads(CONFIG_FILE.read_text()))
            except Exception:
                pass
        return cls()

    def save(self) -> None:
        CONFIG_FILE.write_text(json.dumps(self.to_dict(), indent=2))


# ─────────────────────────────────────────────────────────────────────────────
# MAIN CHATBOT CLASS
# ─────────────────────────────────────────────────────────────────────────────

class Chatbot:
    """
    The main orchestrator. Brings together:
      - Multiple AI backends
      - SQLite persistence
      - Plugin/command system
      - Persona management
      - Session management
      - Safety filtering
      - Rate limiting
      - Rich UI
    """

    def __init__(self, config: Optional[ChatbotConfig] = None):
        self.config  = config or ChatbotConfig.load()
        self.db      = Database()
        self.ui      = ChatUI(use_rich=self.config.use_rich)
        self.tts     = TTSEngine(lang=self.config.tts_language, enabled=self.config.tts_enabled)
        self.safety  = SafetyFilter()
        self.limiter = RateLimiter(requests_per_minute=self.config.requests_per_min)

        # Backend
        self.backend_factory  = BackendFactory()
        self._auto_detect_model()
        self.current_backend  = self.backend_factory.get_backend(self.current_model)

        # Personas
        self.personas: Dict[str, Persona] = {}
        self._load_personas()
        self.current_persona: Optional[Persona] = self.personas.get(self.config.default_persona)

        # Session
        self.session = Session(
            name       = f"Session {datetime.datetime.now().strftime('%b %d %H:%M')}",
            model      = self.current_model,
            persona_id = self.current_persona.id if self.current_persona else None,
        )

        # Settings
        self.temperature         = self.config.temperature
        self.max_tokens          = self.config.max_tokens
        self.stream              = self.config.stream_responses
        self.custom_system_prompt: Optional[str] = self.config.custom_system_prompt

        # Plugins
        self.plugin_manager = PluginManager()
        self.plugin_manager.register_defaults()
        self._load_external_plugins()

        # State
        self._running      = False
        self._message_count = 0

        # Logging
        self._setup_logging()

    def _auto_detect_model(self) -> None:
        saved = self.db.get_setting("last_model")
        if saved:
            self.current_model = saved
        else:
            self.current_model = self.backend_factory.detect_best_backend()
        self.config.default_model = self.current_model

    def _load_personas(self) -> None:
        # Load built-ins
        for p in Persona.default_personas():
            self.personas[p.id] = p
        # Load from DB (user-created)
        for row in self.db.list_personas():
            p = Persona(
                id=row["id"], name=row["name"], description=row["description"],
                system_prompt=row["system_prompt"], avatar=row["avatar"],
                temperature=row["temperature"], max_tokens=row["max_tokens"],
                tags=json.loads(row["tags"] or "[]"),
            )
            self.personas[p.id] = p

    def _load_external_plugins(self) -> None:
        """Dynamically load .py plugin files from the plugins directory."""
        import importlib.util
        for py_file in PLUGIN_DIR.glob("*.py"):
            try:
                spec   = importlib.util.spec_from_file_location(py_file.stem, py_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for name in dir(module):
                    obj = getattr(module, name)
                    if (isinstance(obj, type) and issubclass(obj, Plugin)
                            and obj is not Plugin):
                        self.plugin_manager.register(obj())
                        logging.info(f"Loaded plugin: {obj.__name__} from {py_file.name}")
            except Exception as e:
                logging.warning(f"Failed to load plugin {py_file.name}: {e}")

    def _setup_logging(self) -> None:
        level = getattr(logging, self.config.log_level.upper(), logging.WARNING)
        logging.basicConfig(
            filename=str(LOG_FILE),
            level=level,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    def _build_system_prompt(self) -> Optional[str]:
        if self.custom_system_prompt:
            return self.custom_system_prompt
        if self.current_persona:
            return self.current_persona.system_prompt
        return None

    def _get_context_messages(self) -> List[Message]:
        limit = CONTEXT_LIMITS.get(self.current_model, 4096)
        budget = min(limit // 2, 12_000)
        return self.session.get_context_messages(max_tokens=budget)

    def _save_current_session(self) -> None:
        if self.config.auto_save and self.session.message_count() > 0:
            self.db.save_session(self.session)
            for msg in self.session.messages:
                self.db.save_message(self.session.id, msg)
            self.db.set_setting("last_session_id", self.session.id)
            self.db.set_setting("last_model", self.current_model)

    def send_message(self, user_input: str,
                     attachments: Optional[List[Attachment]] = None) -> Optional[Message]:
        """Core method: send a user message, get AI response."""
        # Safety check
        is_safe, reason = self.safety.check_input(user_input)
        if not is_safe:
            self.ui.error(reason)
            return None

        # Rate limit
        self.limiter.acquire()

        # Build user message
        user_msg = Message(
            role        = Role.USER,
            content     = user_input,
            attachments = attachments or [],
        )
        self.session.add_message(user_msg)
        self._message_count += 1

        # Build context
        context_msgs    = self._get_context_messages()
        system_prompt   = self._build_system_prompt()
        persona_temp    = self.current_persona.temperature if self.current_persona else self.temperature
        persona_maxtok  = self.current_persona.max_tokens  if self.current_persona else self.max_tokens

        try:
            if self.stream:
                stream = self.current_backend.complete(
                    messages      = context_msgs,
                    system_prompt = system_prompt,
                    temperature   = persona_temp,
                    max_tokens    = persona_maxtok,
                    stream        = True,
                )
                full_text = self.ui.display_streaming(stream, self.current_persona, self.current_model)
                ai_msg = Message(
                    role    = Role.ASSISTANT,
                    content = full_text,
                    model   = self.current_model,
                )
            else:
                if self.config.use_rich and rich:
                    with Progress(SpinnerColumn("dots"),
                                  TextColumn("[dim]Thinking...[/dim]"),
                                  transient=True) as prog:
                        prog.add_task("", total=None)
                        ai_msg = self.current_backend.complete(
                            messages      = context_msgs,
                            system_prompt = system_prompt,
                            temperature   = persona_temp,
                            max_tokens    = persona_maxtok,
                            stream        = False,
                        )
                else:
                    ai_msg = self.current_backend.complete(
                        messages      = context_msgs,
                        system_prompt = system_prompt,
                        temperature   = persona_temp,
                        max_tokens    = persona_maxtok,
                        stream        = False,
                    )
                self.ui.display_response(
                    ai_msg.content, self.current_persona,
                    self.current_model, ai_msg.usage,
                )

            # Record usage
            if ai_msg.usage:
                ai_msg.usage.set_cost(self.current_model)
                self.db.record_usage(self.current_model, ai_msg.usage)

            self.session.add_message(ai_msg)

            # TTS
            self.tts.speak(ai_msg.content)

            # Auto-save periodically
            if self._message_count % 5 == 0:
                self._save_current_session()

            return ai_msg

        except KeyboardInterrupt:
            self.ui.info("\n[Response interrupted]")
            return None
        except Exception as e:
            logging.exception("Backend error")
            self.ui.error(f"AI backend error: {e}")
            if "api_key" in str(e).lower() or "unauthorized" in str(e).lower():
                self.ui.info("Tip: Set your API key with an environment variable, e.g.:\n"
                             "  export OPENAI_API_KEY=sk-...\n"
                             "  export ANTHROPIC_API_KEY=sk-ant-...\n"
                             "Or use /model mock-model to test without an API key.")
            return None

    def run(self) -> None:
        """Start the interactive chat loop."""
        self._running = True

        # Setup signal handler for graceful exit
        def _sig_handler(sig, frame):
            self.ui.info("\nSaving session...")
            self._save_current_session()
            self.ui.info("Goodbye! 👋")
            sys.exit(0)
        signal.signal(signal.SIGINT, _sig_handler)
        signal.signal(signal.SIGTERM, _sig_handler)

        # Welcome
        self.ui.banner()
        self._show_welcome_info()
        self.ui.session_header(self.session, self.current_persona, self.current_model)

        # Main loop
        while self._running:
            try:
                raw = self.ui.user_prompt(
                    self.current_persona.avatar if self.current_persona else ""
                ).strip()
            except (EOFError, KeyboardInterrupt):
                break

            if not raw:
                continue

            # Check for command
            cmd_result = self.plugin_manager.dispatch(raw, self)
            if cmd_result is not None:
                self.ui.display_command_result(cmd_result)
                if cmd_result.exit_chat:
                    self._running = False
                    break
                if cmd_result.new_session:
                    self.ui.session_header(self.session, self.current_persona, self.current_model)
                continue

            # Check for inline file attachment syntax: /attach <path>
            if raw.startswith("/attach "):
                path   = raw[8:].strip()
                rest   = ""
                attachments = self._load_attachment(path)
                if not attachments:
                    continue
                prompt = self.ui.user_prompt("").strip() or "Please analyze this file."
                self.send_message(prompt, attachments=attachments)
                continue

            # Regular chat message
            self.send_message(raw)

        # Final save
        self._save_current_session()
        self.ui.info(f"\nSession saved. Total messages: {self.session.message_count()}")

    def _show_welcome_info(self) -> None:
        available = self.backend_factory.available_models()
        n_models  = sum(len(v) for v in available.values())
        self.ui.info(
            f"  {n_models} models available across {len(available)} providers. "
            f"Current: [bold]{self.current_model}[/bold]"
            if self.config.use_rich and rich
            else f"  Current model: {self.current_model}"
        )
        if self.current_model.startswith("mock"):
            self.ui.info(
                "  ⚠️  Running in MOCK mode (no API key detected). "
                "Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or GOOGLE_API_KEY "
                "for real AI responses, then use /model to switch."
            )

    def _load_attachment(self, path: str) -> Optional[List[Attachment]]:
        try:
            att = Attachment.from_path(path)
            self.ui.success(f"Attached: {att.filename} ({att.mime_type}, {len(att.data):,} bytes)")
            return [att]
        except FileNotFoundError:
            self.ui.error(f"File not found: {path}")
        except Exception as e:
            self.ui.error(f"Could not attach file: {e}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
# CLI ARGUMENT PARSER
# ─────────────────────────────────────────────────────────────────────────────

def parse_args() -> Any:
    import argparse
    parser = argparse.ArgumentParser(
        prog="ai_chatbot",
        description=f"{APP_NAME} — {APP_DESCRIPTION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          python ai_chatbot.py
          python ai_chatbot.py --model gpt-4o --persona coder
          python ai_chatbot.py --model claude-sonnet-4-20250514 --stream
          python ai_chatbot.py --prompt "Explain quantum entanglement"
          python ai_chatbot.py --list-models
          python ai_chatbot.py --list-personas
          python ai_chatbot.py --load-session <session_id>
          python ai_chatbot.py --export markdown
        """)
    )
    parser.add_argument("--model",        type=str, help="AI model to use")
    parser.add_argument("--persona",      type=str, help="Persona ID to use")
    parser.add_argument("--temperature",  type=float, help="Response temperature (0.0-2.0)")
    parser.add_argument("--max-tokens",   type=int, help="Max tokens per response")
    parser.add_argument("--stream",       action="store_true", help="Enable streaming responses")
    parser.add_argument("--no-stream",    action="store_true", help="Disable streaming responses")
    parser.add_argument("--no-rich",      action="store_true", help="Disable rich terminal output")
    parser.add_argument("--tts",          action="store_true", help="Enable text-to-speech")
    parser.add_argument("--prompt",       type=str, help="Single prompt (non-interactive)")
    parser.add_argument("--system",       type=str, help="Custom system prompt")
    parser.add_argument("--load-session", type=str, metavar="ID", help="Load a previous session")
    parser.add_argument("--export",       type=str, choices=[f.value for f in ExportFormat],
                        help="Export session to format and exit")
    parser.add_argument("--list-models",  action="store_true", help="List available models and exit")
    parser.add_argument("--list-personas",action="store_true", help="List available personas and exit")
    parser.add_argument("--stats",        action="store_true", help="Show usage stats and exit")
    parser.add_argument("--version",      action="version", version=f"{APP_NAME} {APP_VERSION}")
    return parser.parse_args()


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    args   = parse_args()
    config = ChatbotConfig.load()

    # Apply CLI overrides
    if args.model:        config.default_model   = args.model
    if args.persona:      config.default_persona = args.persona
    if args.temperature:  config.temperature     = args.temperature
    if args.max_tokens:   config.max_tokens      = args.max_tokens
    if args.stream:       config.stream_responses = True
    if args.no_stream:    config.stream_responses = False
    if args.no_rich:      config.use_rich = False
    if args.tts:          config.tts_enabled = True
    if args.system:       config.custom_system_prompt = args.system

    bot = Chatbot(config=config)

    # ── Non-interactive modes ───────────────────────────────────────────────

    if args.list_models:
        available = bot.backend_factory.available_models()
        if not available:
            print("No models available. Set API keys to enable providers.")
        for provider, models in available.items():
            print(f"\n{provider}:")
            for m in models:
                print(f"  • {m}")
        return

    if args.list_personas:
        print("\nAvailable Personas:\n")
        for p in bot.personas.values():
            print(f"  {p.avatar}  {p.id:<12} {p.name:<16} {p.description}")
        return

    if args.stats:
        result = StatsPlugin().execute("", bot)
        print(result.output)
        return

    if args.load_session:
        result = LoadSessionPlugin().execute(args.load_session, bot)
        print(result.output)
        if not result.success:
            return

    if args.prompt:
        # Single-shot non-interactive mode
        response = bot.send_message(args.prompt)
        if response:
            if not config.stream_responses:
                print(response.content)
        if args.export:
            fmt  = ExportFormat(args.export)
            path = ConversationExporter(bot.session).export(fmt, EXPORT_DIR)
            print(f"Exported to: {path}")
        bot._save_current_session()
        return

    if args.export:
        fmt  = ExportFormat(args.export)
        path = ConversationExporter(bot.session).export(fmt, EXPORT_DIR)
        print(f"Exported to: {path}")
        return

    # ── Interactive mode ─────────────────────────────────────────────────────
    bot.run()


if __name__ == "__main__":
    main()
