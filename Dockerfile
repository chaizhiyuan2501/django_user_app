# ベースイメージとして公式のPython 3.9イメージを使用します
FROM python:3.11-slim

# 環境変数を設定します
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 作業ディレクトリを設定します
WORKDIR /app

# システム依存関係をインストールします
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && rm -rf /var/lib/apt/lists/*


# Pythonの依存関係をインストールします
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクトファイルをコピーします
COPY . .

# アプリケーションポートを公開します
EXPOSE 8000

# アプリケーションを実行します
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
