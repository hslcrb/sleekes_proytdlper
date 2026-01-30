from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QLabel, QCheckBox, 
                             QTextEdit, QProgressBar, QFileDialog, QGroupBox, QTabWidget, QMessageBox, QComboBox)
from PySide6.QtCore import Qt, QThread, Signal, Slot, QSize
from PySide6.QtGui import QIcon, QFont, QAction
from sleekes.core.downloader import SleekesDownloader
from sleekes.core.config import load_settings, save_settings
from sleekes.ui import styles, icons, i18n
from sleekes.ui.json_viewer import JsonViewerWidget
from sleekes.ui.guide_view import GuideViewWidget
import os

# =============================================================================
# [Sleekes Download Management]
# =============================================================================

class DownloadThread(QThread):
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
    """Sleekes 메인 윈도우 - 다국어(KO/EN) 및 무채색 디자인 지원"""
    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        self.current_lang = self.settings.get("language", "EN")
        
        self.setWindowTitle("SLEEKES - Potent Universal Archiver")
        self.setMinimumSize(1000, 850)
        
        self.init_ui()
        self.load_settings_to_ui()
        
        # 디자인 및 언어 초기화
        initial_theme = self.settings.get("theme", "Dark")
        self.theme_combo.setCurrentText(initial_theme)
        self.lang_combo.setCurrentText(self.current_lang)
        
        self.apply_theme(initial_theme)
        self.apply_language(self.current_lang)

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
        
        # Language Selector
        lang_layout = QHBoxLayout()
        self.lang_label = QLabel("LANGUAGE:")
        self.lang_label.setStyleSheet("font-size: 11px; font-weight: bold; color: #888;")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["EN", "KO"])
        self.lang_combo.currentTextChanged.connect(self.apply_language)
        lang_layout.addWidget(self.lang_label)
        lang_layout.addWidget(self.lang_combo)
        header.addLayout(lang_layout)
        
        header.addSpacing(15)

        # Design Mode Selector
        mode_layout = QHBoxLayout()
        self.mode_label = QLabel("DESIGN MODE:")
        self.mode_label.setStyleSheet("font-size: 11px; font-weight: bold; color: #888;")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.currentTextChanged.connect(self.apply_theme)
        mode_layout.addWidget(self.mode_label)
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
        is_dark = (theme_name == "Dark")
        self.setStyleSheet(styles.STYLE_DARK if is_dark else styles.STYLE_LIGHT)
        icon_color = "#ffffff" if is_dark else "#000000"
        
        self.update_icons(icon_color)
        self.settings["theme"] = theme_name
        save_settings(self.settings)

    def apply_language(self, lang_code):
        """앱의 모든 텍스트를 선택된 언어로 번역합니다."""
        self.current_lang = lang_code
        t = i18n.TRANSLATIONS[lang_code]
        
        # Nav & Header
        self.tabs.setTabText(0, t["nav_downloader"])
        self.tabs.setTabText(1, t["nav_metadata"])
        self.tabs.setTabText(2, t["nav_guide"])
        self.mode_label.setText(t["design_mode"])
        self.lang_label.setText(t["lang_mode"])
        self.guide_nav_btn.setText(t["btn_guide"])
        
        # Downloader Tab
        self.url_input.setPlaceholderText(t["url_placeholder"])
        self.path_input.setPlaceholderText(t["path_placeholder"])
        self.path_btn.setText(t["btn_browse"])
        self.opt_group.setTitle(t["engine_group"])
        self.archive_mode_cb.setText(t["opt_full_archive"])
        self.audio_mode_cb.setText(t["opt_audio_only"])
        self.skip_download_cb.setText(t["opt_metadata_only"])
        self.stealth_mode_cb.setText(t["opt_stealth"])
        self.rec_btn.setText(t["btn_rec"])
        
        self.desc_cb.setText(t["detail_desc"])
        self.json_cb.setText(t["detail_json"])
        self.subs_cb.setText(t["detail_subs"])
        self.thumb_cb.setText(t["detail_thumb"])
        self.comments_cb.setText(t["detail_comments"])
        
        self.min_sleep_label.setText(t["min_sleep"])
        self.max_sleep_label.setText(t["max_sleep"])
        self.cookie_label.setText(t["auth_cookies"])
        self.flat_output_cb.setText(t["opt_flat"])
        self.run_btn.setText(t["btn_execute"])
        
        # Metadata Tab (JSON Viewer)
        if hasattr(self.tab_metadata, "update_language"):
            self.tab_metadata.update_language(lang_code)
            
        # Reference Tab (Guide)
        if hasattr(self, "tab_guide"):
            self.tab_guide.update_language(lang_code)

        # Settings Save
        self.settings["language"] = lang_code
        save_settings(self.settings)

    def update_icons(self, color):
        self.tabs.setTabIcon(0, icons.svg_to_icon(icons.ICON_DOWNLOAD_CENTER, color))
        self.tabs.setTabIcon(1, icons.svg_to_icon(icons.ICON_METADATA_VIEWER, color))
        self.tabs.setTabIcon(2, icons.svg_to_icon(icons.ICON_GUIDE, color))
        self.tabs.setIconSize(QSize(22, 22))
        self.rec_btn.setIcon(icons.svg_to_icon(icons.ICON_RECOMMENDED, color))
        self.guide_nav_btn.setIcon(icons.svg_to_icon(icons.ICON_GUIDE, color))

    def create_downloader_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 25, 15, 15)
        layout.setSpacing(20)

        self.url_input = QLineEdit()
        self.url_input.setMinimumHeight(45)
        layout.addWidget(self.url_input)

        path_box = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_btn = QPushButton()
        self.path_btn.setObjectName("SecondaryButton")
        self.path_btn.clicked.connect(self.select_path)
        path_box.addWidget(self.path_input)
        path_box.addWidget(self.path_btn)
        layout.addLayout(path_box)

        self.opt_group = QGroupBox()
        opt_layout = QVBoxLayout()
        
        top_opts = QHBoxLayout()
        self.archive_mode_cb = QCheckBox()
        self.audio_mode_cb = QCheckBox()
        self.skip_download_cb = QCheckBox()
        self.stealth_mode_cb = QCheckBox()
        
        self.rec_btn = QPushButton()
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
        self.desc_cb = QCheckBox()
        self.json_cb = QCheckBox()
        self.subs_cb = QCheckBox()
        self.thumb_cb = QCheckBox()
        self.comments_cb = QCheckBox()
        for cb in [self.desc_cb, self.json_cb, self.subs_cb, self.thumb_cb, self.comments_cb]:
            detail_opts.addWidget(cb)
            cb.setEnabled(False)
        self.archive_mode_cb.toggled.connect(self.toggle_archive_options)
        opt_layout.addLayout(detail_opts)
        
        ext_opts = QHBoxLayout()
        self.min_sleep_label = QLabel()
        ext_opts.addWidget(self.min_sleep_label)
        self.sleep_input = QLineEdit()
        self.sleep_input.setMaximumWidth(70)
        ext_opts.addWidget(self.sleep_input)
        
        ext_opts.addSpacing(15)
        self.max_sleep_label = QLabel()
        ext_opts.addWidget(self.max_sleep_label)
        self.max_sleep_input = QLineEdit()
        self.max_sleep_input.setMaximumWidth(70)
        ext_opts.addWidget(self.max_sleep_input)
        
        ext_opts.addSpacing(15)
        self.cookie_label = QLabel()
        ext_opts.addWidget(self.cookie_label)
        self.cookie_browser = QComboBox()
        self.cookie_browser.addItems(["None", "chrome", "firefox", "edge", "safari"])
        ext_opts.addWidget(self.cookie_browser)
        
        self.flat_output_cb = QCheckBox()
        ext_opts.addWidget(self.flat_output_cb)
        opt_layout.addLayout(ext_opts)
        
        self.opt_group.setLayout(opt_layout)
        layout.addWidget(self.opt_group)

        self.run_btn = QPushButton()
        self.run_btn.setObjectName("PrimaryButton")
        self.run_btn.setMinimumHeight(65)
        self.run_btn.clicked.connect(self.start_download)
        layout.addWidget(self.run_btn)

        self.pbar = QProgressBar()
        self.pbar.setValue(0)
        self.pbar.setTextVisible(False)
        layout.addWidget(self.pbar)

        self.log_widget = QTextEdit()
        self.log_widget.setObjectName("LogArea")
        self.log_widget.setReadOnly(True)
        layout.addWidget(self.log_widget)

        return tab

    def select_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Archive Directory", self.path_input.text())
        if path: self.path_input.setText(path)

    def toggle_archive_options(self, checked):
        for cb in [self.desc_cb, self.json_cb, self.subs_cb, self.thumb_cb, self.comments_cb]:
            cb.setEnabled(not checked)

    def apply_recommended_settings(self):
        self.archive_mode_cb.setChecked(True)
        self.stealth_mode_cb.setChecked(True)
        self.sleep_input.setText("5.0")
        self.max_sleep_input.setText("30.0")
        self.add_log(i18n.TRANSLATIONS[self.current_lang]["log_ready_rec"])

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
            "last_path": self.path_input.text(),
            "language": self.current_lang
        })
        save_settings(self.settings)

    def start_download(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", i18n.TRANSLATIONS[self.current_lang]["msg_url_missing"])
            return

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
        self.add_log(i18n.TRANSLATIONS[self.current_lang]["engine_start"].format(url=url))

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
        t = i18n.TRANSLATIONS[self.current_lang]
        if success:
            self.pbar.setValue(100)
            self.add_log(t["success"])
        else:
            self.add_log(t["fail"])

    def closeEvent(self, event):
        self.save_current_settings()
        event.accept()
