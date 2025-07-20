import os
import json
import feedparser
import requests
import re

DATA_FILE = "post_sent.json"
RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCxxnxya_32jcKj4yN1_kD7A"

def load_sent_post_ids():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_sent_post_ids(post_ids):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(post_ids, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Simpan post ID: {e}")

def save_video_id(video_id):
    try:
        with open("last_video.txt", "a") as f:
            f.write(video_id + "\n")
    except Exception as e:
        print(f"[ERROR] Simpan video ID: {e}")

def get_latest_posts(channel_url, max_posts=5):
    results = []
    try:
        response = requests.get(channel_url + "/community", headers={"User-Agent": "Mozilla/5.0"})
        match = re.search(r"var ytInitialData = ({.*?});</script>", response.text)
        if not match:
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

                        text = "".join(run.get("text", "") for run in post_data.get("contentText", {}).get("runs", []))
                        timestamp = post_data.get("publishedTimeText", {}).get("runs", [{}])[0].get("text", "")
                        thumbnail_url = None

                        try:
                            thumbs = post_data.get("backstageAttachment", {}).get("imageAttachmentRenderer", {}).get("image", {}).get("thumbnails", [])
                            if thumbs:
                                thumbnail_url = thumbs[-1].get("url")
                        except:
                            pass

                        if not thumbnail_url:
                            try:
                                thumbs = post_data.get("backstageAttachment", {}).get("videoAttachmentRenderer", {}).get("thumbnail", {}).get("thumbnails", [])
                                if thumbs:
                                    thumbnail_url = thumbs[-1].get("url")
                            except:
                                pass

                        results.append({
                            "id": post_id,
                            "url": f"https://www.youtube.com/post/{post_id}",
                            "text": text.strip(),
                            "timestamp": timestamp,
                            "thumbnail": thumbnail_url
                        })

                        if len(results) >= max_posts:
                            return results
                    except:
                        continue
    except Exception as e:
        print(f"[ERROR] Scrape komunitas: {e}")
    return results

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
    except Exception as e:
        print(f"[ERROR] Ambil RSS: {e}")
    return results
