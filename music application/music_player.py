import os
import random
from flask import Flask, render_template, request

app = Flask(__name__)

audio_path = "music application/audio"

if not os.path.exists(audio_path):
    raise Exception(f"The directory '{audio_path}' does not exist")

# Get the list of music files in the directory
music_files = [filename for filename in os.listdir(audio_path) if filename.endswith('.mp3')]

# Check if there are any music files in the directory
if not music_files:
    raise Exception("There are no music files in the directory")

# Define the list of songs based on the music files
songs = [{'title': filename[:-4], 'artist': 'Unknown', 'file': filename} for filename in music_files]

# Define an empty playlist
playlist = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/playlists', methods=['GET', 'POST'])
def playlists():
    global playlist
    if request.method == 'POST':
        # Clear the playlist
        playlist = []
        return render_template('playlists.html', songs=songs, playlist=playlist)
    else:
        return render_template('playlists.html', songs=songs, playlist=playlist)

@app.route('/create_playlist', methods=['GET', 'POST'])
def create_playlist():
    global playlist
    if request.method == 'POST':
        # Get the selected songs from the form
        selected_songs = request.form.getlist('song')

        # Create a playlist from the selected songs
        playlist = [songs[int(index)] for index in selected_songs]

        return render_template('playlist.html', playlist=playlist)
    else:
        return render_template('create_playlist.html', songs=songs)

@app.route('/playlist', methods=['GET', 'POST'])
def play_playlist():
    global playlist
    if request.method == 'POST':
        # Shuffle the playlist
        random.shuffle(playlist)
        return render_template('playlist.html', playlist=playlist)
    else:
        return render_template('playlist.html', playlist=playlist)

@app.route('/repeat', methods=['GET', 'POST'])
def repeat_song():
    global playlist
    if request.method == 'POST':
        repeat_type = request.form['repeat']
        if repeat_type == 'current':
            # Repeat the current song
            current_song = playlist.pop(0)
            playlist.append(current_song)
        elif repeat_type == 'all':
            # Repeat the entire playlist
            playlist_copy = playlist.copy()
            playlist = []
            playlist.extend(playlist_copy)

        return render_template('playlist.html', playlist=playlist)
    else:
        return render_template('playlist.html', playlist=playlist)

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('q')
    if query:
        # Filter the songs based on the search query
        filtered_songs = [song for song in songs if query.lower() in song['title'].lower() or query.lower() in song['artist'].lower()]
        return render_template('search.html', songs=filtered_songs, query=query)
    else:
        return render_template('search.html', songs=songs, query='')

@app.route('/audio/<filename>')
def serve_audio(filename):
    # Serve the audio files from the static/audio directory
    return app.send_static_file(os.path.join('audio', filename))
