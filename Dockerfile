# app/Dockerfile

# FROM python:3.12-slim
FROM hdgigante/python-opencv:4.10.0-ubuntu

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    build-essential \
    curl \
    python3.12-venv \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="${PATH}:/root/.local/bin"

RUN python3 -m venv .venv
RUN .venv/bin/pip install opencv-python streamlit

ADD ./streamlit_app.py /app
ADD ./test.jpg /app

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT [".venv/bin/streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
