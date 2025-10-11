import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import ast  # untuk konversi string list jadi list Python

# Baca file hasil filtering
df = pd.read_csv(r"D:\Scraping_comments_yt\youtube_comments_filtered.csv")

# Konversi kolom token (jika masih string)
df['filtered_tokens'] = df['filtered_tokens'].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
)

# Buat stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Fungsi untuk stemming setiap token
def stem_tokens(tokens):
    return [stemmer.stem(token) for token in tokens]

# Terapkan stemming
df['stemmed_tokens'] = df['filtered_tokens'].apply(stem_tokens)

# Simpan hasil ke file baru
output_path = r"D:\Scraping_comments_yt\youtube_comments_stemmed.csv"
df.to_csv(output_path, index=False)

print("✅ Proses stemming selesai!")
print("Hasil disimpan di:", output_path)
