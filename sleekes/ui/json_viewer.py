from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QFileDialog, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor
import json
import re

# =============================================================================
# [Sleekes JSON Viewer]
# 
# 이 모듈은 다운로드된 메타데이터 파일(.json)을 사용자에게 보기 좋게 표시하는
# 내장 뷰어 위젯입니다. Syntax Highlighting을 지원하여 가독성을 높였습니다.
# =============================================================================

class JsonHighlighter(QSyntaxHighlighter):
    """
    JSON 형식의 텍스트에 색상을 입히는 구문 강조기(Highlighter) 클래스입니다.
    Key, String Value, Number, Boolean/Null 등을 정규표현식으로 구분하여 색칠합니다.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.rules = []

        # 1. Key (String) - 예: "title":
        # 밝은 하늘색 (#38bdf8) + 굵게
        key_format = QTextCharFormat()
        key_format.setForeground(QColor("#38bdf8")) 
        key_format.setFontWeight(QFont.Bold)
        self.rules.append((re.compile(r'"[^"]*"\s*:'), key_format))

        # 2. String Value - 예: "Hello World"
        # 연한 파란색 (#a5f3fc)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#a5f3fc"))
        self.rules.append((re.compile(r':\s*"[^"]*"'), string_format))

        # 3. Number - 예: 123, 45.67
        # 분홍색 (#f472b6)
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#f472b6")) 
        self.rules.append((re.compile(r'\b[0-9]+(\.[0-9]+)?\b'), number_format))

        # 4. Keyword (Boolean / Null) - 예: true, false, null
        # 보라색 (#c084fc) + 굵게
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#c084fc")) 
        keyword_format.setFontWeight(QFont.Bold)
        self.rules.append((re.compile(r'\b(true|false|null)\b'), keyword_format))

    def highlightBlock(self, text):
        """
        QTextDocument가 텍스트 블록을 렌더링할 때 호출하여 서식을 적용합니다.
        """
        for pattern, format in self.rules:
            expression = pattern
            matches = expression.finditer(text)
            for match in matches:
                self.setFormat(match.start(), match.end() - match.start(), format)

class JsonViewerWidget(QWidget):
    """
    파일 열기 버튼과 하이라이팅된 텍스트 에디터를 포함한 뷰어 메인 위젯입니다.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # [상단 컨트롤 바]
        ctrl_layout = QHBoxLayout()
        self.btn_load = QPushButton("JSON 파일 열기 (.info.json 등)")
        self.btn_load.setObjectName("SecondaryButton")
        self.btn_load.clicked.connect(self.load_json)
        
        self.lbl_status = QLabel("파일을 열어 메타데이터를 확인하세요.")
        self.lbl_status.setStyleSheet("color: #94a3b8; font-style: italic;")

        ctrl_layout.addWidget(self.btn_load)
        ctrl_layout.addWidget(self.lbl_status)
        ctrl_layout.addStretch()
        
        layout.addLayout(ctrl_layout)

        # [메인 에디터 영역]
        self.editor = QTextEdit()
        self.editor.setObjectName("MetadataView")
        self.editor.setReadOnly(True) # 편집 불가능 (뷰어 전용)
        self.editor.setFont(QFont("Consolas", 12)) # 고정폭 글꼴 사용
        
        # 하이라이터 적용
        self.highlighter = JsonHighlighter(self.editor.document())
        
        layout.addWidget(self.editor)

    def load_json(self):
        """
        파일 다이얼로그를 열고 선택된 JSON 파일을 읽어 화면에 표시합니다.
        """
        fname, _ = QFileDialog.getOpenFileName(self, "JSON 파일 선택", "", "JSON Files (*.json);;All Files (*)")
        if fname:
            try:
                with open(fname, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # JSON을 사람이 읽기 좋은 형태(Pretty Print)로 변환
                text = json.dumps(data, indent=4, ensure_ascii=False)
                self.editor.setPlainText(text)
                self.lbl_status.setText(f"로드됨: {os.path.basename(fname)}")
            except Exception as e:
                self.editor.setPlainText(f"파일을 읽는 중 오류가 발생했습니다:\n{str(e)}")
