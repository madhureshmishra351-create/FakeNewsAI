import pandas as pd
import torch
from torch.utils.data import DataLoader
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
from torch.optim import AdamW
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from dataset import FakeNewsDataset
from utils import save_model

# -----------------------------------
# Load NEW dataset (WELFake)
# -----------------------------------
df = pd.read_csv(r"C:\FakeNews-main\WELFake_Dataset.csv")

# Make sure columns are named correctly
df['text'] = df['text'].astype(str)
df['label'] = df['label'].astype(int)

texts = df['text'].tolist()
labels = df['label'].tolist()

# -----------------------------------
# Split BEFORE tokenization
# -----------------------------------
train_texts, test_texts, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42
)

# -----------------------------------
# Tokenizer
# -----------------------------------
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
test_encodings = tokenizer(test_texts, truncation=True, padding=True, max_length=128)

# -----------------------------------
# Datasets & Loaders
# -----------------------------------
train_dataset = FakeNewsDataset(train_encodings, y_train)
test_dataset = FakeNewsDataset(test_encodings, y_test)

train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=8, shuffle=False)

# -----------------------------------
# Model Setup
# -----------------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=2
)
model.to(device)

optimizer = AdamW(model.parameters(), lr=2e-5)

# -----------------------------------
# TRAINING FOR 1 EPOCH
# -----------------------------------
EPOCHS = 1

for epoch in range(EPOCHS):
    model.train()
    loop = tqdm(train_loader, leave=True)

    for batch in loop:
        optimizer.zero_grad()

        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        outputs = model(
            input_ids,
            attention_mask=attention_mask,
            labels=labels
        )

        loss = outputs.loss
        loss.backward()
        optimizer.step()

        loop.set_description(f"Epoch {epoch+1}")
        loop.set_postfix(loss=loss.item())

# -----------------------------------
# Save Model
# -----------------------------------
save_model(model, tokenizer)
print("Model saved successfully!")
