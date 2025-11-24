import torch
def save_model(model, tokenizer, path="models/best_model/"):
    model.save_pretrained(path)
    tokenizer.save_pretrained(path)
    print("Model saved to:", path)

def load_model(path="models/best_model/"):
    from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
    tokenizer = DistilBertTokenizerFast.from_pretrained(path)
    model = DistilBertForSequenceClassification.from_pretrained(path)
    return model, tokenizer
