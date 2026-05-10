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
- **Full Spectrum Archiving**: Secures video, description, metadata (JSON), subtitles, and nested comment trees by default.
- **Daily Counter Naming Convention**: Folders are named `YYYYMMDD_XXXX_Channel_Title` for clarity and organization.
- **Absolute Privacy (Strict Relative Paths)**: All path management is strictly relative to the project root. Absolute paths are never displayed or stored.
- **Path Locking System**: One-click "Default Path" locking to ensure data consistency in the `Archives` directory.

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
- **풀 스펙트럼 아카이빙**: 영상, 설명, 메타데이터(JSON), 자막, 계층형 댓글 트리를 기본으로 모두 보존.
- **일일 카운터 폴더 시스템**: `YYYYMMDD_XXXX_채널명_동영상명` 형식의 폴더명을 통해 체계적인 데이터 분류 지원.
- **철저한 상대 경로 시스템**: 모든 경로는 프로젝트 루트 기준 상대 경로로만 처리되며, UI상에서 절대경로 노출을 원천 차단.
- **경로 잠금 시스템**: '기본 경로 사용' 체크박스를 통해 `Archives` 디렉토리에 정갈하게 데이터 축적 가능.

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
