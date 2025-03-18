import requests
import time
import webbrowser

def NewsFromBBC():
    query_params = {
        "source": "bbc-news",
        "sortBy": "top",
        "apiKey": "14c4fe6f53fc4f4b84ff7bfed0e5123f"
    }
    main_url = "https://newsapi.org/v1/articles"

    try:
        res = requests.get(main_url, params=query_params)
        res.raise_for_status()
        open_bbc_page = res.json()

        article = open_bbc_page["articles"]

        results = []

        print("Top news from BBC:")
        for idx, ar in enumerate(article, start=1):
            results.append(ar["title"])
            print(f"{idx}. {ar['title']}")

        more_details = input("Do you want detailed news on any article? (yes/no): ").strip().lower()

        if more_details == "yes":
            article_index = int(input(f"Please enter the article number (1-{len(results)}): ")) - 1

            if 0 <= article_index < len(results):
                chosen_article = article[article_index]
                print(f"Title: {chosen_article['title']}")
                print(f"Published At: {chosen_article['publishedAt']}")
                print(f"Description: {chosen_article['description']}")
                
                open_article = input(f"Would you like to read the full article in your browser? (yes/no): ").strip().lower()

                if open_article == "yes":
                    webbrowser.open(chosen_article['url'])
                    print(f"Opening the full article in your browser: {chosen_article['url']}")
                else:
                    print("Okay, not opening the full article.")

            else:
                print(f"Invalid article number. Please enter a number between 1 and {len(results)}.")
        
        else:
            print("Okay, no detailed news will be displayed.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the news: {e}")

if __name__ == '__main__':
    NewsFromBBC()
