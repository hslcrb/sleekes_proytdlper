# Sleekes Internationalization (i18n) - Achromatic Translation System

# 가이드 HTML 템플릿 (테마별 색상 주입 가능)
GUIDE_TEMPLATE = """
<style>
    body {{ color: {text_color}; background-color: {bg_color}; font-family: 'Malgun Gothic', sans-serif; line-height: 1.6; padding: 20px; }}
    h1 {{ color: {text_color}; border-bottom: 2px solid {text_color}; padding-bottom: 5px; margin-top: 30px; font-size: 24px; }}
    h2 {{ color: {text_color}; margin-top: 25px; border-left: 4px solid {text_color}; padding-left: 10px; font-size: 20px; }}
    h3 {{ color: {text_color}; margin-top: 20px; font-size: 16px; font-weight: bold; }}
    .highlight {{ color: {text_color}; font-weight: bold; border-bottom: 1px dotted {text_color}; }}
    .code {{ background-color: {box_bg}; padding: 3px 6px; border-radius: 4px; font-family: monospace; color: {text_color}; border: 1px solid {box_border}; }}
    .box {{ border: 1px solid {box_border}; background-color: {box_bg}; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
    hr {{ border: 0; border-top: 1px solid {box_border}; margin: 30px 0; }}
    ul {{ margin-left: -15px; }}
    li {{ margin-bottom: 5px; }}
</style>
<div style="text-align: center; margin-bottom: 40px;">
    <h1 style="border: none; font-size: 36px; margin-bottom: 5px;">SLEEKES REFERENCE</h1>
    <p style="color: {sub_color}; font-weight: bold; letter-spacing: 2px;">POTENT . PURE . PERMANENT</p>
</div>
{content}
<p style="text-align: right; color: {sub_color}; margin-top: 50px; font-size: 11px;">
    <i>POTENT . PURE . PERMANENT | Achromatic build v1.0</i>
</p>
"""

EN_CONTENT = """
<div class="box">
    <h2>SUPPORTED PLATFORMS</h2>
    <p>Sleekes supports thousands of global streaming and social platforms.</p>
    <ul>
        <li><b>YouTube</b>: Videos, Shorts, Playlists, Channels, Community, Subs, Comments.</li>
        <li><b>Social</b>: Instagram (Reels/Posts), TikTok (No Watermark), Facebook, Twitter(X).</li>
        <li><b>Streaming</b>: Twitch (VOD/Clip), Chzzk, AfreecaTV.</li>
        <li><b>Others</b>: Vimeo, Naver TV, Kakao TV, etc.</li>
    </ul>
</div>
<h1>ENGINE ARCHITECTURE</h1>
<h3>1. COMPLETE ARCHIVING</h3>
<p>The core philosophy of Sleekes. When enabled, it secures not just the video but the entire digital heritage: <span class="code">Description, Metadata (JSON), Subtitles, High-Res Thumbnails, and Full Comment Trees</span>. This ensures data remains searchable and permanent.</p>
<h3>2. 403 FORBIDDEN PROTECTION</h3>
<p>To bypass aggressive IP blocks, Sleekes implements:
    <ul>
        <li><span class="highlight">Client Emulation</span>: Spoofs requests as Android/iOS mobile clients.</li>
        <li><span class="highlight">UA Rotation</span>: Cycles through 100+ real-world browser identities.</li>
        <li><span class="highlight">Stealth Mode</span>: Limits concurrent fragments and forces request delays.</li>
    </ul>
</p>
<h3>3. PRECISION SLEEP ENGINE</h3>
<p>Set <span class="highlight">Min/Max Sleep</span> in minutes. Sleekes will calculate a randomized delay for every request. For channel archiving, a range of <span class="code">5.0m to 30.0m</span> is recommended to remain undetected.</p>
<hr>
<h1>COMMAND LINE INTERFACE</h1>
<p>Pure power for server environments and automation.</p>
<div class="box">
    <span class="code">python main.py [URL] [OPTIONS]</span><br><br>
    <b>1. Recommended Stealth Mode (BEST)</b><br>
    <span class="code">python main.py [URL] --rec</span><br><br>
    <b>2. Safe Channel Archiving (5m Delay)</b><br>
    <span class="code">python main.py [URL] --archive --sleep 5</span>
</div>
"""

