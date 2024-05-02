import yt_dlp

# Youtube video URL
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Replace with your desired video

# Options for youtube-dlp (get best audio format)
ydl_opts = {"format": "bestaudio"}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
  # Get information about the video
  info = ydl.extract_info(url, download=False)

  # Extract the audio URL
  audio_url = info["url"]

  # Option 1: Print the audio URL for further processing
  print(f"Audio Stream URL: {audio_url}")