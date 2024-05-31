from flask import Flask, request, render_template
from scraper import Scraper

app = Flask(__name__)
scraper = Scraper()

@app.route('/')
def index():
    scraper.scrape_tournaments('https://liquipedia.net/leagueoflegends/S-Tier_Tournaments')

    international_tournaments = scraper.international_tournaments
    regional_tournaments = scraper.regional_tournaments

    if not international_tournaments and not regional_tournaments:
        return "Failed to retrieve tournaments"

    return render_template('index.html', international_tournaments=international_tournaments, regional_tournaments=regional_tournaments)

@app.route('/tournament', methods=['POST'])
def tournament():
    tournament_name = request.form.get('tournament')
    selected_tournament = scraper.select_tournament(tournament_name)

    if selected_tournament.get_name() == "err":
        return render_template('error.html', message="Tournament not found")

    teams = scraper.scrape_teams(selected_tournament)
    if teams is None:
        return render_template('error.html', message="Failed to retrieve tournament page")

    return render_template('tournament.html', tournament=selected_tournament, teams=teams)

if __name__ == '__main__':
    app.run(debug=True)
