import pandas as pd
import re
import html

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = html.unescape(text)
    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"@\w+", " ", text)
    text = re.sub(r"#", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def load_and_merge(fake_path, real_path):
    df_fake = pd.read_csv(fake_path)
    df_true = pd.read_csv(real_path)

    df_fake['label'] = 1
    df_true['label'] = 0

    df = pd.concat([df_fake, df_true], ignore_index=True)
    df['text'] = df['title'].fillna('') + ". " + df['text'].fillna('')
    df['text'] = df['text'].apply(clean_text)
    df = df[['text', 'label']]

    df.to_csv("data/merged.csv", index=False)
    print("Merged dataset saved at data/merged.csv")
    return df
