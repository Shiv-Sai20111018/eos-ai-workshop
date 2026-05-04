# 🤖 Session 4A - Scikit-Learn (sklearn)

## 🚀 What I Learned

In this session, I learned about **Scikit-Learn (sklearn)** which is a Python library used for Machine Learning and AI.

It helps computers learn patterns from data and make predictions 🤖

---

# 📚 Important Things

## 📦 Importing sklearn

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

# 📊 Dataset

A dataset is a collection of data.

### Example:

| Study Hours | Marks |
|---|---|
| 1 | 40 |
| 2 | 50 |
| 3 | 70 |

The computer learns the pattern from this data.

---

# 🧠 Features and Labels

## 🔹 Features
Input data given to the model.

Example:
- Study hours
- Attendance

## 🔹 Labels
The output we want.

Example:
- Marks
- Rank

---

# 📈 Linear Regression

Used for prediction.

### 💻 Code

```python
from sklearn.linear_model import LinearRegression
import numpy as np

X = np.array([[1], [2], [3], [4]])
y = np.array([40, 50, 60, 80])

model = LinearRegression()

model.fit(X, y)

print(model.predict([[5]]))
```

### 🖥️ Output

```python
[93.]
```

### 🧠 Understanding
If study hours increase, marks also increase 📈

---

# ✂️ Train Test Split

Data is divided into:
- Training data
- Testing data

This helps check model performance.

### 💻 Code

```python
from sklearn.model_selection import train_test_split

X = [[1], [2], [3], [4]]
y = [10, 20, 30, 40]

X_train, X_test, y_train, y_test = train_test_split(X, y)

print(X_train)
```

### 🖥️ Output

```python
[[2], [4]]
```

---

# ❌ Overfitting

When the model memorizes data too much.

### 🎮 Example
Like memorizing only one game map and failing everywhere else 💀

---

# 🌍 Real Life Uses

sklearn is used in:
- 🤖 AI systems
- 🎮 Gaming analytics
- 📱 Social media apps
- 💰 Business predictions

---

# 🧠 Final Understanding

This session helped me understand how Machine Learning works using sklearn.

Instead of giving every instruction manually, the computer learns patterns from data automatically 🤖✨

---

# 📋 Quick Summary

| 📌 Topic | 🧠 Meaning |
|---|---|
| sklearn | Machine Learning library |
| Dataset | Collection of data |
| Features | Input values |
| Labels | Output values |
| Linear Regression | Prediction model |
| Train Test Split | Dividing data |
| Overfitting | Memorizing too much |

---
