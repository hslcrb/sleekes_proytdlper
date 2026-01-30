from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTextBrowser, QTextEdit, 
                             QPushButton, QFileDialog, QHBoxLayout, QLabel, 
                             QStackedWidget, QRadioButton, QButtonGroup, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor, QDesktopServices
import json
import os
import re
import html

class JsonHighlighter(QSyntaxHighlighter):
    """JSON 구문 강조기 (Achromatic Source Mode)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rules = []

        # Key (Bold White/Black)
        key_fmt = QTextCharFormat()
        key_fmt.setForeground(QColor("#ffffff")) 
        key_fmt.setFontWeight(QFont.Bold)
        self.rules.append((re.compile(r'"[^"]*"\s*:'), key_fmt))

        # String (Gray)
        str_fmt = QTextCharFormat()
        str_fmt.setForeground(QColor("#aaaaaa")) 
        self.rules.append((re.compile(r':\s*"[^"]*"'), str_fmt))

        # Number (White)
        num_fmt = QTextCharFormat()
        num_fmt.setForeground(QColor("#ffffff")) 
        self.rules.append((re.compile(r'\b[0-9]+(\.[0-9]+)?\b'), num_fmt))

        # Bool/Null (Bold Gray)
        kwd_fmt = QTextCharFormat()
        kwd_fmt.setForeground(QColor("#888888"))
        kwd_fmt.setFontWeight(QFont.Bold)
        self.rules.append((re.compile(r'\b(true|false|null)\b'), kwd_fmt))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            for match in pattern.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), fmt)

class JsonViewerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_file_path = None
        self.current_data = None
        self.current_lang = "EN"
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # --- 1. Top Control Bar ---
        ctrl_layout = QHBoxLayout()
        
        self.btn_load = QPushButton("Open File")
        self.btn_load.setObjectName("SecondaryButton")
        self.btn_load.clicked.connect(self.load_file)
        ctrl_layout.addWidget(self.btn_load)
        
        self.mode_group = QButtonGroup(self)
        self.rb_render = QRadioButton("REPORTS")
        self.rb_source = QRadioButton("SOURCE")
        
        # Style Radio Buttons (Achromatic)
        rb_style = """
            QRadioButton { color: #888888; font-weight: bold; font-size: 11px; }
            QRadioButton::indicator:checked { background-color: #ffffff; border: 1px solid #ffffff; }
            QRadioButton::indicator:unchecked { border: 1px solid #444444; background: transparent; }
        """
        for rb in [self.rb_render, self.rb_source]:
            rb.setStyleSheet(rb_style)
            self.mode_group.addButton(rb)
        
        self.rb_render.setChecked(True)
        self.mode_group.buttonToggled.connect(self.switch_view)
        
        ctrl_layout.addSpacing(20)
        ctrl_layout.addWidget(self.rb_render)
        ctrl_layout.addWidget(self.rb_source)
        ctrl_layout.addStretch()
        
        layout.addLayout(ctrl_layout)

        self.lbl_status = QLabel("Open a .json or .description file to view metadata.")
        self.lbl_status.setStyleSheet("color: #666666; font-size: 11px;")
        layout.addWidget(self.lbl_status)

        # --- 2. Main View Area ---
        self.stack = QStackedWidget()
        
        self.browser = QTextBrowser()
        self.browser.setObjectName("LogArea")
        self.browser.setOpenExternalLinks(True)
        self.stack.addWidget(self.browser)
        
        self.editor = QTextEdit()
        self.editor.setObjectName("MetadataView")
        self.editor.setReadOnly(True)
        self.editor.setFont(QFont("Consolas", 11))
        self.highlighter = JsonHighlighter(self.editor.document())
        self.stack.addWidget(self.editor)
        
        layout.addWidget(self.stack)

    def update_language(self, lang_code):
        """다국어 지원 레이블 업데이트"""
        self.current_lang = lang_code
        if lang_code == "KO":
            self.btn_load.setText("파일 열기")
            self.rb_render.setText("보고서 형태")
            self.rb_source.setText("소스 코드")
            if not self.current_file_path:
                self.lbl_status.setText("메타데이터(.json) 또는 설명(.description) 파일을 열어보세요.")
        else:
            self.btn_load.setText("Open File")
            self.rb_render.setText("REPORTS")
            self.rb_source.setText("SOURCE")
            if not self.current_file_path:
                self.lbl_status.setText("Open a .json or .description file to view metadata.")

    def load_file(self):
        title = "Select File" if self.current_lang == "EN" else "파일 선택"
        fname, _ = QFileDialog.getOpenFileName(
            self, title, "", 
            "Supported Files (*.json *.description *.txt);;All Files (*)"
        )
        if not fname: return

        self.current_file_path = fname
        status_prefix = "File: " if self.current_lang == "EN" else "파일: "
        self.lbl_status.setText(f"{status_prefix}{os.path.basename(fname)}")
        
        try:
            with open(fname, 'r', encoding='utf-8') as f:
                content = f.read()
            
            is_json = False
            try:
                self.current_data = json.loads(content)
                is_json = True
                source_text = json.dumps(self.current_data, indent=4, ensure_ascii=False)
            except:
                self.current_data = content
                source_text = content
            
            self.editor.setPlainText(source_text)
            
            if is_json:
                html_content = self.render_json_to_html(self.current_data)
            else:
                html_content = self.render_text_to_html(content)
                
            self.browser.setHtml(html_content)
        except Exception as e:
            err_prefix = "Error: " if self.current_lang == "EN" else "오류: "
            self.lbl_status.setText(f"{err_prefix}{str(e)}")

    def switch_view(self, rb):
        self.stack.setCurrentIndex(0) if self.rb_render.isChecked() else self.stack.setCurrentIndex(1)

    def render_text_to_html(self, text):
        safe_text = html.escape(text).replace('\n', '<br>')
        title = "DESCRIPTION" if self.current_lang == "EN" else "상세 설명"
        return f"""
        <style>
            body {{ color: #ffffff; background-color: #000000; font-family: sans-serif; line-height: 1.6; padding: 20px; }}
            .box {{ border: 1px solid #333333; padding: 15px; border-radius: 4px; }}
        </style>
        <h3>{title}</h3>
        <div class="box">{safe_text}</div>
        """

    def render_json_to_html(self, data):
        if not isinstance(data, dict): return self.render_text_to_html(str(data))
        
        title = data.get('title', 'Untitled or Missing')
        uploader = data.get('uploader', 'Unknown')
        
        comments_title = "COMMENTS" if self.current_lang == "EN" else "댓글"
        uploader_label = "Uploader" if self.current_lang == "EN" else "게시자"
        
        comments_html = ""
        if 'comments' in data and isinstance(data['comments'], list):
            comments_html += f"<h3>{comments_title}</h3>"
            for c in data['comments'][:100]: # Show top 100
                author = html.escape(c.get('author', 'Anonymous'))
                text = html.escape(c.get('text', '')).replace('\n', '<br>')
                comments_html += f"""
                <div style="border-bottom: 1px solid #222; padding: 10px 0;">
                    <b style="color: #fff;">{author}</b><br>
                    <span style="color: #888;">{text}</span>
                </div>
                """

        return f"""
        <style>
            body {{ color: #ffffff; background-color: #000000; font-family: sans-serif; line-height: 1.5; padding: 20px; }}
            h1 {{ border-bottom: 2px solid #ffffff; padding-bottom: 10px; font-size: 24px; }}
            .meta {{ color: #888; font-size: 12px; margin-bottom: 20px; }}
            .box {{ border: 1px solid #333; padding: 15px; margin-bottom: 20px; }}
        </style>
        <h1>{html.escape(title)}</h1>
        <div class="meta">{uploader_label}: {uploader}</div>
        <div class="box">{html.escape(data.get('description', '')[:1000]).replace('\n', '<br>')}...</div>
        {comments_html}
        """
