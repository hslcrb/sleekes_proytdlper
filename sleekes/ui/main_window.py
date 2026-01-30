from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QLabel, QCheckBox, 
                             QTextEdit, QProgressBar, QFileDialog, QGroupBox, QTabWidget, QMessageBox, QComboBox)
from PySide6.QtCore import Qt, QThread, Signal, Slot, QSize
from PySide6.QtGui import QIcon, QFont, QAction
from sleekes.core.downloader import SleekesDownloader
from sleekes.core.config import load_settings, save_settings
from sleekes.ui import styles, icons
from sleekes.ui.json_viewer import JsonViewerWidget
from sleekes.ui.guide_view import GuideViewWidget
import os

# =============================================================================
# [Sleekes Download Management]
# =============================================================================

class DownloadThread(QThread):
    """백그라운드에서 yt-dlp 작업을 수행하는 스레드"""
    progress = Signal(dict)
    log = Signal(str)
    finished_signal = Signal(bool)

    def __init__(self, url, output_path, options):
        super().__init__()
        self.url = url
        self.output_path = output_path
        self.options = options

    def run(self):
        downloader = SleekesDownloader(
            progress_callback=self.progress.emit,
            log_callback=self.log.emit
        )
        success = downloader.download(self.url, self.output_path, self.options)
        self.finished_signal.emit(success)

