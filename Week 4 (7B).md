# 🤖 Session 7B — Vibe Code StudyBuddy

## 🎯 StudyBuddy

**StudyBuddy = Notes → AI → Quiz → Flashcards**

### What it does:

* 📝 Paste study notes
* 🤖 Gemini generates a quiz
* ❓ Creates **5 multiple-choice questions**
* 🔘 Each question has **4 options**
* 💾 Saves quizzes using `localStorage`

---

## 🏗️ Architecture

```text
🧑‍💻 Frontend
HTML + CSS + JavaScript
        ↓
🤖 Gemini API
        ↓
🧠 Generated Quiz
        ↓
🃏 Flashcards
        ↓
💾 localStorage
```

### 🖥️ Frontend

* HTML
* CSS
* JavaScript

### 🤖 AI

* Gemini API

### 💾 Storage

* `localStorage`

⚠️ A backend + database comes later in **Session 8**.

---

# ⚡ Setup

### 1️⃣ Open Antigravity

Create a workspace:

```text
studybuddy
```

### 2️⃣ 🔑 Gemini API Key

Get a Gemini API key from Google AI Studio.

⚠️ **Never expose a real API key in public frontend code.**

For the class demo, the key can be stored in `localStorage`.

For a real application:

```text
🌐 Frontend
     ↓
🖥️ Backend
     ↓
🔑 Gemini API
```

---

# 🧠 Main Prompt

```text
Build me a single-page web app called StudyBuddy.
A textarea where I paste study notes. Below it, a button labelled "Generate Quiz". When clicked, generate 5 multiple-choice questions from those notes using the Gemini API.
Show each question as a flashcard with 4 options. Use a clean modern dark theme with purple accents.
Save the generated quiz to localStorage so I can come back to it later. Use plain HTML + JS — no React, no build step.
```

### 🧩 Good Prompt Structure

Think:

**🎯 WHAT → ⚙️ WHAT IT DOES → 🎨 HOW IT LOOKS → 🚫 WHAT TO AVOID**

---

# 🤖 Antigravity Plan

The agent creates:

* 📄 `index.html`
* 🎨 `styles.css`
* ⚙️ `app.js`
* 🤖 Gemini API connection
* 📦 JSON response parsing
* 🃏 Flashcard rendering
* 💾 `localStorage`
* ⏳ Loading spinner

### ⚠️ Important

**Read the plan before approving it.**

Don't blindly click **Approve**.

---

# 🌐 `fetch()`

`fetch()` allows JavaScript to communicate with an API.

### 🔄 The flow

```text
🔗 URL
  ↓
📤 POST request
  ↓
📦 Send JSON
  ↓
⏳ Wait
  ↓
📥 Receive response
  ↓
📋 Convert to JSON
  ↓
🤖 Read AI response
```

### Example

```javascript
const response = await fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    contents: [{
      parts: [{
        text: 'Make 5 MCQs from: ' + notes
      }]
    }]
  })
});

const data = await response.json();

const quizText =
  data.candidates[0].content.parts[0].text;
```

---

# 💾 localStorage

Think of `localStorage` as a **🗃️ tiny storage box inside your browser**.

It survives a page refresh.

### 💾 Save

```javascript
localStorage.setItem(
  'studybuddy_quiz',
  JSON.stringify(quiz)
);
```

### 📂 Load

```javascript
const saved =
  localStorage.getItem('studybuddy_quiz');

if (saved) {
  const quiz = JSON.parse(saved);
  renderFlashcards(quiz);
}
```

### 🗑️ Delete

```javascript
localStorage.removeItem(
  'studybuddy_quiz'
);
```

### ⚠️ Limitation

`localStorage` belongs to **that browser**.

```text
💻 Your laptop
   ↓
💾 Your quiz

💻 Another laptop
   ↓
❌ Your quiz isn't there
```

---

# 🎨 Make the Design Better

A simple prompt can improve the UI:

```text
Make the design feel like Notion meets Duolingo.
Add subtle animations on hover.
```

### 🧠 Remember

Don't just accept AI-generated CSS.

👀 **Read it → Understand it → Improve it**

---

# 🎤 Voice Input

StudyBuddy can also use the browser's **Web Speech API**.

### 🔄 Flow

```text
🎤 Speak
   ↓
🗣️ Speech Recognition
   ↓
📝 Text appears
   ↓
🤖 Generate Quiz
```

### Example

