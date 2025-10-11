import pandas as pd
import nltk
from nltk.tokenize import word_tokenize

# Unduh resource tokenizer jika belum ada
nltk.download('punkt')
nltk.download('punkt_tab')

# Baca file hasil case folding
df = pd.read_csv(r"D:\Scraping_comments_yt\youtube_comments_all_casefold.csv")

# Tokenizing tiap komentar
df['tokens'] = df['comment'].apply(lambda x: word_tokenize(str(x)))

# Simpan hasil tokenizing
output_path = r"D:\Scraping_comments_yt\youtube_comments_tokenized.csv"
df.to_csv(output_path, index=False)

print("✅ Proses tokenizing selesai!")
print("Hasil disimpan di:", output_path)
