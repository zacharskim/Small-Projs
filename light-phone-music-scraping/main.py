
import requests
import urllib.parse
import os
import requests
from dotenv import load_dotenv
import webbrowser

load_dotenv()



#pip freeze > requirements.txt, for when you are done and want to generate a list of dependencies....


#i'd like to print out all the names of playlists and then the corresponding id for each playlist

#then i'd like to design the program to take in the name of the playlist you want to download, and then print 
# out the songs in that playlist and the corresponding artist for each song
# playlist may or may not be by the user....

#api calls i need to make:
#search api for list of playlists 
#grab the playlist i want
# grab the songs from that playlist and the artistis using some sort of loop etc 


def get_authorization_code():
    auth_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": os.environ.get("SPOTIFY_CLIENT_ID"),
        "response_type": "code",
        "redirect_uri": "http://localhost:8000/callback",  # For this example, we'll assume this redirect
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
        "redirect_uri": "http://localhost:8000/callback",
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

def get_playlists(token, user):
    url = "https://api.spotify.com/v1/me/playlists"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

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

            for playlist in playlists:
                print(playlist['name'])  # Print the name of each playlist
                all_playlists.append(playlist['name'])  # Add to the list

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


def main():
    user = input("Enter the name of the user whose playlist you want to download: ")
    token = auth()
    if token:
        playlists = get_playlists(token, user)
        # get_tracks(token)
        # search_arr = search(token, user)
        # download_playlist(search_arr)
    else:
        print("Error: Could not authenticate, please check your spotify client id and secret")
    
    


# # URL of the file to download
# url = "https://example.com/file.txt"

# # Path to the user's desktop
# desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# # Filename to save the downloaded file as
# filename = "downloaded_file.txt"

# # Full path to the downloaded file
# file_path = os.path.join(desktop_path, filename)

# # Download the file and save it to the user's desktop
# response = requests.get(url)
# with open(file_path, "wb") as f:
#     f.write(response.content)

# print(f"File saved to {file_path}")


if __name__ == "__main__":
    main()
    
    
# new idea for this proj: 
# app that shows you ur playlists and then you can choose which one to download
# also shows you songs in your liked songs  + discover weekly and you can pick and choose which ones to donwload....
# use radix + stiches for the ui etc...make the application performant too, so use caching etc i guess?? ask gpt how to ensure it's 
# quick etc...

