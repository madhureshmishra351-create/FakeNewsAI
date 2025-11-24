import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
from fact_check import hybrid_online_check

device = "cuda" if torch.cuda.is_available() else "cpu"

model_path = "models/best_model"
tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)
model = DistilBertForSequenceClassification.from_pretrained(model_path).to(device)
model.eval()


def offline_ai_predict(text, threshold=0.70):
    tokens = tokenizer(text, truncation=True, padding=True, max_length=128, return_tensors="pt")
    tokens = {k: v.to(device) for k, v in tokens.items()}

    with torch.no_grad():
        outputs = model(**tokens)
        probs = torch.softmax(outputs.logits, dim=1)
        fake_prob = probs[0][1].item()

    if fake_prob > threshold:
        return "FAKE", fake_prob
    else:
        return "REAL", fake_prob


def hybrid_predict(text):
    # 1. AI prediction
    ai_label, ai_prob = offline_ai_predict(text)

    # 2. Internet verification
    online = hybrid_online_check(text)

    # 3. Final decision strategy
    final = {
        "ai_label": ai_label,
        "ai_confidence": ai_prob,
        "online_verification": online
    }

    return final
