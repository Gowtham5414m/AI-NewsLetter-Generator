import requests
import os
def get_custom_news(query, language="en", page_size=50):
    api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/everything?q={query}&language={language}&pageSize={page_size}&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["articles"]
    else:
        print("Error fetching custom news:", response.status_code)
        return []

def get_top_headlines(category="general", country="in"):
    api_key = os.getenv("NEWS_API_KEY")

    url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={api_key}"
    response = requests.get(url)

    data = response.json()

    # If no results, fallback to 'everything' endpoint with keyword = country
    if data.get("status") == "ok" and data.get("articles"):
        return data["articles"]
    else:
        print("⚠️ No top headlines. Trying fallback keyword search...")

        # fallback search for India news
        fallback_url = f"https://newsapi.org/v2/everything?q=india&sortBy=publishedAt&language=en&apiKey={api_key}"
        fallback_response = requests.get(fallback_url)
        fallback_data = fallback_response.json()

        if fallback_data.get("status") == "ok" and fallback_data.get("articles"):
            return fallback_data["articles"]
        else:
            return []
