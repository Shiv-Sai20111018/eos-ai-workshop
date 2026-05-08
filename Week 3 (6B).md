# 🧠 Session 6B — Transformers Live

## 📌 What are Transformers?

Transformers are a type of Deep Learning model mainly used in:
- NLP
- Chatbots
- Translation
- AI assistants
- Large Language Models

Examples:
- ChatGPT 🤖
- Gemini
- Claude
- Google Translate 🌍

Transformers became very famous because they understand language much better than older models.

---

# 🤔 Why Transformers Were Created

Before Transformers, people used:
- RNN
- LSTM

Problem:
- very slow
- difficult with long sentences
- forgot old information sometimes

Transformers solved these problems using something called:

# 🔥 Attention Mechanism

I understood this like:
> “The model learns what words are important and focuses on them.”

---

# 🧩 Main Idea of Transformers

Transformers do not read word by word slowly.

Instead:
> they process all words together at the same time.

This makes them:
- faster ⚡
- smarter 🧠
- better with long sentences 📚

---

# 🗣️ Example Sentence

```text
"The animal didn't cross the street because it was tired."
```

Transformer understands:
> “it” refers to the animal.

This happens using attention.

---

# 🔍 Attention Mechanism

Attention helps the model focus on important words.

Example:

```text
"I love playing football because it is fun."
```

The model understands:
- “it” → football

---

## 💻 Simple Attention Example

```python
sentence = [
    "I",
    "love",
    "AI"
]

attention_scores = [
    0.1,
    0.3,
    0.9
]

print(attention_scores)
```

Higher score means:
> more important word.

---

# 🎯 Self Attention

Self Attention means:
> words look at other words in the same sentence.

Example:

```text
"The boy lost his bag."
```

Transformer understands:
- “his” belongs to “boy”

This is one of the most important ideas in Transformers.

---

# 🧠 Q, K, V (Query, Key, Value)

Transformers use:
- Query
- Key
- Value

These help calculate attention.

I understood this like:

| Term | Meaning |
|---|---|
| Query | What am I searching for? |
| Key | What information do I have? |
| Value | Actual information |

---

# 💻 Example Concept

```python
Query = "football"

Key = "football match"

Value = "sports information"
```

The transformer compares Query and Key to decide importance.

---

# 📍 Positional Encoding

Transformers process all words together.

Problem:
> How does the model know word order?

Solution:
# Positional Encoding

It adds position information to words.

Example:

```text
"I love AI"
```

| Word | Position |
|---|---|
| I | 1 |
| love | 2 |
| AI | 3 |

---

## 💻 Example Code

```python
positions = [0, 1, 2]

print(positions)
```

---

# 🏗️ Encoder and Decoder

Transformers mainly have:
- Encoder
- Decoder

---

# 🔹 Encoder

Encoder understands the input sentence.

Example:
```text
"How are you?"
```

Encoder converts this into meaningful information.

---

# 🔹 Decoder

Decoder generates output word by word.

Example:
```text
"I am fine."
```

---

# 🔄 Transformer Flow

```text
Input Sentence
      ↓
Tokenization
      ↓
Embedding
      ↓
Self Attention
      ↓
Encoder
      ↓
Decoder
      ↓
Output Sentence
```

---

# 🧩 Tokenization

Transformers first split text into tokens.

Example:

```text
"I love AI"
```

becomes:

```python
["I", "love", "AI"]
```

---

## 💻 Example Code

```python
text = "I love AI"

tokens = text.split()

print(tokens)
```

---

# 🔢 Embedding

Computers cannot understand words directly.

Embeddings convert words into vectors (numbers).

Example:

| Word | Vector |
|---|---|
| AI | [0.2, 0.7, 0.1] |
| NLP | [0.8, 0.1, 0.4] |

---

## 💻 Example Code

```python
from tensorflow.keras.layers import Embedding

Embedding(
    input_dim=1000,
    output_dim=64
)
```

---

# 🚀 Simple Transformer Example

```python
from transformers import pipeline

chatbot = pipeline(
    "text-generation",
    model="gpt2"
)

result = chatbot(
    "AI is",
    max_length=20
)

print(result)
```

---

# 🤖 Why Transformers Are Powerful

Transformers:
- process data in parallel
- understand context better
- work well with long sentences
- train faster than RNNs
- power modern AI systems

---

# 🌍 Real Life Uses

Transformers are used in:
- ChatGPT 🤖
- Google Translate 🌍
- AI chatbots 💬
- Voice assistants 🎤
- Text generation ✍️
- Summarization 📚

---

# 🧠 What I Understood

- Transformers are modern NLP models
- Attention is the core idea
- Self Attention connects words together
- Positional Encoding stores word order
- Encoders understand input
- Decoders generate output
- Transformers power modern AI

---

# ⭐ Final Understanding

I understood Transformers like this:

> “A super smart language model that understands relationships between words using attention.”

Transformers completely changed modern AI and NLP.

Most AI tools today are based on Transformers.
