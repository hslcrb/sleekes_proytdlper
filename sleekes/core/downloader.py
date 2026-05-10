import os
import yt_dlp
from typing import Callable, Optional
from sleekes.core.uastream import get_random_ua

# =============================================================================
# [Sleekes Core Downloader]
# 
# 이 모듈은 Sleekes의 핵심 엔진으로, yt-dlp 라이브러리를 래핑(Wrapping)하여
# 실질적인 다운로드 및 아카이빙 작업을 수행합니다.
# =============================================================================

class SleekesDownloader:
    def __init__(self, progress_callback: Optional[Callable] = None, log_callback: Optional[Callable] = None):
        self.progress_callback = progress_callback
        self.log_callback = log_callback

    def _progress_hook(self, d):
        if self.progress_callback:
            self.progress_callback(d)
        
        if d['status'] == 'finished':
            if self.log_callback:
                self.log_callback("DONE: Asset secured. Processing...")

    def download(self, url: str, output_path: str, options: dict):
        from datetime import datetime
        from sleekes.core.config import get_next_counter
        
        # 1. 메타데이터 먼저 추출하여 폴더명 결정
        if self.log_callback:
            self.log_callback("ENGINE: Extracting metadata to determine folder structure...")
        
        info = self.get_info(url)
        if not info:
            if self.log_callback:
                self.log_callback("ERROR: Failed to extract metadata. Aborting.")
            return False

        # 채널명 및 동영상명 추출
        uploader = info.get('uploader') or info.get('channel') or 'UnknownChannel'
        title = info.get('title') or 'UnknownTitle'
        
        # 재생목록/채널인 경우
        is_playlist = 'entries' in info
        if is_playlist:
            # 채널 다운로드 시: 채널명_채널명
            folder_suffix = f"{uploader}_{uploader}"
        else:
            # 일반 동영상: 채널명_동영상명
            folder_suffix = f"{uploader}_{title}"

        # 특수문자 제거 (파일명 안전하게)
        import re
        folder_suffix = re.sub(r'[\\/*?:"<>|]', "", folder_suffix)
        
        today = datetime.now().strftime("%Y%m%d")
        xxxx = get_next_counter()
        
        # 최종 폴더명: YYYYMMDD_XXXX_채널명_동영상명
        final_folder_name = f"{today}_{xxxx}_{folder_suffix}"
        full_output_dir = os.path.join(output_path, final_folder_name)
        
        if not os.path.exists(full_output_dir):
            os.makedirs(full_output_dir)

        # 템플릿 설정: 모든 파일을 이 하나의 폴더 안에 때려박음
        out_tmpl = os.path.join(full_output_dir, '%(title)s.%(ext)s')

        # yt-dlp 옵션 구성
        ydl_opts = {
            'progress_hooks': [self._progress_hook],
            'outtmpl': out_tmpl,
            
            # --- [강력한 아카이빙 지원: 모든 기능 활성화] ---
            'writedescription': True,
            'writeinfojson': True,
            'writesubtitles': True,
            'getcomments': True,
            'writeautomaticcaption': True,
            'writethumbnail': True,
            'allsubtitles': True, # 모든 언어 자막
            
            'postprocessors': [],
            
            # --- [강력한 Anti-Ban & 403 방어 설정] ---
            'sleep_interval': options.get('sleep_interval', 0),
            'max_sleep_interval': options.get('max_sleep_interval', 0),
            'sleep_interval_requests': options.get('sleep_requests', 0),
            'ignoreerrors': options.get('ignore_errors', True),
            'no_clean_info_json': True,
            'wait_for_video': (3, 30),
            
            'nocheckcertificate': True,
            'geo_bypass': True,
            'no_warnings': True,
            
            # 클라이언트 플랫폼 분산
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios', 'web_safari'],
                    'player_skip': ['web'],
                }
            },
        }

        # [헤더 및 UA 로테이션]
        random_ua = get_random_ua()
        ydl_opts['user_agent'] = random_ua
        ydl_opts['http_headers'] = {
            'User-Agent': random_ua,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Sec-Fetch-Mode': 'navigate',
            'Referer': 'https://www.google.com/',
        }

        # 스텔스 모드
        if options.get('stealth_mode', False):
            ydl_opts['ratelimit'] = 1024 * 512
            if ydl_opts['sleep_interval'] == 0:
                ydl_opts['sleep_interval'] = 15
                ydl_opts['max_sleep_interval'] = 45
            ydl_opts['concurrent_fragment_downloads'] = 1

        # 포맷 설정
        if options.get('only_audio', False):
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            })
        else:
            ydl_opts['format'] = options.get('format', 'bestvideo+bestaudio/best')
            ydl_opts['merge_output_format'] = 'mp4'

        if options.get('playlist_items'):
            ydl_opts['playlist_items'] = options.get('playlist_items')
        
        if not options.get('use_playlist', True):
            ydl_opts['noplaylist'] = True

        # 자막 변환기
        ydl_opts['postprocessors'].append({
            'key': 'FFmpegSubtitlesConvertor',
            'format': 'srt',
        })

        if options.get('cookies_from_browser'):
            ydl_opts['cookiesfrombrowser'] = (options.get('cookies_from_browser'),)

        if options.get('skip_download', False):
            ydl_opts['skip_download'] = True

        if self.log_callback:
            self.log_callback(f"ENGINE START: Targeting {final_folder_name}")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            if self.log_callback:
                self.log_callback(f"SUCCESS: Archiving session completed in {final_folder_name}")
            return True
        except Exception as e:
            if self.log_callback:
                self.log_callback(f"ERROR: {str(e)}")
            return False

    def get_info(self, url: str):
        random_ua = get_random_ua()
        ydl_opts = {
            'user_agent': random_ua,
            'http_headers': {
                'User-Agent': random_ua,
                'Accept': '*/*',
                'Referer': 'https://www.google.com/',
            },
            'nocheckcertificate': True,
            'geo_bypass': True,
            'extractor_args': {'youtube': {'player_client': ['android']}}
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=False)
        except Exception as e:
            if self.log_callback:
                self.log_callback(f"ERROR: Metadata extraction failed: {str(e)}")
            return None
