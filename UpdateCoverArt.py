import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import openai

class SpotifyService:
    def __init__(self):
        client_id = os.environ['SPOTIPY_CLIENT_ID']
        client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
        redirect_uri = os.environ['SPOTIPY_REDIRECT_URI']
        self.user_id = 'amardian22'

        # Set up authentication
        scope = 'user-read-private user-read-email playlist-modify-private playlist-modify-public ugc-image-upload'  # scope for required permissions

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                            client_secret=client_secret,
                                                            redirect_uri=redirect_uri,
                                                            scope=scope))

        self.playlist_id = None  # Initialize playlist_id

    def set_cover_mage(self, playlist_id, cover_image):
        self.sp.playlist_upload_cover_image(playlist_id, cover_image)

class GPTService:
    def __init__(self):
        openai.api_key = os.environ['OPENAI_API_KEY']

    def generate_image(self, image_prompt):
        response = openai.Image.create(
            prompt=image_prompt,
            n=1,
            size="256x256",
            response_format="b64_json",
        )
        image_data = response['data'][0]['b64_json']
        print(image_data)
        return image_data

image_prompt = "Steaming cup of coffee on top of an abstract globe"

gpt_service = GPTService()
spotify_service = SpotifyService()

cover_art = gpt_service.generate_image(image_prompt)

playlistID = '6ZzDmAbdhZwDwGCVbDbUj1'

print(cover_art)

# spotify_service.set_cover_mage(playlistID, cover_art)