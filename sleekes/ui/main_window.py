from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QLabel, QCheckBox, 
                             QTextEdit, QProgressBar, QFileDialog, QGroupBox, QTabWidget, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QIcon, QFont, QAction
from sleekes.core.downloader import SleekesDownloader
from sleekes.core.config import load_settings, save_settings
from sleekes.ui.styles import MAIN_STYLE
from sleekes.ui.json_viewer import JsonViewerWidget
from sleekes.ui.guide_view import GuideViewWidget
import os

# =============================================================================
# [Sleekes Main Window]
#
# 이 모듈은 Sleekes의 GUI(Graphical User Interface) 메인 윈도우를 정의합니다.
# PySide6(Qt)를 사용하여 모던하고 직관적인 사용자 경험을 제공합니다.
# 
# 주요 기능:
# 1. 3단 탭 구조 (다운로드 센터, 뷰어, 가이드)
# 2. 비동기 다운로드 스레드 (UI 멈춤 방지)
# 3. 설정 자동 로드/저장 및 UI 반영
# 4. 실시간 로그 표시 및 프로그레스바 연동
# =============================================================================

class DownloadThread(QThread):
    """
    다운로드 작업을 백그라운드에서 처리하는 스레드 클래스입니다.
    메인 UI 스레드가 멈추지 않도록 별도의 스레드에서 yt-dlp를 실행합니다.
    """
    progress = Signal(dict)   # 진행률 정보 전달 시그널
    log = Signal(str)         # 로그 메시지 전달 시그널
    finished_signal = Signal(bool) # 작업 완료 여부 전달 시그널

    def __init__(self, url, output_path, options):
        """
        스레드 초기화
        Args:
            url (str): 대상 URL
            output_path (str): 저장 경로
            options (dict): 다운로드 옵션들
        """
        super().__init__()
        self.url = url
        self.output_path = output_path
        self.options = options

    def run(self):
        """
        스레드 시작 시 호출되는 메서드.
        Downloader 인스턴스를 생성하고 다운로드를 수행합니다.
        """
        downloader = SleekesDownloader(
            progress_callback=self.progress.emit,
            log_callback=self.log.emit
        )
        success = downloader.download(self.url, self.output_path, self.options)
        self.finished_signal.emit(success)

