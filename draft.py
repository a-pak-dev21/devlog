import pandas as pd

df = pd.DataFrame({
    "name": ["Alice", "Bob", "charlie"],
    "age": [25, 30, 40]
})

print(df)
row = df.loc[0]
print(type(row))
print(len(row))
print(type(row))
row1 = str(row)
print(row1)
print(type(row1))