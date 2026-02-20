"""
Scroll ブログ執筆支援アプリ
HAGAKUREプログラミング塾のブログ「Scroll」の記事を、一緒に考えながら書くためのアプリです。
"""
import streamlit as st

st.set_page_config(
    page_title="Scroll ブログ執筆支援",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# テンプレート定義（index.html のテンプレート集と対応）
TEMPLATES = {
    "やってみた・作ってみた": {
        "description": "技術検証や制作記事向け。目的・解決方法・使用技術を整理して書けます。",
        "title_placeholder": "例: Streamlit をやってみた",
        "sections": [
            ("目的・課題", "何を目的に、どんな課題を解決しようとしたか", "textarea"),
            ("解決したいこと", "具体的に解決したい問題や実現したいこと", "textarea"),
            ("解決方法", "どのように解決したか、実装の手順や方法", "textarea"),
            ("できないこと", "現時点でできないこと、制限事項、今後の課題", "textarea"),
            ("使用技術", "使用した技術、ツール、ライブラリなど（カンマ区切りでもOK）", "text"),
        ],
        "suggested_tags": ["作ってみた", "使ってみた", "Python", "Tips"],
    },
    "気づき・学び": {
        "description": "学んだことや気づきをまとめる記事向け。",
        "title_placeholder": "例: デバッグの考え方について思ったこと",
        "sections": [
            ("何があったか", "きっかけとなった出来事や経験", "textarea"),
            ("気づいたこと", "気づきを箇条書きで（改行で1項目）", "textarea"),
            ("これからどうしたいか", "今後のアクションや考え", "textarea"),
        ],
        "suggested_tags": ["気づき", "学び", "初心者", "Tips"],
    },
    "日常・雑談": {
        "description": "日常の出来事や雑談を気軽に書く記事向け。",
        "title_placeholder": "例: 週末の出来事",
        "sections": [
            ("今日あったこと", "出来事を箇条書きで（改行で1項目）", "textarea"),
            ("感想", "思ったこと、感じたこと", "textarea"),
            ("まとめ", "一言でまとめると", "text"),
        ],
        "suggested_tags": ["日常", "雑談", "初投稿"],
    },
    "自由形式": {
        "description": "テンプレートに縛られず、見出しと本文を自由に書きます。",
        "title_placeholder": "記事のタイトル",
        "sections": [
            ("本文（マークダウン可）", "自由に書いてください。見出しは ## 見出し のように書けます。", "textarea"),
        ],
        "suggested_tags": [],
    },
}

def build_markdown(template_key: str, title: str, section_values: dict, tags: list) -> str:
    """入力からマークダウン本文を組み立てる"""
    t = TEMPLATES[template_key]
    lines = [f"# {title}", ""]

    if template_key == "自由形式":
        body = section_values.get(t["sections"][0][0], "")
        lines.append(body.strip())
        lines.append("")
    else:
        for section_name, _, _ in t["sections"]:
            value = section_values.get(section_name, "").strip()
            if not value:
                continue
            lines.append(f"## {section_name}")
            lines.append("")
            # 気づいたこと・今日あったことは箇条書きに変換（改行で分割）
            if "気づいたこと" in section_name or "今日あったこと" in section_name:
                for item in value.split("\n"):
                    item = item.strip()
                    if item:
                        lines.append(f"- {item}")
            else:
                lines.append(value)
            lines.append("")

    if tags:
        lines.append("---")
        lines.append("")
        lines.append("**タグ候補（Scrollでは4個まで）**: " + ", ".join(f"`{t}`" for t in tags))

    return "\n".join(lines).strip()


def main():
    st.title("📝 Scroll ブログ執筆支援")
    st.caption("HAGAKUREプログラミング塾のブログ「Scroll」の記事を、一緒に考えながら書くためのツールです。")

    with st.sidebar:
        st.header("📑 使い方")
        st.markdown("""
        1. **記事の種類**を選ぶ  
        2. **タイトル**と各セクションを入力  
        3. 下の**マークダウン**をコピーして、[Scroll](https://hagakurepgm.net/blog/)で記事を作成

        タグは4個まで。既存記事のタグを参考にすると統一感が出ます。
        """)
        st.link_button("📖 Scrollブログを見る", "https://hagakurepgm.net/blog/", use_container_width=True)

    template_key = st.selectbox(
        "どんな記事を書きますか？",
        options=list(TEMPLATES.keys()),
        help="テンプレートに沿って書くと構成がまとまりやすくなります。",
    )

    template = TEMPLATES[template_key]
    st.info(template["description"])

    title = st.text_input("タイトル", placeholder=template["title_placeholder"], key="title")

    st.subheader("内容を書く")
    section_values = {}
    for section_name, hint, field_type in template["sections"]:
        key = f"sec_{section_name}"
        if field_type == "textarea":
            section_values[section_name] = st.text_area(
                section_name,
                placeholder=hint,
                height=120,
                key=key,
            )
        else:
            section_values[section_name] = st.text_input(section_name, placeholder=hint, key=key)

    st.subheader("タグ（任意）")
    default_tags = template.get("suggested_tags", [])
    tag_input = st.text_input(
        "タグをカンマ区切りで入力（例: Python, Tips, 作ってみた）",
        value=", ".join(default_tags) if default_tags else "",
        key="tags",
    )
    tags = [t.strip() for t in tag_input.split(",") if t.strip()][:4]

    st.divider()
    st.subheader("📄 できあがったマークダウン")

    if title:
        markdown_body = build_markdown(template_key, title, section_values, tags)
        st.code(markdown_body, language="markdown")
        st.download_button(
            "マークダウンをダウンロード",
            data=markdown_body,
            file_name="scroll_article.md",
            mime="text/markdown",
            use_container_width=True,
        )
    else:
        st.info("タイトルを入力すると、ここにマークダウンが表示されます。")


if __name__ == "__main__":
    main()
