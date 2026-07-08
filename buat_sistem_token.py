import os
import csv
import random
import string

if not os.path.exists("database.csv"):
    print("Error: Berkas database.csv tidak ditemukan di folder ini! Harap pindahkan dulu.")
    exit()

def buat_token_acak(length=9):
    karakter = string.ascii_letters + string.digits
    return ''.join(random.choice(karakter) for _ in range(length))

print("Membaca database Excel asli Anda...")

with open("database.csv", "r", encoding="utf-8-sig") as f:
    sample = f.read(2048)
    pemisah = ';' if ';' in sample else ','

database_js_content = ""
daftar_link_siap_sebar = []

# =========================================================================
# KODE SUDAH DIKUNCI MATI KHUSUS UNTUK AKUN BARU ANDA BOSKU
# =========================================================================
USERNAME_BARU = "lizaakiw"
REPOSITORI_BARU = "lizakikiw"
# =========================================================================

DOMAIN_ANDA = f"https://{USERNAME_BARU}.github.io/{REPOSITORI_BARU}"

with open("database.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=pemisah)
    
    index = 1
    for row in reader:
        cleaned_row = {k.strip() if k else '': v for k, v in row.items()}
        link_blogspot = next((v for k, v in cleaned_row.items() if 'tombol1' in k.lower()), '').strip()
        
        if not link_blogspot:
            continue
        
        token_unik = buat_token_acak()
        database_js_content += f'            "{token_unik}": "{link_blogspot}",\n'
        
        link_jadi_token = f"{DOMAIN_ANDA}/?video={token_unik}"
        daftar_link_siap_sebar.append([f"Data ke-{index}", link_jadi_token])
        
        index += 1

if database_js_content.endswith(",\n"):
    database_js_content = database_js_content[:-2] + "\n"

print(f"Berhasil memproses {index - 1} link. Sedang merakit 1 file index.html utama...")

html_template_final = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Viral</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #000000;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 1rem;
        }}
        .card-container {{
            background-color: #ffffff;
            width: 100%;
            max-width: 420px;
            border-radius: 1.5rem;
            padding: 2.5rem 1.5rem;
            text-align: center;
            box-shadow: 0 0 40px 10px rgba(236, 72, 153, 0.6); 
        }}
        .title-box {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            font-size: 1.5rem;
            font-weight: 800;
            color: #000000;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 2.5rem;
        }}
        .btn-link {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            background-color: #000000;
            color: #ffffff;
            text-decoration: none;
            font-weight: 700;
            font-size: 1.2rem;
            padding: 1.2rem;
            border-radius: 0.75rem;
            border: 2px solid #eab308;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        }}
    </style>
</head>
<body>
    <div class="card-container">
        <div class="title-box"><span>🔥</span> VIDEO VIRAL <span>🔥</span></div>
        <a href="#" id="tombolMassal" class="btn-link">▶ Watch Video Now</a>
    </div>

    <script>
        var urlParams = new URLSearchParams(window.location.search);
        var tokenIklan = urlParams.get('video');

        var databaseLink = {{
{database_js_content}        }};

        var linkTujuan = databaseLink[tokenIklan] || "https://blogspot.com";
        document.getElementById("tombolMassal").href = linkTujuan;
    </script>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template_final)

print("Sedang mencetak file Excel hasil rekap token huruf acak...")

with open("AKUN_BARU_LINK_TOKEN_ACAK.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["Nomor", "Link Iklan Siap Sebar FB"])
    writer.writerows(daftar_link_siap_sebar)

print(f"\n💥 SUKSES TOTAL BOSKU! 💥")
print(f"1. File 'index.html' berisi {index - 1} database link selesai dirakit.")
print(f"2. File Excel 'AKUN_BARU_LINK_TOKEN_ACAK.csv' isi huruf acak murni selesai dibuat.")
