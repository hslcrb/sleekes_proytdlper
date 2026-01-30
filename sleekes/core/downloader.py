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
                self.log_callback("영상 데이터 확보 완료. 아카이빙 후처리 중...")

    def download(self, url: str, output_path: str, options: dict):
        out_tmpl = os.path.join(output_path, '%(uploader)s/%(upload_date)s - %(title)s/%(title)s.%(ext)s')
        if options.get('flat_output', False):
            out_tmpl = os.path.join(output_path, '%(title)s.%(ext)s')

        # yt-dlp 옵션 구성
        ydl_opts = {
            'progress_hooks': [self._progress_hook],
            'outtmpl': out_tmpl,
            
            # --- 아카이빙 및 메타데이터 관련 ---
            'writedescription': options.get('write_description', False) or options.get('archive_mode', False),
            'writeinfojson': options.get('write_info_json', False) or options.get('archive_mode', False),
            'writesubtitles': options.get('write_subs', False) or options.get('archive_mode', False),
            'getcomments': options.get('get_comments', False) or options.get('archive_mode', False),
            'writeautomaticcaption': options.get('write_auto_subs', False) or options.get('archive_mode', False),
            'writethumbnail': options.get('write_thumbnail', False) or options.get('archive_mode', False),
            
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
            
            # 클라이언트 플랫폼 분산 (웹 대신 모바일 클라이언트 위주로 요청하여 403 우회)
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

        # 스텔스 모드 (속도 제한 및 지연 강화)
        if options.get('stealth_mode', False):
            ydl_opts['ratelimit'] = 1024 * 512 # 512KB/s로 제한 (봇 탐지 회피용)
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

        if ydl_opts['writesubtitles'] or ydl_opts['writeautomaticcaption']:
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegSubtitlesConvertor',
                'format': 'srt',
            })

        if options.get('cookies_from_browser'):
            ydl_opts['cookiesfrombrowser'] = (options.get('cookies_from_browser'),)

        if options.get('skip_download', False):
            ydl_opts['skip_download'] = True

        if self.log_callback:
            self.log_callback(f"Sleekes 스텔스 엔진 가동 중: {url}")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True
        except Exception as e:
            if self.log_callback:
                self.log_callback(f"솔루션 실행 중 오류 발생: {str(e)}")
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
                self.log_callback(f"정보 추출 중 오류: {str(e)}")
            return None
