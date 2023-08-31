import spotipy
from spotipy.oauth2 import SpotifyOAuth
import keyboard, os

USERNAME = '' # Enter your username
CLIENT_ID='' # Use spotify dev to get client ID, Client Secret, and URI
CLIENT_SECRET=''
REDIRECT_URI=''
SCOPE = 'playlist-modify-private, user-read-currently-playing, playlist-modify-public'

ID_PATH = 'playlistID.txt' # Set where the playlist ID is saved


token = spotipy.util.prompt_for_user_token(username = USERNAME, 
                                        scope = SCOPE, 
                                        client_id = CLIENT_ID,  
                                        client_secret = CLIENT_SECRET, 
                                        redirect_uri = REDIRECT_URI)
if token:
    sp = spotipy.Spotify(auth=token)

def readID():
    if os.path.exists(ID_PATH):
        with open(ID_PATH, 'r') as file:
            contents = file.read()
            print ("Loaded Playlist ID from File.")
            return contents
    else:
        ID = input("Please enter the target playlist ID: ")
        with open(ID_PATH, 'w') as file:
            file.write(ID)
            print("Playlist ID written to file")
        return ID

def addCurrentSongToPlaylist(ID):
    try:
        currURI = getCurrentSongURI()
        sp.playlist_add_items(ID, currURI, position=None)
        print(f"Song {currURI} successfully added.")
    except:
        print("Error: No Current Song Returned")

def getCurrentSongURI():
    currentSongDict = sp.current_user_playing_track()
    song = [currentSongDict['item']['uri']]
    return song

def main():
    playlistID = readID()

    # Hotkey Management
    def callback():
        addCurrentSongToPlaylist(playlistID)
    keyboard.add_hotkey('ctrl+alt+p', callback) # Add current song Hotkey
    keyboard.wait('ctrl+alt+esc') # Escape Script Hotkey

if __name__ == '__main__':
    main()