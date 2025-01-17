from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from auth_utils import save_token_to_file, read_token_from_file

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

# Initialize SpotifyOAuth
sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-library-read playlist-modify-public playlist-modify-private"  # Specify the scope you need
)

# Get the URL to authorize
auth_url = sp_oauth.get_authorize_url()
print(f"Please go to this URL to authorize: {auth_url}")

# After the user authorizes, they will be redirected to the redirect URI with a code in the URL.
# You need to capture this code.
response_url = input("Paste the redirect URL here: ")
code = sp_oauth.parse_response_code(response_url)

# Get the access token using the code
token_info = sp_oauth.get_access_token(code)


refresh_token = token_info['refresh_token']
access_token = token_info['access_token']
new_token_info = sp_oauth.refresh_access_token(refresh_token)
# new_access_token = new_token_info['access_token']

print(f"Refresh Token: {refresh_token}")
print(f"Access Token: {token_info['access_token']}")

# Save tokens to files
save_token_to_file(access_token, 'access.json')
save_token_to_file(refresh_token, 'refresh.json')

# Check if token is expired and refresh if necessary
if sp_oauth.is_token_expired(token_info):
    token_info = sp_oauth.refresh_access_token(refresh_token)
    save_token_to_file(token_info['access_token'], 'access.json')
    save_token_to_file(token_info['refresh_token'], 'refresh.json')

answer= input("What year wdo you want to travel to? Type the year in this format; YYYY-MM-DD")
URL = f'https://www.billboard.com/charts/hot-100/{answer}'
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
response = requests.get(URL, headers=header)
# print(response.text)

soup = BeautifulSoup(response.text, 'html.parser')
print(soup.title)



# Assuming the desired h3 tags are inside a specific div or section
specific_h3_tags = soup.select('li.o-chart-results-list__item h3.c-title')

# Extract and clean the text
specific_h3_texts = [tag.get_text(strip=True) for tag in specific_h3_tags]
print(specific_h3_texts)

# Reading tokens when needed
access_token = read_token_from_file('access.json')
refresh_token = read_token_from_file('refresh.json')

# Spotify Authentication
sp = spotipy.Spotify(auth=access_token)

# Create Playlist
user_id = sp.current_user()['id']
playlist = sp.user_playlist_create(user=user_id, name=f"Billboard Hot 100 from {answer}", public=False)

# Search and Add Tracks
track_uris = []
for song in specific_h3_texts:
    result = sp.search(q=song, limit=1, type='track')
    if result['tracks']['items']:
        track_uris.append(result['tracks']['items'][0]['uri'])

sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist['id'], tracks=track_uris)
print(f"Playlist '{playlist['name']}' created successfully with {len(track_uris)} tracks.")