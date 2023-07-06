import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json
import openai


class SpotifyService:
    def __init__(self, title):
        client_id = os.environ['SPOTIPY_CLIENT_ID']
        client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
        redirect_uri = os.environ['SPOTIPY_REDIRECT_URI']
        self.user_id = 'SPOTIFY_USERID'

        # Set up authentication
        scope = 'user-read-private user-read-email playlist-modify-private'  # scope for required permissions

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                            client_secret=client_secret,
                                                            redirect_uri=redirect_uri,
                                                            scope=scope))

        self.playlist_id = None  # Initialize playlist_id

    def search_song(self, song, artist):
        query = 'artist: ' + artist + ' ' + song
        results = self.sp.search(q=query, limit=1, type='track')

        if len(results['tracks']['items']) == 0:
            return None

        track_id = results['tracks']['items'][0]['id']
        return 'spotify:track:' + track_id

    def generate_playlist(self, title, description, user_mood):
        # Generate a unique playlist name
        playlist_description = description
        playlist = self.sp.user_playlist_create(self.user_id, title, public=False,
                                                description=playlist_description + " (prompt: " + "'" + user_mood + "')")
        self.playlist_id = playlist['id']
        print('Generated Playlist:' + 'https://open.spotify.com/playlist/' + self.playlist_id)

    def add_to_playlist(self, uris):
        self.sp.playlist_add_items(self.playlist_id, uris)


class GPTService:
    def __init__(self):
        openai.api_key = os.environ['OPENAI_API_KEY']

    def generate_songs(self, user_mood):
        model = "gpt-3.5-turbo"
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant who recommends music."},
                {"role": "user",
                 "content": "List 10 songs based on the following mood, "
                            "scenario, setting, or idea: " + user_mood +
                            ". You should respond in a valid JSON response with "
                            "a field called title that summarizes the theme of the playlist, "
                            "a field called description that provides a short summary "
                            "description of the mood/theme of the playlist and why these songs were chosen, "
                            "lastly, a field called songs. The 'songs' field should contain an array "
                            "that contains each of the individual songs. For each song, include "
                            "a field called song and a field called artist, both with the appropriate values."},
            ],
            temperature=0, # adjust between 0-1, the higher the temp, the more abstract and random the predictions become
        )

        # Get the generated text
        generated_text = response['choices'][0]['message']['content']
        print(generated_text)
        data = json.loads(generated_text)
        print(data)
        return data['title'], data['description'], data['songs']


if __name__ == '__main__':
    user_mood = input("Enter the type of mood you are in: ")

    gpt_service = GPTService()
    title, description, songs = gpt_service.generate_songs(user_mood)

    # Spotify logic
    spotify_service = SpotifyService(title)  # Create an empty playlist with generated title
    uris = [spotify_service.search_song(song['song'], song['artist']) for song in
            songs]  # get generated song URIs from GPT response
    spotify_service.generate_playlist(title, description, user_mood)
    spotify_service.add_to_playlist(uris)  # Add all songs to playlist based on their URIs
