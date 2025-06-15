from googleapiclient.discovery import build
import os

api_key = os.environ["YOUTUBE_API_KEY"]
channel_id = "" # Add YouTube channel id here
#Get from https://commentpicker.com/youtube-channel-id.php

youtube = build("youtube", "v3", developerKey=api_key)

# Convert channel ID → uploads playlist ID
uploads_playlist_id = "UU" + channel_id[2:]

# Get video IDs from the playlist
def get_all_video_ids_from_uploads(playlist_id):
    video_ids = []
    next_page_token = None

    while True:
        res = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in res["items"]:
            video_ids.append(item["contentDetails"]["videoId"])

        next_page_token = res.get("nextPageToken")
        if not next_page_token:
            break

    return video_ids


video_ids = get_all_video_ids_from_uploads(uploads_playlist_id)

# Save as txt
with open("video_ids.txt", "w", encoding="utf-8") as f:
    for vid in video_ids:
        f.write(f"{vid}\n")

print(f"Saved {len(video_ids)} video IDs.")
