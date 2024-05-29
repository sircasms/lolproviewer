import requests
from bs4 import BeautifulSoup
url = 'https://liquipedia.net/leagueoflegends/S-Tier_Tournaments'
response = requests.get(url)

print(response.status_code)

class Tournament:
    def __init__(self, name):
        self.name = name
        self.teams = []
        self.matches = []

    def get_name(self):
        return self.name

class Team: 
    def __init__(self, name):
        self.name = name
        self.players = []

class Player:
    def __init__(self, name, role):
        self.name = name
        self.role = role


international_tournaments = []
regional_tournaments = []

tournament_wrapper = [international_tournaments, regional_tournaments]

# Check if the request was successful
if response.status_code == 200:
    html_content = response.content
    print("Successfully retrieved page.")
    soup = BeautifulSoup(html_content, 'html.parser')

    reg_t = soup.find_all('div', class_='divCell Tournament Header')
    int_t = soup.find_all('div', class_='divCell Tournament Header-Premier')

    for t in reg_t:
        regional_tournaments.append(Tournament(t.text.strip()))

    for t in int_t:
        international_tournaments.append(Tournament(t.text.strip()))
        
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

get_tournament = Tournament("err")

tournament = input("Pick a tournament: ")

for t in tournament_wrapper[0] + tournament_wrapper[1]:
    if t.get_name() == tournament:
        get_tournament = t

print(get_tournament.get_name())

# change test