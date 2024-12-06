from youtubesearchpython.__future__ import VideosSearch
from config import YOUTUBE_IMG_URL  # استيراد المتغير YOUTUBE_IMG_URL من ملف config.py

async def gen_thumb(videoid):
    try:
        # في هذا المثال، سنعيد YOUTUBE_IMG_URL مباشرة بدلاً من البحث عن صورة الفيديو
        return YOUTUBE_IMG_URL
    except Exception as e:
        return YOUTUBE_IMG_URL  # في حالة الخطأ، يتم إعادة YOUTUBE_IMG_URL

async def gen_qthumb(vidid):
    try:
        # في هذا المثال، سنعيد YOUTUBE_IMG_URL مباشرة بدلاً من البحث عن صورة الفيديو
        return YOUTUBE_IMG_URL
    except Exception as e:
        return YOUTUBE_IMG_URL  # في حالة الخطأ، يتم إعادة YOUTUBE_IMG_URL

async def get_thumb_url(videoid):
    try:
        # في هذا المثال، سنعيد YOUTUBE_IMG_URL مباشرة بدلاً من البحث عن صورة الفيديو
        return YOUTUBE_IMG_URL
    except Exception as e:
        return YOUTUBE_IMG_URL  # في حالة الخطأ، يتم إعادة YOUTUBE_IMG_URL
