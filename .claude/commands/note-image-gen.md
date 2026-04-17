# note記事 画像生成

note記事ドラフトの内容に基づき、記事に挿入する画像を設計・生成する。
NanoBanana Pro（Gemini画像生成API）を使用。

## トリガー

「記事の画像作って」「note画像」「記事ビジュアル」

## 引数

$ARGUMENTS — 以下のいずれか:
- 記事ドラフトのファイルパス
- 省略時: `articles/drafts/` の最新ドラフトを探す

オプション:
- `plan-only` — 画像配置計画とプロンプトのみ生成（画像生成は実行しない）
- `generate-only` — 既存プロンプトから画像生成のみ実行

---

## Phase 1: 記事分析 + 画像配置計画

1. 記事ドラフトを読み込み、構造を把握:
   - 全セクション（h2/h3）のリスト化
   - 各セクションの文字数カウント
   - 記事全体の文字数

2. 発表資料があれば読み込む（`materials/morning-sessions/` or 引数で指定）:
   - 資料中の図表・概念図を画像化候補として抽出

3. 画像配置ルールに基づき、挿入箇所を決定:

### 画像配置ルール

| ルール | 基準 |
|--------|------|
| **間隔** | 800～1,200文字ごとに1枚。読者が長文を読み続ける疲労を防ぐ |
| **最低枚数** | 記事全体で最低2枚（サムネイル除く） |
| **最大枚数** | 記事全体で最大5枚。多すぎると読み込み速度に影響 |
| **配置位置** | セクション（h2）の直後が基本。h3の途中には入れない |
| **冒頭** | 最初の画像は導入セクション直後（800文字以内） |
| **末尾** | 「おわりに」セクションには入れない |

4. 各画像について以下を決定:
   - **挿入位置**: どのセクションの後に入れるか
   - **画像タイプ**: 概念図 / メタファー / データ可視化 / アイコン構成 / 図解
   - **伝えるべきメッセージ**: そのセクションの核心を1文で

5. 出力: 画像配置計画

```markdown
## 画像配置計画

| # | 挿入位置（セクション名の後） | タイプ | メッセージ | サイズ |
|---|---------------------------|--------|-----------|--------|
| 1 | 「～」の後 | 概念図 | ～ | 1280×720 |
| 2 | ... | ... | ... | ... |
```

`plan-only` 指定時はここで完了。

---

## Phase 2: プロンプト生成

各画像について、NanoBanana Pro用の英語プロンプトを生成。

### note記事画像の基本方針

- **スタイル**: クリーンなインフォグラフィック / コンセプト図解。LP画像ではないので、CTAボタンやセールスコピーは不要
- **アスペクト比**: 16:9（1280×720px）— noteの本文幅に最適
- **テキスト**: 最小限。キーワード2-3語のみ。長いテキストは入れない（noteの本文で説明する）
- **カラー**: ニュートラル系（ネイビー #1A237E ベース）。シリーズ統一感
- **トーン**: プロフェッショナル、知的、ミニマル。企業ブログにふさわしい品位
- **禁止**: stock photo感、generic なビジネスイラスト、握手する人、地球儀、歯車アイコンの安直な使用

### プロンプト構造

各画像のプロンプトは以下の構造で生成:

```
Create a clean infographic-style illustration for a business article.

Topic: {セクションの核心メッセージ}
Visual concept: {具体的なビジュアルコンセプト}
Key text elements: {画像内に入れるキーワード2-3語、日本語OK}

Style: Clean, minimal infographic on dark navy (#1A237E) background.
Professional business magazine quality.
Flat design with subtle gradients.
Accent color: {アクセントカラー}

Aspect ratio: 16:9 (1280x720px)
No stock photo aesthetics. No generic business clip art.
No device frames, browser UI, or mockup elements.
Fill the entire canvas — no gray empty areas.
```

### 発表資料からの変換

発表資料のスライドを参照する場合:
- スライドの図表構造を抽出し、note向けに再設計
- パワポのレイアウトをそのまま再現しない（情報密度を下げ、1メッセージに絞る）
- 色・フォントをシリーズ統一トーンに変換

---

## Phase 3: 画像生成

`generate-only` 指定時はここから開始（Phase 2の出力を読み込む）。

1. Gemini APIで画像を生成:

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
    ),
)
```

2. 生成結果を保存:
   - `articles/drafts/images/{slug}/img_01.png` ～

3. 生成結果をユーザーに提示し、修正が必要か確認

---

## Phase 4: 記事への埋め込み指示

画像が確定したら、記事ドラフトの該当箇所に画像挿入マーカーを追加:

```markdown
![セクションの要約テキスト](images/{slug}/img_01.png)
```

note投稿時は画像をアップロードして挿入する手順をユーザーに案内。

---

## 出力ファイル

```
articles/drafts/
├── {NN}_{slug}.md              # 記事本体
├── images/{slug}/
│   ├── img_01.png              # 生成画像
│   ├── img_02.png
│   └── ...
├── image_plan.md               # 画像配置計画
└── image_prompts.md            # 生成プロンプト一覧
```

## エラー対応

| エラー | 対応 |
|--------|------|
| API keyなし | 環境変数 GEMINI_API_KEY を確認 |
| 生成失敗 | プロンプトを簡略化して再試行。複雑すぎる構図は分割 |
| テキスト崩壊 | テキスト要素を減らし、キーワード1-2語に限定して再生成 |
| 品質不足 | `Award-winning infographic design` 等のメタ指示を追加 |

## 関連

- サムネイル生成: `.claude/commands/thumbnail-gen.md`（サムネ特化、別スキル）
- note記事制作: `.claude/commands/note-article.md`