class SleekesMainWindow(QMainWindow):
    """
    Sleekes 애플리케이션의 메인 윈도우 클래스입니다.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sleekes - 범용 동영상 아카이빙 솔루션")
        self.setMinimumSize(950, 800) # 쾌적한 화면 크기 설정
        
        # 설정 파일 로드
        self.settings = load_settings() 
        
        # UI 구성요소 초기화
        self.init_ui()
        
        # 로드된 설정을 UI 컴포넌트에 반영
        self.load_settings_to_ui() 
        
        # 전체 스타일시트 적용 (다크 테마, 글래스모피즘)
        self.setStyleSheet(MAIN_STYLE)

    def init_ui(self):
        """
        화면의 전체적인 레이아웃과 위젯들을 생성하고 배치합니다.
        """
        central_widget = QWidget()
        central_widget.setObjectName("MainFrame")
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # --- 1. 상단 헤더 및 헬프 버튼 ---
        header_layout = QHBoxLayout()
        
        title_box = QVBoxLayout()
        title_label = QLabel("Sleekes")
        title_label.setObjectName("TitleLabel")
        subtitle_label = QLabel("Potent. Pure. Permanent. 초월적 아카이빙 시스템")
        subtitle_label.setStyleSheet("color: #64748b; margin-top: -5px; margin-bottom: 5px;")
        title_box.addWidget(title_label)
        title_box.addWidget(subtitle_label)
        
        header_layout.addLayout(title_box)
        header_layout.addStretch()
        
        # 도움말 바로가기 버튼
        self.help_btn = QPushButton("도움말 및 가이드")
        self.help_btn.setObjectName("SecondaryButton")
        self.help_btn.setCursor(Qt.PointingHandCursor)
        self.help_btn.clicked.connect(self.go_to_guide_tab)
        header_layout.addWidget(self.help_btn)
        
        main_layout.addLayout(header_layout)

        # --- 2. 메인 탭 위젯 구성 ---
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_main_tab(), "📂 다운로드 센터")
        self.tabs.addTab(JsonViewerWidget(), "📊 메타데이터 뷰어")
        # 가이드 탭은 인스턴스를 멤버변수로 저장해두어 나중에 접근 가능하게 함
        self.guide_tab = GuideViewWidget()
        self.tabs.addTab(self.guide_tab, "📘 플랫폼 & 가이드")
        
        main_layout.addWidget(self.tabs)

    def create_main_tab(self):
        """
        '다운로드 센터' 탭의 내부 UI를 생성합니다.
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 20, 10, 10)
        layout.setSpacing(15)

        # [입력 섹션] URL 입력창
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("동영상, 재생목록, 또는 채널 URL을 입력하세요 (유튜브, 인스타, 틱톡 등 지원)")
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)

        # [경로 섹션] 저장 폴더 선택
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("저장될 폴더 경로")
        path_btn = QPushButton("폴더 선택")
        path_btn.setObjectName("SecondaryButton")
        path_btn.clicked.connect(self.select_path)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(path_btn)
        layout.addLayout(path_layout)

        # [옵션 그룹] 아카이빙 설정 컨테이너
        options_group = QGroupBox("아카이빙 및 엔진 설정")
        options_layout = QVBoxLayout()
        
        # > 상단 옵션: 핵심 모드 선택
        main_opts_layout = QHBoxLayout()
        self.archive_mode_cb = QCheckBox("전체 아카이빙 모드 (권장)")
        self.archive_mode_cb.setToolTip("영상과 함께 설명, 자막, 댓글 등 모든 데이터를 수집합니다.")
        self.archive_mode_cb.setStyleSheet("color: #38bdf8; font-weight: bold;")
        
        self.audio_mode_cb = QCheckBox("오디오만 추출 (MP3)")
        self.audio_mode_cb.setToolTip("영상 없이 고음질 음원만 추출합니다.")
        
        self.skip_download_cb = QCheckBox("데이터만 수집 (영상 제외)")
        self.skip_download_cb.setToolTip("용량이 큰 영상 파일은 받지 않고 메타데이터만 빠르게 수집합니다.")
        
        self.stealth_mode_cb = QCheckBox("차단방지 스텔스 모드")
        self.stealth_mode_cb.setToolTip("속도를 늦추고 유저에이전트를 무작위화하여 403 차단을 방지합니다.")
        self.stealth_mode_cb.setStyleSheet("color: #f87171; font-weight: bold;")

        # > 권장 설정 원클릭 버튼
        self.rec_btn = QPushButton("✨ 권장 설정 적용")
        self.rec_btn.setObjectName("SecondaryButton")
        self.rec_btn.setToolTip("채널 통째로 아카이빙할 때 추천하는 [안전+스텔스] 설정을 적용합니다.")
        self.rec_btn.clicked.connect(self.apply_recommended_settings)
        self.rec_btn.setStyleSheet("color: #facc15; border-color: #facc15;")

        main_opts_layout.addWidget(self.archive_mode_cb)
        main_opts_layout.addWidget(self.audio_mode_cb)
        main_opts_layout.addWidget(self.skip_download_cb)
        main_opts_layout.addWidget(self.stealth_mode_cb)
        main_opts_layout.addStretch()
        main_opts_layout.addWidget(self.rec_btn)
        options_layout.addLayout(main_opts_layout)
        
        # > 상세 데이터 옵션 (체크박스)
        detail_grid = QHBoxLayout()
        self.desc_cb = QCheckBox("설명")
        self.json_cb = QCheckBox("정보(JSON)")
        self.subs_cb = QCheckBox("자막")
        self.thumb_cb = QCheckBox("썸네일")
        self.comments_cb = QCheckBox("댓글(JSON)")

        for cb in [self.desc_cb, self.json_cb, self.subs_cb, self.thumb_cb, self.comments_cb]:
            detail_grid.addWidget(cb)
            cb.setEnabled(False) # 아카이브 모드가 켜져있으면 기본 활성화(비활성 상태)

        # 아카이브 모드 토글 시 상세 옵션 상태 변경 연결
        self.archive_mode_cb.toggled.connect(self.toggle_archive_options)
        options_layout.addLayout(detail_grid)

        # > 하단 엔진/고급 설정
        adv_layout = QHBoxLayout()
        
        # 휴식 시간 (Anti-Ban)
        adv_layout.addWidget(QLabel("휴식(초):"))
        self.sleep_input = QLineEdit()
        self.sleep_input.setToolTip("영상 다운로드 사이의 대기 시간(초). IP 차단 방지용.")
        self.sleep_input.setMaximumWidth(50)
        self.sleep_input.setAlignment(Qt.AlignCenter)
        adv_layout.addWidget(self.sleep_input)

        # 쿠키 브라우저 선택
        adv_layout.addSpacing(15)
        adv_layout.addWidget(QLabel("쿠키 연동:"))
        from PySide6.QtWidgets import QComboBox
        self.cookie_browser = QComboBox()
        self.cookie_browser.setToolTip("비공개/성인인증 영상을 위해 브라우저 로그인 정보를 빌려옵니다.")
        self.cookie_browser.addItems(["None", "chrome", "firefox", "edge", "safari"])
        self.cookie_browser.setMinimumWidth(100)
        adv_layout.addWidget(self.cookie_browser)

        # 플레이리스트 범위 지정
        adv_layout.addSpacing(15)
        adv_layout.addWidget(QLabel("Playlist범위:"))
        self.playlist_items_input = QLineEdit()
        self.playlist_items_input.setPlaceholderText("예: 1-5, 10")
        self.playlist_items_input.setToolTip("전체가 아닌 특정 순번의 영상만 받고 싶을 때 입력하세요.")
        adv_layout.addWidget(self.playlist_items_input)

        # 폴더 구조 플랫하게
        self.flat_output_cb = QCheckBox("폴더정리 끄기")
        self.flat_output_cb.setToolTip("채널/날짜별 폴더를 만들지 않고 한 곳에 파일을 저장합니다.")
        adv_layout.addWidget(self.flat_output_cb)

        options_layout.addLayout(adv_layout)
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)

        # [실행 버튼]
        self.download_button = QPushButton("아카이빙 시작")
        self.download_button.setObjectName("PrimaryButton")
        self.download_button.clicked.connect(self.start_download)
        self.download_button.setCursor(Qt.PointingHandCursor)
        self.download_button.setMinimumHeight(50) # 버튼 크기 키움
        layout.addWidget(self.download_button)

        # [진행 표시줄]
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False) # 텍스트 대신 깔끔한 바만 표시
        layout.addWidget(self.progress_bar)

        # [로그 영역]
        self.log_area = QTextEdit()
        self.log_area.setObjectName("LogArea")
        self.log_area.setReadOnly(True)
        self.log_area.setPlaceholderText("작업 로그가 여기에 표시됩니다... (자세한 진행 상황 확인 가능)")
        layout.addWidget(self.log_area)

        return tab

    def go_to_guide_tab(self):
        """
        '도움말' 버튼 클릭 시 가이드 탭으로 이동합니다.
        """
        self.tabs.setCurrentIndex(2) # 2번 인덱스가 가이드 탭

    def load_settings_to_ui(self):
        """
        저장된 설정(settings 딕셔너리)을 UI 위젯들의 상태에 반영합니다.
        """
        s = self.settings
        self.archive_mode_cb.setChecked(s.get("archive_mode", True))
        self.audio_mode_cb.setChecked(s.get("only_audio", False))
        self.skip_download_cb.setChecked(s.get("skip_download", False))
        self.stealth_mode_cb.setChecked(s.get("stealth_mode", True)) # 기본적으로 켜둠 (안전제일)
        self.sleep_input.setText(str(s.get("sleep_interval", 15)))
        
        # 콤보박스 텍스트로 인덱스 찾아 설정
        cb_idx = self.cookie_browser.findText(s.get("cookie_browser", "None"))
        if cb_idx >= 0:
            self.cookie_browser.setCurrentIndex(cb_idx)
            
        self.flat_output_cb.setChecked(s.get("flat_output", False))
        
        # 마지막 경로 복원
        last_path = s.get("last_path", os.getcwd())
        if os.path.exists(last_path):
            self.path_input.setText(last_path)
        else:
            self.path_input.setText(os.getcwd())

        # 아카이브 모드에 따른 상세 체크박스 활성/비활성 초기화
        self.toggle_archive_options(self.archive_mode_cb.isChecked())

    def save_current_settings(self):
        """
        현재 UI 위젯들의 값을 읽어 설정 파일(JSON)에 저장합니다.
        프로그램 종료 시나 작업 시작 시 호출됩니다.
        """
        try:
            sleep_val = int(self.sleep_input.text())
        except:
            sleep_val = 5 # 예외 발생 시 기본값 5

        self.settings.update({
            "archive_mode": self.archive_mode_cb.isChecked(),
            "only_audio": self.audio_mode_cb.isChecked(),
            "skip_download": self.skip_download_cb.isChecked(),
            "stealth_mode": self.stealth_mode_cb.isChecked(),
            "sleep_interval": sleep_val,
            "cookie_browser": self.cookie_browser.currentText(),
            "flat_output": self.flat_output_cb.isChecked(),
            "last_path": self.path_input.text()
        })
        save_settings(self.settings)

    def apply_recommended_settings(self):
        """
        '권장 설정 적용' 버튼 핸들러.
        채널 전체 아카이빙 시 403 차단을 피하기 위한 가장 안전한 설정을 강제 적용합니다.
        """
        self.archive_mode_cb.setChecked(True)  # 전체 아카이빙 켜기
        self.stealth_mode_cb.setChecked(True)   # 스텔스 모드 (403 방어) 켜기
        self.audio_mode_cb.setChecked(False)   # 오디오 전용 끄기
        self.skip_download_cb.setChecked(False)# 영상 생략 끄기
        self.sleep_input.setText("15")         # 15초(최대 30초) 랜덤 휴식 설정
        self.flat_output_cb.setChecked(False)  # 폴더 정리 켜기
        self.cookie_browser.setCurrentText("None") # 쿠키 제외 (요청사항)
        self.add_log("💡 채널 보존을 위한 [안전 아카이빙 + 스텔스 모드]가 적용되었습니다.")
        self.add_log("   (속도는 조금 느리지만 차단 위험을 최소화합니다.)")

    def toggle_archive_options(self, checked):
        """
        '전체 아카이빙 모드' 체크박스 토글 시 호출.
        하위 상세 옵션들을 비활성화(자동 처리됨을 의미)하거나 활성화합니다.
        """
        for cb in [self.desc_cb, self.json_cb, self.subs_cb, self.thumb_cb, self.comments_cb]:
            cb.setEnabled(not checked)

    def select_path(self):
        """
        폴더 선택 다이얼로그를 띄웁니다.
        """
        path = QFileDialog.getExistingDirectory(self, "저장 폴더 선택", self.path_input.text())
        if path:
            self.path_input.setText(path)

    def start_download(self):
        """
        '아카이빙 시작' 버튼 핸들러.
        설정을 읽고 검증한 뒤, 다운로드 스레드를 시작합니다.
        """
        url = self.url_input.text().strip()
        if not url:
            self.add_log("⚠️ URL을 먼저 입력해주세요.")
            QMessageBox.warning(self, "URL 누락", "다운로드할 URL을 입력해주세요.")
            return

        self.save_current_settings() # 작업 전 설정 자동 저장

        # 휴식 시간 파싱
        try:
            sleep_val = int(self.sleep_input.text())
        except:
            sleep_val = 0

        # 쿠키 브라우저
        cookie_b = self.cookie_browser.currentText()
        if cookie_b == "None":
            cookie_b = None

        # 옵션 딕셔너리 구성
        options = {
            'archive_mode': self.archive_mode_cb.isChecked(),
            # 아카이브 모드면 하위 옵션은 무조건 True로 간주
            'write_description': self.desc_cb.isChecked() or self.archive_mode_cb.isChecked(),
            'write_info_json': self.json_cb.isChecked() or self.archive_mode_cb.isChecked(),
            'write_subs': self.subs_cb.isChecked() or self.archive_mode_cb.isChecked(),
            'write_auto_subs': self.subs_cb.isChecked() or self.archive_mode_cb.isChecked(),
            'write_thumbnail': self.thumb_cb.isChecked() or self.archive_mode_cb.isChecked(),
            'get_comments': self.comments_cb.isChecked() or self.archive_mode_cb.isChecked(),
            
            'only_audio': self.audio_mode_cb.isChecked(),
            'skip_download': self.skip_download_cb.isChecked(),
            
            # Anti-ban sleep settings
            'max_sleep_interval': sleep_val * 2 if sleep_val > 0 else 30, # 최소 30초 랜덤성 확보
            'sleep_interval': sleep_val,
            'sleep_requests': 5 if self.stealth_mode_cb.isChecked() else 0, # 요청마다 5초 대기
            
            'stealth_mode': self.stealth_mode_cb.isChecked(),
            'cookies_from_browser': cookie_b,
            'playlist_items': self.playlist_items_input.text().strip() or None,
            'flat_output': self.flat_output_cb.isChecked(),
            'ignore_errors': True
        }

        # UI 상태 변경 (중복 실행 방지)
        self.download_button.setEnabled(False)
        self.download_button.setText("작업 진행 중...")
        self.progress_bar.setValue(0)
        self.add_log(f"--- Sleekes Engine 가동: {url} ---")

        # 스레드 생성 및 시작
        self.thread = DownloadThread(url, self.path_input.text(), options)
        self.thread.progress.connect(self.update_progress)
        self.thread.log.connect(self.add_log)
        self.thread.finished_signal.connect(self.on_finished)
        self.thread.start()

    @Slot(dict)
    def update_progress(self, d):
        """
        스레드에서 보내오는 진행률 정보를 받아 프로그레스바를 업데이트합니다.
        """
        if d['status'] == 'downloading':
            try:
                p_text = d.get('_percent_str', '0%').replace('%', '')
                p_val = float(p_text)
                self.progress_bar.setValue(int(p_val))
            except:
                pass

    @Slot(str)
    def add_log(self, message):
        """
        로그창에 텍스트를 추가하고 자동으로 스크롤을 내립니다.
        """
        self.log_area.append(message)
        self.log_area.verticalScrollBar().setValue(self.log_area.verticalScrollBar().maximum())

    @Slot(bool)
    def on_finished(self, success):
        """
        작업이 완료되었을 때 호출되는 슬롯.
        UI를 다시 활성화하고 완료 메시지를 띄웁니다.
        """
        self.download_button.setEnabled(True)
        self.download_button.setText("아카이빙 시작")
        
        if success:
            self.progress_bar.setValue(100)
            self.add_log("--- ✅ 아카이빙 작업이 성공적으로 완료되었습니다 ---")
            self.save_current_settings() 
            QMessageBox.information(self, "완료", "모든 아카이빙 작업이 완료되었습니다.")
        else:
            self.add_log("--- ❌ 작업 중 오류가 발생했습니다 (로그 확인 필요) ---")
            QMessageBox.critical(self, "실패", "작업 중 오류가 발생했습니다.\n로그를 확인해주세요.")
    
    def closeEvent(self, event):
        """
        창 닫기 이벤트 핸들러. 종료 전 설정을 자동 저장합니다.
        """
        self.save_current_settings()
        event.accept()
