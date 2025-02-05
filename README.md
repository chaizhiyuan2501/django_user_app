# 💻 Django ユーザ管理サイト

## 📄 概要
このプロジェクトは Django で作成した**ユーザ管理サイト**アプリケーションのです。

---

## 🛠️ 使用技術
- **フレームワーク**: Django
- **プログラミング言語**: python:3.11-slim
- **データベース**: PostgreSQL
- **フロントエンド**: HTML / CSS / bootstrap5
- **仮想環境**: Docker

---

## 🚀 実行方法

### 1️⃣ **リポジトリをクローン**
```bash
git clone https://github.com/chaizhiyuan2501/django_user_app.git
cd django_user_app
```

### 2️⃣ **Docker を使用してコンテナを起動**
```bash
docker-compose up --build
```

### 3️⃣ **データベースのマイグレーション**
```bash
docker-compose exec web python manage.py migrate
```

### 4️⃣ **スーパーユーザーの作成（管理者アカウント）**
```bash
docker-compose exec web python manage.py createsuperuser
```

### 5️⃣ **テストツールを実行する**
```bash
docker-compose exec web python manage.py test
```
### 5️⃣ **テスト用ユーザーを作成する**
```bash
docker-compose exec web python main.py
```

### 6️⃣ **サーバーの起動**
コンテナはすでに起動しているので、以下の URL にアクセスしてください。
```
http://127.0.0.1:8000/
```

---

## 🎯 主な機能
- ユーザー認証(新規登録､ログイン､ログアウト)
- ユーザーの情報の変更

---


---

## 📑 今後の改善点
- [ ] Viewテストコードの追加
- [ ]
- [ ]

---

## 👨‍💻 作者
[Chai ZhiYuan](https://github.com/chaizhiyuan2501)
お問合せ: chaizhiyuan2501@gmail.com

---


