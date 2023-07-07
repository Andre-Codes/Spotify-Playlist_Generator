# Spotify-Playlist_Generator
Generates a playlist of tracks based on user input passed to OpenAI API to match the input with related tracks

User prompted input is passed to ChatGPT

The prompt is formatted for ChatGPT to understand. The user input is passed along with instructions on how to process it.

A successful prompt will include details about mood, setting, theme, style, genre, etc.

  Exmaple: I'm relaxing at home with my cat, trying to unwind. Not really in the mood for classical, but I do love instrumentals.

ChatGPT will generate X number of tracks by analyzing factors in user input and matching with tracks containing related attributes.

Tracks are processed by Spotify API and a playlist is generated, along with a ChatGPT generated description and playlist title related to the chosen tracks (see attached screenshot)
