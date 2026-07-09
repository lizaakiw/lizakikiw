import re
import os
import csv

# Memastikan file penting ada di folder
if not os.path.exists("index.html") or not os.path.exists("database.csv"):
    print("Error: File index.html atau database.csv tidak ditemukan di folder ini!")
    exit()

print("Membaca database Excel asli Anda...")

# Deteksi otomatis pemisah koma (,) atau titik koma (;) pada Excel
with open("database.csv", "r", encoding="utf-8-sig") as f:
    sample = f.read(2048)
    pemisah = ';' if ';' in sample else ','

# Mengambil dan MEMBERSIHKAN link Blogspot dari kolom 'Tombol1'
link_blogspot_baru = []
with open("database.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=pemisah)
    for row in reader:
        cleaned_row = {k.strip() if k else '': v for k, v in row.items()}
        link = next((v for k, v in cleaned_row.items() if 'tombol1' in k.lower()), '').strip()
        if link:
            # MEMOTONG format /?id= atau ?id= yang terbawa dari Excel
            link_bersih = link.split('?')[0].rstrip('/')
            link_blogspot_baru.append(link_bersih)

print("Membaca file index.html lama untuk mengambil token Anda...")
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Mencari semua baris token lama di index.html
pattern = r'(\s*"[a-zA-Z0-9]+":\s*")[^"]*?(\?id=[a-zA-Z0-9]+")'
matches = re.findall(pattern, html_content)

if not matches:
    print("Error: Tidak menemukan struktur database token di dalam index.html!")
    exit()

print("Menyambungkan kembali token lama dengan link bersih...")
updated_js_content = ""
for i, match in enumerate(matches):
    prefix = match[0] # Bagian '"TOKEN_LAMA": "'
    suffix = match[1] # Bagian '?id=TOKEN_ID"'
    
    # Ambil domain blogspot bersih dari baris Excel sesuai urutan
    blog_baru = link_blogspot_baru[i] if i < len(link_blogspot_baru) else link_blogspot_baru[0]
    
    # Menyatukan kembali menjadi format yang benar dan rapi demi keamanan Google
    updated_js_content += f'{prefix}{blog_baru}/{suffix},\n'

# Memotong bagian databaseLink lama di HTML dan menggantinya dengan yang baru
start_pattern = r'var databaseLink = \s*\{'
end_pattern = r'\}\s*;'

start_match = re.search(start_pattern, html_content)
end_match = re.search(end_pattern, html_content)

if start_match and end_match:
    start_pos = start_match.end()
    end_pos = start_match.start()
    
    final_html = html_content[:start_pos] + "\n" + updated_js_content + "        " + html_content[end_pos:]
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_html)
        
    print("\n💥 SUKSES TOTAL BOSKU! 💥")
    print("1. Link Excel yang double '?id=' sudah dibersihkan otomatis oleh robot.")
    print("2. Struktur index.html sudah rapi, TOKEN LAMA DI FACEBOOK AMAN!")
    print("3. Silakan buka GitHub Desktop, lalu Commit dan Push origin.")
else:
    print("Error: Gagal merakit ulang struktur HTML.")
