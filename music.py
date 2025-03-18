import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Authentication - Replace with your Spotify credentials
client_id = 'f5184f59eb6042428f873e12643b07f1'
client_secret = '907d5d15e3294169b51f90334ce10dc1'
redirect_uri = 'https://google.com/callback'

scope = "user-library-modify user-library-read playlist-modify-public playlist-modify-private user-modify-playback-state user-read-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

def play():
    """Plays the current track."""
    sp.start_playback()

def pause():
    """Pauses the currently playing track."""
    sp.pause_playback()

def next_track():
    """Skips to the next track."""
    sp.next_track()

def previous_track():
    """Goes to the previous track."""
    sp.previous_track()

def play_song(song_name):
    """Searches for and plays a specific song by name."""
    result = sp.search(q=song_name, type='track', limit=1)
    if result['tracks']['items']:
        song_uri = result['tracks']['items'][0]['uri']
        sp.start_playback(uris=[song_uri])
        song_info = result['tracks']['items'][0]
        print(f"Playing '{song_info['name']}' by {', '.join([artist['name'] for artist in song_info['artists']])}")
    else:
        print(f"Song '{song_name}' not found")

def set_volume(volume_level):
    """Sets the volume to a specific level (0-100)."""
    sp.volume(volume_level)

def get_current_song():
    """Gets details of the currently playing song."""
    current = sp.current_playback()
    if current and current['is_playing']:
        track = current['item']
        return f"Currently playing: {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}"
    else:
        return "No song is currently playing."

def add_to_favorites(song_name=None):
    """Adds a song to your Liked Songs."""
    if song_name:
        result = sp.search(q=song_name, type='track', limit=1)
        if result['tracks']['items']:
            song_uri = result['tracks']['items'][0]['uri']
            sp.current_user_saved_tracks_add([song_uri])
            print(f"Added '{song_name}' to Liked Songs")
        else:
            print(f"Song '{song_name}' not found")
    else:
        current = sp.current_playback()
        if current and current['is_playing']:
            track_uri = current['item']['uri']
            sp.current_user_saved_tracks_add([track_uri])
            print(f"Added '{current['item']['name']}' to Liked Songs")

def add_to_playlist(playlist_name, song_name=None):
    """Adds a song to a playlist by its name, or adds the currently playing song."""
    playlists = sp.current_user_playlists(limit=50)
    playlist_id = None

    for playlist in playlists['items']:
        if playlist['name'].lower() == playlist_name.lower():
            playlist_id = playlist['id']
            break
    
    if playlist_id:
        if song_name:
            result = sp.search(q=song_name, type='track', limit=1)
            if result['tracks']['items']:
                song_uri = result['tracks']['items'][0]['uri']
                sp.playlist_add_items(playlist_id, [song_uri])
                print(f"Added '{song_name}' to '{playlist_name}' playlist")
            else:
                print(f"Song '{song_name}' not found")

            current = sp.current_playback()
            if current and current['is_playing']:
                track_uri = current['item']['uri']
                sp.playlist_add_items(playlist_id, [track_uri])
                print(f"Added '{current['item']['name']}' to '{playlist_name}' playlist")
            else:
                print("No song is currently playing")
    else:
        print(f"Playlist '{playlist_name}' not found")

def list_playlists():
    """Lists all the user's playlists."""
    playlists = sp.current_user_playlists(limit=50)
    return [playlist['name'] for playlist in playlists['items']]

# play_song('Shape of You')
# play()
# pause()
# next_track()
# previous_track()
# set_volume(50)
# get_current_song()
# add_to_favorites()
# add_to_playlist('My Playlist', 'Blinding Lights')
# list_playlists()
