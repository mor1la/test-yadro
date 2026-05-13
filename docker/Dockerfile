ARG UBUNTU_DIGEST=sha256:962f6cadeae0ea6284001009daa4cc9a8c37e75d1f5191cf0eb83fe565b63dd7

FROM ubuntu:22.04@${UBUNTU_DIGEST}

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VENV_PATH=/opt/venv \
    PATH="/opt/venv/bin:${PATH}"

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv "${VENV_PATH}"

COPY script/requirements.txt .

RUN "${VENV_PATH}/bin/pip" install --no-cache-dir -r requirements.txt

COPY script/check_status.py /app/check_status.py

RUN groupadd -r appgroup \
    && useradd -r -g appgroup appuser \
    && chown -R appuser:appgroup /app /opt/venv

USER appuser

CMD ["python3", "/app/check_status.py"]