import requests
import json


url = "https://www.sofascore.com/api/v1/sport/football/events/live"

payload = ""
headers = {
    "^accept": "*/*^",
    "^accept-language": "en-US,en;q=0.9^",
    "^baggage": "sentry-environment=production,sentry-release=-tQxTjjp91ro8B4mricn2,sentry-public_key=d693747a6bb242d9bb9cf7069fb57988,sentry-trace_id=bb1ee390b51b4917974cb9159c35cd77^",
    "^cache-control": "max-age=0^",
    "^cookie": "_lr_retry_request=true; _lr_env_src_ats=false; _ga=GA1.1.1640475335.1735131380; _ga_HNQ9P9MGZR=GS1.1.1735131379.1.0.1735131384.55.0.0^",
    "^if-none-match": "W/^\^e8e98400f1^^^",
    "^priority": "u=1, i^",
    "^referer": "https://www.sofascore.com/^",
    "^sec-ch-ua": "^\^Google",
    "^sec-ch-ua-mobile": "?0^",
    "^sec-ch-ua-platform": "^\^Windows^^^",
    "^sec-fetch-dest": "empty^",
    "^sec-fetch-mode": "cors^",
    "^sec-fetch-site": "same-origin^",
    "^sentry-trace": "bb1ee390b51b4917974cb9159c35cd77-94262895385e73b0^",
    "^user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36^",
    "^x-requested-with": "b298d6^"
}

response = requests.request("GET", url, data=payload, headers=headers)
data = json.loads(response.text)

with open('scores.json', "w") as f:
    json.dump(data, f, indent=4)

with open('scores.json', 'r') as f:
    data = json.load(f)

print(len(data["events"]))

for el in data['events']:
    tournament = el["tournament"]["name"]
    home_team = el["homeTeam"]["name"]
    away_team = el["awayTeam"]["name"]
    home_score = el["homeScore"]["current"]
    away_score = el["awayScore"]["current"]

    print("*"*30)
    print(tournament)
    print(f"{home_team} {home_score}:{away_score} {away_team}")

