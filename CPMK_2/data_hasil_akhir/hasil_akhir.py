import pandas as pd
import re

# Daftar stopwords yang akan dihapus untuk hasil akhir
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

def final_cleaning(text):
    """Pembersihan final: hapus stopwords dan kata tidak bermakna"""
    if pd.isna(text) or not text.strip():
        return ""
    
    # Split kata
    words = text.split()
    
    # Filter: hapus stopwords dan kata pendek
    clean_words = []
    for word in words:
        # Hanya simpan kata yang:
        # 1. Bukan stopword
        # 2. Panjang >= 3 huruf
        # 3. Hanya huruf (bukan angka)
        if (word not in STOPWORDS and 
            len(word) >= 3 and 
            word.isalpha()):
            clean_words.append(word)
    
    # Gabungkan kembali
    result = ' '.join(clean_words)
    
    return result.strip()

# ============ MAIN PROGRAM ============

print("="*70)
print("PROGRAM PEMBERSIHAN FINAL KOMENTAR YOUTUBE")
print("="*70)

# Baca file hasil normalisasi
print("\nMembaca file youtube_comments_normalized.csv...")
df = pd.read_csv('youtube_comments_normalized.csv')

# Gunakan kolom yang sudah dinormalisasi
if 'normalized_comment' in df.columns:
    comment_column = 'normalized_comment'
else:
    comment_column = df.columns[0]

print(f"Kolom yang digunakan: '{comment_column}'")
print(f"Total komentar awal: {len(df)}")

# Tampilkan contoh SEBELUM pembersihan final
print("\n" + "="*70)
print("CONTOH KOMENTAR SEBELUM PEMBERSIHAN FINAL")
print("="*70)
for idx, comment in enumerate(df[comment_column].head(5), 1):
    print(f"{idx}. {comment}")

# Lakukan pembersihan final
print("\n" + "="*70)
print("MELAKUKAN PEMBERSIHAN FINAL...")
print("="*70)
print("Proses: Menghapus stopwords dan kata tidak bermakna...")

df['clean_comment'] = df[comment_column].apply(final_cleaning)

# Hapus komentar yang kosong setelah pembersihan
df_clean = df[df['clean_comment'].str.strip() != ''].copy()

print(f"✓ Pembersihan selesai!")
print(f"✓ Komentar tersisa: {len(df_clean)}")
print(f"✓ Komentar dihapus (kosong): {len(df) - len(df_clean)}")

# Tampilkan contoh SETELAH pembersihan final
print("\n" + "="*70)
print("CONTOH KOMENTAR SETELAH PEMBERSIHAN FINAL")
print("="*70)
for idx, comment in enumerate(df_clean['clean_comment'].head(10), 1):
    print(f"{idx}. {comment}")

# Buat DataFrame baru dengan HANYA 1 kolom
final_df = pd.DataFrame({
    'comment': df_clean['clean_comment']
})

# Simpan ke CSV
output_file = 'youtube_comments_final_clean.csv'
final_df.to_csv(output_file, index=False)

print("\n" + "="*70)
print("FILE BERHASIL DISIMPAN!")
print("="*70)
print(f"✓ Nama file: {output_file}")
print(f"✓ Jumlah kolom: 1 (hanya kolom 'comment')")
print(f"✓ Jumlah baris: {len(final_df)}")

# Statistik detail
print("\n" + "="*70)
print("STATISTIK DETAIL")
print("="*70)
print(f"Komentar asli: {len(df)}")
print(f"Komentar bersih: {len(df_clean)}")
print(f"Persentase tersisa: {len(df_clean)/len(df)*100:.2f}%")
print(f"\nPanjang komentar:")
print(f"  Min: {df_clean['clean_comment'].str.split().str.len().min()} kata")
print(f"  Max: {df_clean['clean_comment'].str.split().str.len().max()} kata")
print(f"  Rata-rata: {df_clean['clean_comment'].str.split().str.len().mean():.2f} kata")

# Total kata unik
all_words = ' '.join(df_clean['clean_comment']).split()
unique_words = set(all_words)
print(f"\nTotal kata: {len(all_words)}")
print(f"Kata unik: {len(unique_words)}")

# Preview isi file
print("\n" + "="*70)
print("PREVIEW ISI FILE FINAL (10 Baris Pertama)")
print("="*70)
print(final_df.head(10).to_string(index=False))

print("\n" + "="*70)
print("SELESAI! File siap digunakan untuk analisis lanjutan.")
print("="*70)

# Informasi tambahan
print("\n📁 File yang dihasilkan:")
print(f"   {output_file}")
print("\n📊 Format:")
print("   - 1 kolom: 'comment'")
print("   - Encoding: UTF-8")
print("   - Separator: koma (,)")
print("\n✨ Komentar sudah benar-benar bersih dari:")
print("   ✓ Stopwords")
print("   ✓ Kata singkat (< 3 huruf)")
print("   ✓ Angka dan karakter spesial")
print("   ✓ Kata tidak bermakna")