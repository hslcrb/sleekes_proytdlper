from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
from sleekes.ui import i18n

class GuideViewWidget(QWidget):
    """
    무채색 테마 및 다국어를 지원하는 가이드 뷰어 위젯입니다.
    """
    def __init__(self):
        super().__init__()
        self.current_lang = "EN"
        self.current_theme = "Dark"
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)
        self.browser.setObjectName("GuideArea")
        
        layout.addWidget(self.browser)

    def update_content(self, lang_code=None, theme_name=None):
        """언어와 테마를 조합하여 가이드 내용을 즉시 갱신합니다."""
        if lang_code: self.current_lang = lang_code
        if theme_name: self.current_theme = theme_name
        
        is_dark = (self.current_theme == "Dark")
        
        # 테마별 색상 정의
        colors = {
            "bg_color": "#050505" if is_dark else "#ffffff",
            "text_color": "#ffffff" if is_dark else "#000000",
            "sub_color": "#444" if is_dark else "#999",
            "box_bg": "#111" if is_dark else "#f9f9f9",
            "box_border": "#333" if is_dark else "#ddd",
            "content": i18n.TRANSLATIONS[self.current_lang]["content_html"]
        }
        
        html_content = i18n.GUIDE_TEMPLATE.format(**colors)
        self.browser.setHtml(html_content)

    def update_language(self, lang_code):
        self.update_content(lang_code=lang_code)
        
    def update_theme(self, theme_name):
        self.update_content(theme_name=theme_name)
