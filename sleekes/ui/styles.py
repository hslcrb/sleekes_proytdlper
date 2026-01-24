MAIN_STYLE = """
QMainWindow {
    background-color: #0f172a;
}

QWidget {
    color: #e2e8f0;
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
}

#MainFrame {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f172a, stop:0.5 #1e293b, stop:1 #0f172a);
    border-radius: 15px;
}

QLabel#TitleLabel {
    font-size: 36px;
    font-weight: 900;
    color: #38bdf8;
    margin-bottom: 5px;
    letter-spacing: 2px;
}

QLineEdit {
    background-color: rgba(30, 41, 59, 180);
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 12px;
    font-size: 14px;
    color: #f1f5f9;
}

QLineEdit:focus {
    border: 1px solid #38bdf8;
    background-color: rgba(30, 41, 59, 255);
}

QPushButton#PrimaryButton {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0ea5e9, stop:1 #2dd4bf);
    color: #ffffff;
    border-radius: 10px;
    padding: 15px 30px;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

QPushButton#PrimaryButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #38bdf8, stop:1 #5eead4);
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.5);
}


QPushButton#PrimaryButton:pressed {
    background-color: #0ea5e9;
}

QPushButton#SecondaryButton {
    background-color: transparent;
    border: 1px solid #475569;
    color: #94a3b8;
    border-radius: 8px;
    padding: 8px 16px;
}

QPushButton#SecondaryButton:hover {
    background-color: rgba(71, 85, 105, 50);
    color: #f1f5f9;
}

QCheckBox {
    spacing: 8px;
    font-size: 13px;
    color: #94a3b8;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #475569;
    border-radius: 4px;
}

QCheckBox::indicator:checked {
    background-color: #38bdf8;
    image: url(check.png); /* 실제로는 스타일로 더 복잡하게 할 수 있음 */
}

QTextEdit#LogArea {
    background-color: rgba(15, 23, 42, 220);
    border: 1px solid #1e293b;
    border-radius: 10px;
    font-family: 'Consolas', 'Cascadia Code', monospace;
    font-size: 12px;
    color: #94a3b8;
    padding: 10px;
}

QTabWidget::pane {
    border: 1px solid #1e293b;
    background: transparent;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}

QTabBar::tab {
    background: #1e293b;
    color: #94a3b8;
    padding: 10px 20px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    margin-right: 5px;
}

QTabBar::tab:selected {
    background: #38bdf8;
    color: #0f172a;
    font-weight: bold;
}

#GuideArea {
    background-color: rgba(15, 23, 42, 180);
    border-radius: 10px;
    padding: 20px;
}

#MetadataView {
    background-color: #020617;
    border: 1px solid #1e293b;
    border-radius: 8px;
    font-family: 'Consolas', monospace;
    color: #38bdf8;
}
"""
