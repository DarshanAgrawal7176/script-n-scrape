import requests
from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent

def get_movie_data(url):
    user_agent = UserAgent().random  
    headers = {"User-Agent": user_agent}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        
        title = soup.find("h1").get_text(strip=True) if soup.find("h1") else "N/A"

        
        year = (
            soup.find("span", {"id": "titleYear"}).get_text(strip=True).strip("()")
            if soup.find("span", {"id": "titleYear"})
            else "N/A"
        )
    
        duration = (
            soup.find("time").get_text(strip=True) if soup.find("time") else "N/A"
        )

        rating = (
            soup.find("span", {"itemprop": "ratingValue"}).get_text(strip=True)
            if soup.find("span", {"itemprop": "ratingValue"})
            else "N/A"
        )

        # Genres
        genres = [
            genre.get_text(strip=True)
            for genre in soup.findAll("span", {"class": "genre"})
        ] or ["N/A"]

    
        directors = [
            director.get_text(strip=True)
            for director in soup.findAll("a", href=True)
            if "dr_" in director.get("href", "")
        ] or ["N/A"]

       
        cast = [
            actor.get_text(strip=True)
            for actor in soup.select("table.cast_list a")[:5]
        ] or ["N/A"]

        
        summary = (
            soup.find("div", {"class": "summary_text"}).get_text(strip=True)
            if soup.find("div", {"class": "summary_text"})
            else "N/A"
        )

        
        image_url = (
            soup.find("div", {"class": "poster"}).find("img")["src"]
            if soup.find("div", {"class": "poster"}) and soup.find("div", {"class": "poster"}).find("img")
            else "N/A"
        )

        return {
            "title": title,
            "year": year,
            "duration": duration,
            "rating": rating,
            "genres": genres,
            "directors": directors,
            "main_cast": cast,
            "summary": summary,
            "image_url": image_url,
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def scrape_movies(base_url, count):
    movies = []

    
    for i in range(1, count + 1):
        try:
            url = f"{base_url}?start={i * 50}&ref_=adv_nxt"  
            movie_data = get_movie_data(url)
            if movie_data:
                movies.append(movie_data)
                print(f"Scraped: {movie_data['title']}")
        except Exception as e:
            print(f"Error scraping page {i}: {e}")

    
    with open("movies.json", "w") as f:
        json.dump(movies, f, indent=4)

    print(f"Scraped {len(movies)} movies and saved to movies.json!")


if __name__ == "__main__":
    BASE_URL = "https://www.imdb.com/search/title/?groups=top_1000"
    MOVIE_COUNT = 100  
    scrape_movies(BASE_URL, MOVIE_COUNT)