class SleekesMainWindow(QMainWindow):
    """Sleekes 메인 윈도우 - 무채색 디자인(Design Mode) 지원"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SLEEKES - Potent Universal Archiver")
        self.setMinimumSize(1000, 850)
        
        self.settings = load_settings() 
        self.init_ui()
        self.load_settings_to_ui()
        
        # 테마 초기화
        initial_theme = self.settings.get("theme", "Dark")
        idx = self.theme_combo.findText(initial_theme)
        if idx >= 0:
            self.theme_combo.setCurrentIndex(idx)
        self.apply_theme(initial_theme)

    def init_ui(self):
        central_widget = QWidget()
        central_widget.setObjectName("MainFrame")
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        
        # --- [Header Area] ---
        header = QHBoxLayout()
        
        title_vbox = QVBoxLayout()
        title = QLabel("SLEEKES")
        title.setObjectName("TitleLabel")
        subtitle = QLabel("POTENT . PURE . PERMANENT")
        subtitle.setStyleSheet("color: #888888; letter-spacing: 5px; font-weight: bold; font-size: 10px; margin-top: -5px;")
        title_vbox.addWidget(title)
        title_vbox.addWidget(subtitle)
        header.addLayout(title_vbox)
        
        header.addStretch()
        
        # Design Mode Dropdown
        mode_layout = QHBoxLayout()
        mode_label = QLabel("DESIGN MODE:")
        mode_label.setStyleSheet("font-size: 11px; font-weight: bold; color: #888,888;")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.currentTextChanged.connect(self.apply_theme)
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.theme_combo)
        header.addLayout(mode_layout)
        
        header.addSpacing(20)
        
        self.guide_nav_btn = QPushButton(" Guide")
        self.guide_nav_btn.setObjectName("SecondaryButton")
        self.guide_nav_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(2))
        header.addWidget(self.guide_nav_btn)
        
        main_layout.addLayout(header)

        # --- [Tab System] ---
        self.tabs = QTabWidget()
        self.tab_downloader = self.create_downloader_tab()
        self.tab_metadata = JsonViewerWidget()
        self.tab_guide = GuideViewWidget()
        
        self.tabs.addTab(self.tab_downloader, "Downloader")
        self.tabs.addTab(self.tab_metadata, "Metadata")
        self.tabs.addTab(self.tab_guide, "Reference")
        
        main_layout.addWidget(self.tabs)

    def apply_theme(self, theme_name):
        """무채색 테마 즉시 전환 및 SVG 아이콘 동기화"""
        is_dark = (theme_name == "Dark")
        self.setStyleSheet(styles.STYLE_DARK if is_dark else styles.STYLE_LIGHT)
        
        icon_color = "#ffffff" if is_dark else "#000000"
        
        # Tab Icons
        self.tabs.setTabIcon(0, icons.svg_to_icon(icons.ICON_DOWNLOAD_CENTER, icon_color))
        self.tabs.setTabIcon(1, icons.svg_to_icon(icons.ICON_METADATA_VIEWER, icon_color))
        self.tabs.setTabIcon(2, icons.svg_to_icon(icons.ICON_GUIDE, icon_color))
        self.tabs.setIconSize(QSize(22, 22))
        
        # UI Button Icons
        self.rec_btn.setIcon(icons.svg_to_icon(icons.ICON_RECOMMENDED, icon_color))
        self.guide_nav_btn.setIcon(icons.svg_to_icon(icons.ICON_GUIDE, icon_color))
        
        # Save preference
        self.settings["theme"] = theme_name
        save_settings(self.settings)

    def create_downloader_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 25, 15, 15)
        layout.setSpacing(20)

        # 1. URL Input
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste video, playlist, or channel URL here...")
        self.url_input.setMinimumHeight(45)
        layout.addWidget(self.url_input)

        # 2. Path Selection
        path_box = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Select archiving directory...")
        path_btn = QPushButton("Browse")
        path_btn.setObjectName("SecondaryButton")
        path_btn.clicked.connect(self.select_path)
        path_box.addWidget(self.path_input)
        path_box.addWidget(path_btn)
        layout.addLayout(path_box)

        # 3. Engine Options
        opt_group = QGroupBox("ENGINE CONFIGURATION")
        opt_layout = QVBoxLayout()
        
        top_opts = QHBoxLayout()
        self.archive_mode_cb = QCheckBox("Complete Archiving")
        self.audio_mode_cb = QCheckBox("Extraction Only (MP3)")
        self.skip_download_cb = QCheckBox("Metadata Only")
        self.stealth_mode_cb = QCheckBox("Anti-Ban Stealth")
        
        self.rec_btn = QPushButton(" Load Recommended")
        self.rec_btn.setObjectName("SecondaryButton")
        self.rec_btn.clicked.connect(self.apply_recommended_settings)
        
        top_opts.addWidget(self.archive_mode_cb)
        top_opts.addWidget(self.audio_mode_cb)
        top_opts.addWidget(self.skip_download_cb)
        top_opts.addWidget(self.stealth_mode_cb)
        top_opts.addStretch()
        top_opts.addWidget(self.rec_btn)
        opt_layout.addLayout(top_opts)
        
        detail_opts = QHBoxLayout()
        self.desc_cb = QCheckBox("Desc")
        self.json_cb = QCheckBox("JSON")
        self.subs_cb = QCheckBox("Subs")
        self.thumb_cb = QCheckBox("Thumb")
        self.comments_cb = QCheckBox("Comments")
        for cb in [self.desc_cb, self.json_cb, self.subs_cb, self.thumb_cb, self.comments_cb]:
            detail_opts.addWidget(cb)
            cb.setEnabled(False)
        self.archive_mode_cb.toggled.connect(self.toggle_archive_options)
        opt_layout.addLayout(detail_opts)
        
        # Advanced/Sleep Settings
        ext_opts = QHBoxLayout()
        ext_opts.addWidget(QLabel("MIN SLEEP(m):"))
        self.sleep_input = QLineEdit()
        self.sleep_input.setMaximumWidth(70)
        ext_opts.addWidget(self.sleep_input)
        
        ext_opts.addSpacing(15)
        ext_opts.addWidget(QLabel("MAX SLEEP(m):"))
        self.max_sleep_input = QLineEdit()
        self.max_sleep_input.setMaximumWidth(70)
        self.max_sleep_input.setPlaceholderText("30.0")
        ext_opts.addWidget(self.max_sleep_input)
        
        ext_opts.addSpacing(15)
        ext_opts.addWidget(QLabel("AUTH COOKIES:"))
        self.cookie_browser = QComboBox()
        self.cookie_browser.addItems(["None", "chrome", "firefox", "edge", "safari"])
        ext_opts.addWidget(self.cookie_browser)
        
        self.flat_output_cb = QCheckBox("Bypass Folder Structure")
        ext_opts.addWidget(self.flat_output_cb)
        opt_layout.addLayout(ext_opts)
        
        opt_group.setLayout(opt_layout)
        layout.addWidget(opt_group)

        # 4. Action Button
        self.run_btn = QPushButton("EXECUTE ARCHIVING")
        self.run_btn.setObjectName("PrimaryButton")
        self.run_btn.setMinimumHeight(65)
        self.run_btn.clicked.connect(self.start_download)
        layout.addWidget(self.run_btn)

        # 5. Monitoring
        self.pbar = QProgressBar()
        self.pbar.setValue(0)
        self.pbar.setTextVisible(False)
        layout.addWidget(self.pbar)

        self.log_widget = QTextEdit()
        self.log_widget.setObjectName("LogArea")
        self.log_widget.setReadOnly(True)
        layout.addWidget(self.log_widget)

        return tab

    # --- [Logic Methods] ---

    def select_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Archive Directory", self.path_input.text())
        if path:
            self.path_input.setText(path)

    def toggle_archive_options(self, checked):
        for cb in [self.desc_cb, self.json_cb, self.subs_cb, self.thumb_cb, self.comments_cb]:
            cb.setEnabled(not checked)

    def apply_recommended_settings(self):
        self.archive_mode_cb.setChecked(True)
        self.stealth_mode_cb.setChecked(True)
        self.sleep_input.setText("5.0")
        self.max_sleep_input.setText("30.0")
        self.audio_mode_cb.setChecked(False)
        self.skip_download_cb.setChecked(False)
        self.flat_output_cb.setChecked(False)
        self.cookie_browser.setCurrentText("None")
        self.add_log("READY: Ultra-Stealth Channel Archiving Mode (5m~30m Random Sleep)")

    def load_settings_to_ui(self):
        s = self.settings
        self.archive_mode_cb.setChecked(s.get("archive_mode", True))
        self.audio_mode_cb.setChecked(s.get("only_audio", False))
        self.skip_download_cb.setChecked(s.get("skip_download", False))
        self.stealth_mode_cb.setChecked(s.get("stealth_mode", True))
        self.sleep_input.setText(str(s.get("sleep_interval_min", "1.0")))
        self.max_sleep_input.setText(str(s.get("max_sleep_interval_min", "30.0")))
        idx = self.cookie_browser.findText(s.get("cookie_browser", "None"))
        if idx >= 0: self.cookie_browser.setCurrentIndex(idx)
        self.flat_output_cb.setChecked(s.get("flat_output", False))
        self.path_input.setText(s.get("last_path", os.getcwd()))

    def save_current_settings(self):
        try: sleep_min = float(self.sleep_input.text())
        except: sleep_min = 1.0
        try: max_sleep = float(self.max_sleep_input.text())
        except: max_sleep = 30.0
        
        self.settings.update({
            "archive_mode": self.archive_mode_cb.isChecked(),
            "only_audio": self.audio_mode_cb.isChecked(),
            "skip_download": self.skip_download_cb.isChecked(),
            "stealth_mode": self.stealth_mode_cb.isChecked(),
            "sleep_interval_min": sleep_min,
            "max_sleep_interval_min": max_sleep,
            "cookie_browser": self.cookie_browser.currentText(),
            "flat_output": self.flat_output_cb.isChecked(),
            "last_path": self.path_input.text()
        })
        save_settings(self.settings)

    def start_download(self):
        url = self.url_input.text().strip()
        if not url: return

        self.save_current_settings()
        
        try: sleep_sec = float(self.sleep_input.text()) * 60.0
        except: sleep_sec = 60.0
        try: max_sleep_sec = float(self.max_sleep_input.text()) * 60.0
        except: max_sleep_sec = 1800.0

        options = {
            'archive_mode': self.archive_mode_cb.isChecked(),
            'write_description': self.desc_cb.isChecked() or self.archive_mode_cb.isChecked(),
            'write_info_json': self.json_cb.isChecked() or self.archive_mode_cb.isChecked(),
            'write_subs': self.subs_cb.isChecked() or self.archive_mode_cb.isChecked(),
            'write_auto_subs': self.subs_cb.isChecked() or self.archive_mode_cb.isChecked(),
            'write_thumbnail': self.thumb_cb.isChecked() or self.archive_mode_cb.isChecked(),
            'get_comments': self.comments_cb.isChecked() or self.archive_mode_cb.isChecked(),
            'only_audio': self.audio_mode_cb.isChecked(),
            'skip_download': self.skip_download_cb.isChecked(),
            'sleep_interval': sleep_sec,
            'max_sleep_interval': max_sleep_sec if self.stealth_mode_cb.isChecked() else sleep_sec * 2,
            'sleep_requests': min(sleep_sec / 2.0, 300.0) if self.stealth_mode_cb.isChecked() else 0,
            'stealth_mode': self.stealth_mode_cb.isChecked(),
            'cookies_from_browser': None if self.cookie_browser.currentText() == "None" else self.cookie_browser.currentText(),
            'flat_output': self.flat_output_cb.isChecked(),
            'ignore_errors': True
        }

        self.run_btn.setEnabled(False)
        self.pbar.setValue(0)
        self.add_log(f"ENGINE START: Initializing secure stream for {url}")

        self.thread = DownloadThread(url, self.path_input.text(), options)
        self.thread.progress.connect(self.update_progress)
        self.thread.log.connect(self.add_log)
        self.thread.finished_signal.connect(self.on_finished)
        self.thread.start()

    @Slot(dict)
    def update_progress(self, d):
        if d['status'] == 'downloading':
            try:
                p = float(d.get('_percent_str', '0%').replace('%', ''))
                self.pbar.setValue(int(p))
            except: pass

    @Slot(str)
    def add_log(self, message):
        self.log_widget.append(message)
        self.log_widget.verticalScrollBar().setValue(self.log_widget.verticalScrollBar().maximum())

    @Slot(bool)
    def on_finished(self, success):
        self.run_btn.setEnabled(True)
        if success:
            self.pbar.setValue(100)
            self.add_log("SYSTEM: All assets secured and archived successfully.")
        else:
            self.add_log("SYSTEM: Task interrupted or failed. Check logs above.")

    def closeEvent(self, event):
        self.save_current_settings()
        event.accept()
