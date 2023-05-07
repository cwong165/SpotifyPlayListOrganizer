import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from langdetect import detect
import lyricsgenius

# Set your Spotify API credentials
os.environ["SPOTIPY_CLIENT_ID"] = "your_client_id"
os.environ["SPOTIPY_CLIENT_SECRET"] = "your_client_secret"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8888/callback"

# Set your Genius API access token
genius_access_token = "your_genius_access_token"

# Define the scope required for the tasks
scope = "playlist-modify-public playlist-modify-private"

# Authenticate with the Spotify and Genius APIs
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
genius = lyricsgenius.Genius(genius_access_token)


def get_playlist_tracks(playlist_id):
	results = sp.playlist_tracks(playlist_id)
	tracks = results['items']
	while results['next']:
		results = sp.next(results)
		tracks.extend(results['items'])
	return tracks


def detect_language_from_lyrics(track_name, artist_name):
	try:
		song = genius.search_song(track_name, artist_name)
		if song and song.lyrics:
			return detect(song.lyrics)
	except Exception as e:
		print(f"Error detecting language from lyrics: {e}")
	return None


def organize_playlist_by_language(playlist_id):
	tracks = get_playlist_tracks(playlist_id)
	organized_tracks = {'en': [], 'zh': [], 'ja': [], 'ko': [], 'undetected': []}

	for track in tracks:
		track_id = track['track']['id']
		track_name = track['track']['name']
		artist_name = track['track']['artists'][0]['name']

		# Try to detect language from lyrics
		language = detect_language_from_lyrics(track_name, artist_name)

		# If lyrics-based detection fails, try to detect language from track name
		if language is None:
			try:
				language = detect(track_name)
			except:
				print(f"Could not detect language for track: {track_name}")
				language = 'undetected'

		if language in organized_tracks:
			organized_tracks[language].append(track_id)

	for language, track_ids in organized_tracks.items():
		if not track_ids:
			continue

		# Create a new playlist for each language or undetected language tracks
		if language == 'undetected':
			playlist_name = "Organized by Language (Undetected)"
		else:
			playlist_name = f"Organized by Language ({language.upper()})"

		new_playlist = sp.user_playlist_create(sp.me()['id'], playlist_name)
		new_playlist_id = new_playlist['id']

		# Add the tracks to the new playlist
		sp.playlist_add_items(new_playlist_id, track_ids)


if __name__ == "__main__":
	# Replace with the ID of the playlist you want to organize
	playlist_id = "your_playlist_id"
	organize_playlist_by_language(playlist_id)
