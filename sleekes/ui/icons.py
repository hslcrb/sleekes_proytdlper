from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QByteArray, QSize, Qt

def svg_to_icon(svg_str, color="#ffffff", size=QSize(24, 24)):
    """SVG 문자열을 QIcon으로 변환합니다."""
    # 색상 적용 (단순 문자열 치환)
    svg_colored = svg_str.replace('currentColor', color)
    
    renderer = QSvgRenderer(QByteArray(svg_colored.encode('utf-8')))
    pixmap = QPixmap(size)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    
    return QIcon(pixmap)

# --- SVG Icon Definitions (Achromatic Design) ---

# 📂 다운로드 센터 (Folder)
ICON_DOWNLOAD_CENTER = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M3 7V17C3 18.1046 3.89543 19 5 19H19C20.1046 19 21 18.1046 21 17V9C21 7.89543 20.1046 7 19 7H11L9 5H5C3.89543 5 3 5.89543 3 7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

# 📊 메타데이터 뷰어 (Chart/List)
ICON_METADATA_VIEWER = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M9 17L9 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M12 17L12 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M15 17L15 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="3" y="4" width="18" height="16" rx="2" stroke="currentColor" stroke-width="2"/>
</svg>
"""

# 📘 가이드 (Book)
ICON_GUIDE = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M4 19.5C4 18.837 4.26339 18.2011 4.73223 17.7322C5.20107 17.2634 5.83696 17 6.5 17H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M6.5 2H20V22H6.5C5.83696 22 5.20107 21.7366 4.73223 21.2678C4.26339 20.7989 4 20.163 4 19.5V4.5C4 3.83696 4.26339 3.20107 4.73223 2.73223C5.20107 2.26339 5.83696 2 6.5 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

# ✨ 권장 설정 (Sparkle)
ICON_RECOMMENDED = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 3L14.5 9L21 12L14.5 15L12 21L9.5 15L3 12L9.5 9L12 3Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

# ✅ 완료 (Check)
ICON_SUCCESS = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M22 11.08V12C21.9988 14.1564 21.3005 16.2547 20.0093 17.9818C18.7182 19.709 16.9033 20.9725 14.8354 21.5839C12.7674 22.1953 10.5573 22.1219 8.53447 21.3746C6.51168 20.6273 4.78465 19.2461 3.61096 17.4371C2.43727 15.628 1.87979 13.4881 2.02168 11.3363C2.16356 9.18455 2.99721 7.13631 4.39828 5.49706C5.79935 3.85782 7.69279 2.71537 9.79614 2.24013C11.8995 1.7649 14.1003 1.98234 16.07 2.85999" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M22 4L12 14.01L9 11.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

# ❌ 실패 (Error)
ICON_ERROR = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
    <path d="M15 9L9 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M9 9L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

# ⚠️ 경고 (Warning)
ICON_WARNING = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M10.29 3.86L1.82 18C1.64537 18.3024 1.55299 18.6452 1.55197 18.9939C1.55095 19.3427 1.64134 19.6858 1.81406 19.9883C1.98678 20.2908 2.23512 20.5422 2.5332 20.7171C2.83129 20.892 3.16853 20.9842 3.51 20.9842H20.49C20.8315 20.9842 21.1687 20.892 21.4668 20.7171C21.7649 20.5422 22.0132 20.2908 22.1859 19.9883C22.3587 19.6858 22.4491 19.3427 22.448 18.9939C22.447 18.6452 22.3546 18.3024 22.18 18L13.71 3.86C13.5317 3.56611 13.2807 3.32319 12.9812 3.15449C12.6817 2.98579 12.3438 2.89722 12 2.89722C11.6562 2.89722 11.3183 2.98579 11.0188 3.15449C10.7193 3.32319 10.4683 3.56611 10.29 3.86V3.86Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M12 9V13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M12 17H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

# 💡 아이디어/팁 (Idea)
ICON_IDEA = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M9 21H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M9 18H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M10 22V18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M14 22V18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M12 15C15.3137 15 18 12.3137 18 9C18 5.68629 15.3137 3 12 3C8.68629 3 6 5.68629 6 9C6 11.1732 7.15546 13.0762 8.87823 14.1568C9.18241 14.3479 9.38791 14.6565 9.45262 15L10 18H14L14.5474 15C14.6121 14.6565 14.8176 14.3479 15.1218 14.1568C16.8445 13.0762 18 11.1732 18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

# 🎨 디자인 (Design/Theme)
ICON_THEME = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2C6.47 2 2 6.47 2 12C2 17.53 6.47 22 12 22C17.53 22 22 17.53 22 12C22 11.2 21.8 10.4 21.43 9.7L18 3.5C17.61 2.8 16.9 2.45 16.14 2.45L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="7.5" cy="10.5" r="1.5" fill="currentColor"/>
    <circle cx="12" cy="7.5" r="1.5" fill="currentColor"/>
    <circle cx="16.5" cy="10.5" r="1.5" fill="currentColor"/>
</svg>
"""
