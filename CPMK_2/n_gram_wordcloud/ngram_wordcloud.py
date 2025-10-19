import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')

# Daftar kata yang tidak bermakna (stopwords)
STOPWORDS = {
    'yang', 'dan', 'untuk', 'dengan', 'dari', 'pada', 'adalah', 'ini', 'itu',
    'dalam', 'atau', 'akan', 'telah', 'dapat', 'juga', 'ada', 'oleh', 'kami',
    'mereka', 'dia', 'saya', 'kamu', 'anda', 'tidak', 'bisa', 'sudah', 'sangat',
    'lebih', 'hanya', 'semua', 'masih', 'lagi', 'paling', 'saja', 'karena',
    'kalau', 'tapi', 'belum', 'sedang', 'harus', 'sebagai', 'antara', 'sampai',
    'kepada', 'melalui', 'terhadap', 'tentang', 'sebelum', 'sesudah', 'selama',
    'tetapi', 'bahwa', 'jika', 'maka', 'tersebut', 'apakah', 'dimana', 'bagaimana',
    'kenapa', 'kapan', 'siapa', 'apa', 'mana', 'berapa', 'seperti', 'sama',
    'sendiri', 'banyak', 'beberapa', 'setiap', 'seluruh', 'memang', 'banget',
    'sekali', 'sering', 'jarang', 'sekarang', 'nanti', 'kemarin', 'besok',
    'hari', 'waktu', 'tahun', 'bulan', 'minggu', 'tanggal', 'jam', 'menit',
    'detik', 'kali', 'pernah', 'jangan', 'jadi', 'bakal', 'ingin', 'mau',
    'biar', 'supaya', 'agar', 'deh', 'sih', 'dong', 'kok', 'yah', 'iya',
    'oke', 'haha', 'wkwk', 'hehe', 'hihi', 'wah', 'aduh', 'astaga',
    'terima', 'kasih', 'maaf', 'tolong', 'mohon', 'silakan', 'coba',
    'lihat', 'dengar', 'bicara', 'kata', 'cerita', 'tanya', 'jawab',
    'jelas', 'pasti', 'mungkin', 'kira', 'rasa', 'pikir', 'ingat',
    'tahu', 'kenal', 'paham', 'mengerti', 'baru', 'lama', 'dulu', 'kembali'
}

def create_ngrams(text, n):
    """Membuat n-gram dari teks"""
    words = text.split()
    ngrams = []
    for i in range(len(words) - n + 1):
        ngram = ' '.join(words[i:i+n])
        ngrams.append(ngram)
    return ngrams

def is_meaningful_ngram(ngram):
    """Cek apakah n-gram bermakna"""
    words = ngram.split()
    
    # Cek apakah semua kata adalah stopwords
    all_stopwords = all(word in STOPWORDS for word in words)
    if all_stopwords:
        return False
    
    # Cek panjang kata minimal
    for word in words:
        if len(word) < 3:
            return False
    
    return True

def filter_ngrams(ngram_freq, min_freq=2):
    """Filter n-gram yang tidak bermakna"""
    meaningful = {}
    for ngram, freq in ngram_freq.items():
        if is_meaningful_ngram(ngram) and freq >= min_freq:
            meaningful[ngram] = freq
    return meaningful

