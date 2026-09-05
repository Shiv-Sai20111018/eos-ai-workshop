# 🚀 Session 8A — Backend + Database

## 🌍 Make It Real

Yesterday, StudyBuddy lived only inside the browser.

Today:

```text
🖥️ Frontend
     ↓
⚙️ Backend
     ↓
🤖 Gemini
     ↓
🗄️ Database
     ↓
🔗 Shareable URL
```

### Today's stack

* 🐍 Python backend
* 🗄️ Vercel KV database
* 🔗 Shareable URLs

---

# 🤔 Why `localStorage` Isn't Enough

### 📱 Yesterday

The quiz was stored in the browser.

❌ Friends couldn't see it
❌ Couldn't easily open it on another device
❌ Clearing Chrome could remove it
❌ API key was visible in the browser

### 🌍 Today

The quiz lives on a server.

✅ Anyone with the URL can take it
✅ Works on phones, tablets, laptops
✅ Data survives browser resets
✅ API key stays on the server

### 🔥 The Upgrade

Add:

```text
🐍 Python backend
        +
🗄️ Vercel KV
        ↓
🔗 Unique quiz ID
```

Example:

```text
studybuddy-abc123
```

---

# 🏗️ Full-Stack Diagram

```text
🌐 BROWSER
studybuddy.vercel.app
HTML + JS
      ↕
⚙️ /api/quiz
Python on Vercel
      ↕
🤖 GEMINI
generates quiz
      ↕
🗄️ VERCEL KV
stores quizzes
```

### 🔄 The Flow

```text
1️⃣ Browser asks /api/quiz
        ↓
2️⃣ Python receives request
        ↓
3️⃣ Python calls Gemini
        ↓
4️⃣ Quiz is saved to KV
        ↓
5️⃣ Backend returns quiz ID
        ↓
6️⃣ Browser shows shareable URL
```

Example:

```text
studybuddy.vercel.app/quiz?id=abc123
```

---

# 🛣️ What Is an API Route?

An **API route** is a server URL that performs a specific job.

| Method     | Route              | Job                  |
| ---------- | ------------------ | -------------------- |
| 📤 POST    | `/api/quiz`        | Generate + save quiz |
| 📥 GET     | `/api/quiz?id=abc` | Load quiz            |
| 🗑️ DELETE | `/api/quiz?id=abc` | Delete quiz          |
| 🏠 GET     | `/`                | Homepage             |

📌 Put `quiz.py` inside the `api/` folder and Vercel automatically makes it available at `/api/quiz`.

---

# 🌌 Prompt #1 — Build the Backend

```text
Add a Python backend route at api/quiz.py.
POST should accept JSON {notes}. Use the GEMINI_API_KEY environment variable to call Gemini 2.0 Flash, generate 5 MCQs, save the quiz to Vercel KV under a unique ID (use nanoid or uuid), and return the ID.
GET /api/quiz?id=XYZ should fetch and return the saved quiz.
Update the frontend so after generating a quiz, the browser navigates to /?id=XYZ — that URL re-loads the quiz from the backend.
```

⚠️ **Read every line of AI-generated backend code before approving it.**

---

# 🐍 Backend

The important shape is:

```python
from http.server import BaseHTTPRequestHandler
import json, os, uuid
```

### 🤖 Configure Gemini

```python
genai.configure(
    api_key=os.environ['GEMINI_API_KEY']
)
```

### 📤 POST

```text
📝 Receive notes
      ↓
🤖 Generate quiz
      ↓
🆔 Create unique ID
      ↓
💾 Save quiz
      ↓
📤 Return ID
```

### 📥 GET

```text
🔗 Receive ID
      ↓
🗄️ Search database
      ↓
📤 Return quiz
```

---

# 🔐 Environment Variables

Secrets should **never** be hard-coded.

### ❌ NEVER

```python
GEMINI_API_KEY = "AIzaSy...secret"
```

Anyone who sees your code can steal the key.

### ✅ DO THIS

Vercel:

```text
Project Settings
      ↓
Environment Variables
      ↓
GEMINI_API_KEY
```

Then Python reads:

```python
import os

key = os.environ['GEMINI_API_KEY']
```

### 🧠 Rule

**If it's a secret → Environment Variable.**

Examples:

