# 記事レビュー（品質チェック・機密チェック）

note記事ドラフトの品質・機密チェックを実行する。4軸15項目 + 機密3段階判定。

エージェント定義: `.claude/agents/article-review.md`

## 引数

$ARGUMENTS — 以下のいずれか:
- 記事ドラフトのファイルパス（例: `output/bizdev-note-project/articles/marketing-ax/article_draft.md`）
- 省略時: ユーザーにパスまたはテキスト貼り付けを依頼

## 実行手順

1. `.claude/agents/article-review.md` を読み込み、チェック仕様を把握する

2. `$ARGUMENTS` を解析:
   - ファイルパスの場合 → Read ツールで記事を読み込む
   - テキスト貼り付けの場合 → そのまま使用
   - 省略時 → ユーザーに入力を依頼

3. エージェント定義に従い、以下の順序でチェックを実行:
   - **Step 2: 機密チェック（軸3）を最優先で実行**
   - 機密FAIL → 即停止、該当箇所をハイライトしてユーザーに報告
   - 機密PASS → Step 3: SEO/LPO/ブランドチェック（軸1, 2, 4）を実行

4. レポートをユーザーに提示:
   - 各軸のPASS/FAIL + 具体的な指摘箇所
   - FAIL項目には修正提案を併記
   - 機密3段階判定（🟢/🟡/🔴）の詳細

5. 記事と同ディレクトリに `quality_report.md` を保存（ファイルパス指定時）

## `/note-article` からの呼び出し

`/note-article` の Phase 4 で Agent ツール経由で呼び出される場合:
- PASS → Phase 4完了を報告
- FAIL → 修正指示を Article Writer に返却（最大2回差し戻し）
- 機密FAIL → 即停止・ユーザーにエスカレーション
- 3回目FAIL → ユーザーにエスカレーション
