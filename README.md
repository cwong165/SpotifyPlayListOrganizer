# Spotify Playlist Organizer by Language

This Python script organizes a Spotify playlist based on the language of the songs. It supports English, Chinese, Japanese, Korean, and undetected languages. The script uses the Spotify Web API to interact with playlists and the Genius API to fetch song lyrics for better language detection.

## Requirements

- Python 3.6 or later
- Spotify API credentials (Client ID, Client Secret, and Redirect URI)
- Genius API access token
- A Spotify playlist ID you want to organize

## Installation

1. Clone the repository or download the script file.

2. Install the required packages:

```bash
pip install spotipy lyricsgenius langdetect
```

3. Set your Spotify API credentials and Genius API access token in the script:

```python
os.environ["SPOTIPY_CLIENT_ID"] = "your_client_id"
os.environ["SPOTIPY_CLIENT_SECRET"] = "your_client_secret"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8888/callback"

genius_access_token = "your_genius_access_token"
```

4. Replace `"your_playlist_id"` with the ID of the playlist you want to organize:

```python
if __name__ == "__main__":
    playlist_id = "your_playlist_id"
    organize_playlist_by_language(playlist_id)
```

## Usage

1. Run the script:

```bash
python playlist_organizer_by_language.py
```

2. The script will create new playlists for each detected language (English, Chinese, Japanese, and Korean) and a separate playlist for undetected language tracks. The new playlists will be added to your Spotify account.

## Limitations

- Language detection accuracy depends on the quality of the track names and lyrics.
- The Genius API may not always find the correct lyrics for every song.
- The script requires write access to your Spotify account to create and modify playlists.
