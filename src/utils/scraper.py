from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup
from datetime import datetime


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

    driver.quit()

    return match_links

def scrape_match(url: str):
    service = Service(executable_path="/Users/jamesgough/Documents/OtherMLwork/Match_Prediction_Project/src/utils/chromedriver")
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Stats")]'))
    )

    stats_page_button = driver.find_element(By.XPATH, '//button[contains(text(), "Stats")]')
    stats_page_button.click()

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # MATCH DATE AND TIME
    match_date, match_time = scrape_match_date_time(soup)

    # TEAM NAMES
    home_team = soup.select_one(".css-12r3z1-TeamName span.css-dpbuul-TeamNameItself-TeamNameOnTabletUp").text.strip()
    away_team = soup.select_one(".css-4nnvmn-TeamName span.css-dpbuul-TeamNameItself-TeamNameOnTabletUp").text.strip()

    # MATCH RESULT & TEAM GOAL DIFFERENCE
    match_result = soup.select_one(".css-ktw5ic-MFHeaderStatusScore").text.strip()

    home_team_GF = int(match_result.split(" - ")[0])
    away_team_GF = int(match_result.split(" - ")[1])

    home_team_GA = away_team_GF
    away_team_GA = home_team_GF

    result_home_win = 0
    result_away_win = 0
    result_draw = 0

    if home_team_GF > away_team_GF:
        result_home_win = 1
    elif home_team_GF < away_team_GF:
        result_away_win = 1
    else:
        result_draw = 1

    home_team_GD = home_team_GF - home_team_GA
    away_team_GD = away_team_GF - away_team_GA

    # MATCH NPXG TOTALS
    home_npxg, away_npxg = scrape_stat("Non-penalty xG", soup)
    home_npxgd = home_npxg - away_npxg
    away_npxgd = away_npxg - home_npxg

    # MATCH BIG CHANCE TOTALS
    home_bcc, away_bcc = scrape_stat("Big chances", soup)
    home_bcd = home_bcc - away_bcc
    away_bcd = away_bcc - home_bcc

    # MATCH FINISHING QUALITY TOTALS
    home_xg, away_xg = scrape_stat("Expected goals (xG)", soup)
    home_xgot, away_xgot = scrape_stat("xG on target (xGOT)", soup)

    home_finishing_quality = home_xgot - home_xg
    away_finishing_quality = away_xgot - away_xg

    # HEAD-TO-HEAD MATCH HISTORY
    h2h_home_win_pct, h2h_draw_pct, h2h_away_win_pct = scrape_head_2_head(driver)

    driver.quit()

    # WHAT TO RETURN!!!!!!!
    return

def scrape_stat(stat: str, soup: BeautifulSoup):
    # Finds span element with provided stat text
    span = soup.find("span", string=stat)
    # Gets the parent element containing the divs for the stat values
    li_tag = span.find_parent('li')
    # Collects home and away values from their respective divs and removes potential whitespace
    home_val = float(li_tag.select_one("div.css-129ncdm-StatBox span span").text.strip())
    away_val = float(li_tag.select_one("div.css-1t9answ-StatBox span span").text.strip())

    return home_val, away_val

def scrape_head_2_head(driver: webdriver.Chrome):
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Head-to-Head')]"))
    )

    head_2_head_page_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Head-to-Head')]")
    head_2_head_page_button.click()

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Home')]"))
    )

    home_team_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Home')]")
    home_team_button.click()

    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    home_team_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Home')]")
    home_team_button.click()

    head_2_head_div = soup.select(".css-18yfvdy-WinsContainer")
    print(head_2_head_div)

    home_wins = int(head_2_head_div[0].select_one("[class*='NumberOfWins'] span").text.strip())
    draws = int(head_2_head_div[1].select_one("[class*='NumberOfWins'] span").text.strip())
    away_wins = int(head_2_head_div[2].select_one("[class*='NumberOfWins'] span").text.strip())

    print(home_wins)
    print(draws)
    print(away_wins)

    total_meetings = home_wins + draws + away_wins

    home_win_pct = round(home_wins / total_meetings, 3)
    draw_pct = round(draws / total_meetings, 3)
    away_win_pct = round(away_wins / total_meetings, 3)

    print(home_win_pct)
    print(draw_pct)
    print(away_win_pct)

    return home_win_pct, draw_pct, away_win_pct

def scrape_match_date_time(soup: BeautifulSoup):
    match_date_time_string = soup.find("h1", style_="position: absolute; left: -9999px;").text.strip().split("(")[1].split("T")
    match_date_string = match_date_time_string[0]
    match_time_string = match_date_time_string[1].split(".")[0]

    match_date = datetime.strptime(match_date_string, '%Y-%m-%d').date()
    match_time = datetime.strptime(match_time_string, '%H:%M:%S').time()

    return match_date, match_time

def scrape_matches(league: str, season: str, gameweek: int):
    match_links = find_matches(league, season, gameweek)

    for match in match_links:
        match_data = scrape_match(match)
        # HOW TO TRANSFORM/WORK WITH VALUES SCRAPED??????
    return
