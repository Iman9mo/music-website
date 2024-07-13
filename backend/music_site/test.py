import requests

# Endpoint to retrieve the user profile
url = "http://127.0.0.1:8000/api/profile/"

headers = {
    "Authorization": "Token a38484f8f90e166fbc31b17041ead396d9903b59",
} 

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Failed to retrieve profile: {response.status_code}")


url = "http://127.0.0.1:8000/api/songs/category/1/"  # Change 1 to the desired category ID
 

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Failed to retrieve songs by category: {response.status_code}")



url = "http://127.0.0.1:8000/api/songs/artist/1/"  # Change 1 to the desired artist ID
 

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Failed to retrieve songs by artist: {response.status_code}")



url = "http://127.0.0.1:8000/api/songs/user/1/"  # Change 1 to the desired user ID
 

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Failed to retrieve songs by user: {response.status_code}")



url = "http://127.0.0.1:8000/api/songs/hottest/"
 

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Failed to retrieve hottest songs: {response.status_code}")



url = "http://127.0.0.1:8000/api/songs/unapproved/"
 

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Failed to retrieve unapproved songs: {response.status_code}")



url = "http://127.0.0.1:8000/api/comments/unapproved/"
 

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Failed to retrieve unapproved comments: {response.status_code}")


url = "http://127.0.0.1:8000/api/users/profile/likes-views/"
 

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Failed to retrieve total likes and views: {response.status_code}")


url = "http://127.0.0.1:8000/api/songs/"
 
files = {
    "file": ("song.mp3", open("songs/file3.mp3", "rb"), "audio/mpeg"),
    "cover_image": ("cover.jpg", open("songs/1.jpg", "rb"), "image/jpeg"),
}
data = {
    "title": "Test Song",
    "artist": 1,  # Change to the desired artist ID
    "category": 1,  # Change to the desired category ID
    "user": 1,  # Change to the desired user ID
    "likes": 0,
    "views": 0,
    "approved": False,
}

response = requests.post(url, headers=headers, files=files, data=data)

if response.status_code == 201:
    print(response.json())
else:
    print(f"Failed to create song: {response.status_code}")


url = "http://127.0.0.1:8000/api/comments/"
 
data = {
    "user": 1,  # Change to the desired user ID
    "song": 1,  # Change to the desired song ID
    "content": "Great song!",
    "approved": False,
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 201:
    print(response.json())
else:
    print(f"Failed to create comment: {response.status_code}")




url = "http://127.0.0.1:8000/api/songs/by-period/"

params = {
    "start_date": "2023-01-01",
    "end_date": "2024-12-31"
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Failed to retrieve songs by period: {response.status_code}")