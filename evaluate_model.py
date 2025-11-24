import pandas as pd
import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from concurrent.futures import ThreadPoolExecutor
import numpy as np

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load model + tokenizer
model_path = "models/best_model"
tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)
model = DistilBertForSequenceClassification.from_pretrained(model_path)
model.to(device)
model.eval()

# Load test dataset
df = pd.read_csv("data/test.csv")

# CLEAN TEXT
df["text"] = df["text"].fillna("").astype(str)
df["label"] = df["label"].astype(int)

texts = df["text"].tolist()
labels = df["label"].tolist()

print(f"Loaded {len(texts)} test samples")

# ---------------------------
# ⚡ MULTI-THREAD TOKENIZATION
# ---------------------------
def tokenize_batch(batch):
    return tokenizer(batch, truncation=True, padding=True, max_length=128)

batch_size = 64
all_preds = []

print("\nEvaluating... please wait...\n")

for start in range(0, len(texts), batch_size):

    end = start + batch_size
    batch_texts = texts[start:end]

    # Threaded tokenization (4 threads)
    with ThreadPoolExecutor(max_workers=4) as executor:
        future = executor.submit(tokenize_batch, batch_texts)
        encodings = future.result()

    # Convert to torch tensors
    input_ids = torch.tensor(encodings["input_ids"]).to(device)
    attention_mask = torch.tensor(encodings["attention_mask"]).to(device)

    # Run model
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        preds = torch.argmax(outputs.logits, dim=1).cpu().numpy()

    all_preds.extend(preds)

# Metrics
accuracy = accuracy_score(labels, all_preds)
precision, recall, f1, _ = precision_recall_fscore_support(labels, all_preds, average="binary")
cm = confusion_matrix(labels, all_preds)

print("\n===== MODEL PERFORMANCE =====")
print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")

print("\nConfusion Matrix:")
print(cm)
