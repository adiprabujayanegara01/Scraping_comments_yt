import pandas as pd
from collections import Counter
import re

# Daftar kata yang tidak bermakna (stopwords + kata umum tanpa makna)
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

def create_bigrams(text):
    """Membuat bi-gram dari teks"""
    words = text.split()
    bigrams = []
    for i in range(len(words) - 1):
        bigram = f"{words[i]} {words[i+1]}"
        bigrams.append(bigram)
    return bigrams

def is_meaningful_bigram(bigram):
    """Cek apakah bi-gram bermakna (tidak mengandung stopwords)"""
    words = bigram.split()
    
    # Jika salah satu kata adalah stopword, bi-gram tidak bermakna
    if words[0] in STOPWORDS or words[1] in STOPWORDS:
        return False
    
    # Jika kata terlalu pendek (kurang dari 3 huruf), tidak bermakna
    if len(words[0]) < 3 or len(words[1]) < 3:
        return False
    
    return True

def filter_meaningless_bigrams(bigram_freq, min_freq=2):
    """Filter bi-gram yang tidak bermakna"""
    meaningful_bigrams = {}
    
    for bigram, freq in bigram_freq.items():
        if is_meaningful_bigram(bigram) and freq >= min_freq:
            meaningful_bigrams[bigram] = freq
    
    return meaningful_bigrams

# Baca file hasil normalisasi
print("Membaca file youtube_comments_normalized.csv...")
df = pd.read_csv('youtube_comments_normalized.csv')

# Gunakan kolom yang sudah dinormalisasi
if 'normalized_comment' in df.columns:
    comment_column = 'normalized_comment'
else:
    comment_column = df.columns[0]

print(f"Menggunakan kolom: '{comment_column}'")

# Buat bi-gram dari semua komentar
print("\nMembuat bi-gram dari semua komentar...")
all_bigrams = []

for text in df[comment_column]:
    if pd.notna(text) and text.strip():
        bigrams = create_bigrams(text)
        all_bigrams.extend(bigrams)

# Hitung frekuensi bi-gram
bigram_freq = Counter(all_bigrams)

print(f"\nTotal bi-gram yang ditemukan: {len(bigram_freq)}")
print(f"Total kemunculan bi-gram: {sum(bigram_freq.values())}")

# Tampilkan top 20 bi-gram SEBELUM filtering
print("\n=== TOP 20 BI-GRAM SEBELUM FILTERING ===")
print(f"{'No':<4} {'Bi-gram':<30} {'Frekuensi':<10}")
print("-" * 50)
for idx, (bigram, freq) in enumerate(bigram_freq.most_common(20), 1):
    print(f"{idx:<4} {bigram:<30} {freq:<10}")

# Filter bi-gram yang tidak bermakna
print("\n\nMemfilter bi-gram yang tidak bermakna...")
meaningful_bigrams = filter_meaningless_bigrams(bigram_freq, min_freq=2)

print(f"\nBi-gram setelah filtering: {len(meaningful_bigrams)}")
print(f"Bi-gram yang dihapus: {len(bigram_freq) - len(meaningful_bigrams)}")

# Tampilkan top 20 bi-gram SETELAH filtering
print("\n=== TOP 20 BI-GRAM SETELAH FILTERING (BERMAKNA) ===")
print(f"{'No':<4} {'Bi-gram':<30} {'Frekuensi':<10}")
print("-" * 50)

sorted_meaningful = sorted(meaningful_bigrams.items(), key=lambda x: x[1], reverse=True)
for idx, (bigram, freq) in enumerate(sorted_meaningful[:20], 1):
    print(f"{idx:<4} {bigram:<30} {freq:<10}")

# Simpan hasil ke CSV
bigram_df = pd.DataFrame(sorted_meaningful, columns=['bigram', 'frequency'])
bigram_df.to_csv('bigram_meaningful.csv', index=False)

# Simpan juga semua bi-gram (sebelum filtering) untuk perbandingan
all_bigram_df = pd.DataFrame(bigram_freq.most_common(), columns=['bigram', 'frequency'])
all_bigram_df.to_csv('bigram_all.csv', index=False)

print(f"\n✓ Hasil disimpan ke:")
print(f"  - 'bigram_meaningful.csv' (bi-gram bermakna)")
print(f"  - 'bigram_all.csv' (semua bi-gram)")

# Statistik tambahan
print("\n=== STATISTIK ===")
print(f"Persentase bi-gram yang bermakna: {len(meaningful_bigrams)/len(bigram_freq)*100:.2f}%")
print(f"Rata-rata frekuensi (bermakna): {sum(meaningful_bigrams.values())/len(meaningful_bigrams):.2f}")
print(f"Frekuensi tertinggi: {sorted_meaningful[0][1] if sorted_meaningful else 0}")
print(f"Frekuensi terendah (min=2): {min(meaningful_bigrams.values()) if meaningful_bigrams else 0}")

# Contoh bi-gram yang dihapus
print("\n=== CONTOH BI-GRAM YANG DIHAPUS (Tidak Bermakna) ===")
removed_bigrams = [(bg, freq) for bg, freq in bigram_freq.most_common(50) 
                   if bg not in meaningful_bigrams]
for idx, (bigram, freq) in enumerate(removed_bigrams[:10], 1):
    reason = []
    words = bigram.split()
    if words[0] in STOPWORDS or words[1] in STOPWORDS:
        reason.append("mengandung stopword")
    if len(words[0]) < 3 or len(words[1]) < 3:
        reason.append("kata terlalu pendek")
    print(f"{idx}. '{bigram}' (freq: {freq}) - Alasan: {', '.join(reason)}")