🔑 API keys
🔐 Database passwords
🎟️ OAuth tokens

---

# 🗄️ Database Family

A database is a place where data survives after the server restarts.

### 📄 Plain File

```text
quizzes.json
```

Good for:

* Small personal projects
* Around a few users

### 🔑 Key-Value

Examples:

* Vercel KV
* Redis
* Upstash

Example:

```python
kv.set('quiz:abc', data)
```

### 🗂️ SQL

Examples:

* PostgreSQL
* MySQL
* SQLite

Used for structured applications.

### 📦 Document

Examples:

* MongoDB
* Firestore

Useful when data has varying structures.

### 🎯 Today's Choice

**Vercel KV**

Simple cloud storage for StudyBuddy.

---

# ⚡ Vercel KV — 4 Operations

### ➕ Create

```python
kv.set(
    'quiz:abc123',
    {'questions': [...]}
)
```

### 👀 Read

```python
quiz = kv.get('quiz:abc123')
```

### ✏️ Update

```python
kv.set(
    'quiz:abc123',
    new_data
)
```

### 🗑️ Delete

```python
kv.delete('quiz:abc123')
```

---

# 🔄 CRUD

These four operations appear in basically every database system.

| CRUD       | HTTP     | Meaning     |
| ---------- | -------- | ----------- |
| ➕ Create   | `POST`   | Add data    |
| 👀 Read    | `GET`    | Load data   |
| ✏️ Update  | `PUT`    | Modify data |
| 🗑️ Delete | `DELETE` | Remove data |

### 🧠 StudyBuddy Example

```text
➕ Generate quiz → Create
👀 Open shared quiz → Read
✏️ Edit flashcard → Update
🗑️ Delete quiz → Delete
```

---

# 🔗 Shareable URLs

This is the **killer feature**.

### 📤 Generate

```text
📝 Notes
 ↓
🤖 Backend
 ↓
🗄️ Save quiz
 ↓
🆔 Generate ID
 ↓
🔗 Return URL
```

Example:

```text
studybuddy.vercel.app/?id=abc123
```

### 📥 Share

Send the URL to a friend.

Their browser:

```text
🔗 ?id=abc123
      ↓
📖 Read ID
      ↓
📡 GET /api/quiz
      ↓
🗄️ Database
      ↓
🃏 Display quiz
```

### JavaScript

```javascript
const id =
  new URLSearchParams(location.search).get('id');

if (id) {
  const res =
    await fetch('/api/quiz?id=' + id);

  const data = await res.json();

  renderQuiz(data.quiz);
}
```

---

# 🛡️ Security 101

Three important habits:

## 1️⃣ 🔐 Keep Secrets Secret

API keys and database passwords:

❌ Don't put them in code
❌ Don't commit `.env`
✅ Use environment variables

---

## 2️⃣ 🧹 Validate Inputs

Anything coming from the browser could be bad.

✅ Limit text length
✅ Validate IDs
❌ Don't run user input as code

---

## 3️⃣ 🚦 Rate Limit

Without limits, someone could spam:

```text
/api/quiz
/api/quiz
/api/quiz
...
```

This could use up your Gemini quota.

---

# ☠️ Dangerous Backend Example

```python
API_KEY = "secret"

def do_POST(self):
    body = json.loads(...)
    user_code = body['code']

    result = eval(user_code)

    kv.set(body['key'], result)
```

### 🚨 Three Problems

**BUG 1 — Hard-coded API key**

❌ Anyone with the code can get it.

✅ Use environment variables.

**BUG 2 — `eval()` on user input**

❌ Never execute arbitrary user input as code.

**BUG 3 — User-controlled database keys**

❌ A user could overwrite other data.

✅ Validate the key format.

### 🧠 Golden Rule

> **Never trust the network.**

**Validate → Sanitise → Rate-limit → Protect secrets**

---

# 🛠️ Live Build

Use yesterday's StudyBuddy and run these prompts in order.

### 📋 Prompt 1 — Backend

```text
Add api/quiz.py with POST + GET handlers. Use Gemini 2.0 Flash. Save to Vercel KV. Return shareable ID.
```

### 📋 Prompt 2 — Environment Variables

```text
Read GEMINI_API_KEY and KV_REST_API_URL/TOKEN from os.environ. Add a .env.example file documenting which vars are needed.
```

