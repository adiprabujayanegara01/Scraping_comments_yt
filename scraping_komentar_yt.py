from youtube_comment_downloader import YoutubeCommentDownloader
import csv

# Input video URL
video_url = "https://youtu.be/LjNGYXuLA1I?si=Js-tqXg-Hz65EwHA"

downloader = YoutubeCommentDownloader()
comments = downloader.get_comments_from_url(video_url, sort_by=0)  # 0 = top, 1 = newest

all_comments = []

for comment in comments:
    username = comment.get("author", "Unknown")
    text = comment.get("text", "")
    time = comment.get("time", "Unknown")  # biasanya format "2 days ago"
    
    all_comments.append({
        "username": username,
        "comment": text,
        "time": time
    })

# Simpan ke CSV
with open("youtube_comments_all.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["username", "comment", "time"])
    writer.writeheader()
    for c in all_comments:
        writer.writerow(c)

print(f"Berhasil menyimpan {len(all_comments)} komentar ke youtube_comments_all.csv")