KO_CONTENT = """
<div class="box">
    <h2>지원 플랫폼</h2>
    <p>Sleekes는 전 세계 수천 개의 스트리밍 및 소셜 플랫폼을 지원합니다.</p>
    <ul>
        <li><b>YouTube</b>: 영상, 쇼츠, 재생목록, 채널 전체, 커뮤니티, 자막, 댓글.</li>
        <li><b>Social</b>: 인스타그램 (릴스/게시물), 틱톡 (워터마크 제거), 페이스북, 트위터(X).</li>
        <li><b>Streaming</b>: 트위치 (VOD/클립), 치지직, 아프리카TV.</li>
        <li><b>기타</b>: 비메오, 네이버TV, 카카오TV 등 수천여 사이트.</li>
    </ul>
</div>
<h1>엔진 아키텍처</h1>
<h3>1. 전체 아카이빙 (Full Archive)</h3>
<p>Sleekes의 핵심 철학입니다. 활성화 시 영상뿐만 아니라 모든 디지털 유산을 동시에 확보합니다: <span class="code">텍스트 설명, 상세 메타데이터(JSON), 자막파일, 고화질 썸네일, 전체 댓글 트리</span>. 이를 통해 영원히 검색 가능하고 보존 가능한 데이터를 구축합니다.</p>
<h3>2. 403 Forbidden 차단 완벽 방어</h3>
<p>유튜브의 강력한 IP 차단 로직을 회피하기 위해 다음 기술을 사용합니다:
    <ul>
        <li><span class="highlight">클라이언트 위장</span>: 요청을 안드로이드/iOS 모바일 앱 요청으로 변환합니다.</li>
        <li><span class="highlight">UA 로테이션</span>: 100여 개의 실제 브라우저 식별 정보를 무작위로 교체합니다.</li>
        <li><span class="highlight">스텔스 모드</span>: 동시 연결 수를 제한하고 요청 간 지연을 강제합니다.</li>
    </ul>
</p>
<h3>3. 정밀 휴식 엔진 (Sleep Engine)</h3>
<p><span class="highlight">최소/최대 휴식</span> 시간을 분 단위로 설정하세요. Sleekes는 매 요청 시마다 설정 범위 내에서 무작위 시간을 계산하여 쉽니다. 채널 아카이빙 시에는 <span class="code">5.0분 ~ 30.0분</span> 범위를 권장합니다.</p>
<hr>
<h1>CLI (터미널) 인터페이스</h1>
<p>서버 환경 및 자동화를 위한 강력한 터미널 명령어를 제공합니다.</p>
<div class="box">
    <span class="code">python main.py [URL] [옵션]</span><br><br>
    <b>1. 권장 스텔스 모드 (추천)</b><br>
    <span class="code">python main.py [URL] --rec</span><br><br>
    <b>2. 안전한 채널 아카이빙 (5분 지연)</b><br>
    <span class="code">python main.py [URL] --archive --sleep 5</span>
</div>
"""

TRANSLATIONS = {
    "EN": {
        "nav_downloader": "Downloader",
        "nav_metadata": "Metadata",
        "nav_guide": "Reference",
        "design_mode": "DESIGN MODE:",
        "lang_mode": "LANGUAGE:",
        "url_placeholder": "Paste video, playlist, or channel URL here...",
        "path_placeholder": "Select archiving directory...",
        "btn_browse": "Browse",
        "engine_group": "ENGINE CONFIGURATION",
        "opt_full_archive": "Complete Archiving",
        "opt_audio_only": "Extraction Only (MP3)",
        "opt_metadata_only": "Metadata Only",
        "opt_stealth": "Anti-Ban Stealth",
        "btn_rec": " Load Recommended",
        "detail_desc": "Desc",
        "detail_json": "JSON",
        "detail_subs": "Subs",
        "detail_thumb": "Thumb",
        "detail_comments": "Comments",
        "min_sleep": "MIN SLEEP(m):",
        "max_sleep": "MAX SLEEP(m):",
        "auth_cookies": "AUTH COOKIES:",
        "opt_flat": "Bypass Folder Structure",
        "btn_execute": "EXECUTE ARCHIVING",
        "log_ready_rec": "READY: Ultra-Stealth Channel Archiving Mode (5m~30m Random Sleep)",
        "msg_url_missing": "Enter a URL first.",
        "engine_start": "ENGINE START: Initializing secure stream for {url}",
        "success": "SYSTEM: All assets secured and archived successfully.",
        "fail": "SYSTEM: Task interrupted or failed. Check logs above.",
        "btn_guide": " Guide",
        "content_html": EN_CONTENT
    },
    "KO": {
        "nav_downloader": "다운로더",
        "nav_metadata": "메타데이터",
        "nav_guide": "레퍼런스",
        "design_mode": "디자인 모드:",
        "lang_mode": "언어 설정:",
        "url_placeholder": "영상, 재생목록, 채널 URL을 입력하세요...",
        "path_placeholder": "아카이빙 경로 선택...",
        "btn_browse": "폴더 선택",
        "engine_group": "엔진 구성 설정",
        "opt_full_archive": "전체 아카이빙",
        "opt_audio_only": "오디오 추출 (MP3)",
        "opt_metadata_only": "데이터만 수집",
        "opt_stealth": "차단방지 스텔스",
        "btn_rec": " 권장 설정 로드",
        "detail_desc": "설명",
        "detail_json": "정보",
        "detail_subs": "자막",
        "detail_thumb": "썸네일",
        "detail_comments": "댓글",
        "min_sleep": "최소 휴식(분):",
        "max_sleep": "최대 휴식(분):",
        "auth_cookies": "인증 쿠키:",
        "opt_flat": "폴더 트리 생략",
        "btn_execute": "아카이빙 시작",
        "log_ready_rec": "준비 완료: 초강력 스텔스 채널 보존 모드 (5분~30분 랜덤 휴식)",
        "msg_url_missing": "URL을 먼저 입력해주세요.",
        "engine_start": "엔진 기동: {url} 보안 스트림 초기화 중",
        "success": "시스템: 모든 에셋이 안전하게 아카이빙되었습니다.",
        "fail": "시스템: 작업이 중단되었거나 실패했습니다. 로그를 확인하세요.",
        "btn_guide": " 가이드",
        "content_html": KO_CONTENT
    }
}
