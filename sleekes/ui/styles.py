# --- Achromatic Design System for Sleekes ---

# 다크 모드 (무채색)
STYLE_DARK = """
QMainWindow {
    background-color: #000000;
}

QWidget {
    color: #ffffff;
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
}

#MainFrame {
    background-color: #111111;
    border: 1px solid #333333;
    border-radius: 12px;
}

QLabel#TitleLabel {
    font-size: 32px;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: 1px;
}

QLineEdit {
    background-color: #222222;
    border: 1px solid #444444;
    border-radius: 6px;
    padding: 10px;
    font-size: 14px;
    color: #ffffff;
}

QLineEdit:focus {
    border: 1px solid #ffffff;
}

QPushButton#PrimaryButton {
    background-color: #ffffff;
    color: #000000;
    border-radius: 6px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    border: none;
}

QPushButton#PrimaryButton:hover {
    background-color: #cccccc;
}

QPushButton#SecondaryButton {
    background-color: transparent;
    border: 1px solid #444444;
    color: #aaaaaa;
    border-radius: 6px;
    padding: 6px 12px;
}

QPushButton#SecondaryButton:hover {
    background-color: #222222;
    color: #ffffff;
    border: 1px solid #ffffff;
}

QComboBox {
    background-color: #222222;
    border: 1px solid #444444;
    border-radius: 6px;
    padding: 5px;
    color: #ffffff;
}

QTabWidget::pane {
    border: 1px solid #333333;
    background: transparent;
}

QTabBar::tab {
    background: #222222;
    color: #888888;
    padding: 10px 15px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background: #333333;
    color: #ffffff;
    font-weight: bold;
}

QTextEdit#LogArea, QTextBrowser#GuideArea {
    background-color: #050505;
    border: 1px solid #222222;
    border-radius: 8px;
    font-family: 'Consolas', monospace;
    color: #cccccc;
}

QCheckBox {
    spacing: 10px;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border: 1px solid #444444;
    border-radius: 4px;
    background-color: #111111;
}

QCheckBox::indicator:checked {
    background-color: #ffffff;
    border: 1px solid #ffffff;
}
"""

# 라이트 모드 (무채색)
STYLE_LIGHT = """
QMainWindow {
    background-color: #f5f5f5;
}

QWidget {
    color: #000000;
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
}

#MainFrame {
    background-color: #ffffff;
    border: 1px solid #dddddd;
    border-radius: 12px;
}

QLabel#TitleLabel {
    font-size: 32px;
    font-weight: 900;
    color: #000000;
    letter-spacing: 1px;
}

QLineEdit {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 6px;
    padding: 10px;
    font-size: 14px;
    color: #000000;
}

QLineEdit:focus {
    border: 1px solid #000000;
}

QPushButton#PrimaryButton {
    background-color: #000000;
    color: #ffffff;
    border-radius: 6px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    border: none;
}

QPushButton#PrimaryButton:hover {
    background-color: #333333;
}

QPushButton#SecondaryButton {
    background-color: transparent;
    border: 1px solid #cccccc;
    color: #666666;
    border-radius: 6px;
    padding: 6px 12px;
}

QPushButton#SecondaryButton:hover {
    background-color: #f0f0f0;
    color: #000000;
    border: 1px solid #000000;
}

QComboBox {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 6px;
    padding: 5px;
    color: #000000;
}

QTabWidget::pane {
    border: 1px solid #dddddd;
    background: transparent;
}

QTabBar::tab {
    background: #eeeeee;
    color: #999999;
    padding: 10px 15px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background: #ffffff;
    color: #000000;
    font-weight: bold;
}

QTextEdit#LogArea, QTextBrowser#GuideArea {
    background-color: #ffffff;
    border: 1px solid #dddddd;
    border-radius: 8px;
    font-family: 'Consolas', monospace;
    color: #333333;
}

QCheckBox {
    spacing: 10px;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border: 1px solid #cccccc;
    border-radius: 4px;
    background-color: #ffffff;
}

QCheckBox::indicator:checked {
    background-color: #000000;
    border: 1px solid #000000;
}
"""