```javascript
const rec = new webkitSpeechRecognition();

rec.lang = 'en-IN';

rec.onresult = (e) => {
  document.getElementById('notes').value =
    e.results[0][0].transcript;
};

rec.start();
```

### 🌎 Languages

* 🇮🇳 `en-IN`
* 🇮🇳 `hi-IN`
* 🇮🇳 `ta-IN`
* 🇮🇳 `te-IN`

---

# 💥 5 AI Coding Failure Modes

## 1️⃣ 👻 Hallucinated API

AI might call a function that doesn't exist.

❌ Example:

```text
geminiAPI.generateQuiz()
```

✅ **Fix:** Check the documentation.

---

## 2️⃣ 🏷️ Wrong Model Name

AI might use an outdated model name.

✅ **Fix:** Check the API console for valid model names.

---

## 3️⃣ 🚧 CORS Error

The browser may block the API request.

✅ **Fix:** Move the API call to a backend.

---

## 4️⃣ 📦 Wrong Response Shape

AI may assume:

```javascript
data.text
```

when the actual response is:

```javascript
data.candidates[0].content.parts[0].text
```

✅ **Fix:**

```javascript
console.log(data);
```

👀 Inspect what the API actually returned.

---

## 5️⃣ 🏗️ Over-engineering

AI might turn a simple project into:

```text
React
TypeScript
Webpack
Redux
47 packages
💀
```

For a simple project:

```text
Keep it plain HTML/JS.
No build step.
```

---

# 🐛 Debugging Loop

When something breaks:

### 1️⃣ 🔴 Read the error

Press:

```text
F12 → Console
```

Look at the first red error.

### 2️⃣ 🔁 Reproduce it

Try the bug again.

Ask:

> Does it happen every time?

### 3️⃣ 🧠 Hypothesise

Think about what might be causing it.

### 4️⃣ 🤖 Ask AI with context

❌ Bad:

```text
fix it
```

✅ Better:

```text
Line 12 throws X when I click the button.
I think it might be because Y.
Can you check?
```

### 🧠 Golden Rule

**🐛 Debugging > 🔄 blindly re-prompting**

---

# 🧪 Debugging Example

There are **4 bugs** in the AI-generated code:

### 🆔 Bug 1 — Wrong Element IDs

HTML and JavaScript are looking for different IDs.

### 🔗 Bug 2 — Fake API URL

The AI invented an API URL.

### 📤 Bug 3 — Incorrect `fetch()`

Important request options are missing.

### 📦 Bug 4 — Wrong Response Shape

The code expects the wrong structure from the API.

### 🎯 Main Lesson

> 🤖 AI can confidently generate code that looks correct but is actually wrong.

So:

**👀 READ → 🧪 TEST → 🐛 DEBUG → ✅ VERIFY**

---

# 🧪 Mini-Lab

Build your own **StudyBuddy variant**.

### ✅ Required

* 📝 Paste notes
* 🤖 Generate quiz
* 🃏 See flashcards

### 🎮 Choose ONE personal feature

🎤 **Voice Input**

🏆 **Score Tracker**

🔥 **Difficulty Levels**

🎨 **Subject Themes**

---

# 📤 Submission

Submit:

* 📸 Screenshot of StudyBuddy working
* ✨ Your personal twist
* 🐛 One bug you encountered
* 🔧 How you fixed it

Example:

```text
🐛 Bug:
Quiz wasn't appearing.

🔧 Fix:
I checked the browser console and found
that the response was being read incorrectly.
```

---

# 🚀 Stretch

Try adding:

```text
📄 Upload PDF
      ↓
📖 Extract text
      ↓
🤖 Generate quiz
```

---

# 🧠 Session 7B — Quick Recap

| 🧩 Topic          | 💡 What it means                                  |
| ----------------- | ------------------------------------------------- |
| 🤖 Vibe Coding    | Build with AI using natural-language instructions |
| 🌐 API            | Lets your app communicate with another service    |
| 📤 `fetch()`      | Sends requests to an API                          |
| 📦 JSON           | Structured data used by APIs                      |
| 💾 `localStorage` | Stores data inside the browser                    |
| 🐛 Debugging      | Finding and fixing problems                       |
| 🧠 Prompting      | Clearly telling AI what you want                  |

---

# 🏆 Final Rule

```text
🤖 AI writes code
        ↓
👀 YOU read it
        ↓
🧪 YOU test it
        ↓
🐛 YOU debug it
        ↓
🚀 YOU improve it
```

**You are still the programmer. 🧑‍💻🔥**
