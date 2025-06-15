from youtube_transcript_api import YouTubeTranscriptApi
import os
import tqdm


def save_youtube_transcript(video_id: str):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])

        cleaned_entries = [
            entry["text"].strip() for entry in transcript
            if entry["text"].strip().lower() not in ["[music]"]
        ]

        full_text = " ".join(cleaned_entries)
        filename = os.path.join("Transcripts/", f"{video_id}.txt")

        with open(filename, "w", encoding="utf-8") as f:
            f.write(full_text)

        return filename

    except Exception as e:
        print(f"Error: {e}")
        return None


with open("video_ids.txt", "r", encoding="utf-8") as f:
    video_ids = [line.strip() for line in f if line.strip()]

for video_id in tqdm.tqdm(video_ids):
    save_youtube_transcript(video_id)
