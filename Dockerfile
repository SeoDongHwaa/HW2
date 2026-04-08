# 1. Builder Stage: 의존성 패키지를 설치하기 위한 임시 환경입니다. 빌드에만 쓰이고 버려지므로 용량 최적화에 유리합니다.
FROM python:3.9-slim as builder

WORKDIR /app

# 파이썬 가상환경 생성 (전역 패키지 오염 방지 및 복사 용이)
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# 2. Production Stage: 실제 배포되어 구동될 환경입니다.
FROM python:3.9-slim

# 보안: root 권한 대신 애플리케이션 단독 실행용 유저(appuser) 생성
RUN useradd -m -r appuser

WORKDIR /app

# builder에서 생성한 가상 환경(설치된 패키지)만 복사
COPY --from=builder /opt/venv /opt/venv

# 파이썬 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# 실제 애플리케이션 코드 복사 및 소유권 변경
COPY --chown=appuser:appuser ./app ./app

# 생성해 둔 비권한 유저로 실행 권한 전환 (주요 보안 최적화)
USER appuser

EXPOSE 8000

# 서버 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
