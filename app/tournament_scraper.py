import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

ROLE_NAMES = ["TOP", "JGL", "MID", "ADC", "SUP"]
MAIN_URL = "https://liquipedia.net"

INTERNATIONAL = 0
REGIONAL = 1

international_tournaments = []
regional_tournaments = []

tournament_wrapper = [international_tournaments, regional_tournaments]


class Player:
    # roles are ints 0-4 for easy sorting later

    def __init__(self, name: str, role: int) -> None:
        self.name = name
        self.role = role

    def get_name(self) -> str:
        return self.name
        
    def get_role(self) -> int:
        return self.role

    def get_role_name(self) -> str:
        return ROLE_NAMES[self.role]


class Team: 
    def __init__(self, name: str, link: str) -> None:
        self.name = name
        self.link = link
        self.players = []

    def __str__(self) -> str:
        return f"{self.name}\n{self.link}\n"

    def get_name(self) -> str:
        return self.name
    
    def get_link(self) -> str:
        return self.link
    
    def get_players(self) -> list[Player]:
        return self.players

    def get_player(self, role: int) -> Player:
        return self.players[role]


class Tournament:
    def __init__(self, name: str, link: str) -> None:
        self.name = name
        self.teams = []
        self.matches = []
        self.link = link

    def __str__(self) -> str:
        return f"\nTournament Name: {self.name}\nLink: {self.link}\n"

    def get_name(self) -> str:
        return self.name
    
    def get_teams(self) -> list[Team]:
        return self.teams
    
    def get_matches(self) -> list: # should make a match class later
        return self.matches
    
    def get_link(self) -> str:
        return self.link


url = 'https://liquipedia.net/leagueoflegends/S-Tier_Tournaments'
response = requests.get(url)


# Check if the request was successful
if response.status_code == 200:
    html_content = response.content
    print("Successfully retrieved page.")
        
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
    exit

soup = BeautifulSoup(html_content, 'html.parser')

reg_t = soup.find_all('div', class_='divCell Tournament Header')
int_t = soup.find_all('div', class_='divCell Tournament Header-Premier')

for t in int_t:
    a = t.find_all('a')[-1]
    if a and 'href' in a.attrs:
        link = urljoin(MAIN_URL, a['href'])
    
    international_tournaments.append(Tournament(t.text.strip(), link))

for t in reg_t:
    a = t.find_all('a')[-1]
    if a and 'href' in a.attrs:
        link = urljoin(MAIN_URL, a['href'])
    
    regional_tournaments.append(Tournament(t.text.strip(), link))


tournament_list = tournament_wrapper[INTERNATIONAL] + tournament_wrapper[REGIONAL]

get_tournament = Tournament("err", "")

tournament = input("Pick a tournament: ")

for t in tournament_wrapper[0] + tournament_wrapper[1]:
    if t.get_name() == tournament:
        get_tournament = t

print(get_tournament)


# SEARCH FOR TEAMS WITHIN TOURNAMENT

TEAMS = []

if get_tournament.get_link() == "":
    print("Tournament link does not exist.")
    exit

response = requests.get(get_tournament.get_link())

# Check if the request was successful
if response.status_code == 200:
    html_content = response.content

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
    exit

soup = BeautifulSoup(html_content, 'html.parser')

team_containers = soup.find_all('div', class_='teamcard toggle-area toggle-area-1')

for c in team_containers:
    a = c.find_all('a')[0]
    if a and 'href' in a.attrs:
        TEAMS.append(Team(a.text, urljoin(MAIN_URL, a['href'])))

for team in TEAMS:
    print(team)