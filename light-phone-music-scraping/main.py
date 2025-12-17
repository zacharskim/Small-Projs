import requests
import urllib.parse
import os
import requests
from dotenv import load_dotenv
import webbrowser
import yt_dlp
import re

load_dotenv()


def get_authorization_code():
    auth_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": os.environ.get("SPOTIFY_CLIENT_ID"),
        "response_type": "code",
        "redirect_uri": "http://127.0.0.1:8000/callback",  # For this example, we'll assume this redirect
        "scope": "playlist-read-private user-library-read"
    }

    # Open the URL in the default browser to let the user authorize the app
    webbrowser.open(requests.Request('GET', auth_url, params=params).prepare().url)
    
    # Prompt the user to paste the redirected URL
    redirected_url = input("Please copy and paste the redirected URL here: ")
    
    # Extract the authorization code from the URL
    code = redirected_url.split("?code=")[1].split("&")[0]

    return code
    

def auth():
    code = get_authorization_code()  # This will be the authorization code after user's consent
    
    
    url_for_token = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:8000/callback",
        "client_id": os.environ.get("SPOTIFY_CLIENT_ID"),
        "client_secret": os.environ.get("SPOTIFY_CLIENT_SECRET")
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url_for_token, data=data, headers=headers)

    if response.status_code == 200:
        access_token = response.json()["access_token"]
        return access_token
    else:
        print("Error:", response.text)
        return





# def auth():
#     url_for_token = "https://accounts.spotify.com/api/token"
#     data = {
#         "grant_type": "client_credentials",
#         "client_id": os.environ.get("SPOTIFY_CLIENT_ID"),
#         "client_secret": os.environ.get("SPOTIFY_CLIENT_SECRET")
#     }
#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded"
#     }

#     response = requests.post(url_for_token, data=data, headers=headers)

#     if response.status_code == 200:
#         access_token = response.json()["access_token"]
#         return access_token
#     else:
#         print("Error:", response.text)
#         return
    

def search(token, user):
    url = f"https://api.spotify.com/v1/users/{user}/playlists"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    
    if response.status_code == 200:
        playlist_data = response.json()
        index = 1
        for playlist in playlist_data["items"]:
            playlist_name = playlist["name"]
            print(str(index) + ':', playlist_name)
            index += 1
        index_res = input("Choose a playlist to download by selecting an index number: ")
        if index_res.isdigit():
            playlist_id = playlist_data["items"][int(index_res) - 1]["id"]
            print(playlist_id, "is the id of the playlist you chose")
            url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                playlist_tracks = response.json()
                for track in playlist_tracks["items"]:
                    print(track["track"]["name"], "by", track["track"]["artists"][0]["name"])

def download_playlist(search_arr):
    #will complete later
    pass

def get_playlists(token):
    url = "https://api.spotify.com/v1/me/playlists"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    all_playlists = []  # List to store all playlists

    # Start with an offset of 0, and keep incrementing until all playlists are fetched
    offset = 0
    limit = 50  # Maximum allowed by Spotify
    
    while True:  # Keep looping until all playlists are fetched
        params = {
            'limit': limit,
            'offset': offset
        }
        
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            playlists = response.json()['items']
            if not playlists:  # If no more playlists are returned, break out of the loop
                break

            for i, playlist in enumerate(playlists, start=len(all_playlists) + 1):
                print(f"{i}: {playlist['name']}")  # Print numbered list
                all_playlists.append({'name': playlist['name'], 'id': playlist['id']})

            offset += limit  # Increment the offset by limit for the next batch
        else:
            print("Error fetching playlists:", response.text)
            break

    return all_playlists 

