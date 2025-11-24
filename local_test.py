from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast
import torch

model_path = "models/best_model"

# Load model + tokenizer
model = DistilBertForSequenceClassification.from_pretrained(model_path)
tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)

def predict(text):
    tokens = tokenizer(text, truncation=True, padding=True, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**tokens)
        probs = torch.softmax(outputs.logits, dim=1)
        fake_prob = probs[0][1].item()
        label = "FAKE" if fake_prob > 0.5 else "REAL"

    return label, round(fake_prob, 4)

print(predict("India changes its currency from rupees to dollars"))
print(predict("The earth revolves around the sun"))
