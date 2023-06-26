
import requests
import urllib.parse
import os
import requests
from dotenv import load_dotenv

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


def auth():
    url_for_token = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "client_credentials",
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

def main():
    user = input("Enter the name of the user whose playlist you want to download: ")
    token = auth()
    if token:
        search_arr = search(token, user)
        download_playlist(search_arr)
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