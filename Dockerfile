FROM python:3.10

WORKDIR /app

# 시스템 의존성 설치 (ffmpeg 및 필수 라이브러리)
# full 이미지에는 대부분의 라이브러리가 포함되어 있으나, ffmpeg와 일부 GL 라이브러리는 명시 필요
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1-mesa-glx \
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
