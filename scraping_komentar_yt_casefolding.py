# Case Folding
from youtube_comment_downloader import YoutubeCommentDownloader
import csv

# --- Input URL Video YouTube ---
video_url = "https://youtu.be/LjNGYXuLA1I?si=Js-tqXg-Hz65EwHA"

# --- Inisialisasi Downloader ---
downloader = YoutubeCommentDownloader()
comments = downloader.get_comments_from_url(video_url, sort_by=0)  # 0 = top, 1 = newest

# --- List untuk menyimpan semua komentar ---
all_comments = []

print("⏳ Sedang mengunduh komentar dari YouTube...")

# --- Loop pengambilan komentar ---
for comment in comments:
    username = comment.get("author", "Unknown")
    text = comment.get("text", "")
    time = comment.get("time", "Unknown")

    # === Tahap CASE FOLDING ===
    username_cf = username.lower()  # ubah ke huruf kecil
    text_cf = text.lower()          # ubah ke huruf kecil

    all_comments.append({
        "username": username_cf,
        "comment": text_cf,
        "time": time
    })

# --- Simpan ke file CSV ---
output_file = "youtube_comments_all_casefold.csv"

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["username", "comment", "time"])
    writer.writeheader()
    for c in all_comments:
        writer.writerow(c)

print(f"✅ Berhasil menyimpan {len(all_comments)} komentar (dengan case folding) ke {output_file}")
