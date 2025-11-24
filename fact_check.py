import requests

# -------------------------
# 1. WIKIPEDIA CHECK
# -------------------------
def wiki_verify(query):
    try:
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json"
        }

        response = requests.get(url, params=params).json()

        if len(response["query"]["search"]) == 0:
            return None

        # Get top page
        title = response["query"]["search"][0]["title"]
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"

        summary_data = requests.get(summary_url).json()
        return summary_data.get("extract", None)

    except Exception:
        return None


# -------------------------
# 2. GNEWS SEARCH (FREE TIER)
# -------------------------
def gnews_verify(query):
    API_KEY = "082fc7ce2050690282adc285e57bf445"  # free 100 req/day
    url = f"https://gnews.io/api/v4/search?q={query}&token={API_KEY}"

    try:
        r = requests.get(url).json()
        if "articles" not in r:
            return None

        titles = [article["title"] for article in r["articles"]]
        return titles
    except Exception:
        return None


# -------------------------
# 3. GOOGLE FACT CHECK API
# -------------------------
def google_factcheck(query):
    API_KEY = "AIzaSyAaNyl-QLQdgztBa-fxkq3JVp31PFaI0MQ"  # free, no card required
    API_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

    params = {
        "key": API_KEY,
        "query": query,
        "pageSize": 5
    }

    try:
        response = requests.get(API_URL, params=params).json()

        if "claims" not in response:
            return None

        result = []
        for claim in response["claims"]:
            info = claim["claimReview"][0]
            result.append({
                "claim": claim.get("text", ""),
                "rating": info.get("textualRating", ""),
                "source": info.get("publisher", {}).get("name", ""),
                "url": info.get("url", "")
            })

        return result

    except Exception:
        return None


# -------------------------
# HYBRID ONLINE VERIFICATION
# -------------------------

def hybrid_online_check(text):
    return {
        "wikipedia": wiki_verify(text),
        "gnews": gnews_verify(text),
        "google_factcheck": google_factcheck(text)
    }
