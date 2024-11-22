from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup



def find_url(league: str):
    league_code = {
        "premier-league": "47",
        "ligue-1": "53",
        "laliga": "87",
        "bundesliga": "54",
        "serie": "55"
    }

    return f"https://www.fotmob.com/leagues/{league_code[league]}/matches/{league}"

def find_matches(league: str, season: str, gameweek: int):
    service = Service(executable_path="/Users/jamesgough/Documents/OtherMLwork/Match_Prediction_Project/src/utils/chromedriver")
    driver = webdriver.Chrome(service=service)
    driver.get(find_url(league))

    # By Round
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "css-6r1k3j-TabCSS-navCommonStyles-TabIndicatorStyle-navStyles.e1pwpk670"))
    )

    by_round_button = driver.find_element(By.CLASS_NAME, "css-6r1k3j-TabCSS-navCommonStyles-TabIndicatorStyle-navStyles.e1pwpk670")
    by_round_button.click()

    # Select year
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "css-pf0wkf-Select.e1nudmbp0"))
    )

    season_dropdown = driver.find_element(By.CLASS_NAME, "css-pf0wkf-Select.e1nudmbp0")
    selection = Select(season_dropdown)
    selection.select_by_visible_text(season)
    season_dropdown.click()

    round_class_code = {
        "premier-league": {
            "2024/2025": "e74wx4",
            "2023/2024": "rvl1i2",
            "2022/2023": "rvl1i2",
            "2021/2022": "rvl1i2"
        },
        "ligue-1": {
            "2024/2025": "e74wx4",
            "2023/2024": "rf6vlc",
            "2022/2023": "rvl1i2",
            "2021/2022": "rvl1i2"
        },
        "serie": {
            "2024/2025": "1mo91hl",
            "2023/2024": "rvl1i2",
            "2022/2023": "1anwnbh",
            "2021/2022": "rvl1i2"
        },
        "bundesliga": {
            "2024/2025": "18qsom",
            "2023/2024": "rf6vlc",
            "2022/2023": "rf6vlc",
            "2021/2022": "rf6vlc"
        },
        "laliga": {
            "2024/2025": "qoqv6y",
            "2023/2024": "rvl1i2",
            "2022/2023": "rvl1i2",
            "2021/2022": "rvl1i2"
        },
    } 

    # Select Round
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, f"css-{round_class_code[league][season]}-Select.e1nudmbp0"))
    )

    round_dropdown = driver.find_element(By.CLASS_NAME, f"css-{round_class_code[league][season]}-Select.e1nudmbp0")
    selection = Select(round_dropdown)
    selection.select_by_visible_text("Round " + str(gameweek))
    round_dropdown.click()

    # Find Matches
    matches_page = driver.find_element(By.CLASS_NAME, "slick-slide.slick-active.slick-current")
    match_sections = matches_page.find_elements(By.TAG_NAME, "section")

    match_links = []

    for section in match_sections:
        links = section.find_elements(By.TAG_NAME, "a")

        for link in links:
            href = link.get_attribute("href")
            # Check that the href is not "None"
            if href:
                match_links.append(href)

    print(match_links)

    driver.quit()

    return match_links

find_matches("premier-league", "2024/2025", 7)

    # if season == "2021-22":
    #     if league == "bundesliga":
    #         return f"https://www.fotmob.com/leagues/{league_code[league]}/matches/{league}?group=by-round&round={str(gameweek)}&season={season}"
    #     if league == "serie":
    #         return f"https://www.fotmob.com/leagues/{league_code[league]}/matches/{league}?season={season}&group=by-round&round={str(gameweek)}"
    #     return f"https://www.fotmob.com/leagues/{league_code[league]}/matches/{league}?group=by-round&season={season}&round={str(gameweek)}"
    
    # if season == "2022-23":
    #     if league == "serie":
    #         return f"https://www.fotmob.com/leagues/{league_code[league]}/matches/{league}?group=by-round&season={season}&round={str(gameweek)}"
    #     return f"https://www.fotmob.com/leagues/{league_code[league]}/matches/{league}?season={season}&group=by-round&round={str(gameweek)}"
    
    # if season == "2023-24":
    #     if league == "premier-league":
    #         return f"https://www.fotmob.com/leagues/{league_code[league]}/matches/{league}?group=by-round&round={str(gameweek)}&season={season}"
    #     if league == "serie":
    #         return f"https://www.fotmob.com/leagues/{league_code[league]}/matches/{league}?group=by-round&season={season}&round={str(gameweek)}"
    #     return f"https://www.fotmob.com/leagues/{league_code[league]}/matches/{league}?season={season}&group=by-round&round={str(gameweek)}"


# def scrape_matches(league: str, season: str, gameweek: int):
#     url = find_url(league, season, gameweek)

#     print(url)

#     response = requests.get(url)

#     if response.status_code != 200:
#         print("Error! Invalid Status Code!")

#     soup = BeautifulSoup(response.content, "html.parser")

#     dates = soup.select_one('h1[style="position:absolute;left:-9999px"]')

#     print(dates)

#     match_list = soup.select('section[class="css-3v2ydy-LeagueMatchesSectionCSS e1qa64rr0"] a')

#     print(match_list)

#     matches = [match.attrs['href'] for match in match_list]

#     print(matches)
    
# scrape_matches("laliga", "2022-23", 34)

