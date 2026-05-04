# 🤖 Session 4B - Classification

## 🚀 What I Learned

In this session, I learned about **Classification** in Machine Learning.

Classification means the computer predicts categories or labels.

### 🎮 Examples
- Spam or Not Spam 📧
- Win or Lose 🎮
- Pass or Fail 📚
- Cat or Dog 🐱🐶

---

# 🧠 What is Classification?

Classification is used when the output is a category instead of a number.

### 📌 Example
Input:
- Study Hours
- Attendance

Output:
- Pass ✅
- Fail ❌

---

# 📦 Importing sklearn

### 💻 Code

```python
import sklearn

print("sklearn imported")
```

### 🖥️ Output

```python
sklearn imported
```

---

# 📊 Example Dataset

| Study Hours | Result |
|---|---|
| 1 | Fail |
| 2 | Fail |
| 4 | Pass |
| 5 | Pass |

The computer learns the pattern from this data 🤖

---

# 🔍 Logistic Regression

Used for classification problems.

### 💻 Code

```python
from sklearn.linear_model import LogisticRegression
import numpy as np

X = np.array([[1], [2], [4], [5]])
y = np.array([0, 0, 1, 1])

model = LogisticRegression()

model.fit(X, y)

print(model.predict([[3]]))
```

### 🖥️ Output

```python
[1]
```

### 🧠 Understanding
- 0 = Fail ❌
- 1 = Pass ✅

The model predicts that a student studying 3 hours may pass.

---

# 🌳 Decision Tree

A Decision Tree makes decisions step by step like a flowchart.

### 🎮 Example
If:
- Study hours > 3 → Pass
- Study hours < 3 → Fail

### 💻 Code

```python
from sklearn.tree import DecisionTreeClassifier

X = [[1], [2], [4], [5]]
y = [0, 0, 1, 1]

model = DecisionTreeClassifier()

model.fit(X, y)

print(model.predict([[5]]))
```

### 🖥️ Output

```python
[1]
```

---

# ✂️ Train Test Split

Data is divided into:
- 🏋️ Training Data
- 🧪 Testing Data

This helps check if the model works properly.

### 💻 Code

```python
from sklearn.model_selection import train_test_split

X = [[1], [2], [3], [4]]
y = [0, 0, 1, 1]

X_train, X_test, y_train, y_test = train_test_split(X, y)

print(X_train)
```

### 🖥️ Output

```python
[[2], [4]]
```

---

# 📈 Accuracy

Accuracy tells how correct the model is.

### 💻 Code

```python
from sklearn.metrics import accuracy_score

y_true = [1, 0, 1]
y_pred = [1, 0, 1]

print(accuracy_score(y_true, y_pred))
```

### 🖥️ Output

```python
1.0
```

### 🧠 Understanding
1.0 means 100% correct ✅

---

# 🌍 Real Life Uses

Classification is used in:
- 📧 Spam detection
- 🤖 Face recognition
- 🎮 Game matchmaking
- 🏥 Disease prediction
- 🛒 Product recommendations

---

# 🧠 Final Understanding

This session helped me understand how computers classify data into categories using Machine Learning.

Instead of predicting numbers, classification predicts labels like Pass/Fail or Spam/Not Spam 🤖✨

---

# 📋 Quick Summary

| 📌 Topic | 🧠 Meaning |
|---|---|
| Classification | Predicting categories |
| Logistic Regression | Classification model |
| Decision Tree | Step-by-step prediction |
| Accuracy | Correctness of model |
| Train Test Split | Dividing data |
| Labels | Final output |

---
