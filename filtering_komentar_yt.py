import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Unduh stopwords NLTK (jika belum ada)
nltk.download('stopwords')

# Muat file hasil tokenizing
df = pd.read_csv(r"D:\Scraping_comments_yt\youtube_comments_tokenized.csv")

# Jika kolom 'tokens' masih berupa string seperti "['kata1', 'kata2']"
# maka ubah jadi list Python kembali
df['tokens'] = df['tokens'].apply(lambda x: eval(x) if isinstance(x, str) else x)

# =============================
# 1️⃣ Hapus noise (tanda baca, simbol, angka, dll.)
# =============================
def clean_tokens(tokens):
    cleaned = []
    for token in tokens:
        # Hapus karakter non-alfanumerik
        token = re.sub(r'[^a-zA-Z0-9]', '', token)
        # Hapus token kosong
        if token.strip() != '':
            cleaned.append(token)
    return cleaned

df['cleaned_tokens'] = df['tokens'].apply(clean_tokens)

# =============================
# 2️⃣ Hapus stopwords Bahasa Indonesia
# =============================
# Gabungkan stopwords dari NLTK + Sastrawi
stop_factory = StopWordRemoverFactory()
stop_sastrawi = set(stop_factory.get_stop_words())
stop_nltk = set(stopwords.words('indonesian'))
stopwords_all = stop_sastrawi.union(stop_nltk)

def remove_stopwords(tokens):
    return [t for t in tokens if t not in stopwords_all]

df['filtered_tokens'] = df['cleaned_tokens'].apply(remove_stopwords)

# Simpan hasil filtering
output_path = r"D:\Scraping_comments_yt\youtube_comments_filtered.csv"
df.to_csv(output_path, index=False)

print("✅ Proses filtering selesai!")
print("Hasil disimpan di:", output_path)
