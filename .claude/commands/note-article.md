# note記事作成

朝会の発表+議論からnote記事ドラフトを一気通貫で生成するオーケストレータースキル。

## 引数
$ARGUMENTS — 朝会テーマ or 資料ファイルパス。省略時は `materials/morning-sessions/` の最新資料を使用

## 実行手順

### Phase 0: 素材整理

1. `$ARGUMENTS` から入力素材を特定:
   - ファイルパス指定時: そのファイルを読み込み
   - テーマ指定時: `materials/morning-sessions/` から該当資料を検索
   - 省略時: `materials/morning-sessions/` の最新ファイルを使用
2. 発表内容と議論メモを分離（素材内に議論メモが含まれる場合）
3. `materials/team-strategy/` からチーム方針資料も参照（整合性確認用）

### Phase 1: リサーチ（並列3エージェント）

**リサーチャーA（note同テーマ調査）** — Agent(Explore):
- note.com で同テーマの記事を調査
- どのような切り口・構成が人気かを分析
- 差別化ポイントを特定

**リサーチャーB（最新情報収集）** — Agent(Explore):
- テーマに関する最新情報をWeb検索で収集
- 統計データ・引用可能なソースを収集（GEO最適化: AI引用率40%+向上）
- 業界動向・事例を収集

**リサーチャーC（チーム方針整合性確認）** — Agent(Explore):
- `materials/team-strategy/` の資料を読み込み
- 記事内容がチーム方針と矛盾しないか確認
- 方針資料から引用・言及できるポイントを抽出

### Phase 2: 構成案作成 → ユーザー承認ゲート

リサーチ結果を統合し、`templates/article-template.md` に沿って構成案を作成:

- タイトル案（30-35文字、【BizDev朝会 #N】形式）
- H2/H3見出し構成
- 各セクションの要点（3行以内）
- カテゴリ・タグ候補
- 差別化ポイント

→ **ユーザーに構成案を提示して承認を得る**

### Phase 3: 原稿執筆

構成案に基づいて執筆。以下のトーンガイドを適用:

**トーン**:
- 一人称: 「私たち」（チームの公開日誌）
- 文体: 「です・ます」ベース
- 文字数: 1,500〜2,000字

**構成ルール**:
- 冒頭120字: メタディスクリプション代替。キーワード＋要約＋ベネフィット
- H2/H3にキーワード配置
- リスト・テーブルを活用（GEO最適化）
- 統計データ・数値を含める（AI引用率40%+向上）
- 「結論が出なかった問い」セクション必須

**禁止事項**:
- 戦略方針・顧客情報・財務数値の記載
- 社内事例の具体社名・具体数値（抽象化する）

### Phase 4: 並列サブエージェント呼び出し

以下の4つを並列実行:

1. **article-review** サブエージェント — 5軸評価 + 機密チェック
2. **cross-linker** サブエージェント — 関連リンク提案
3. `/title-optimizer` スキル — タイトル6パターン生成
4. `/thumbnail-gen` スキル — サムネイル3パターン提案

### Phase 5: 統合・修正

1. article-review の評価が合格基準未達の場合: 修正指示に基づき原稿を修正（最大2回）
2. cross-linker のリンク提案を本文に埋め込み
3. title-optimizer の結果をユーザーに提示し、タイトルを確定
4. thumbnail-gen の結果をユーザーに提示

### Phase 6: 保存

1. 記事原稿を `published/YYYY-MM-DD-slug.md` に保存
2. `published/content-registry.json` に新規エントリーを追加:

```json
{
  "id": N,
  "slug": "slug-name",
  "title": "【BizDev朝会 #N】タイトル",
  "date": "YYYY-MM-DD",
  "author": "発表者名",
  "category": "カテゴリ",
  "tags": ["#AIBizDev", "..."],
  "noteUrl": "",
  "file": "published/YYYY-MM-DD-slug.md",
  "linkedFrom": [],
  "linkedTo": []
}
```

3. ユーザーに完成報告:
   - 記事ファイルパス
   - タイトル
   - サムネイルプロンプト
   - 推奨投稿時間: 水-木 12:00 or 20:00-21:00
   - タグ5つ
   - note公開後のチェックリスト（`templates/review-checklist.md` の公開後チェックセクション）

## 出力フォーマット

```markdown
---
title: 【BizDev朝会 #N】サブタイトル
category: カテゴリ
author: 発表者名
date: YYYY-MM-DD
tags: ["#AIBizDev", "#ノバセルBizDev", "...", "...", "..."]
noteUrl: ""
---

[本文]

---

## 次に読む
[カードリンク]

## BizDev朝会シリーズ
[カードリンク]
```
