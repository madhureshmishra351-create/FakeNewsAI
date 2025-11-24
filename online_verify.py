import json
from local_test import predict   # your local model function
from online_sources import hybrid_online_check


# --------------------------------------
# ORIGINAL FINAL VERDICT LOGIC
# --------------------------------------
def final_verdict(text, local_pred, wiki, gnews, factcheck):
    label, conf = local_pred["label"], local_pred["confidence"]

    # 1. FACT CHECK API → Highest priority
    if factcheck:
        for fc in factcheck:
            rating = fc.get("rating", "").lower()
            if rating in ["false", "fake", "misleading", "altered"]:
                return "FAKE", "Fact-check API says the claim is false/misleading."

    # 2. Wikipedia strongly matches → TRUE
    if wiki:
        words = text.lower().split()
        matches = sum(1 for w in words if w in wiki.lower())
        if matches >= 2:
            return "TRUE", "Wikipedia strongly confirms this information."

    # 3. GNews confirms → TRUE
    if gnews and len(gnews) >= 1:
        return "TRUE", "Multiple live news articles support this claim."

    # 4. Local model says FAKE but no evidence online → UNCERTAIN
    if label == "FAKE" and conf > 0.95:
        return ("UNCERTAIN",
                "Model predicts fake but online sources cannot confirm. "
                "Treat as suspicious and verify manually.")

    # 5. Default fallback
    return label, "Based on AI model + available online verification."


# --------------------------------------
# MAIN LOOP
# --------------------------------------
if __name__ == "__main__":

    while True:
        text = input("\nEnter news text (or 'q' to quit): ")

        if text.lower() == "q":
            break

        print("\n==== LOCAL AI MODEL PREDICTION ====")
        
        # Call your local test model
        raw_label, raw_conf = predict(text)

        local_pred = {
            "label": raw_label,
            "confidence": float(raw_conf)
        }

        print(f"Local Model: {local_pred['label']} (confidence: {local_pred['confidence']:.4f})")

        print("\n==== ONLINE VERIFICATION SOURCES ====")
        sources = hybrid_online_check(text)

        wiki = sources.get("wikipedia")
        gnews = sources.get("gnews")
        factcheck = sources.get("google_factcheck")

        print("\nWikipedia Summary:")
        print(wiki if wiki else "No info found.")

        print("\nGNews Headlines:")
        print(gnews if gnews else "No related news found.")

        print("\nGoogle Fact Check Results:")
        if factcheck:
            print(json.dumps(factcheck, indent=2, ensure_ascii=False))
        else:
            print("No fact-check results.")

        print("\n===== FINAL VERDICT =====")
        label, reason = final_verdict(text, local_pred, wiki, gnews, factcheck)
        print("Label:", label)
        print("Reason:", reason)
        print()