### 📋 Prompt 3 — Frontend

```text
After the user clicks Generate, POST notes to /api/quiz. Get back {id}. Navigate to /?id=<id>. On page load, if ?id= is present, GET that quiz from /api/quiz?id=...
```

### 📋 Prompt 4 — Share Button

```text
Add a Share button that copies the full URL to clipboard. Show a toast "URL copied!". Use the modern navigator.clipboard.writeText() API.
```

---

# 😱 Backend Errors

## 1️⃣ `KeyError: GEMINI_API_KEY`

The environment variable doesn't exist.

### ✅ Fix

Add it to:

```text
Vercel Dashboard
→ Settings
→ Environment Variables
```

---

## 2️⃣ 🚧 CORS Error

The frontend and backend are running on different origins.

### ✅ Fix

Deploy them together on Vercel or configure proper CORS headers.

---

## 3️⃣ 🤖 Gemini Returned Bad JSON

You asked Gemini for JSON, but it returned extra text.

Example:

```text
Sure! Here's your JSON:
{ ... }
```

### ✅ Fix

Use:

```text
response_mime_type =
'application/json'
```

This forces structured JSON output.

---

# 🧪 Test Locally

Install Vercel CLI:

```bash
npm i -g vercel
```

Then inside the project:

```bash
vercel dev
```

This starts:

```text
🌐 http://localhost:3000
```

### `vercel dev`

It lets you test:

* 🌐 Frontend
* ⚙️ Backend
* 🗄️ Database
* 🔐 Environment variables

locally before deploying.

---

# 📐 Design Your Data Shape First

Before writing backend code, decide exactly what a quiz looks like.

### ❌ Vague

```json
{
  "data": "some quiz text",
  "stuff": []
}
```

The frontend doesn't know what to expect.

### ✅ Specific

```json
{
  "id": "abc123",
  "created_at": "2026-05-17",
  "topic": "Photosynthesis",
  "questions": [
    {
      "q": "What gas...",
      "options": ["O2", "N2", "CO2", "H2"],
      "correct": 0
    }
  ]
}
```

### 🧠 Important

Put the exact data shape inside your AI prompt.

```text
Return JSON with this exact shape:
{ ... }
```

---

# 🔁 Pro AI Workflow

Don't ask AI to build everything at once.

Use:

```text
💭 PROMPT
specific feature
      ↓
👀 READ
every line
      ↓
🧪 TEST
does it work?
      ↓
💾 COMMIT
save point
```

### 🕐 Why Commit Often?

If your next AI prompt breaks the project:

```bash
git reset
```

can take you back to a working version.

> **Git = your time machine ⏪**

---

# 🐛 Predict the Bug

A friend opens:

```text
studybuddy.vercel.app/?id=abc123
```

But gets a blank page.

### Possible Bug 1️⃣

Backend returns:

```json
{
  "quiz": {
    "questions": []
  }
}
```

But the frontend passes the entire response to `renderCards()`.

✅ Check the actual response structure.

### Possible Bug 2️⃣

The ID doesn't exist in the database.

Backend returns:

```json
{
  "error": "not found"
}
```

✅ Check for `.error` and show:

```text
😢 Quiz not found
```

### 🧰 Debugging Checklist

1. Open DevTools → **Network**
2. Inspect the API request
3. `console.log()` the response
4. Check Vercel function logs
5. Confirm the KV value exists

---

# 🧠 Part A Recap

| 🧩 Topic                 | 💡 Key Idea                      |
| ------------------------ | -------------------------------- |
| ⚙️ API Routes            | `api/quiz.py` becomes a live URL |
| 🔐 Environment Variables | Keep secrets out of code         |
| 🗄️ Vercel KV            | `set / get / delete`             |
| 🔄 CRUD                  | Create, Read, Update, Delete     |
| 🔗 Shareable URLs        | `?id=` lets users load quizzes   |
| 🛡️ Security             | Validate + protect + rate-limit  |

## 🏆 Big Idea

Every modern app has these main pieces:

```text
🎨 Frontend
     ↓
⚙️ Backend
     ↓
🗄️ Database
     +
🤖 AI
```

**That's the foundation of full-stack development. 🚀**
