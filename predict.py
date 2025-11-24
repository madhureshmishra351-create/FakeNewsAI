import torch
from utils import load_model

model, tokenizer = load_model()
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(device)

def predict(text):
    tokens = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=128)
    tokens = {k: v.to(device) for k, v in tokens.items()}
    with torch.no_grad():
        output = model(**tokens)
    pred = torch.argmax(output.logits, dim=1).item()
    return "FAKE" if pred == 1 else "REAL"

if __name__ == "__main__":
    while True:
        txt = input("\nEnter text: ")
        print("Prediction:", predict(txt))
