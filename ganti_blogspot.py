import re
import os
import csv

# Memastikan file penting ada di folder
if not os.path.exists("index.html") or not os.path.exists("database.csv"):
    print("Error: File index.html atau database.csv tidak ditemukan di folder ini!")
    exit()

print("Membaca database Excel untuk mengambil link Blogspot baru...")

# Deteksi otomatis pemisah koma (,) atau titik koma (;) pada Excel
with open("database.csv", "r", encoding="utf-8-sig") as f:
    sample = f.read(2048)
    pemisah = ';' if ';' in sample else ','

# Mengambil semua link Blogspot baru dari kolom 'tombol1' di Excel
link_blogspot_baru = []
with open("database.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=pemisah)
    for row in reader:
        cleaned_row = {k.strip() if k else '': v for k, v in row.items()}
        link = next((v for k, v in cleaned_row.items() if 'tombol1' in k.lower()), '').strip()
        if link:
            link_blogspot_baru.append(link)

print("Membaca file index.html lama untuk mengambil token Anda...")
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Patenkan pola pencarian fleksibel untuk segala jenis subdomain/subfolder Blogspot
pattern = r'(\s*"[a-zA-Z0-9]+":\s*")[^"]*?(\?id=[a-zA-Z0-9]+")'
matches = re.findall(pattern, html_content)

if not matches:
    print("Error: Tidak menemukan struktur database token di dalam index.html!")
    exit()

# Proses menyatukan TOKEN LAMA dengan LINK BLOGSPOT BARU dari Excel
print("Menghubungkan token lama dengan link Excel baru...")
updated_js_content = ""
for i, match in enumerate(matches):
    prefix = match[0] # Bagian '"TOKEN_LAMA": "'
    suffix = match[1] # Bagian '?id=TOKEN_ID"'
    
    # Ambil link blogspot baru sesuai urutan baris Excel
    blog_baru = link_blogspot_baru[i] if i < len(link_blogspot_baru) else link_blogspot_baru[0]
    
    # Bersihkan domain jika di excel tidak sengaja terbawa parameter tanda tanya
    blog_baru = blog_baru.split('?')[0]
    
    updated_js_content += f'{prefix}{blog_baru}{suffix},\n'

# Memotong bagian databaseLink lama di HTML dan menggantinya dengan yang baru
start_pattern = r'var databaseLink = \s*\{'
end_pattern = r'\}\s*;'

start_match = re.search(start_pattern, html_content)
end_match = re.search(end_pattern, html_content)

if start_match and end_match:
    start_pos = start_match.end()
    end_pos = end_match.start()
    
    final_html = html_content[:start_pos] + "\n" + updated_js_content + "        " + html_content[end_pos:]
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_html)
        
    print("\n💥 SUKSES TOTAL BOSKU! 💥")
    print("1. Link Blogspot baru sukses ditarik dari Excel otomatis.")
    print("2. Semua TOKEN LAMA DI FACEBOOK TETAP AMAN dan tidak berubah!")
    print("3. Silakan buka GitHub Desktop, lalu Commit dan Push origin.")
else:
    print("Error: Gagal merakit ulang struktur HTML.")
