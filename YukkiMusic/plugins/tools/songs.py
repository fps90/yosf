import os
import glob
import random
import wget
import requests
import re
import yt_dlp
import logging
import asyncio
from pyrogram import Client, filters
from strings.filters import command
from youtube_search import YoutubeSearch
from YukkiMusic import app
import httpx
import time
import requests
from bs4 import BeautifulSoup
import json
import re

def extract_quality(textes):
  los = []
  for text in textes:
    match = re.search(r'(\d{3,4})p', text['resolution'])
    if match:
      los.append(int(match.group(1)))
  return sorted(los)
# الرؤوس

def get_res(video_id):
    
    headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ar,en-GB;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6,en-US;q=0.5',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://yt1d.com',
    'priority': 'u=1, i',
    'referer': 'https://yt1d.com/en11/',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    }  
      
    # البيانات
    data = {
        'url': f'https://youtu.be/watch?v={video_id}',
        'ajax': '1',
        'lang': 'en',
    }

    # الطلب

    response = requests.post('https://yt1d.com/mates/en/analyze/ajax', headers=headers, data=data)

    # تحليل الرد JSON
    response_json = response.json()
    html_content = response_json.get('result', '')
    # print(html_content)

    # استخدام BeautifulSoup لتحليل الكود HTML المستخرج
    soup = BeautifulSoup(html_content, 'html.parser')

    # البحث عن الأزرار باستخدام الصنف المحدد
    tables = soup.find('table', class_='table table-bordered table-hover table-responsive-sm')
    # print(tables.td)

    # استخراج قيم onclick وتحويلها إلى قاموس باستخدام التعبيرات العادية
    downloads = []
    
    resolutions = set()  # استخدام مجموعة للتأكد من الفريدات
    
    if tables:
        td_elements = tables.find_all('td')
        for td in td_elements:
            text = td.get_text(strip=True)
            if 'p60' in text or '360p' in text or '(.mp4)' in text:
                resolutions.add(text)
    
    # تحويل المجموعة إلى قائمة مع عرض النتائج
    data = [{'resolution': res} for res in resolutions]
    
    return data

def send_request(video_id,res):
    
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'ar,en-GB;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6,en-US;q=0.5',
        'origin': 'https://loader.to',
        'priority': 'u=1, i',
        'referer': 'https://loader.to/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    params = {
        'start': '1',
        'end': '1',
        'format': res,
        'url': f'https://www.youtube.com/watch?v={video_id}',
    }

    response = requests.get('https://ab.cococococ.com/ajax/download.php', params=params, headers=headers)
    return response.json()

def get_progress(id):

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'ar,en-GB;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6,en-US;q=0.5',
        'origin': 'https://loader.to',
        'priority': 'u=1, i',
        'referer': 'https://loader.to/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    params = {
        'id': id,
    }

    response = requests.get('https://p.oceansaver.in/ajax/progress.php', params=params, headers=headers)
    return response.json()
def get_bytes(url):
    bytees = requests.get(url).content
    return bytees

def get_cookies_file():
    cookie_dir = "YukkiMusic/utils/cookies"
    cookies_files = [f for f in os.listdir(cookie_dir) if f.endswith(".txt")]

    cookie_file = os.path.join(cookie_dir, random.choice(cookies_files))
    return cookie_file


def sanitize_filename(title):
    return re.sub(r'[<>:"/\\|?*]', '', title).replace(' ', '_')

def download_audio_and_thumbnail(link, ydl_opts):
    
    id = send_request(link.split('v=')[1],360)['id'] 
    while True:
        progress = get_progress(id)
        if progress['text'] == 'Finished': 
            print(progress['download_url'])
            Do = requests.get(progress['download_url'])
            break
            
    with open(f"downloads/{link.split('v=')[1]}.mp3",'wb') as D:
        D.write(Do.content)
    thumbnail_url = "https://k.top4top.io/p_3262rs3261.jpg"
    if thumbnail_url:
            
                thumb_file = wget.download(thumbnail_url)
    else:
            thumb_file = None
            
    return f"downloads/{link.split('v=')[1]}.mp3", thumb_file

@app.on_message(command(["song", "بحث", "تحميل", "تنزيل", "يوت", "yt"]) & (filters.private | filters.group | filters.channel))
async def song(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    chutiya = message.from_user.mention

    query = " ".join(message.command[1:])
    
    m = await message.reply("⦗ جارٍ البحث ... ⦘")
    
    ydl_opts = {
        "format": "bestaudio[ext=m4a]",
        "cookiefile": get_cookies_file()
    }

    if "youtube.com" in query or "youtu.be" in query:
        link = query
    else:
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            link = f"https://youtube.com{results[0]['url_suffix']}"
        except Exception as e:
            await m.edit("⦗ لم يتم العثور على الصوت ⦘")
            logging.error(f"Failed to fetch YouTube video: {str(e)}")
            return
    try:
        await m.edit("⦗ جارٍ التحميل ... ⦘")
    except:
        pass

    try:
        loop = asyncio.get_event_loop()
        audio_file, thumb_file = await loop.run_in_executor(None, download_audio_and_thumbnail, link, ydl_opts)
        
        rep = f"- بواسطة : {chutiya}" if chutiya else "voice"
        
        await message.reply_audio(
            audio_file,
            caption=rep,
            performer=" voice .",
            thumb=thumb_file,  # Use the fetched thumbnail
            title=None,
        )
        await m.delete()
    
    except Exception as e:
        await m.edit(f"[Victorious] **\n\\خطأ :** {e}")
        logging.error(f"Error while downloading audio: {str(e)}")

    finally:
        try:
            os.remove(audio_file)
            if thumb_file:
                os.remove(thumb_file)  # Delete the thumbnail file
        except Exception as e:
            logging.error(f"Failed to delete temporary files: {str(e)}")

@app.on_message(command(["نزلي فيديو","نزلي الفيديو"]) & (filters.private | filters.group | filters.channel))
async def vsong(client, message):
    ydl_opts = {
        "format": "best",
        "cookiefile": get_cookies_file(),
        "keepvideo": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quiet": True,
    }

    query = " ".join(message.command[1:])

    m = await message.reply("⦗ جارٍ البحث ... ⦘")

    if "youtube.com" in query or "youtu.be" in query:
        link = query
    else:
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            link = f"https://youtube.com{results[0]['url_suffix']}"
        except Exception as e:
            await m.edit("🚫 **خطأ:** لم يتم العثور على الفيديو")
            return

    await m.edit("⦗ جارٍ التحميل ... ⦘")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
        
        await message.reply_video(
            file_name,
            duration=int(ytdl_data["duration"]),
            thumb=None,
            caption=ytdl_data["title"],
        )

        await m.delete()  

    except Exception as e:
        await m.edit(f"🚫 **خطأ:** {e}")

    finally:
        try:
            os.remove(file_name)
        except Exception as e:
            logging.error(f"Failed to delete temporary files: {str(e)}")
