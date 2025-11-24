import pandas as pd
from sklearn.model_selection import train_test_split

# Load the WELFake dataset
df = pd.read_csv("data/WELFake_Dataset.csv")

# Make sure columns exist: title, text, label
df['text'] = df['text'].astype(str)
df['label'] = df['label'].astype(int)

# Create train/test split
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Save the splits
train_df.to_csv("data/train.csv", index=False)
test_df.to_csv("data/test.csv", index=False)

print("Train and test files created successfully.")
