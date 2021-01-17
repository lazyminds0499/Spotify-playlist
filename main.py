from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


date = input("Which Year u wanna travel to. (Date format: YYYY-MM-DD): ")
response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}")
site_data = response.text
soup = BeautifulSoup(site_data, "html.parser")
all_songs = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
all_artist = soup.find_all(name="span", class_="chart-element__information__artist text--truncate color--secondary")
songs = [song.text for song in all_songs]
artists = [artist.text for artist in all_artist]

client_id = "d16aa4647e5743eaa173f846b3cd5043"
client_secret = "4ac129d749014abfbced919094dd71ec"

scope = "playlist-modify-private"
data = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": "http://example.com",

}

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com/callback",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
headers = {
    "Authorization": "Bearer BQAaF3wQs0iU4QKq3x9EWecr-TTHPBNwWz6_79yeFyVtRE8eDG2EZ3Tn5lPBgLNMCObqaB1aBQowRiucKLzagNRdcxlcNk5U4e0mrEWBt4KdySawOXbjiF9zpLQSABLfIUlhrSQcn7s82EziRK-H1SpKXEG7HCkEySX88HsgAxElVhVfD1Wq9AaAhE9M0TapqW_1YxNXOC9MeQ",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

year = "2000"
uri_id = []
for index in range(len(songs)-1):
    try:
        result = sp.search(q=f"{songs[index]} year:{year}", type="track", limit=1, market="US")
        uri_id.append(result["tracks"]["items"][0]["uri"])
    except IndexError:
        pass

spotify_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
body = {
    "name": f"{date} Billboard 100",
    "description": "top songs",
    "public": False
}
adding_response = requests.post(url=spotify_url, json=body, headers=headers)
playlist_data = adding_response.json()
playlist_id = playlist_data["id"]

spotify_playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?"
playlist_header = {
    "Authorization": "Bearer BQAaF3wQs0iU4QKq3x9EWecr-TTHPBNwWz6_79yeFyVtRE8eDG2EZ3Tn5lPBgLNMCObqaB1aBQowRiucKLzagNRdcxlcNk5U4e0mrEWBt4KdySawOXbjiF9zpLQSABLfIUlhrSQcn7s82EziRK-H1SpKXEG7HCkEySX88HsgAxElVhVfD1Wq9AaAhE9M0TapqW_1YxNXOC9MeQ",
    "Content-Type": "application/json"
}
for uri in uri_id:
    params = {
        "uris": uri
    }
    playlist_response = requests.post(url=f"{spotify_playlist_url}uris={uri}",  headers=playlist_header)




