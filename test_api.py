import requests, urllib.parse, json

q = "nepal genz chose their government via discord vote"
print("=== WIKI SEARCH ===")
r = requests.get("https://en.wikipedia.org/w/api.php",
                 params={"action":"query","list":"search","srsearch": q,"format":"json"})
print(r.status_code, r.json().get("query", {}).get("search")[:2])

print("\n=== GNEWS ===")
gnews_key = "YOUR GNEWS API KEY"
r = requests.get("https://gnews.io/api/v4/search",
                 params={"q": q, "token": gnews_key, "lang":"en", "max": 10})
print(r.status_code, list(r.json().keys()) )
if "articles" in r.json(): print(len(r.json()["articles"]))

print("\n=== GOOGLE FACTCHECK ===")
fact_key = "YOUR GOOGLE FACTCHECK API"
r = requests.get("https://factchecktools.googleapis.com/v1alpha1/claims:search",
                 params={"key": fact_key, "query": q, "pageSize": 5})
print(r.status_code)
print(json.dumps(r.json(), indent=2)[:1000])

