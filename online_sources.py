import requests
import re

# -----------------------------
# CLEAN QUERY FOR SEARCH ENGINES
# -----------------------------
def clean_query(text):
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    words = text.split()
    words = words[:6]   # keep first 6 words only
    return " ".join(words)


# -----------------------------
# WIKIPEDIA SEARCH FIXED
# -----------------------------
def wiki_verify(query):
    try:
        clean = clean_query(query)

        url = "https://en.wikipedia.org/w/api.php"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        params = {
            "action": "query",
            "list": "search",
            "srsearch": clean,
            "format": "json"
        }

        r = requests.get(url, params=params, headers=headers)
        data = r.json()

        if "query" not in data or len(data["query"]["search"]) == 0:
            return None

        title = data["query"]["search"][0]["title"]

        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
        summary = requests.get(summary_url, headers=headers).json()

        return summary.get("extract", None)

    except:
        return None


# -----------------------------
# GNEWS SEARCH
# -----------------------------
def gnews_verify(query):
    try:
        clean = clean_query(query)

        API_KEY = "082fc7ce2050690282adc285e57bf445"
        url = f"https://gnews.io/api/v4/search?q={clean}&token={API_KEY}"

        data = requests.get(url).json()

        if "articles" not in data:
            return None

        return [a["title"] for a in data["articles"][:5]]

    except:
        return None


# -----------------------------
# GOOGLE FACTCHECK
# -----------------------------
def google_factcheck(query):
    try:
        clean = clean_query(query)

        API_KEY = "AIzaSyAaNyl-QLQdgztBa-fxkq3JVp31PFaI0MQ"
        API_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

        params = {
            "query": clean,
            "pageSize": 5,
            "key": API_KEY
        }

        data = requests.get(API_URL, params=params).json()

        if "claims" not in data:
            return None

        results = []
        for claim in data["claims"]:
            review = claim["claimReview"][0]
            results.append({
                "claim": claim.get("text", ""),
                "rating": review.get("textualRating", ""),
                "source": review.get("publisher", {}).get("name", ""),
                "url": review.get("url", "")
            })

        return results

    except:
        return None



# -----------------------------
# HYBRID CHECK
# -----------------------------
def hybrid_online_check(text):
    return {
        "wikipedia": wiki_verify(text),
        "gnews": gnews_verify(text),
        "google_factcheck": google_factcheck(text)
    }
