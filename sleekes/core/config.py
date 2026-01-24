import json
import os

# =============================================================================
# [Sleekes Configuration Manager]
# 
# 이 모듈은 애플리케이션의 사용자 설정(Settings)을 관리합니다.
# 설정을 JSON 파일로 저장하고 불러오며, 파일이 없을 경우 기본값을 생성합니다.
# =============================================================================

SETTINGS_DIR = "settings"
SETTINGS_FILE = os.path.join(SETTINGS_DIR, "config.json")

# 기본 설정값 정의 (최초 실행 시 사용됨)
DEFAULT_SETTINGS = {
    "archive_mode": True,       # 전체 아카이빙 모드 켜기
    "only_audio": False,        # 오디오 전용 끄기
    "skip_download": False,     # 영상 생략 끄기
    "sleep_interval": 5,        # 기본 휴식 시간 5초
    "max_sleep_interval": 10,   # 최대 랜덤 휴식 10초
    "cookie_browser": "None",   # 쿠키 브라우저 없음
    "flat_output": False,       # 폴더 구조 만들기
    "ignore_errors": True,      # 에러 무시하고 계속 진행
    "last_path": os.getcwd()    # 마지막 사용 경로는 현재 폴더
}

def load_settings():
    """
    설정 파일(config.json)을 읽어 딕셔너리로 반환합니다.
    파일이 없거나 손상된 경우 기본값(DEFAULT_SETTINGS)을 반환하고 파일을 새로 생성합니다.

    Returns:
        dict: 설정 딕셔너리
    """
    # 설정 폴더가 없으면 생성
    if not os.path.exists(SETTINGS_DIR):
        os.makedirs(SETTINGS_DIR)
    
    # 설정 파일이 없으면 기본값으로 생성 후 반환
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS
    
    # 파일 읽기 시도
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        # 읽기 실패 시(JSON 깨짐 등) 기본값 반환
        return DEFAULT_SETTINGS

def save_settings(settings):
    """
    주어진 설정 딕셔너리를 파일에 저장합니다.

    Args:
        settings (dict): 저장할 설정 데이터
    """
    if not os.path.exists(SETTINGS_DIR):
        os.makedirs(SETTINGS_DIR)
        
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        # indent=4로 저장하여 사람도 읽고 수정하기 편하게 함
        json.dump(settings, f, indent=4, ensure_ascii=False)
