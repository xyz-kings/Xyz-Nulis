# ✍️ XYZ NULIS GENERATOR

Script Python untuk **membagi teks panjang menjadi beberapa gambar tulisan tangan otomatis** menggunakan API publik [`api-nulis-iota`](https://api-nulis-iota.vercel.app).

Script ini akan membaca teks dari file `request_nulis.txt`, memotongnya otomatis agar tidak melebihi batas 28 baris per gambar, lalu menyimpannya dalam folder hasil dengan format waktu.

---

## ⚙️ Fitur

- Deteksi otomatis teks yang terlalu panjang  
- Pembagian teks jadi beberapa batch (maks. 28 baris per gambar)  
- Koreksi otomatis bila kelebihan baris berdasarkan estimasi karakter  
- Output tersimpan otomatis dengan penamaan terstruktur  
- Tampilan terminal interaktif dengan tabel status  

---

## 📦 Konfigurasi

```python
API_URL = "https://api-nulis-iota.vercel.app/api/generate"
MAX_LINES = 28
AVG_CHAR_PER_LINE = 100     # untuk kalkulasi pengurangan kalau overflow
MAX_CHARS = 1104            # batas awal karakter per batch
MIN_CHUNK_CHARS = 50        # batas minimal biar tidak nyangkut
OUTPUT_BASE = os.getcwd()
REQUEST_FILE = "request_nulis.txt"
```

---

## 🧠 Cara Kerja Singkat

1. Program membaca isi `request_nulis.txt`
2. Membagi teks menjadi potongan berdasarkan `MAX_CHARS`
3. Mengirim setiap potongan ke API
4. Jika API mengembalikan error “kelebihan baris”, script mengurangi teks sesuai `AVG_CHAR_PER_LINE * selisih_baris`
5. Ulangi sampai API menerima
6. Simpan semua hasil gambar ke folder `/NULIS/<tanggal_folder>/`

---

## 🚀 Cara Menjalankan

1. Pastikan sudah terinstal **Python 3** dan module `requests`:
   ```bash
   pkg install python
   pip install requests rich
   ```

2. Simpan file script sebagai `nulis.py`

3. Buat file teks `request_nulis.txt` berisi paragraf yang ingin ditulis.

4. Jalankan script:
   ```bash
   python nulis.py
   ```

---

## 🖼️ Contoh Output Terminal

```
╭─────────────────────── Status ────────────────────────╮
│ XYZ NULIS GENERATOR                                   │
│ Membagi teks panjang menjadi beberapa gambar otomatis │
╰───────────────────────────────────────────────────────╯
✓ Disimpan:
 /storage/emulated/0/NULIS/Sabtu8_j13-m20-d17/xyzresp_2.png
┏━━━━━━━┳━━━━━━━━┓
┃ Batch ┃ Status ┃
┡━━━━━━━╇━━━━━━━━┩
│   1   │ Sukses │
│   2   │ Sukses │
└───────┴────────┘
╭─────────────────── Hasil ────────────────────╮
│ Selesai!                                     │
│ Total 2 gambar dibuat di folder:             │
│ /storage/emulated/0/NULIS/Sabtu8_j13-m20-d17 │
╰──────────────────────────────────────────────╯
```

---

## 📸 TAMPILAN OUTPUT V1 BETA

![Contoh Output](https://files.catbox.moe/5h1f6d.jpg)

---

## 🧾 Catatan

- Setiap gambar berisi maksimal **28 baris tulisan**.  
- Jika teks lebih dari itu, script otomatis membuat batch baru.  
- Tidak perlu memotong teks secara manual.  
- Hasil gambar disimpan dengan nama otomatis seperti:
  ```
  xyzresp_1.png
  xyzresp_2.png
  xyzresp_3.png
  ```

---

## 💡 Tips

- Gunakan teks bersih tanpa emoji agar hasil lebih stabil.  
