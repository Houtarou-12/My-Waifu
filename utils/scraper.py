import os
import json
import feedparser
import requests
import re

DATA_FILE = "data.json"  # Sesuaikan jika kamu pakai nama lain
RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCxxnxya_32jcKj4yN1_kD7A"

# 💾 ───── Handling ID Storage ─────
def load_sent_post_ids():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"[ERROR] Gagal load post_sent.json: {e}")
    return []

def save_sent_post_ids(post_ids):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(post_ids, f, indent=2)
        print(f"[SAVE] {len(post_ids)} post ID disimpan")
    except Exception as e:
        print(f"[ERROR] Gagal simpan post_sent.json: {e}")

# 🔍 ───── Scraper Komunitas ─────
def get_latest_posts(channel_url, max_posts=5):
    results = []
    try:
        response = requests.get(channel_url + "/community", headers={"User-Agent": "Mozilla/5.0"})
        match = re.search(r"var ytInitialData = ({.*?});</script>", response.text)
        if not match:
            print("[ERROR] ytInitialData tidak ditemukan.")
            return []

        data = json.loads(match.group(1))
        tabs = data.get("contents", {}).get("twoColumnBrowseResultsRenderer", {}).get("tabs", [])

        for tab in tabs:
            content = tab.get("tabRenderer", {}).get("content", {})
            sections = content.get("sectionListRenderer", {}).get("contents", [])
            for section in sections:
                posts = section.get("itemSectionRenderer", {}).get("contents", [])
                for item in posts:
                    try:
                        post_data = item["backstagePostThreadRenderer"]["post"]["backstagePostRenderer"]
                        post_id = post_data.get("postId", "")
                        if not post_id.startswith("Ugk"):
                            continue

                        text_runs = post_data.get("contentText", {}).get("runs", [])
                        text = "".join(run.get("text", "") for run in text_runs).strip()
                        timestamp = post_data.get("publishedTimeText", {}).get("runs", [{}])[0].get("text", "")

                        # 🎯 Detect thumbnail image
                        thumbnail_url = None
                        try:
                            img = post_data.get("backstageAttachment", {}).get("imageAttachmentRenderer", {}).get("image", {})
                            thumbnails = img.get("thumbnails", [])
                            if thumbnails:
                                thumbnail_url = thumbnails[-1].get("url")
                        except Exception as e:
                            print(f"[IMG] Gagal ambil gambar: {e}")

                        # 🎯 Fallback to videoAttachmentRenderer thumbnail
                        if not thumbnail_url:
                            try:
                                vid = post_data.get("backstageAttachment", {}).get("videoAttachmentRenderer", {}).get("thumbnail", {})
                                thumbnails = vid.get("thumbnails", [])
                                if thumbnails:
                                    thumbnail_url = thumbnails[-1].get("url")
                            except Exception as e:
                                print(f"[VIDEO] Gagal ambil thumbnail video: {e}")

                        results.append({
                            "id": post_id,
                            "url": f"https://www.youtube.com/post/{post_id}",
                            "text": text,
                            "timestamp": timestamp,
                            "thumbnail": thumbnail_url
                        })

                        if len(results) >= max_posts:
                            return results
                    except Exception:
                        continue
    except Exception as e:
        print(f"[ERROR] Gagal scrape komunitas: {e}")
    return results

# 🔍 ───── Scraper Video via RSS ─────
def get_latest_rss_videos(rss_url=RSS_URL, max_items=3):
    results = []
    try:
        with open("last_video.txt", "r") as f:
            sent_ids = f.read().splitlines()
    except:
        sent_ids = []

    try:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            video_id = entry.yt_videoid
            if video_id in sent_ids:
                continue

            results.append({
                "id": video_id,
                "title": entry.title,
                "url": entry.link,
                "published": entry.published
            })

            if len(results) >= max_items:
                break
        print(f"[RSS] Ditemukan {len(results)} video baru")
    except Exception as e:
        print(f"[ERROR] Gagal ambil RSS: {e}")
    return results

def save_video_id(video_id):
    try:
        with open("last_video.txt", "a") as f:
            f.write(video_id + "\n")
    except Exception as e:
        print(f"[ERROR] Gagal simpan video ID: {e}")
