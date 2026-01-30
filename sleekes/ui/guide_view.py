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
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)
        self.browser.setObjectName("GuideArea")
        
        # 초기화 (기본값 EN)
        self.update_language("EN")
        
        layout.addWidget(self.browser)

    def update_language(self, lang_code):
        """언어 코드를 받아 가이드 내용을 즉시 갱신합니다."""
        if lang_code in i18n.TRANSLATIONS:
            html_content = i18n.TRANSLATIONS[lang_code]["guide_html"]
            self.browser.setHtml(html_content)