def create_wordcloud(ngram_dict, title, filename):
    """Membuat WordCloud dari n-gram"""
    if not ngram_dict:
        print(f"Tidak ada data untuk {title}")
        return
    
    # Buat WordCloud
    wordcloud = WordCloud(
        width=1200,
        height=600,
        background_color='white',
        colormap='viridis',
        max_words=100,
        relative_scaling=0.5,
        min_font_size=10
    ).generate_from_frequencies(ngram_dict)
    
    # Plot
    plt.figure(figsize=(15, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout(pad=0)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✓ WordCloud disimpan: {filename}")
    plt.close()

# ============ MAIN PROGRAM ============

# Baca file hasil normalisasi
print("="*60)
print("PROGRAM N-GRAM (1-3) DAN WORDCLOUD")
print("="*60)
print("\nMembaca file youtube_comments_normalized.csv...")

df = pd.read_csv('youtube_comments_normalized.csv')

# Gunakan kolom yang sudah dinormalisasi
if 'normalized_comment' in df.columns:
    comment_column = 'normalized_comment'
else:
    comment_column = df.columns[0]

print(f"Menggunakan kolom: '{comment_column}'")
print(f"Total komentar: {len(df)}")

# Dictionary untuk menyimpan hasil
ngram_results = {}

# ============ PROSES UNIGRAM (1-GRAM) ============
print("\n" + "="*60)
print("MEMPROSES UNIGRAM (1-GRAM)")
print("="*60)

all_unigrams = []
for text in df[comment_column]:
    if pd.notna(text) and text.strip():
        words = text.split()
        all_unigrams.extend(words)

unigram_freq = Counter(all_unigrams)
unigram_meaningful = filter_ngrams(unigram_freq, min_freq=2)

print(f"Total unigram: {len(unigram_freq)}")
print(f"Unigram bermakna: {len(unigram_meaningful)}")
print(f"\nTop 15 Unigram:")
print(f"{'No':<4} {'Kata':<30} {'Frekuensi':<10}")
print("-" * 50)
for idx, (word, freq) in enumerate(sorted(unigram_meaningful.items(), key=lambda x: x[1], reverse=True)[:15], 1):
    print(f"{idx:<4} {word:<30} {freq:<10}")

ngram_results['unigram'] = unigram_meaningful

# ============ PROSES BIGRAM (2-GRAM) ============
print("\n" + "="*60)
print("MEMPROSES BIGRAM (2-GRAM)")
print("="*60)

all_bigrams = []
for text in df[comment_column]:
    if pd.notna(text) and text.strip():
        bigrams = create_ngrams(text, 2)
        all_bigrams.extend(bigrams)

bigram_freq = Counter(all_bigrams)
bigram_meaningful = filter_ngrams(bigram_freq, min_freq=2)

print(f"Total bigram: {len(bigram_freq)}")
print(f"Bigram bermakna: {len(bigram_meaningful)}")
print(f"\nTop 15 Bigram:")
print(f"{'No':<4} {'Bigram':<30} {'Frekuensi':<10}")
print("-" * 50)
for idx, (bigram, freq) in enumerate(sorted(bigram_meaningful.items(), key=lambda x: x[1], reverse=True)[:15], 1):
    print(f"{idx:<4} {bigram:<30} {freq:<10}")

ngram_results['bigram'] = bigram_meaningful

# ============ PROSES TRIGRAM (3-GRAM) ============
print("\n" + "="*60)
print("MEMPROSES TRIGRAM (3-GRAM)")
print("="*60)

all_trigrams = []
for text in df[comment_column]:
    if pd.notna(text) and text.strip():
        trigrams = create_ngrams(text, 3)
        all_trigrams.extend(trigrams)

trigram_freq = Counter(all_trigrams)
trigram_meaningful = filter_ngrams(trigram_freq, min_freq=2)

print(f"Total trigram: {len(trigram_freq)}")
print(f"Trigram bermakna: {len(trigram_meaningful)}")
print(f"\nTop 15 Trigram:")
print(f"{'No':<4} {'Trigram':<40} {'Frekuensi':<10}")
print("-" * 60)
for idx, (trigram, freq) in enumerate(sorted(trigram_meaningful.items(), key=lambda x: x[1], reverse=True)[:15], 1):
    print(f"{idx:<4} {trigram:<40} {freq:<10}")

ngram_results['trigram'] = trigram_meaningful

# ============ SIMPAN HASIL KE CSV ============
print("\n" + "="*60)
print("MENYIMPAN HASIL KE CSV")
print("="*60)

# Simpan Unigram
unigram_df = pd.DataFrame(sorted(unigram_meaningful.items(), key=lambda x: x[1], reverse=True),
                          columns=['unigram', 'frequency'])
unigram_df.to_csv('unigram_meaningful.csv', index=False)
print("✓ unigram_meaningful.csv")

# Simpan Bigram
bigram_df = pd.DataFrame(sorted(bigram_meaningful.items(), key=lambda x: x[1], reverse=True),
                         columns=['bigram', 'frequency'])
bigram_df.to_csv('bigram_meaningful.csv', index=False)
print("✓ bigram_meaningful.csv")

# Simpan Trigram
trigram_df = pd.DataFrame(sorted(trigram_meaningful.items(), key=lambda x: x[1], reverse=True),
                          columns=['trigram', 'frequency'])
trigram_df.to_csv('trigram_meaningful.csv', index=False)
print("✓ trigram_meaningful.csv")

# ============ BUAT WORDCLOUD ============
print("\n" + "="*60)
print("MEMBUAT WORDCLOUD")
print("="*60)

create_wordcloud(unigram_meaningful, 
                'WordCloud Unigram (1-Gram)', 
                'wordcloud_unigram.png')

create_wordcloud(bigram_meaningful, 
                'WordCloud Bigram (2-Gram)', 
                'wordcloud_bigram.png')

create_wordcloud(trigram_meaningful, 
                'WordCloud Trigram (3-Gram)', 
                'wordcloud_trigram.png')

# ============ STATISTIK AKHIR ============
print("\n" + "="*60)
print("STATISTIK AKHIR")
print("="*60)
print(f"Unigram bermakna: {len(unigram_meaningful)}")
print(f"Bigram bermakna: {len(bigram_meaningful)}")
print(f"Trigram bermakna: {len(trigram_meaningful)}")
print(f"\nTotal kemunculan:")
print(f"  Unigram: {sum(unigram_meaningful.values())}")
print(f"  Bigram: {sum(bigram_meaningful.values())}")
print(f"  Trigram: {sum(trigram_meaningful.values())}")

print("\n" + "="*60)
print("SELESAI!")
print("="*60)