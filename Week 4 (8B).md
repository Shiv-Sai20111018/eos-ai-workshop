# 🚀 Session 8B — Deploy + Hackathon

## 🌍 From "My Laptop" to "The Internet"

### 🖥️ Before Deployment

```text
localhost:3000
```

* Works only on your laptop
* Turn off the laptop → app is gone
* Only you can use it

### 🌍 After Deployment

```text
studybuddy-arjun.vercel.app
```

* 🌐 Live 24/7
* 👥 Anyone with the URL can use it
* 📱 Can be shared on WhatsApp

### 🧠 Analogy

🏠 **localhost** = inviting friends to your house

🏬 **deployment** = opening a shop in a mall

Same product, but now anyone can visit.

---

# 🚀 What Deployment Actually Does

Deployment performs 3 main things:

### 1️⃣ 📦 Package

Vercel uploads your:

* HTML
* JavaScript
* Python
* CSS

### 2️⃣ ⚙️ Build

Vercel:

* Runs `pip install`
* Sets up Python
* Prepares API routes as serverless functions

### 3️⃣ 🌍 Publish

Your code is placed on Vercel's servers and DNS gives you a:

```text
.vercel.app
```

URL.

### ⚡ The Magic

```text
📦 Package
   ↓
⚙️ Build
   ↓
🌍 Publish
```

All automatically.

---

# ⚡ Vercel

Vercel is a cloud hosting platform.

### 🆓 Free

* 100 GB bandwidth/month
* No credit card

### ⚡ Fast

* Servers in 100+ cities
* Global CDN

### 🔄 Automatic

```text
GitHub
  ↓
Push code
  ↓
Vercel
  ↓
🚀 Automatic redeploy
```

### 🧪 Preview Deployments

Each Git branch can get its own URL for testing.

---

# 💻 One Command — Deploy

Install Vercel CLI:

```bash
npm i -g vercel
```

Login:

```bash
vercel login
```

Go to your project:

```bash
cd studybuddy
```

Deploy:

```bash
vercel deploy --prod
```

### 🔄 Deployment Flow

```text
📁 Project
   ↓
vercel deploy --prod
   ↓
⚙️ Build
   ↓
🚀 Production
   ↓
🌍 Public URL
```

---

# 🔐 Environment Variables

Your local app works because of `.env`.

Production also needs the environment variables.

Important ones:

```text
GEMINI_API_KEY
KV_REST_API_URL
KV_REST_API_TOKEN
```

Add them in:

```text
Vercel Dashboard
→ Project
→ Settings
→ Environment Variables
```

### ⚠️ Important

After adding or changing environment variables:

**Redeploy the project.**

Vercel doesn't automatically redeploy after environment-variable changes.

---

# 📱 Mobile Check

Most users access websites from phones.

### ❌ Bad Mobile Design

* 🔤 Text too small
* 🔘 Buttons too tiny
* ↔️ Horizontal overflow
* 🐌 Images take too long to load

### ✅ Good Mobile Design

* 🔤 16px+ readable text
* 👆 Buttons around 40px+ tall
* 📱 Single-column layout
* ⚡ Loads quickly

### 🤖 Antigravity Prompt

```text
Make this app responsive. On screens <600px wide,
stack the layout vertically, increase button sizes
to 44px, and use a hamburger menu.
```

---

# 😱 5 Deploy Errors

## 1️⃣ ❌ Build Failed

### Problem

Missing dependency in `requirements.txt`.

### ✅ Fix

Add the missing package and redeploy.

---

## 2️⃣ 💥 500 Internal Server Error

### Problem

Your Python code crashed in production.

### ✅ Fix

Check:

```text
Vercel Dashboard
→ Functions
→ Logs
```

---

## 3️⃣ ⏱️ Function Timeout

The Hobby plan has a **10-second maximum** per function call.

### ✅ Fix

Stream the output or use a suitable plan with a higher limit.

---

## 4️⃣ 🔑 Environment Variable Not Found

### Problem

You have `.env` locally but didn't add the variable to Vercel.

### ✅ Fix

```text
Dashboard
→ Settings
→ Environment Variables
→ Add variable
→ Redeploy
```

---

## 5️⃣ 🖥️ Site Loads but Is Blank

### Problem

A JavaScript error prevents rendering.

### ✅ Fix

```text
F12
→ Console
→ Find 🔴 red error
→ Fix the line
→ Redeploy
```

---

# 🧠 Universal Debugging Trick

If deployment fails:

```text
📋 Vercel deploy log
        ↓
📋 Copy
        ↓
🤖 Ask AI:
"What is wrong and how do I fix it?"
```

---

# 🔎 Predict the Bug

Suppose deployment succeeds but the website shows:

```text
FUNCTION_INVOCATION_FAILED
```

Vercel logs show:

```text
KeyError: 'GEMINI_API_KEY'
```

### 🚨 What happened?

Your local `.env` has the key.

But the Vercel project doesn't.

So:

```python
os.environ['GEMINI_API_KEY']
```

throws a `KeyError`.

### 🛠️ Fix

```text
1️⃣ Vercel Dashboard
2️⃣ Open project
3️⃣ Settings
4️⃣ Environment Variables
5️⃣ Add GEMINI_API_KEY
6️⃣ Apply to Production / Preview / Development
7️⃣ Save
8️⃣ Redeploy
```

### 🎯 Lesson

```text
.env
= 💻 Your laptop

Vercel Environment Variables
= 🌍 Production
```

You need to configure secrets in both places.

---

# 🏆 The Capstone Hackathon

