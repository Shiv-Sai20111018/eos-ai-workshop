# 🧠 Understanding TP, TN, FP, FN in Machine Learning

## 📌 What are TP, TN, FP, FN?

These are terms used in **Classification Models** in Machine Learning.

They help us understand:
- how correct the model is
- what mistakes the model makes
- how good predictions actually are

These are usually shown using something called a **Confusion Matrix**.

---

# 📦 Confusion Matrix

```text
                    Actual Value
                 Positive   Negative

Predicted Positive    TP         FP
Predicted Negative    FN         TN
```

I understood this like:
> “Comparing prediction vs actual answer.”

---

# 1️⃣ TP — True Positive

True Positive means:

✅ Model predicted YES  
✅ Actual answer was also YES

So the prediction was correct.

---

## 🎯 Example

Spam Email Detector 📧

| Situation | Result |
|---|---|
| Email is spam | YES |
| Model says spam | YES |

This is:
# ✅ True Positive

---

## 💻 Example Code

```python
actual = 1
predicted = 1

if actual == 1 and predicted == 1:
    print("True Positive")
```

---

# 2️⃣ TN — True Negative

True Negative means:

✅ Model predicted NO  
✅ Actual answer was also NO

Correct rejection.

---

## 🎯 Example

| Situation | Result |
|---|---|
| Email is NOT spam | NO |
| Model says NOT spam | NO |

This is:
# ✅ True Negative

---

## 💻 Example Code

```python
actual = 0
predicted = 0

if actual == 0 and predicted == 0:
    print("True Negative")
```

---

# 3️⃣ FP — False Positive

False Positive means:

❌ Model predicted YES  
❌ Actual answer was NO

Wrong positive prediction.

---

## 🎯 Example

| Situation | Result |
|---|---|
| Email is NOT spam | NO |
| Model says spam | YES |

This is:
# ❌ False Positive

---

## 🧠 Easy Understanding

FP is like:
> “Model got overconfident and said YES incorrectly.”

---

## 💻 Example Code

```python
actual = 0
predicted = 1

if actual == 0 and predicted == 1:
    print("False Positive")
```

---

# 4️⃣ FN — False Negative

False Negative means:

❌ Model predicted NO  
❌ Actual answer was YES

Wrong negative prediction.

---

## 🎯 Example

| Situation | Result |
|---|---|
| Email is spam | YES |
| Model says NOT spam | NO |

This is:
# ❌ False Negative

---

## 🧠 Easy Understanding

FN is like:
> “Model failed to detect something important.”

---

## 💻 Example Code

```python
actual = 1
predicted = 0

if actual == 1 and predicted == 0:
    print("False Negative")
```

---

# 🎮 Gamer Analogy

Imagine an enemy detector in a game 🎮

| Situation | Meaning |
|---|---|
| Enemy detected correctly | TP |
| No enemy detected correctly | TN |
| Detector says enemy but nobody there | FP |
| Detector misses actual enemy | FN |

This made it super easy for me to understand.

---

# 📊 Real Example

Suppose:

- 100 emails checked
- 70 correctly detected spam
- 20 correctly detected normal emails
- 5 normal emails marked spam
- 5 spam emails missed

Then:

| Type | Value |
|---|---|
| TP | 70 |
| TN | 20 |
| FP | 5 |
| FN | 5 |

---

# 📈 Why These Are Important

Using TP, TN, FP, FN we calculate:
- Accuracy
- Precision
- Recall
- F1 Score

These help measure model performance.

---

# 🎯 Accuracy

Accuracy means:
> How many predictions were correct overall.

Formula:

```text
(TP + TN) / Total Predictions
```

---

## 💻 Example Code

```python
TP = 70
TN = 20
FP = 5
FN = 5

accuracy = (TP + TN) / (TP + TN + FP + FN)

print(accuracy)
```

---

# 🎯 Precision

Precision means:
> Out of all predicted YES, how many were actually YES?

Formula:

```text
TP / (TP + FP)
```

---

## 💻 Example Code

```python
precision = TP / (TP + FP)

print(precision)
```

---

# 🎯 Recall

Recall means:
> Out of all actual YES cases, how many did the model detect?

Formula:

```text
TP / (TP + FN)
```

---

## 💻 Example Code

```python
recall = TP / (TP + FN)

print(recall)
```

---

# 🎯 F1 Score

F1 Score balances:
- Precision
- Recall

Formula:

```text
2 × (Precision × Recall)
-------------------------
   Precision + Recall
```

---

## 💻 Example Code

```python
f1 = 2 * (precision * recall) / (precision + recall)

print(f1)
```

---

# 🚀 Full Example Program

```python
TP = 70
TN = 20
FP = 5
FN = 5

accuracy = (TP + TN) / (TP + TN + FP + FN)

precision = TP / (TP + FP)

recall = TP / (TP + FN)

f1 = 2 * (precision * recall) / (precision + recall)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
```

---

# 🧠 What I Understood

- TP = predicted YES correctly
- TN = predicted NO correctly
- FP = wrong YES prediction
- FN = wrong NO prediction

These values help us understand:
- model mistakes
- model performance
- prediction quality

---

# ⭐ Final Understanding

I understood TP, TN, FP, FN like this:

> “They are basically the report card of a Machine Learning model.”

They show:
- where the model is smart
- where the model gets confused
- how reliable predictions actually are
