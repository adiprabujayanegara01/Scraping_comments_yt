import pandas as pd
import ast
import re

# === 1. Baca file hasil stemming ===
df = pd.read_csv(r"D:\Scraping_comments_yt\youtube_comments_stemmed.csv")

# === 2. Ambil hanya kolom 'stemmed_tokens' ===
if 'stemmed_tokens' in df.columns:
    df_clean = df[['stemmed_tokens']].copy()
else:
    raise KeyError("Kolom 'stemmed_tokens' tidak ditemukan di CSV!")

# === 3. Konversi list string → teks dan bersihkan tanda kutip + baris kosong ===
def tokens_to_text(tokens):
    if isinstance(tokens, str):
        try:
            tokens = ast.literal_eval(tokens)
        except:
            tokens = [tokens]
    text = " ".join(tokens)
    # Hapus semua jenis tanda kutip
    text = re.sub(r'[\"\'“”‘’]+', '', text)
    # Hapus spasi berlebih
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Terapkan fungsi pembersihan
df_clean['clean_comment'] = df_clean['stemmed_tokens'].apply(tokens_to_text)

# === 4. Hapus baris yang kosong atau hanya berisi spasi ===
df_clean = df_clean[df_clean['clean_comment'].str.strip() != ""]

# === 5. Hapus duplikat komentar (hanya sisakan satu) ===
df_clean = df_clean.drop_duplicates(subset=['clean_comment'], keep='first')

# === 6. Hapus komentar yang hanya berisi angka ===
df_clean = df_clean[~df_clean['clean_comment'].str.fullmatch(r'\d+')]

# === 7. Hapus komentar yang hanya 1 atau 2 huruf ===
df_clean = df_clean[~df_clean['clean_comment'].str.fullmatch(r'[a-zA-Z]{1,2}')]

# === 8. Simpan hasil akhir ===
output_path = r"D:\Scraping_comments_yt\youtube_comments_clean_only.csv"
df_clean[['clean_comment']].to_csv(output_path, index=False)

print("✅ Komentar bersih 100% tanpa tanda kutip, duplikat, angka, dan komentar terlalu pendek.")
print("💾 File disimpan di:", output_path)
