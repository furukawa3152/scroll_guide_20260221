# Scroll 書き方ガイド - Cloudflare Pages デプロイ手順

## 概要
このディレクトリには、Scrollブログの書き方説明サイトが含まれています。
Cloudflare Pagesで静的サイトとして公開できます。

## ファイル構成
```
scroll_guide/
├── index.html          # メインの説明ページ
├── images/             # キャラクター画像（コピーが必要）
├── blog_writer_app.py  # ブログ執筆支援アプリ（Streamlit）
├── requirements.txt    # Python依存関係（Streamlit）
├── venv/               # Python仮想環境（別途作成）
└── README.md           # このファイル
```

## ブログ執筆支援アプリ（Streamlit）

記事の種類（やってみた・気づき・日常など）を選び、テンプレートに沿って入力するとマークダウンを組み立てられます。Scrollにそのままコピーして使えます。

### セットアップと起動

```bash
# 仮想環境を作成（初回のみ）
python3 -m venv venv

# 有効化（macOS/Linux）
source venv/bin/activate

# 依存関係インストール
pip install -r requirements.txt

# アプリ起動
streamlit run blog_writer_app.py
```

ブラウザで `http://localhost:8501` が開きます。

### Streamlit Community Cloud にデプロイする

アプリを [Streamlit Community Cloud](https://share.streamlit.io/) にアップロードすると、URLを共有して誰でも使えるようになります。

**前提**: このプロジェクトを **GitHub のリポジトリにプッシュ**しておくこと（未プッシュの場合は下記の「1. GitHubにプッシュ」を先に実行）。

1. **GitHub にプッシュ（まだの場合）**
   ```bash
   git add blog_writer_app.py requirements.txt README.md
   git commit -m "Add Streamlit blog writer app"
   git remote add origin https://github.com/<あなたのユーザー名>/<リポジトリ名>.git
   git push -u origin main
   ```

2. **Streamlit Community Cloud でアプリ作成**
   - [share.streamlit.io](https://share.streamlit.io/) にアクセス
   - GitHub でサインイン
   - 右上 **「Create app」** → **「Yup, I have an app」** を選択

3. **設定を入力**
   - **Repository**: 対象の GitHub リポジトリ（例: `your-username/scroll_guide_20260221`）
   - **Branch**: `main`（または使いたいブランチ）
   - **Main file path**: `blog_writer_app.py`
   - **App URL**（任意）: サブドメインを指定すると、`https://<サブドメイン>.streamlit.app` で公開されます（例: `scroll-blog-writer`）

4. **「Deploy!」** をクリック  
   数分でビルドが終わり、表示されたURLでアプリにアクセスできます。コードをプッシュするたびに自動で再デプロイされます。

**補足**
- 無料枠では **パブリックリポジトリ** のアプリは公開可能。プライベートリポジトリのアプリは1つまで。
- Python バージョンや環境変数は「Advanced settings」で変更可能（既定は Python 3.12）。

## 画像の準備

デプロイ前に、画像をコピーする必要があります：

```bash
# スクリプトを実行
chmod +x copy_images.sh
./copy_images.sh

# または手動でコピー
mkdir -p images
cp ../Scroll_introduction/images/*.png images/
```

## Cloudflare Pagesへのデプロイ手順

### 方法1: Cloudflare Pagesダッシュボードから直接アップロード

1. **Cloudflareダッシュボードにログイン**
   - https://dash.cloudflare.com/ にアクセス

2. **Pagesプロジェクトを作成**
   - 左メニューから「Pages」を選択
   - 「プロジェクトを作成」をクリック
   - 「フォルダーを直接アップロード」を選択

3. **プロジェクト設定**
   - プロジェクト名: `scroll-guide`（任意）
   - ビルドコマンド: （不要）
   - ビルド出力ディレクトリ: `/` または空白

4. **ファイルをアップロード**
   - `index.html` をアップロード
   - 「デプロイ」をクリック

5. **カスタムドメインの設定（オプション）**
   - プロジェクト設定 → カスタムドメイン
   - 例: `guide.hagakurepgm.net` を設定
   - **重要**: メインドメイン（`hagakurepgm.net`）は使わず、サブドメインを使用すること

### 方法2: Gitリポジトリから連携（推奨）

1. **Gitリポジトリにプッシュ**
   ```bash
   git add scroll_guide/
   git commit -m "Add Scroll guide site"
   git push
   ```

2. **Cloudflare PagesでGit連携**
   - Pagesダッシュボード → 「プロジェクトを作成」
   - 「GitHub」または「GitLab」を選択
   - リポジトリを選択
   - ビルド設定:
     - ビルドコマンド: （空白）
     - ビルド出力ディレクトリ: `scroll_guide`

3. **デプロイ**
   - 「デプロイ」をクリック
   - 自動的にデプロイされます

## カスタムドメイン設定時の注意

⚠️ **重要**: メインドメイン（`hagakurepgm.net`）を直接使用すると、メインサイトが閲覧不能になる可能性があります。

**推奨**: サブドメインを使用
- `guide.hagakurepgm.net`
- `howto.hagakurepgm.net`
- `help.hagakurepgm.net`

## 更新方法

### 直接アップロードの場合
1. `index.html` を編集
2. Cloudflare Pagesダッシュボードから再アップロード

### Git連携の場合
1. `index.html` を編集
2. Gitにコミット・プッシュ
3. 自動的に再デプロイされます

## ローカルで確認

ブラウザで `index.html` を直接開くか、ローカルサーバーで確認：

```bash
# Python 3の場合
cd scroll_guide
python -m http.server 8000

# ブラウザで http://localhost:8000 にアクセス
```

## カスタマイズ

- **色の変更**: `<style>` タグ内のカラーコードを変更
- **コンテンツの追加**: HTML内の各セクションを編集
- **テンプレートの追加**: 「テンプレート集」セクションに新しいテンプレートを追加

## トラブルシューティング

### デプロイ後、ページが表示されない
- ビルド出力ディレクトリの設定を確認
- `index.html` がルートディレクトリにあることを確認

### カスタムドメインが反映されない
- DNS設定を確認（CNAMEレコード）
- CloudflareのDNS設定でプロキシが有効になっているか確認

## 参考リンク

- [Cloudflare Pages ドキュメント](https://developers.cloudflare.com/pages/)
- [Scrollブログサイト](https://hagakurepgm.net/blog/)