def get_tracks(access_token):
    url = "https://api.spotify.com/v1/me/tracks"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    all_tracks = []  # List to store all tracks

    # Start with an offset of 0, and keep incrementing until all tracks are fetched
    offset = 0
    limit = 50  # Maximum allowed by Spotify

    while True:  # Keep looping until all tracks are fetched
        params = {
            'limit': limit,
            'offset': offset
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            tracks = response.json()['items']
            if not tracks:  # If no more tracks are returned, break out of the loop
                break

            for track in tracks:
                print(track['track']['name'])  # Print the name of each track
                all_tracks.append(track['track']['name'])  # Add to the list

            offset += limit  # Increment the offset by limit for the next batch
        else:
            print("Error fetching tracks:", response.text)
            break

    return all_tracks  # Return the list of all track names

def get_playlist_tracks(access_token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    all_tracks = []  # List to store all tracks

    # Start with an offset of 0, and keep incrementing until all tracks are fetched
    offset = 0
    limit = 50  # Maximum allowed by Spotify

    while True:  # Keep looping until all tracks are fetched
        params = {
            'limit': limit,
            'offset': offset
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            tracks = response.json()['items']
            if not tracks:  # If no more tracks are returned, break out of the loop
                break

            for track_item in tracks:
                if track_item['track']:  # Make sure track exists (some might be null)
                    track = track_item['track']
                    track_name = track['name']
                    artist_name = track['artists'][0]['name'] if track['artists'] else 'Unknown Artist'
                    print(f"{track_name} by {artist_name}")
                    all_tracks.append({'name': track_name, 'artist': artist_name})

            offset += limit  # Increment the offset by limit for the next batch
        else:
            print("Error fetching playlist tracks:", response.text)
            break

    return all_tracks  # Return the list of all tracks

def sanitize_filename(filename):
    """Remove or replace characters that aren't valid in filenames"""
    # Replace problematic characters with safe alternatives
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove any trailing periods or spaces
    filename = filename.strip('. ')
    return filename

def download_song_from_youtube(track_name, artist_name, download_folder="downloads"):
    """Download a song from YouTube as MP3"""
    # Create download folder if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    # Create search query
    search_query = f"{track_name} {artist_name}"
    
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_folder, sanitize_filename(f'{track_name} - {artist_name}') + '.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,  # Suppress most output
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Search for the song and download the first result
            info = ydl.extract_info(f"ytsearch1:{search_query}", download=True)
            if info and 'entries' in info and len(info['entries']) > 0:
                print(f"✓ Downloaded: {track_name} by {artist_name}")
                return True
            else:
                print(f"✗ Could not find: {track_name} by {artist_name}")
                return False
    except Exception as e:
        print(f"✗ Error downloading {track_name} by {artist_name}: {str(e)}")
        return False

def download_playlist_tracks(tracks, playlist_name):
    """Download all tracks from a playlist"""
    print(f"\n🎵 Starting download of {len(tracks)} songs from '{playlist_name}'...")
    
    # Create a folder for this specific playlist
    playlist_folder = os.path.join("downloads", sanitize_filename(playlist_name))
    
    successful_downloads = 0
    failed_downloads = 0
    
    for i, track in enumerate(tracks, 1):
        print(f"\n[{i}/{len(tracks)}] Searching for: {track['name']} by {track['artist']}")
        
        if download_song_from_youtube(track['name'], track['artist'], playlist_folder):
            successful_downloads += 1
        else:
            failed_downloads += 1
    
    print(f"\n🎉 Download complete!")
    print(f"✓ Successfully downloaded: {successful_downloads} songs")
    print(f"✗ Failed to download: {failed_downloads} songs")
    print(f"📁 Files saved in: {playlist_folder}")

def main():
    token = auth()
    if token:
        print("\nFetching your playlists...")
        playlists = get_playlists(token)
        
        if playlists:
            print("\nChoose a playlist to view its songs:")
            while True:
                try:
                    choice = int(input("Enter the number of the playlist you want to view: ")) - 1
                    if 0 <= choice < len(playlists):
                        selected_playlist = playlists[choice]
                        print(f"\nFetching songs from '{selected_playlist['name']}'...")
                        tracks = get_playlist_tracks(token, selected_playlist['id'])
                        
                        # Ask user if they want to download the playlist
                        download_choice = input("Do you want to download this playlist as MP3? (y/n): ")
                        if download_choice.lower() == 'y':
                            download_playlist_tracks(tracks, selected_playlist['name'])
                        break
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
        else:
            print("No playlists found.")
    else:
        print("Error: Could not authenticate, please check your spotify client id and secret")
    

if __name__ == "__main__":
    main()


