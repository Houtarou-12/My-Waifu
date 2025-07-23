# 🌸 Waifu-chan Discord Bot

Waifu-chan adalah bot Discord anime-themed yang dirancang untuk memberi notifikasi otomatis dari YouTube, interaksi komunitas, dan fitur admin untuk server. Cocok untuk digunakan di komunitas penggemar konten Jepang, animasi, dan server interaktif!

---

## 🚀 Fitur Utama

### 🔁 Notifikasi Otomatis
- **Video Baru**  
  Deteksi video terbaru dari Muse Indonesia melalui RSS dan kirim embed ke channel utama secara otomatis.
- **Post Komunitas YouTube**  
  Scraping halaman komunitas Muse Indonesia dan kirim notifikasi post terbaru ke channel Discord.

---

## 💬 Command Manual

### 📌 Umum
| Command          | Deskripsi                                     |
|------------------|-----------------------------------------------|
| `~ping`          | Cek status bot                                |
| `~waifuhelp`     | Tampilkan daftar command Waifu-chan           |
| `~botinfo`       | Info detail bot, uptime & sistem              |
| `~peraturan`     | Tampilkan peraturan server                    |
| `~cekvideo`      | Cek video terbaru dari Muse Indonesia         |
| `~cekpost`       | Cek post komunitas terbaru dari Muse Indonesia |

### 🔧 Admin & Owner
| Command                       | Deskripsi                                                   |
|-------------------------------|--------------------------------------------------------------|
| `~forward #channel <pesan>`   | Kirim embed admin ke channel tertentu + tombol balasan       |
| `~to <pesan> #channel`        | Kirim pesan anonim ke channel pilihan                       |
| `~kickout @user`              | Kick member dari server                                     |
| `~vkick @user`                | Keluarkan member dari voice channel                         |
| `~tambahperaturan`            | Tambahkan peraturan baru                                    |
| `~editperaturan`              | Edit isi peraturan berdasarkan nomor                        |
| `~hapusperaturan`             | Hapus peraturan tertentu                                    |
| `~resetperaturan`             | Reset seluruh peraturan                                     |
| `~clear` / `~confirmclear`    | Bersihkan semua peraturan setelah konfirmasi                |
| `~setchannel`                 | Atur channel utama notifikasi                               |
| `~cekpost_all`                | Cek semua post komunitas tanpa filter ID                    |

---

## 🧠 Teknologi & Integrasi

- **discord.py** v2+
- YouTube RSS & komunitas scraping
- Embed Discord dengan tombol & modal balasan
- JSON storage untuk validasi ID video/post
- Modular command handler untuk ekspansi

---

## ✨ Estetika & Tujuan

Waifu-chan dibuat dengan sentuhan visual dan interaksi bertema anime untuk menghadirkan karakter yang imut namun fungsional sebagai sekretaris digital komunitasmu.

---

## ⚙️ Setup & Konfigurasi

1. Buat file `.env` berisi konfigurasi:
    ```env
    DISCORD_TOKEN=your_token_here
    CHANNEL_ID=channel_post_id
    VIDEO_CHANNEL_ID=channel_video_id
    YT_COMMUNITY_URL=https://www.youtube.com/@MuseIndonesia
    ```

2. Jalankan bot:
    ```bash
    python main.py
    ```

---

## 📜 Status & License

Waifu-chan dikembangkan secara pribadi dan belum dirilis untuk publik. Proyek ini bebas digunakan dan dimodifikasi untuk keperluan personal.

---
#### Fun fact
Bot ini dibuat dengan bantuan, bahkan bisa dibilang ini full buatan [AI](https://copilot.github.com/) :smile:
