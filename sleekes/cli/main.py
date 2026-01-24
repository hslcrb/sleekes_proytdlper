import argparse
import os
import sys
import json
from sleekes.core.downloader import SleekesDownloader
from sleekes.core.config import load_settings, save_settings

# =============================================================================
# [Sleekes CLI 메인 모듈]
# 
# 이 모듈은 터미널(Command Line Interface) 환경에서 Sleekes를 실행하기 위한 진입점입니다.
# 사용자의 명령어를 해석(Parsing)하고, 설정(Config)을 로드하여,
# 핵심 다운로더 엔진(SleekesDownloader)을 구동하는 역할을 수행합니다.
#
# 주요 기능:
# 1. 명령어 인자 파싱 (argparse 사용)
# 2. 도움말 및 가이드 출력
# 3. 사용자 설정 로드 및 저장
# 4. JSON 뷰어 모드 실행
# 5. 다운로드 작업 실행 및 결과 리포트
# =============================================================================

def print_guide():
    """
    사용자에게 상세한 사용 가이드와 팁을 출력합니다.
    '--info' 옵션이나 'help' 명령어를 사용했을 때 호출됩니다.
    """
    print("""
================================================================
  Sleekes: Potent. Pure. Permanent. (CLI 상세 가이드)
================================================================

[소개]
Sleekes는 yt-dlp를 기반으로 한 강력한 동영상 아카이빙 솔루션입니다.
단순 다운로드를 넘어, 영상의 모든 메타데이터를 영구 보존합니다.

[기본 사용법]
  python main.py [URL] [옵션]

[주요 명령어 예시]

1. 권장 아카이빙 (가장 추천)
   설명, 자막, 댓글 등 모든 데이터를 포함하고, IP 차단을 막기 위해
   5초씩 쉬어가며 안전하게 다운로드합니다.
   $ python main.py https://youtu.be/... --rec

2. 오디오 추출 모드
   영상 없이 고음질 오디오(MP3)만 추출합니다. (음악, 강연 등)
   $ python main.py https://youtu.be/... -x

3. 쿠키 연동 다운로드
   연령 제한이나 비공개 영상을 브라우저 로그인 정보로 받습니다.
   $ python main.py https://youtu.be/... --cookies chrome

4. 플랫폼별 폴더 정리
   인스타, 유튜브 등 출처별로 폴더를 나누고 싶을 때 사용합니다.
   (기본적으로 되어있으나, 더 명확히 하려면)
   $ python main.py [URL]

[옵션 상세 설명]

  --rec          : 권장 설정 적용 (전체 아카이빙 + 5초 휴식)
  --save         : 현재 입력한 옵션(경로, 쿠키 등)을 기본값으로 저장
  --view [파일]  : .json 메타데이터 파일을 보기 좋게 출력
  --info         : 이 도움말 화면을 출력

  -a, --archive  : 전체 아카이빙 모드 (영상+모든 데이터)
  -x, --audio    : 오디오만 추출 (MP3 변환)
  --skip-video   : 영상 파일은 건너뛰고 댓글/정보만 수집
  --cookies [브라우저] : chrome, edge, firefox 등에서 쿠키 가져오기
  --sleep [초]   : 영상 다운로드 사이의 휴식 시간 (안티 밴)
  --playlist-items : 1-5, 10 등 특정 번호의 영상만 다운로드

================================================================
""")

def view_json(path):
    """
    JSON 파일을 사람이 읽기 편한 형태(Pretty Print)로 터미널에 출력합니다.
    
    Args:
        path (str): 읽을 JSON 파일의 경로
    """
    if not os.path.exists(path):
        print(f"[오류] 파일을 찾을 수 없습니다: {path}")
        return
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # indent=4를 사용하여 들여쓰기를 적용, 가독성을 높입니다.
        print(json.dumps(data, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"[오류] 파일을 읽는 중 문제가 발생했습니다: {str(e)}")

def main():
    """
    CLI 프로그램의 메인 실행 함수입니다.
    """
    
    # 1. 'help' 명령어 처리 (argparse 실행 전)
    # 사용자가 'python main.py help'라고 입력하면 즉시 가이드를 보여줍니다.
    if len(sys.argv) > 1 and sys.argv[1] == "help":
        print_guide()
        sys.exit(0)

    # 2. 사용자 설정 로드
    # 이전에 저장된 설정이 있다면 불러옵니다 (GUI와 설정 공유)
    settings = load_settings()

    # 3. 파서(Parser) 설정
    # 터미널에서 입력받을 명령어 옵션들을 정의합니다.
    parser = argparse.ArgumentParser(
        description="Sleekes: 초월적 범용 동영상 아카이빙 솔루션 (CLI)",
        epilog="팁: 'python main.py help'를 입력하면 상세 가이드를 볼 수 있습니다.",
        formatter_class=argparse.RawTextHelpFormatter # 줄바꿈 유지를 위해 사용
    )

    # URL 인자 (선택적)
    parser.add_argument("url", nargs="?", help="다운로드할 동영상/채널 URL (또는 뷰어용 파일 경로)")

    # [특수 모드 그룹]
    mode_group = parser.add_argument_group('특수 모드')
    mode_group.add_argument("--info", action="store_true", help="지원 플랫폼 및 상세 사용 가이드 출력")
    mode_group.add_argument("--view", action="store_true", help="JSON 파일 뷰어 모드 실행 (URL 자리에 파일 경로 입력)")
    mode_group.add_argument("--rec", action="store_true", help="✨ 권장 설정 적용 (전체 아카이빙 + 5초 휴식 + 안전 모드)")
    mode_group.add_argument("--save", action="store_true", help="현재 입력한 옵션을 다음 실행 시 기본값으로 저장")

    # [다운로드 옵션 그룹]
    dl_group = parser.add_argument_group('다운로드 옵션')
    dl_group.add_argument("-o", "--output", default=settings.get("last_path", "."), help="저장할 폴더 경로 (기본값: 마지막 사용 경로)")
    dl_group.add_argument("-a", "--archive", action="store_true", help="전체 아카이빙 모드 (영상 + 자막 + 댓글 + 설명 + 썸네일)")
    dl_group.add_argument("-x", "--audio", action="store_true", help="오디오 전용 모드 (영상 없이 MP3 추출)")
    dl_group.add_argument("--skip-video", action="store_true", help="영상 다운로드 제외 (메타데이터만 빠르게 수집)")
    
    # [상세 데이터 수집 옵션 그룹]
    meta_group = parser.add_argument_group('데이터 수집 상세 설정')
    meta_group.add_argument("--desc", action="store_true", help="영상 설명(.description) 저장")
    meta_group.add_argument("--json", action="store_true", help="메타데이터(.json) 저장")
    meta_group.add_argument("--subs", action="store_true", help="자막 파일 저장")
    meta_group.add_argument("--thumb", action="store_true", help="썸네일 이미지 저장")
    meta_group.add_argument("--comments", action="store_true", help="댓글 목록(.json) 저장")
    
    # [엔진 및 안전 설정 그룹]
    engine_group = parser.add_argument_group('엔진 및 안전 설정 (Anti-Ban)')
    engine_group.add_argument("--sleep", type=int, help="영상 다운로드 사이 휴식 시간 (초 단위, IP 차단 방지)")
    engine_group.add_argument("--max-sleep", type=int, default=0, help="최대 랜덤 휴식 시간 (설정 시 sleep~max 사이 랜덤 휴식)")
    engine_group.add_argument("--cookies", choices=['chrome', 'firefox', 'edge', 'safari'], help="브라우저 쿠키 연동 (비공개/성인인증 영상용)")
    engine_group.add_argument("--playlist-items", help="플레이리스트 다운로드 범위 지정 (예: 1-5, 10)")
    engine_group.add_argument("--no-playlist", action="store_true", help="플레이리스트 URL이라도 단일 영상만 다운로드")
    engine_group.add_argument("--flat", action="store_true", help="폴더 구조를 만들지 않고 파일만 저장")

    # 기본값 적용 (Config 내용 반영)
    # argparse의 set_defaults를 사용하여 저장된 설정을 기본값으로 주입합니다.
    defaults = {
        "archive": settings.get("archive_mode", False),
        "audio": settings.get("only_audio", False),
        "skip_video": settings.get("skip_download", False),
        "sleep": settings.get("sleep_interval", 0),
        "flat": settings.get("flat_output", False),
    }
    
    cookie_val = settings.get("cookie_browser", "None")
    if cookie_val and cookie_val != "None":
        defaults["cookies"] = cookie_val

    parser.set_defaults(**defaults)

    # 인자 파싱 수행
    args = parser.parse_args()

    # --- 실행 로직 분기 ---

    # 1. 가이드/정보 모드
    if args.info:
        print_guide()
        return

    # 2. JSON 뷰어 모드
    if args.view:
        if not args.url:
            print("[오류] --view 옵션 사용 시, 분석할 JSON 파일의 경로를 입력해 주세요.")
            print("예: python main.py video_info.json --view")
        else:
            view_json(args.url)
        return

    # 3. URL 유효성 확인
    if not args.url:
        parser.print_help() # URL이 없으면 기본 도움말 출력
        return

    # 4. 권장 설정(Rec) 적용
    # 사용자가 --rec를 켰으면 강제로 안전하고 추천하는 설정으로 덮어씁니다.
    if args.rec:
        args.archive = True
        args.sleep = 5
        args.audio = False
        args.skip_video = False
        print("✨ [권장 설정 적용] 전체 아카이빙 모드 및 5초 안전 휴식이 활성화되었습니다.")

    # 5. 설정 저장 (--save)
    # 현재 실행 옵션을 설정 파일에 영구 저장합니다.
    if args.save:
        new_settings = settings.copy()
        new_settings.update({
            "archive_mode": args.archive,
            "only_audio": args.audio,
            "skip_download": args.skip_video,
            "sleep_interval": args.sleep if args.sleep else 0,
            "cookie_browser": args.cookies if args.cookies else "None",
            "flat_output": args.flat,
            "last_path": args.output
        })
        save_settings(new_settings)
        print("💾 [설정 저장] 현재 옵션이 기본값으로 저장되었습니다.")

    # 6. 최종 옵션 딕셔너리 생성
    # Downloader 클래스에 전달할 통합 옵션 객체를 만듭니다.
    options = {
        'write_description': args.desc or args.archive,
        'write_info_json': args.json or args.archive,
        'write_subs': args.subs or args.archive,
        'write_auto_subs': args.subs or args.archive,
        'write_thumbnail': args.thumb or args.archive,
        'get_comments': args.comments or args.archive,
        'archive_mode': args.archive,
        'only_audio': args.audio,
        'skip_download': args.skip_video,
        'sleep_interval': args.sleep,
        'max_sleep_interval': args.max_sleep,
        'cookies_from_browser': args.cookies,
        'playlist_items': args.playlist_items,
        'use_playlist': not args.no_playlist,
        'flat_output': args.flat
    }

    # 7. 다운로더 엔진 구동 및 실행
    downloader = SleekesDownloader(log_callback=print)
    
    print(f"\n--- Sleekes Pro CLI 엔진 가동 ---")
    print(f"타겟 URL: {args.url}")
    print(f"저장 경로: {os.path.abspath(args.output)}")
    
    if args.cookies:
        print(f"쿠키 연동: {args.cookies} (로그인/성인인증 우회)")
    if args.sleep and args.sleep > 0:
        print(f"안티 밴: 요청 간 {args.sleep}초 휴식 활성화")

    print("-" * 40)
    
    # 실제 다운로드 수행
    success = downloader.download(args.url, args.output, options)
    
    # 결과 처리
    if success:
        print("\n[성공] 모든 아카이빙 작업이 완료되었습니다.")
    else:
        print("\n[실패] 작업 중 오류가 발생했습니다. 로그를 확인해 주세요.")

if __name__ == "__main__":
    main()