## ⏰ 2 Weeks

Your final project.

### 📋 Requirements

Build an:

🤖 **AI-powered web app**

that:

* 👤 Is useful to a real person you know
* 🌍 Runs on a public URL
* 🧠 Uses at least one LLM call

### 👥 Teams

* Pairs are allowed
* Submit individually

---

# 🗓️ Hackathon Timeline

```text
💡 TODAY
Pick idea
   ↓
🛠️ WEEK 5
Build MVP
   ↓
✨ WEEK 6
Polish + Deploy
   ↓
🎤 FINAL
Present
```

---

# 💡 12 Project Ideas

### 📚 StudyBuddy Pro

PDF upload + spaced repetition + study streaks.

### 🎵 Lyric Explainer

AI explains metaphors and cultural context.

### 🏏 Cricket Pundit-bot

Live cricket data + AI-generated commentary.

### 🍳 Fridge Chef

Upload a fridge photo → get recipe suggestions.

### 📰 News in 30s

News URL → short summary + bias check.

### 🎤 Voice Notebook

Speak Tamil/Hindi → transcribe → translate → summarise.

### 🌱 Plant Doctor

Leaf photo → identify possible plant disease + suggested fix.

### 📚 Homework Copilot

Math/physics problem → step-by-step explanation.

### 🎮 AI Dungeon Lite

AI-generated text adventure.

### 💌 Letter Generator

Generate formal letters from simple instructions.

### 🗺️ Trip Planner

Create an itinerary from a destination, duration and budget.

### 🌟 Your Own Idea

> Solve a problem **you** have.

---

# 🎁 Starter Template

Don't start completely from zero.

```bash
git clone https://github.com/eos-workshop/capstone-starter
```

Then:

```bash
cd capstone-starter
vercel link
```

Pull environment variables:

```bash
vercel env pull .env.local
```

Run locally:

```bash
vercel dev
```

---

# 📦 What's Inside the Template?

```text
📄 index.html
🎨 app.js
⚙️ api/example.py
📦 requirements.txt
⚙️ vercel.json
🔐 .env.example
📖 README.md
```

### `index.html`

Clean starter page.

### `app.js`

Example `fetch()` call to the backend.

### `api/example.py`

Backend route calling Gemini + KV.

### `requirements.txt`

Python dependencies.

### `vercel.json`

Routing configuration.

### `.env.example`

Required environment variables.

### `README.md`

Setup guide.

---

# 🎤 30-Second Pitch

Stand up and say:

### ① 👋 Who

> "Hi, I'm Arjun."

### ② 💡 What

> "I'm building Plant Doctor."

### ③ ❤️ Why

> "My grandma can't tell yellow leaves are nitrogen deficiency. The app will."

### 🎯 Rule

**3 sentences maximum.**

---

# 👥 Find a Partner

Choose someone with:

* 🤝 A complementary idea
* 🧠 A different skill

A strong combination:

```text
🎨 Frontend-strong
       +
⚙️ Backend-strong
```

Working alone is also fine.

---

# 📅 2-Week Timeline

### 🟢 Sat — 17 May

**Kickoff**

* Pitch
* Pair up
* Fork starter
* Deploy "Hello World"

### 🟡 Tue — 20 May

**MVP Day**

* Core feature working
* Ugly is fine
* Share URL for feedback

### 🔵 Sat — 24 May

**Mid-review**

* Debug with instructors
* Bring your biggest problem

### 🟠 Wed — 28 May

**Polish**

* 📱 Mobile responsive
* 🖼️ Logo
* 🎨 Clean styling
* 📖 README
* 🔒 Feature freeze

### 🔴 Fri — 30 May

**Final Push**

* 🐛 Fix bugs
* 🎥 Record 90-second demo
* 📊 Prepare slides

### 🏆 Sat — 31 May

**Presentations**

* 5 minutes each
* Show live URL
* Answer 2 questions

---

# ⚖️ Capstone Rubric

| 🏆 Criterion           |  Marks |
| ---------------------- | -----: |
| ⚙️ Works end-to-end    |     15 |
| 🤖 Real AI use         |     10 |
| 🧹 Code quality        |     10 |
| 📱 Mobile responsive   |      5 |
| 💡 Originality         |      5 |
| 🎤 Demo + presentation |      5 |
| **Total**              | **50** |

### ⭐ Bonus — +5

* 🌐 Open-source on GitHub
* 📢 Share publicly
* 👥 Get 5 real users

---

# 🆘 If You're Stuck

Available help:

* 🤖 AI Tutor in the lecture
* 💬 Google Chat group
* 👨‍🏫 Mid-review
* 📢 Daily standup channel
* 🤖 Claude / ChatGPT

### 🧠 Important Rule

> **Done is better than perfect.**

Build an ugly working app first.

Then improve it.

---

# 🎓 4-Week Recap

### 🟢 Week 1 — Python + Git

* Python syntax
* Loops
* Functions
* GitHub

### 🔵 Week 2 — Data + ML

* Pandas
* Statistics
* Scikit-learn
* IPL predictor

### 🟣 Week 3 — CV + NLP

* CNNs
* Transformers
* HuggingFace

### 🟠 Week 4 — Ship It

* Stack
* Vibe coding
* Backend
* Deployment

---

# 🚀 Final Takeaway

```text
🐍 Python
   +
🤖 AI
   +
⚙️ Backend
   +
🗄️ Database
   +
🌍 Deployment
   ↓
🚀 REAL AI APP
```

**Now go build something real. 🔥**
