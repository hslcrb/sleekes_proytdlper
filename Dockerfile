FROM python:3.10

WORKDIR /app

# 시스템 의존성 설치 (ffmpeg 및 PySide6 필수 라이브러리)
# Debian Bookworm 대응 패키지명 사용
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1 \
    libxkbcommon-x11-0 \
    libegl1 \
    libdbus-1-3 \
    && rm -rf /var/lib/apt/lists/*


# 요구사항 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 실행 권한 부여
RUN chmod +x run.sh

# 기본 실행 명령 (CLI 모드)
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
