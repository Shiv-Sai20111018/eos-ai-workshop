# 🧠 Session 6A — NLP Foundations

## 📌 What is NLP?

NLP stands for **Natural Language Processing**.

It is a field in AI where computers learn to understand human language.

Examples:
- ChatGPT 🤖
- Google Translate 🌍
- Voice assistants 🎤
- Spam detection 📧
- Chatbots 💬

NLP helps computers understand:
- text
- speech
- sentences
- meaning

I understood NLP like:
> “Teaching computers to understand human language.”

---

# 🗣️ Why NLP is Important

Humans speak naturally, but computers only understand numbers.

NLP converts human language into a format computers can process.

Example:

```text
"I love AI"
```

Computer sees it as:
```text
[23, 54, 12]
```

---

# 🔍 Main Steps in NLP

NLP usually works like this:

```text
Text
 ↓
Cleaning
 ↓
Tokenization
 ↓
Vectorization
 ↓
Model Training
 ↓
Prediction
```

---

# 1️⃣ Text Cleaning

Before using text, we clean unnecessary things like:
- symbols
- punctuation
- extra spaces
- emojis sometimes

Example:

```text
"Hello!!! How are you???"
```

becomes:

```text
"hello how are you"
```

---

## 💻 Example Code

```python
text = "Hello!!! How are you???"

cleaned = text.lower()

print(cleaned)
```

---

# 2️⃣ Tokenization

Tokenization means splitting sentences into smaller pieces called tokens.

Example:

```text
"I love AI"
```

becomes:

```python
["I", "love", "AI"]
```

I understood it like:
> “Breaking sentences into small understandable pieces.”

---

## 💻 Example Code

```python
text = "I love AI"

tokens = text.split()

print(tokens)
```

---

# 3️⃣ Stop Words Removal

Some words are not very useful.

Example:
- is
- the
- are
- and

These are called stop words.

Example:

```text
"I am learning AI"
```

becomes:

```text
"learning AI"
```

---

## 💻 Example Code

```python
from nltk.corpus import stopwords

words = ["I", "am", "learning", "AI"]

stop_words = ["I", "am"]

filtered = [
    word for word in words
    if word not in stop_words
]

print(filtered)
```

---

# 4️⃣ Stemming

Stemming reduces words to their root form.

Example:

| Original | Stem |
|---|---|
| playing | play |
| running | run |
| studied | studi |

---

## 💻 Example Code

```python
from nltk.stem import PorterStemmer

ps = PorterStemmer()

print(ps.stem("playing"))
```

---

# 5️⃣ Lemmatization

Lemmatization is similar to stemming but smarter.

It converts words into meaningful root words.

Example:

| Word | Lemma |
|---|---|
| better | good |
| running | run |

---

## 💻 Example Code

```python
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

print(
    lemmatizer.lemmatize("running")
)
```

---

# 6️⃣ Vectorization

Computers cannot understand text directly.

So NLP converts words into numbers.

This process is called vectorization.

Example:

| Word | Number |
|---|---|
| AI | 1 |
| NLP | 2 |
| Python | 3 |

---

## 💻 Example Code

```python
from sklearn.feature_extraction.text import CountVectorizer

texts = [
    "I love AI",
    "AI is amazing"
]

vectorizer = CountVectorizer()

result = vectorizer.fit_transform(texts)

print(result.toarray())
```

---

# 📦 Bag of Words (BoW)

Bag of Words counts how many times words appear.

Example:

```text
"I love AI"
"AI is powerful"
```

Vocabulary:

```text
["I", "love", "AI", "is", "powerful"]
```

Then NLP converts sentences into numerical vectors.

---

# 💻 Example

```python
from sklearn.feature_extraction.text import CountVectorizer

sentences = [
    "I love AI",
    "AI is powerful"
]

cv = CountVectorizer()

vectors = cv.fit_transform(sentences)

print(vectors.toarray())
```

---

# 🧠 Sentiment Analysis

NLP can detect emotions in text.

Example:

| Text | Sentiment |
|---|---|
| "I love this movie" | Positive 😀 |
| "This is terrible" | Negative 😡 |

---

## 💻 Example Code

```python
from textblob import TextBlob

text = TextBlob("I love AI")

print(text.sentiment)
```

---

# 🤖 NLP Applications

NLP is used in:
- Chatbots 💬
- Google Translate 🌍
- Voice assistants 🎤
- Spam filters 📧
- Recommendation systems 🎬
- AI assistants 🤖

---

# 🚀 Simple NLP Pipeline Example

```python
text = "I love learning AI"

# Lowercase
text = text.lower()

# Tokenization
tokens = text.split()

print(tokens)
```

---

# 🧠 What I Understood

- NLP helps computers understand language
- Text must be cleaned first
- Tokenization splits sentences
- Stop words are removed
- Stemming and lemmatization find root words
- Vectorization converts text into numbers
- NLP is used in many AI applications

---

# ⭐ Final Understanding

I understood NLP like this:

> “NLP is the bridge between human language and computers.”

Without NLP:
- chatbots would not work
- translation apps would fail
- voice assistants would not understand us

NLP basically helps AI communicate with humans.
