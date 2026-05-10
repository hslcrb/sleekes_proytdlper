# SLEEKES: Achromatic Archiving System

<p align="center">
  <img src="https://img.shields.io/github/license/hslcrb/sleekes_proytdlper?style=flat-square&color=000000" alt="License">
  <img src="https://img.shields.io/github/v/release/hslcrb/sleekes_proytdlper?style=flat-square&color=000000" alt="Version">
  <img src="https://img.shields.io/github/issues/hslcrb/sleekes_proytdlper?style=flat-square&color=000000" alt="Issues">
  <img src="https://img.shields.io/github/stars/hslcrb/sleekes_proytdlper?style=flat-square&color=000000" alt="Stars">
  <img src="https://img.shields.io/badge/Theme-Achromatic-000000?style=flat-square" alt="Theme">
</p>

[English](#english) | [한국어](#한국어)

---

## English

**SLEEKES** is a potent, minimalist video archiving solution built on the power of the `yt-dlp` engine. It is designed to secure digital heritage with a focus on permanence and ultimate purity.

### Key Features
- **Achromatic Design Mode**: Focus-oriented Pure Dark and Pure Light themes.
- **Multi-Language Engine**: Instant toggle between English and Korean for all UI elements.
- **403 Forbidden Mitigation**: Bypasses aggressive IP blocks via Android/iOS client emulation and intelligent User-Agent rotation.
- **Precision Sleep Engine**: Configurable minute-based randomized delay (e.g., 5m to 30m) to mimic human behavior.
- **Full Spectrum Archiving**: Secures video, description, metadata (JSON), subtitles, and nested comment trees.
- **Absolute Privacy (Strict Relative Paths)**: All path management is strictly relative to the project root. Absolute paths are never displayed or stored.
- **Path Locking System**: One-click "Default Path" locking to ensure data consistency in the `Archives` directory.
- **Metadata Viewer**: Built-in JSON report renderer with multi-theme support and enhanced selection styles.

### Installation (Windows PowerShell)
```powershell
python -m venv venv; .\venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

### Usage
```powershell
# GUI Mode
python main.py

# CLI Mode (Stealth Recommended)
python main.py [URL] --rec
```

---

## 한국어

**SLEEKES**는 `yt-dlp` 엔진의 강력함을 기반으로 설계된 초전절제형 동영상 아카이빙 솔루션입니다. 디지털 유산을 가장 순수하고 영구적인 상태로 보존하는 데 최적화되어 있습니다.

### 주요 기능
- **무채색 디자인 모드**: 집중력을 극대화하는 퓨어 다크 및 퓨어 라이트 테마 지원.
- **다국어 엔진**: 한국어와 영어로 즉시 전환 가능한 i18n 시스템 탑재.
- **403 차단 완벽 방어**: 모바일 클라이언트 위장 및 유저에이전트 로테이션을 통한 IP 차단 회피.
- **정밀 휴식 엔진**: 분 단위 랜덤 지연(5분~30분)을 통해 기계적 접근 탐지를 완벽히 우회.
- **풀 스펙트럼 아카이빙**: 영상, 설명, 메타데이터(JSON), 자막, 계층형 댓글 트리를 단번에 보존.
- **철저한 상대 경로 시스템**: 모든 경로는 프로젝트 루트 기준 상대 경로로만 처리되며, UI상에서 절대경로 노출을 원천 차단.
- **경로 잠금 시스템**: '기본 경로 사용' 체크박스를 통해 `Archives` 디렉토리에 정갈하게 데이터 축적 가능.
- **메타데이터 뷰어**: 보존된 JSON 데이터를 HTML 보고서 형태로 렌더링하며, 테마별 선택(Selection) 스타일 최적화.

### 설치 방법 (Windows PowerShell)
```powershell
python -m venv venv; .\venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

### 실행 방법
```powershell
# GUI 모드
python main.py

# CLI 모드 (권장 스텔스 모드)
python main.py [URL] --rec
```

---
*Developed by Antigravity. Potent . Pure . Permanent.*
