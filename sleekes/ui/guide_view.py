from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

# =============================================================================
# [Sleekes Guide View]
# 
# 이 모듈은 사용자에게 사용법 가이드와 팁을 제공하는 HTML 기반 뷰어입니다.
# GUI 탭 내에서 웹 브라우저처럼 도움말을 랜더링합니다.
# =============================================================================

GUIDE_CONTENT = """
<style>
    body { color: #e2e8f0; font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif; line-height: 1.6; }
    h1 { color: #38bdf8; border-bottom: 2px solid #38bdf8; padding-bottom: 5px; margin-top: 30px; }
    h2 { color: #7dd3fc; margin-top: 25px; border-left: 4px solid #0ea5e9; padding-left: 10px; }
    h3 { color: #bae6fd; margin-top: 15px; }
    ul { margin-left: -20px; }
    li { margin-bottom: 8px; }
    .highlight { color: #f472b6; font-weight: bold; }
    .code { background-color: #1e293b; padding: 3px 6px; border-radius: 4px; font-family: 'Consolas', monospace; color: #a5f3fc; border: 1px solid #334155; }
    .box { background-color: rgba(30, 41, 59, 0.5); padding: 15px; border-radius: 8px; border: 1px solid #1e293b; }
    a { color: #38bdf8; text-decoration: none; font-weight: bold; }
</style>

<div style="text-align: center; margin-bottom: 20px;">
    <h1 style="border: none; font-size: 32px; color: #38bdf8;">Sleekes Pro Guide</h1>
    <p style="color: #94a3b8;">Potent. Pure. Permanent.<br>가장 완벽한 디지털 아카이빙 솔루션</p>
</div>

<div class="box">
    <h2>🧩 지원 플랫폼 (글로벌 통합)</h2>
    <p>Sleekes는 유튜브 하나에 국한되지 않습니다. 전 세계 수천 개의 사이트를 지원합니다.</p>
    <ul>
        <li><b>YouTube</b>: 영상, Shorts, 재생목록, 믹스, 채널 전체, 커뮤니티, 자막, 댓글</li>
        <li><b>Instagram</b>: Reels(릴스), IGTV, 스토리, 게시물 (쿠키 연동 필요)</li>
        <li><b>TikTok</b>: 워터마크가 제거된 원본 퀄리티 추출</li>
        <li><b>Streaming</b>: Twitch(VOD/Clip), Chzzk(치지직), AfreecaTV</li>
        <li><b>Etc</b>: Facebook, Twitter(X), Vimeo, Naver TV, Kakao TV 등</li>
    </ul>
</div>

<h1>🚀 주요 기능 및 활용 팁</h1>

<h3>1. 나만의 도서관 구축 (아카이빙 모드)</h3>
<p>
    Sleekes의 핵심 기능입니다. <span class="highlight">전체 아카이빙 모드</span>를 체크하면 영상뿐만 아니라
    <span class="code">설명, 메타데이터(JSON), 자막파일, 고화질 썸네일, 전체 댓글</span>을 모두 수집합니다.<br>
    이렇게 수집된 데이터는 나중에 검색이나 분석 용도로 활용할 수 있어 진정한 '디지털 도서관'이 됩니다.
</p>

<h3>2. IP 차단 방지 (Safe Archiving)</h3>
<p>
    채널 전체를 받을 때는 <span class="highlight">휴식 시간(Sleep)</span>을 <b>5초~10초</b>로 설정하세요.<br>
    Sleekes가 영상 사이사이에 사람처럼 쉬는 시간을 가져 유튜브의 기계적 접근 차단(429 Error)을 완벽히 방지합니다.
</p>

<h3>3. 로그인 전용 영상 (Cookies)</h3>
<p>
    "로그인이 필요합니다"라는 메시지가 뜨나요? <br>
    Chrome이나 Edge 브라우저로 해당 사이트에 로그인한 뒤, 
    <b>설정 > 쿠키 연동</b>에서 해당 브라우저를 선택하면 마법처럼 다운로드가 가능해집니다.<br>
    (인스타그램, 성인 인증 영상, 비공개 영상 등에 필수)
</p>

<h3>4. 오디오 & 데이터 모드</h3>
<ul>
    <li><b>오디오 모드</b>: 강연이나 음악 믹스 등 영상이 불필요할 때 최고 음질 <span class="code">MP3</span>로 추출합니다.</li>
    <li><b>데이터 모드</b>: 영상 용량이 부담되고 댓글/설명만 필요할 때 <span class="code">데이터만 수집</span>을 켜세요.</li>
</ul>

<br>
<hr>

<h1>💻 CLI (터미널) 사용법</h1>
<p>GUI와 동일한 강력한 기능을 터미널에서도 사용할 수 있습니다. 서버 환경이나 자동화에 적합합니다.</p>

<div class="box">
    <h3>기본 명령어</h3>
    <span class="code">python main.py [URL] [옵션]</span>
    <br><br>
    
    <h3>자주 쓰는 명령 예시</h3>
    
    <b>1. 권장 설정으로 안전하게 받기 (BEST)</b><br>
    <span class="code">python main.py https://youtu.be/... --rec</span>
    <br><br>
    
    <b>2. 오디오만 추출하기</b><br>
    <span class="code">python main.py https://youtu.be/... -x</span>
    <br><br>
    
    <b>3. 채널 전체 안전하게 받기 (5초 휴식)</b><br>
    <span class="code">python main.py [채널URL] --archive --sleep 5</span>
    <br><br>
    
    <b>4. 도움말 보기</b><br>
    <span class="code">python main.py help</span>
</div>

<p style="text-align: right; color: #64748b; margin-top: 30px;">
    <i>Designed by Antigravity for Archivists.</i>
</p>
"""

class GuideViewWidget(QWidget):
    """
    HTML 가이드 콘텐츠를 표시하는 위젯 클래스입니다.
    외부 링크 클릭 시 시스템 기본 브라우저를 엽니다.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True) # 링크 클릭 허용
        self.browser.setObjectName("GuideArea")
        self.browser.setHtml(GUIDE_CONTENT)
        
        layout.addWidget(self.browser)
