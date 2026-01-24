import sys
import argparse
from sleekes.ui.main_window import SleekesMainWindow
from sleekes.cli.main import main as cli_main
from PySide6.QtWidgets import QApplication

def main():
    # 간단한 인자 체크로 CLI 모드 진입 여부 결정
    if len(sys.argv) > 1 and sys.argv[1] not in ["--gui", "-g"]:
        cli_main()
    else:
        app = QApplication(sys.argv)
        app.setApplicationName("Sleekes")
        window = SleekesMainWindow()
        window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()
