from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTextBrowser, QTextEdit, 
                             QPushButton, QFileDialog, QHBoxLayout, QLabel, 
                             QStackedWidget, QRadioButton, QButtonGroup, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor, QDesktopServices
import json
import os
import re
import html

# =============================================================================
# [Sleekes Advanced Viewer]
# 
# 이 모듈은 JSON 메타데이터와 Description 파일을 위한 고급 뷰어입니다.
# 1. 렌더링 모드 (HTML): 데이터를 사람이 읽기 쉬운 보고서 형태로 변환
# 2. 소스 모드 (Raw): Syntax Highlighting이 적용된 원본 코드 뷰
# =============================================================================

class JsonHighlighter(QSyntaxHighlighter):
    """JSON 구문 강조기 (Source Mode용)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rules = []

        # Key
        key_fmt = QTextCharFormat()
        key_fmt.setForeground(QColor("#38bdf8")) # Sky Blue
        key_fmt.setFontWeight(QFont.Bold)
        self.rules.append((re.compile(r'"[^"]*"\s*:'), key_fmt))

        # String
        str_fmt = QTextCharFormat()
        str_fmt.setForeground(QColor("#a5f3fc")) # Light Blue
        self.rules.append((re.compile(r':\s*"[^"]*"'), str_fmt))

        # Number
        num_fmt = QTextCharFormat()
        num_fmt.setForeground(QColor("#f472b6")) # Pink
        self.rules.append((re.compile(r'\b[0-9]+(\.[0-9]+)?\b'), num_fmt))

        # Bool/Null
        kwd_fmt = QTextCharFormat()
        kwd_fmt.setForeground(QColor("#c084fc")) # Purple
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
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # --- 1. Top Control Bar ---
        ctrl_layout = QHBoxLayout()
        
        # Load Button
        self.btn_load = QPushButton("파일 열기 (.json / .description)")
        self.btn_load.setObjectName("SecondaryButton")
        self.btn_load.clicked.connect(self.load_file)
        self.btn_load.setCursor(Qt.PointingHandCursor)
        ctrl_layout.addWidget(self.btn_load)
        
        # View Mode Toggles
        self.mode_group = QButtonGroup(self)
        self.rb_render = QRadioButton("✨ 렌더링 보기")
        self.rb_source = QRadioButton("📝 소스 보기")
        
        # Style Radio Buttons
        for rb in [self.rb_render, self.rb_source]:
            rb.setStyleSheet("""
                QRadioButton { color: #94a3b8; font-weight: bold; }
                QRadioButton::indicator:checked { background-color: #38bdf8; border: 2px solid #38bdf8; border-radius: 6px; }
                QRadioButton::indicator:unchecked { border: 2px solid #475569; border-radius: 6px; background: transparent; }
            """)
            rb.setCursor(Qt.PointingHandCursor)
            self.mode_group.addButton(rb)
        
        self.rb_render.setChecked(True)
        self.mode_group.buttonToggled.connect(self.switch_view)
        
        ctrl_layout.addSpacing(20)
        ctrl_layout.addWidget(self.rb_render)
        ctrl_layout.addWidget(self.rb_source)
        ctrl_layout.addStretch()
        
        layout.addLayout(ctrl_layout)

        # File Info Label
        self.lbl_status = QLabel("파일을 열어 메타데이터를 확인하세요.")
        self.lbl_status.setStyleSheet("color: #64748b; font-size: 11px; margin-bottom: 5px;")
        layout.addWidget(self.lbl_status)

        # --- 2. Main View Area (Stacked) ---
        self.stack = QStackedWidget()
        
        # View 1: Rendered HTML Browser
        self.browser = QTextBrowser()
        self.browser.setObjectName("GuideArea") # Re-use guide style
        self.browser.setOpenExternalLinks(True)
        self.stack.addWidget(self.browser)
        
        # View 2: Source Code Editor
        self.editor = QTextEdit()
        self.editor.setObjectName("MetadataView") # Dark code style
        self.editor.setReadOnly(True)
        self.editor.setFont(QFont("Consolas", 11))
        self.highlighter = JsonHighlighter(self.editor.document())
        self.stack.addWidget(self.editor)
        
        layout.addWidget(self.stack)

    def load_file(self):
        """파일 열기 다이얼로그"""
        fname, _ = QFileDialog.getOpenFileName(
            self, "파일 선택", "", 
            "Supported Files (*.json *.description *.txt);;JSON Files (*.json);;All Files (*)"
        )
        
        if not fname:
            return

        self.current_file_path = fname
        self.lbl_status.setText(f"파일명: {os.path.basename(fname)} ({fname})")
        
        try:
            with open(fname, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 1. Parse Data
            is_json = False
            try:
                self.current_data = json.loads(content)
                is_json = True
                # 소스 뷰용 정형화
                source_text = json.dumps(self.current_data, indent=4, ensure_ascii=False)
            except:
                self.current_data = content
                source_text = content
            
            # 2. Set Source View
            self.editor.setPlainText(source_text)
            
            # 3. Render HTML View
            if is_json:
                html_content = self.render_json_to_html(self.current_data)
            else:
                html_content = self.render_text_to_html(content)
                
            self.browser.setHtml(html_content)
            
        except Exception as e:
            self.lbl_status.setText(f"오류 발생: {str(e)}")
            self.editor.setPlainText(f"Error reading file:\n{str(e)}")
            self.browser.setText(f"Error reading file:\n{str(e)}")

    def switch_view(self, rb):
        """보기 모드 전환"""
        if self.rb_render.isChecked():
            self.stack.setCurrentIndex(0)
        else:
            self.stack.setCurrentIndex(1)

    def render_text_to_html(self, text):
        """일반 텍스트(.description)를 HTML로 변환"""
        # HTML 이스케이프 및 줄바꿈 처리
        safe_text = html.escape(text).replace('\n', '<br>')
        # URL 자동 링크
        safe_text = re.sub(
            r'(https?://\S+)', 
            r'<a href="\1">\1</a>', 
            safe_text
        )
        
        return f"""
        <style>
            body {{ color: #e2e8f0; font-family: 'Malgun Gothic', sans-serif; line-height: 1.6; }}
            .content {{ background-color: rgba(30, 41, 59, 0.5); padding: 20px; border-radius: 8px; border: 1px solid #1e293b; }}
            a {{ color: #38bdf8; text-decoration: none; }}
        </style>
        <h2>📄 Description Viewer</h2>
        <div class="content">{safe_text}</div>
        """

    def render_json_to_html(self, data):
        """JSON 데이터를 분석하여 예쁜 HTML 리포트로 변환"""
        if not isinstance(data, dict):
            return self.render_text_to_html(str(data))

        # 주요 메타데이터 추출 (없으면 공란)
        title = data.get('title', 'Unknown Title')
        uploader = data.get('uploader', 'Unknown Uploader')
        upload_date = data.get('upload_date', '')
        # 날짜 포맷팅 (20240101 -> 2024-01-01)
        if len(upload_date) == 8:
            upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"
            
        view_count = f"{data.get('view_count', 0):,}"
        like_count = f"{data.get('like_count', 0):,}"
        desc = html.escape(data.get('description', 'No description provided.')).replace('\n', '<br>')
        desc = re.sub(r'(https?://\S+)', r'<a href="\1">\1</a>', desc)
        
        # 썸네일
        thumb_url = data.get('thumbnail', '')
        
        # 댓글 처리 (계층 구조 렌더링)
        comments_html = ""
        if 'comments' in data and isinstance(data['comments'], list):
            comments_list = data['comments']
            count = len(comments_list)
            
            # 1. 트리 구조 빌드
            # id를 키로 하는 맵 생성
            comment_map = {}
            children_map = {} # parent_id -> [child_comments...]
            root_comments = []

            for c in comments_list:
                c_id = c.get('id')
                if not c_id: continue
                comment_map[c_id] = c
                
                parent_id = c.get('parent')
                # parent가 없거나 'root'인 경우 최상위 댓글
                if not parent_id or parent_id == 'root':
                    root_comments.append(c)
                else:
                    if parent_id not in children_map:
                        children_map[parent_id] = []
                    children_map[parent_id].append(c)

            comments_html += f"<h3>💬 전체 댓글 ({count})</h3>"

            # 2. 재귀 렌더링 함수
            def render_comment_recursive(comment, depth=0):
                c_id = comment.get('id')
                author = html.escape(comment.get('author', 'Anonymous'))
                raw_text = comment.get('text', '')
                text = html.escape(raw_text).replace('\n', '<br>')
                
                # 스타일 계산
                margin_left = depth * 40
                if margin_left > 0: # 대댓글 스타일
                    box_style = f"margin-left: {margin_left}px; border-left: 3px solid #38bdf8; padding-left: 15px; background-color: rgba(56, 189, 248, 0.05);"
                    prefix = "↳ "
                else: # 최상위 댓글 스타일
                    box_style = "border-bottom: 1px solid #334155; padding-bottom: 10px;"
                    prefix = ""
                
                # 댓글 HTML 생성
                item_html = f"""
                <div style="margin-bottom: 15px; {box_style}">
                    <div style="font-size: 14px; margin-bottom: 4px;">
                        <span style="color: #94a3b8;">{prefix}</span>
                        <b style="color: #7dd3fc;">{author}</b>
                        <span style="color: #64748b; font-size: 12px; margin-left:10px;">({comment.get('like_count', 0)} likes)</span>
                    </div>
                    <span style="color: #e2e8f0; line-height: 1.5;">{text}</span>
                </div>
                """
                
                # 자식(대댓글)이 있다면 재귀 호출
                if c_id in children_map:
                    # 날짜순 정렬 등을 할 수도 있지만, 여기선 리스트 순서대로
                    for child in children_map[c_id]:
                        item_html += render_comment_recursive(child, depth + 1)
                
                return item_html

            # 3. 루트 댓글부터 순회하며 렌더링
            for root in root_comments:
                comments_html += render_comment_recursive(root)

            # 만약 댓글 구조가 트리형이 아니고 플랫한데 parent 정보가 없는 경우 (예: 구버전 데이터)
            if not root_comments and comments_list:
                 comments_html += "<p style='color: #fbbf24;'>⚠️ 계층 구조 정보를 찾을 수 없어 리스트로 표시합니다.</p>"
                 for c in comments_list:
                    author = html.escape(c.get('author', 'Anonymous'))
                    text = html.escape(c.get('text', '')).replace('\n', '<br>')
                    comments_html += f"""
                    <div style="margin-bottom: 15px; border-bottom: 1px solid #334155; padding-bottom: 10px;">
                        <b style="color: #7dd3fc;">{author}</b><br>
                        <span style="color: #cbd5e1;">{text}</span>
                    </div>
                    """

        return f"""
        <style>
            body {{ color: #e2e8f0; font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif; line-height: 1.6; }}
            h1 {{ color: #38bdf8; font-size: 26px; margin-bottom: 5px; border-bottom: 2px solid #38bdf8; padding-bottom: 10px; }}
            .meta {{ color: #94a3b8; font-size: 13px; margin-bottom: 20px; }}
            .box {{ background-color: rgba(30, 41, 59, 0.5); padding: 20px; border-radius: 8px; border: 1px solid #1e293b; margin-bottom: 30px; }}
            .label {{ color: #7dd3fc; font-weight: bold; margin-right: 5px; }}
            a {{ color: #38bdf8; text-decoration: none; font-weight: bold; }}
            a:hover {{ text-decoration: underline; }}
            hr {{ border: 0; border-top: 1px solid #334155; margin: 20px 0; }}
        </style>
        
        <h1>{html.escape(title)}</h1>
        <div class="meta">
            <span class="label">📅 업로드:</span> {upload_date} &nbsp;|&nbsp; 
            <span class="label">👤 게시자:</span> {uploader} &nbsp;|&nbsp; 
            <span class="label">👁️ 조회수:</span> {view_count} &nbsp;|&nbsp; 
            <span class="label">👍 좋아요:</span> {like_count}
        </div>

        <h3>📝 설명</h3>
        <div class="box">
            {desc}
        </div>

        {comments_html}
        """


