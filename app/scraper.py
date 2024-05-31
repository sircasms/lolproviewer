import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

ROLE_NAMES = ["TOP", "JGL", "MID", "ADC", "SUP"]
MAIN_URL = "https://liquipedia.net"

INTERNATIONAL = 0
REGIONAL = 1


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


class Scraper:
    def __init__(self):
        self.international_tournaments = []
        self.regional_tournaments = []
        self.tournament_wrapper = [self.international_tournaments, self.regional_tournaments]

    def fetch_page(self, url: str) -> BeautifulSoup:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.content
            print("Successfully retrieved page.")
            return BeautifulSoup(html_content, 'html.parser')
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return None

    def scrape_tournaments(self, url: str):
        soup = self.fetch_page(url)
        if not soup:
            return

        reg_t = soup.find_all('div', class_='divCell Tournament Header')
        int_t = soup.find_all('div', class_='divCell Tournament Header-Premier')

        for t in int_t:
            a = t.find_all('a')[-1]
            if a and 'href' in a.attrs:
                link = urljoin(MAIN_URL, a['href'])
                self.international_tournaments.append(Tournament(t.text.strip(), link))

        for t in reg_t:
            a = t.find_all('a')[-1]
            if a and 'href' in a.attrs:
                link = urljoin(MAIN_URL, a['href'])
                self.regional_tournaments.append(Tournament(t.text.strip(), link))

    def select_tournament(self, tournament_name: str) -> Tournament:
        for t in self.tournament_wrapper[INTERNATIONAL] + self.tournament_wrapper[REGIONAL]:
            if t.get_name() == tournament_name:
                return t
        return Tournament("err", "")

    def scrape_teams(self, tournament: Tournament) -> list[Team]:
        if tournament.get_link() == "":
            print("Tournament link does not exist.")
            return []

        soup = self.fetch_page(tournament.get_link())
        if not soup:
            return []

        team_containers = soup.find_all('div', class_='teamcard toggle-area toggle-area-1')
        teams = []
        for c in team_containers:
            a = c.find_all('a')[0]
            if a and 'href' in a.attrs:
                teams.append(Team(a.text, urljoin(MAIN_URL, a['href'])))
        return teams


if __name__ == "__main__":
    scraper = Scraper()
    
    scraper.scrape_tournaments('https://liquipedia.net/leagueoflegends/S-Tier_Tournaments')

    tournament_name = input("Pick a tournament: ")
    selected_tournament = scraper.select_tournament(tournament_name)

    print(selected_tournament)

    teams = scraper.scrape_teams(selected_tournament)
    for team in teams:
        print(team)