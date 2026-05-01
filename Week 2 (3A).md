# 📊 Session 3A – Pandas 

## 🌟 What is Pandas?
- Pandas is a Python library used to handle data in tables (like Excel).
- It makes data easy to read, clean, and analyze.
- Think of it as a tool that helps you **organize messy data into neat rows and columns**.

---

## 🛠️ Loading Data
- First step is always to bring data into Pandas.
- Data usually comes from `CSV files` (comma‑separated values).

```python
import pandas as pd

url = "https://orent.vercel.app/data.csv"
ipl = pd.read_csv(url)

ipl.head()       # shows first 5 rows
ipl.info()       # shows column names and data types
ipl.describe()   # shows summary like mean, min, max
```

---

## 🔍 Selecting & Filtering Data
- You can pick specific columns or rows.

- You can also filter rows based on conditions.

```
ipl['runs']                     # single column
ipl[['player','runs']]          # multiple columns
ipl[ipl['runs'] > 500]          # players with runs > 500
ipl[(ipl['team']=='CSK') & (ipl['runs']>200)]  # CSK players with >200 runs
ipl[(ipl['team']=='CSK') | (ipl['team']=='MI')] # CSK or MI players
ipl[~(ipl['team']=='CSK')]      # players not in CSK
```
---

## 🎯 Indexing (iloc vs loc)
- `iloc` → uses row numbers (like positions).

- `loc` → uses labels (like names).


```
ipl.iloc[1]              # 2nd row
ipl.loc['Dhoni']         # row with label 'Dhoni'
ipl.iloc[0:2]            # first 2 rows (end excluded)
ipl.loc['Kohli':'Dhoni'] # rows from Kohli to Dhoni (end included)
ipl.iloc[1,2]            # single cell by position
ipl.loc['Kohli','runs']  # single cell by label
```

- `iloc` excludes last index, loc includes last label.

---

## 🧹 Cleaning Data
- Real data is messy → missing values, duplicates, wrong types.

- Pandas gives tools to fix this.


```
ipl.isna().sum()                       # count missing values
ipl = ipl.dropna()                     # remove rows with missing values
ipl['avg'] = ipl['avg'].fillna(ipl['avg'].mean())  # fill with mean

ipl = ipl.drop_duplicates()            # remove duplicate rows
ipl['runs'] = ipl['runs'].astype(int)  # change type to integer
ipl['date'] = pd.to_datetime(ipl['date'])  # convert to date format
```
---

## 📊 Grouping & Aggregation
- Grouping means splitting data into categories and applying functions


```
ipl.groupby('team')['runs'].mean()     # average runs per team
ipl.groupby('team')['runs'].agg(['mean','max','count'])
```



---

## 📈 Sorting & Leaderboards
- Sorting helps find top or bottom values.

```
top10 = ipl.sort_values('runs', ascending=False).head(10)
top10[['player','team','runs']]
```






---

## 🧾 Pandas Quick Table

| Task                | Code Example                                |
|---------------------|---------------------------------------------|
| Load CSV            | `pd.read_csv('file.csv')`                   |
| First look          | `df.head(); df.info(); df.describe()`       |
| Select column       | `df['col']`                                 |
| Filter rows         | `df[df['col'] > 5]`                         |
| Multiple conditions | `df[(a>5) & (b<10)]`                        |
| Drop NaN            | `df.dropna()`                               |
| Fill NaN            | `df.fillna(value)`                          |
| Drop duplicates     | `df.drop_duplicates()`                      |
| Group + aggregate   | `df.groupby('col')['x'].mean()`             |
| Sort                | `df.sort_values('col', ascending=False)`    |








------















