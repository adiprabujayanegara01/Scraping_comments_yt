import pandas as pd
import re

# Kamus normalisasi untuk kata gaul, singkatan, dan typo bahasa Indonesia
normalization_dict = {
    # Kata gaul dan singkatan umum
    'gak': 'tidak', 'ga': 'tidak', 'gk': 'tidak', 'g': 'tidak',
    'ngga': 'tidak', 'nggak': 'tidak', 'gag': 'tidak',
    'udah': 'sudah', 'udh': 'sudah', 'dah': 'sudah',
    'blm': 'belum', 'blom': 'belum',
    'yg': 'yang', 'yng': 'yang',
    'dgn': 'dengan', 'sama': 'dengan',
    'utk': 'untuk', 'buat': 'untuk',
    'krn': 'karena', 'krna': 'karena', 'soalnya': 'karena',
    'jd': 'jadi', 'jdi': 'jadi',
    'emg': 'memang', 'emang': 'memang', 'mmg': 'memang',
    'bgt': 'banget', 'bgt': 'banget', 'bgtt': 'banget', 'bngtt': 'banget',
    'bgt': 'banget', 'bngt': 'banget', 'bangettt': 'banget',
    'lg': 'lagi', 'lgi': 'lagi',
    'org': 'orang', 'orng': 'orang',
    'tdk': 'tidak', 'tak': 'tidak',
    'gmn': 'bagaimana', 'gimana': 'bagaimana', 'gmana': 'bagaimana',
    'knp': 'kenapa', 'knapa': 'kenapa', 'napa': 'kenapa',
    'klo': 'kalau', 'kalo': 'kalau', 'klu': 'kalau',
    'tp': 'tapi', 'tpi': 'tapi',
    'gw': 'saya', 'gue': 'saya', 'ane': 'saya',
    'lo': 'kamu', 'lu': 'kamu', 'elu': 'kamu',
    'wkwk': 'haha', 'wkwkwk': 'haha', 'kwkw': 'haha',
    'mksh': 'terima kasih', 'tq': 'terima kasih', 'thx': 'terima kasih',
    'thanks': 'terima kasih', 'tengkyu': 'terima kasih',
    'sih': '', 'deh': '', 'dong': '', 'kok': '',
    'bkn': 'bukan', 'bukn': 'bukan',
    'hrs': 'harus', 'hrus': 'harus',
    'jgn': 'jangan', 'jngn': 'jangan',
    'sm': 'sama', 'sma': 'sama',
    'skrg': 'sekarang', 'skrang': 'sekarang', 'skr': 'sekarang',
    'sdh': 'sudah', 'tlh': 'telah',
    'bs': 'bisa', 'bsa': 'bisa',
    'kpn': 'kapan', 'kapn': 'kapan',
    'dmn': 'dimana', 'mana': 'dimana',
    'jwb': 'jawab', 'jwab': 'jawab',
    'msh': 'masih', 'masi': 'masih',
    'cb': 'coba', 'cba': 'coba',
    'ni': 'ini', 'nih': 'ini',
    'tu': 'itu', 'tuh': 'itu',
    'sy': 'saya', 'aku': 'saya',
    'km': 'kamu', 'kmu': 'kamu',
    'org': 'orang',
    'trs': 'terus', 'truz': 'terus',
    'pengen': 'ingin', 'pngen': 'ingin',
    'mau': 'ingin', 'mw': 'ingin',
    'bkl': 'bakal', 'akan': 'bakal',
    'ntar': 'nanti', 'ntr': 'nanti',
    'aja': 'saja', 'aj': 'saja',
    'sbg': 'sebagai', 'sbgai': 'sebagai',
    'dr': 'dari', 'dri': 'dari',
    'pd': 'pada', 'pda': 'pada',
    'dlm': 'dalam', 'di': 'dalam',
    'dgr': 'dengar', 'dngr': 'dengar',
    'lihat': 'lihat', 'lht': 'lihat',
    'gimana': 'bagaimana',
    'kayak': 'seperti', 'kyk': 'seperti', 'kyak': 'seperti',
    'ya': 'iya', 'iyh': 'iya', 'yah': 'iya',
    'oke': 'oke', 'ok': 'oke', 'okeh': 'oke',
    'mantap': 'bagus', 'mantul': 'bagus', 'mantab': 'bagus',
    'jelek': 'buruk', 'jlek': 'buruk',
    'cakep': 'tampan', 'ganteng': 'tampan',
    'cantik': 'cantik', 'cntk': 'cantik',
    'keren': 'keren', 'krn': 'keren',
}

def remove_repeated_chars(text):
    """Menghapus karakter yang berulang lebih dari 2 kali"""
    # Contoh: 'kerennnnn' menjadi 'keren', 'huaaaaa' menjadi 'hua'
    return re.sub(r'(.)\1{2,}', r'\1\1', text)

def normalize_text(text):
    """Normalisasi teks komentar"""
    if pd.isna(text):
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Hapus URL
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # Hapus mention dan hashtag
    text = re.sub(r'@\w+|#\w+', '', text)
    
    # Hapus karakter berulang
    text = remove_repeated_chars(text)
    
    # Hapus karakter spesial kecuali spasi
    text = re.sub(r'[^a-z\s]', ' ', text)
    
    # Normalisasi kata berdasarkan kamus
    words = text.split()
    normalized_words = []
    
    for word in words:
        # Normalisasi kata berdasarkan kamus
        normalized_word = normalization_dict.get(word, word)
        
        # Hapus kata yang kurang dari 3 huruf
        if len(normalized_word) >= 3:
            normalized_words.append(normalized_word)
    
    # Gabungkan kembali kata-kata
    result = ' '.join(normalized_words)
    
    # Hapus spasi berlebih
    result = re.sub(r'\s+', ' ', result).strip()
    
    return result

# Baca file CSV
print("Membaca file youtube_comments.csv...")
df = pd.read_csv('youtube_comments.csv')

# Cek nama kolom
print(f"\nKolom yang tersedia: {df.columns.tolist()}")
comment_column = df.columns[0]  # Ambil kolom pertama
print(f"Menggunakan kolom: '{comment_column}'")

# Tampilkan beberapa data asli
print("\n=== Contoh Data Asli ===")
print(df.head())

# Normalisasi data
print("\nMemproses normalisasi data...")
df['normalized_comment'] = df[comment_column].apply(normalize_text)

# Hapus baris dengan komentar kosong setelah normalisasi
df = df[df['normalized_comment'].str.strip() != '']

# Tampilkan hasil normalisasi
print("\n=== Hasil Normalisasi ===")
print(df[[comment_column, 'normalized_comment']].head(10))

# Simpan hasil
output_file = 'youtube_comments_normalized.csv'
df.to_csv(output_file, index=False)
print(f"\n✓ Data berhasil dinormalisasi dan disimpan ke '{output_file}'")
print(f"✓ Total komentar yang diproses: {len(df)}")

# Statistik
print("\n=== Statistik ===")
print(f"Jumlah kata rata-rata (asli): {df[comment_column].str.split().str.len().mean():.2f}")
print(f"Jumlah kata rata-rata (normalisasi): {df['normalized_comment'].str.split().str.len().mean():.2f}")