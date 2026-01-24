import os
import yt_dlp
from typing import Callable, Optional

# =============================================================================
# [Sleekes Core Downloader]
# 
# 이 모듈은 Sleekes의 핵심 엔진으로, yt-dlp 라이브러리를 래핑(Wrapping)하여
# 실질적인 다운로드 및 아카이빙 작업을 수행합니다.
# GUI와 CLI 양쪽에서 공통으로 사용되며, 비동기 처리를 위한 콜백(Callback)을 지원합니다.
# =============================================================================

class SleekesDownloader:
    """
    Sleekes 다운로드 및 아카이빙 관리 클래스입니다.
    yt-dlp의 복잡한 옵션들을 사용자 친화적인 메서드로 추상화합니다.
    """
    
    def __init__(self, progress_callback: Optional[Callable] = None, log_callback: Optional[Callable] = None):
        """
        초기화 메서드

        Args:
            progress_callback (Callable, optional): 다운로드 진행률 정보를 받아 처리할 함수. (GUI 프로그레스바 연동용)
            log_callback (Callable, optional): 텍스트 로그 메시지를 받아 처리할 함수. (GUI 로그창/CLI 출력용)
        """
        self.progress_callback = progress_callback
        self.log_callback = log_callback

    def _progress_hook(self, d):
        """
        yt-dlp 내부에서 호출되는 진행률 훅(Hook) 함수입니다.
        다운로드 상태가 변할 때마다 호출되어, 등록된 콜백 함수로 정보를 전달합니다.

        Args:
            d (dict): yt-dlp가 전달하는 상태 정보 딕셔너리
                      (status, _percent_str, _speed_str, _eta_str 등 포함)
        """
        if self.progress_callback:
            self.progress_callback(d)
        
        # 상태별 로그 메시지 처리
        if d['status'] == 'downloading':
            # 다운로드 중일 때: 퍼센트, 속도, 잔여 시간 파싱
            p = d.get('_percent_str', '0%')
            s = d.get('_speed_str', 'N/A')
            t = d.get('_eta_str', 'N/A')
            
            # 너무 빈번한 로그 출력을 막기 위해 별도 로직을 둘 수 있으나,
            # 현재는 모든 진행 상황을 실시간으로 전달합니다.
            pass 
            # (GUI에서는 update_progress 슬롯에서 처리하므로 여기서는 텍스트 출력 생략 가능)
            
        elif d['status'] == 'finished':
            # 파일 하나(영상 본체 등)의 다운로드가 끝났을 때
            if self.log_callback:
                self.log_callback("다운로드 완료. 변환(Convert) 및 아카이빙 후처리 중...")

    def download(self, url: str, output_path: str, options: dict):
        """
        yt-dlp를 사용하여 동영상 및 관련 데이터를 다운로드/아카이빙합니다.
        
        Args:
            url (str): 다운로드할 대상 URL (영상, 재생목록, 채널 등)
            output_path (str): 파일을 저장할 디렉토리 경로
            options (dict): 사용자가 설정한 옵션 딕셔너리
                - archive_mode (bool): 전체 아카이빙 모드 여부
                - only_audio (bool): 오디오 전용 모드 여부
                - sleep_interval (int): 다운로드 간 휴식 시간 (안티 밴)
                - cookies_from_browser (str): 쿠키를 가져올 브라우저명
                ... (기타 상세 옵션)

        Returns:
            bool: 작업 성공 여부 (True: 성공, False: 실패)
        """
        
        # 1. 파일 이름 및 폴더 구조 템플릿 설정
        # 기본: [업로더명] / [날짜 - 제목] / [제목.확장자]
        out_tmpl = os.path.join(output_path, '%(uploader)s/%(upload_date)s - %(title)s/%(title)s.%(ext)s')
        
        # 'flat_output' 옵션 시: 구조 없이 파일명만 유지
        if options.get('flat_output', False):
            out_tmpl = os.path.join(output_path, '%(title)s.%(ext)s')

        # 2. yt-dlp 옵션 구성 (YoutubeDL 객체에 전달할 인자들)
        ydl_opts = {
            'progress_hooks': [self._progress_hook], # 진행률 콜백 등록
            'outtmpl': out_tmpl,                     # 출력 경로 템플릿
            
            # --- 아카이빙 및 메타데이터 관련 ---
            # archive_mode가 True면 개별 옵션이 꺼져 있어도 강제로 켭니다.
            'writedescription': options.get('write_description', False) or options.get('archive_mode', False),
            'writeinfojson': options.get('write_info_json', False) or options.get('archive_mode', False),
            'writesubtitles': options.get('write_subs', False) or options.get('archive_mode', False),
            'getcomments': options.get('get_comments', False) or options.get('archive_mode', False),
            'writeautomaticcaption': options.get('write_auto_subs', False) or options.get('archive_mode', False),
            'writethumbnail': options.get('write_thumbnail', False) or options.get('archive_mode', False),
            
            # --- 후처리 및 포맷 관련 ---
            'postprocessors': [],
            
            # --- 안전 및 우회(Anti-Ban) 관련 ---
            'sleep_interval': options.get('sleep_interval', 0),         # 고정 휴식 시간
            'max_sleep_interval': options.get('max_sleep_interval', 0), # 랜덤 최대 휴식 시간
            'sleep_interval_requests': options.get('sleep_requests', 0), # 요청 간 휴식
            'ignoreerrors': options.get('ignore_errors', True),          # 에러 발생 시(비공개 영상 등) 멈추지 않고 건너뜀
            'no_clean_info_json': True,  # JSON 파일을 한 줄이 아닌, 들여쓰기 된 형태로 저장 (가독성 향상)
        }

        # 3. 포맷(화질/음질) 설정
        if options.get('only_audio', False):
            # 오디오 전용 모드: 최고의 오디오 품질 선택
            ydl_opts['format'] = 'bestaudio/best'
            # 후처리기: 다운받은 오디오를 MP3로 변환
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            })
        else:
            # 일반 비디오 모드: 최고 화질 비디오 + 최고 음질 오디오
            ydl_opts['format'] = options.get('format', 'bestvideo+bestaudio/best')
            # 호환성을 위해 mp4 컨테이너로 병합
            ydl_opts['merge_output_format'] = 'mp4'

        # 4. 플레이리스트 제어
        # 특정 범위(예: 1-10)만 다운로드할 경우
        if options.get('playlist_items'):
            ydl_opts['playlist_items'] = options.get('playlist_items')
        
        # 단일 영상 모드인 경우 (플레이리스트 URL이어도 하나만)
        if not options.get('use_playlist', True):
            ydl_opts['noplaylist'] = True

        # 5. 자막 변환 (SRT 권장)
        # VTT 등 다양한 포맷의 자막을 가장 호환성 좋은 SRT로 변환합니다.
        if ydl_opts['writesubtitles'] or ydl_opts['writeautomaticcaption']:
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegSubtitlesConvertor',
                'format': 'srt',
            })

        # 6. 쿠키 (브라우저 연동)
        # 인스타그램, 성인인증 영상 등을 위해 브라우저 쿠키를 빌려옵니다.
        if options.get('cookies_from_browser'):
            ydl_opts['cookiesfrombrowser'] = (options.get('cookies_from_browser'),)

        # 7. 영상 파일 생략 모드 (메타데이터만 수집 시)
        if options.get('skip_download', False):
            ydl_opts['skip_download'] = True

        # --- 실행 ---
        if self.log_callback:
            self.log_callback(f"작업 시작 (Sleekes Engine): {url}")

        try:
            # yt_dlp 라이브러리 실행 (Context Manager 사용)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            if self.log_callback:
                self.log_callback("모든 작업이 영구 보존용으로 아카이빙되었습니다.")
            return True
            
        except Exception as e:
            # 예외 처리: 다운로드 중 발생한 에러를 로그로 남기고 실패 처리
            if self.log_callback:
                self.log_callback(f"솔루션 실행 중 오류 발생: {str(e)}")
            return False

    def get_info(self, url: str):
        """
        다운로드 없이 영상의 정보(제목, 길이 등)만 미리 가져옵니다.
        
        Args:
            url (str): 대상 URL
            
        Returns:
            dict: 영상 정보 딕셔너리 (실패 시 None)
        """
        ydl_opts = {}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            if self.log_callback:
                self.log_callback(f"정보 추출 중 오류: {str(e)}")
            return None
