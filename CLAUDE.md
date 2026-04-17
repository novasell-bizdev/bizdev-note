# BizDev公開日誌 × note運営プロジェクト

## プロジェクト概要

**コンセプト**: 「AI時代のBizDevを考えるチーム公開日誌」

- 公開日誌の議論をそのままnote記事化し、採用ブランディング＋企業ブランディングに活用
- 完成された論考ではなく、チームで議論している過程をリアルに見せる
- 「答えを出す」ではなく「問いを立てる」スタイル

---

## ディレクトリ構成

| ディレクトリ | 役割 |
|-------------|------|
| `articles/drafts/` | 記事ドラフト（ブランチで作業→PRでレビュー） |
| `published/` | 公開済み記事アーカイブ + `content-registry.json`（メタデータ管理） |
| `meeting-notes/` | Google Meet議事録・公開日誌素材の集約先 |
| `templates/` | 記事テンプレート・レビューチェックリスト・タグ体系 |
| `assets/` | サムネイル画像等 |
| `materials/team-strategy/` | チーム方針資料（pptx等） |
| `materials/morning-sessions/` | 公開日誌発表資料（pptx等） |
| `research/` | リサーチレポート（SEO/GEO・相互リンク・ベストプラクティス） |

---

## 週次運用フロー

### 役割

| 役割 | 担当 |
|------|------|
| **発表者** | その週の公開日誌発表担当（輪番） |
| **編集長** | 馬場。記事チェック・公開判断・全体管理 |

### タイムライン

1. **月曜（チーム議論）**: 発表→議論。Google Meet 録画ON・議事録自動生成
2. **火曜**: 馬場が Meet議事録 → **GitHub Issue** に素材集約（テンプレート: `.github/ISSUE_TEMPLATE/article-issue.yml`）
3. **火～水**: 発表者がドラフト執筆（Claude Code skills支援）→ `articles/drafts/` にcommit
4. **木曜**: 発表者が **PR** 作成 → 馬場がレビュー（機密+品質チェック、テンプレート: `.github/pull_request_template.md`）
5. **金曜**: PR Merge → noteに公開 → チームSNS拡散

---

## スキル / サブエージェント

| 名前 | 種別 | トリガー | 機能 |
|------|------|---------|------|
| `/note-article` | skill | 「note記事書いて」「公開日誌記事化」 | 公開日誌素材→note記事の一気通貫オーケストレーター |
| `/title-optimizer` | skill | 「タイトル最適化」 | SEO/note検索を意識したタイトル案6パターン生成 |
| `/thumbnail-gen` | skill | 「サムネ作って」 | サムネイル用プロンプト/デザイン指示3パターン生成 |
| `article-review` | subagent | note-articleから呼び出し | 6軸品質チェック + 機密判定 |
| `cross-linker` | subagent | note-articleから呼び出し | 過去記事との関連リンク提案 |
| `/note-image-gen` | skill | 「記事の画像作って」「note画像」 | 記事内インフォグラフィック画像の設計・生成 |
| `/article-pipeline` | skill | 「パイプライン実行」「後工程やって」「仕上げて」 | 記事完成後の後工程を自動チェーン（title-optimizer→cross-linker→article-review→note-image-gen→thumbnail-gen→sns-teaser） |

---

## コンテンツ方針

### 記事カテゴリ

| カテゴリ | テーマ例 |
|---------|----------|
| AI技術の実務理解 | ベクトル検索、ナレッジグラフ、RAG |
| フレームワーク分析 | 7 Powers、MOAT、競争戦略 |
| 組織・人材論 | 頭脳労働代替、AI時代のスキル |
| AI×ビジネスモデル | 事業開発の解像度、AIネイティブBizDev |

### タグ体系

詳細は `templates/tag-taxonomy.md` を参照。

**共通タグ**: `#AIBizDev` `#ノバセルBizDev` `#AI事業開発` `#BizDev公開日誌`

### 機密基準

| 判定 | 基準 |
|------|------|
| 公開OK | 一般論・フレームワーク解説・技術知見・「業界としての問い」 |
| 要加工 | 社内事例は抽象化（具体社名・数値を除去） |
| 非公開 | 戦略方針・顧客情報・財務数値・投資判断 |

---

## トーンガイド

### 基本
- **一人称**: 「私たち」（チームの公開日誌として）
- **文体**: 「です・ます」ベース。堅すぎず柔らかすぎない
- **文字数**: 1,500～2,000字（note最適レンジ）
- **シリーズ命名**: 【BizDev公開日誌 #N】サブタイトル

### GEO最適化構造（AI検索対応）
- **結論ファースト**: 冒頭3行以内に簡潔なサマリー
- **冒頭120字**: メタディスクリプション代替。キーワード＋要約＋ベネフィット
- **リスト・テーブル活用**: AIが情報を構造的に抽出しやすくする
- **統計データ・数値**: AI引用率40%+向上（GEO研究）
- **FAQ形式**: Q&A構造はAI抽出に強い

### タイトル制約
- 30～35文字
- キーワードは前半（左側）に配置
- フォーマット: 【BizDev公開日誌 #N】サブタイトル

### サムネイル
- サイズ: 1280×670px（note推奨比率）
- シリーズロゴ「BizDev公開日誌」+ 連番 #N

### 推奨投稿時間
- 水～木曜日 12:00 or 20:00～21:00

---

## Git運用

### 記事制作（PRベース）
- 記事ドラフトはブランチで作業 → PR → 馬場がレビュー → Approve = 公開GO
- PR Merge 後、`published/` に記事を移動 + `content-registry.json` を更新
- PRテンプレートに機密チェック + 品質チェックリストを組み込み済み

### テンプレート・設定変更
- main直push可（`templates/`, `research/`, `.claude/` 等の変更）
- コミットメッセージ: `docs: {変更内容の要約}` 形式

---

## 参照資料

| ファイル | 内容 |
|---------|------|
| `research/note-seo-strategy.md` | note.com SEO/GEO戦略リサーチ |
| `research/content-interlinking-strategy.md` | 相互リンク・内部リンク戦略 |
| `research/note-writing-best-practices.md` | note記事ベストプラクティス |
| `templates/article-template.md` | 記事テンプレート |
| `templates/review-checklist.md` | レビューチェックリスト |
| `templates/tag-taxonomy.md` | タグ体系 |
