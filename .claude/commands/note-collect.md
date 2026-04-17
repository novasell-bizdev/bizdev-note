# 関係者note記事の収集

登録済みアカウントの新着note記事を収集し、link-registry.mdを更新する。
週次で `/loop 7d /note-collect` として定期実行、または手動実行。

## 引数

$ARGUMENTS — 以下のいずれか:
- 省略: 全アカウントの新着を収集
- `add {noteURL}`: 新しいアカウントをレジストリに追加
- `full`: 全アカウントの全記事を再取得（初回セットアップ用）

## データソース

- レジストリ: `output/bizdev-note-project/link-registry.md`
- 生データ: `output/bizdev-note-project/note-articles-raw.json`

## 実行手順

### 通常実行（新着収集）

1. `link-registry.md` のアカウント一覧を読み込む
2. 各アカウントについて WebSearch `site:note.com/{id}` で最新記事を取得
   - ラクスル公式（note.raksul.com）のみ直近3ヶ月に限定
3. `note-articles-raw.json` と照合し、新着記事を特定
4. 新着記事があれば:
   - WebFetch で内容を読み込み、要旨（2-3文）を生成
   - 既存記事との関連セクションを判定
   - リンク推奨度を判定（A: インライン引用候補 / B: 末尾関連記事 / C: registry登録のみ）
5. `note-articles-raw.json` を更新
6. `link-registry.md` を更新
7. 新着サマリをユーザーに報告

### `add {noteURL}` モード

1. 指定URLのnoteアカウントをWebFetchでプロフィール取得
2. 全記事をWebSearchで取得
3. `link-registry.md` のアカウント一覧に追加
4. `note-articles-raw.json` に記事データを追加

### `full` モード

1. 全アカウントの全記事を再取得（WebSearch × 全アカウント）
2. `note-articles-raw.json` を全面更新
3. `link-registry.md` を全面更新

## 登録済みアカウント

link-registry.md で管理。現在の登録:
- tabemasaki（田部正志）— ノバセル代表
- tetsuro_horikawa（堀川哲朗）— ノバセルCOO
- tatsuya_manabe（真鍋達哉）— ノバセル Marketing DX事業部長
- noki_31（楠勇真）— ノバセルBizDev / FUSION CRO
- fusion_inc — FUSION公式
- maeta_r（前田遼介）— FUSION代表
- novasell_baba（馬場）— 本人
- note.raksul.com — ラクスル公式（直近3ヶ月のみ）

## 報告フォーマット

```
## note新着レポート（{date}）

### 新着記事
| アカウント | タイトル | 日付 | 推奨度 | 関連 |
|-----------|---------|------|--------|------|

### 推奨アクション
- [A推奨] {title} → 記事#Xの{section}にインライン引用を検討
```

## 注意
- 「朝会」「ミーティング」等の内部用語はnote記事に使わない（BizDev 公開日誌）
- link-registry.md の更新時、既存の記事データは保持する（追記のみ）
