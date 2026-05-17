# 記事パイプライン（後工程自動チェーン）

記事ドラフト完成後の後工程スキルを自動で順次・並列実行する。
記事執筆スキル（note-article / note-draft / write-article）の完了後に呼ぶ。

## トリガー

「パイプライン実行」「後工程やって」「仕上げて」

## 引数

$ARGUMENTS — 以下のいずれか:
- 記事ドラフトのファイルパス
- 省略時: `articles/` の最新ドラフトを自動検出

オプション:
- `skip:{スキル名}` — 特定スキルをスキップ（例: `skip:cross-linker`）
- `only:{スキル名}` — 特定スキルのみ実行（例: `only:title-optimizer,note-image-gen`）

---

## パイプライン構成

```
                    [記事ドラフト]
                         │
              ┌──────────┼──────────────┐
              ▼          ▼              ▼
      ┌──────────┐ ┌──────────┐ ┌────────────┐
      │ title-   │ │ cross-   │ │ article-   │
      │optimizer │ │ linker   │ │ review     │
      └────┬─────┘ └────┬─────┘ └─────┬──────┘
           │             │             │
           ▼             ▼             ▼
        [タイトル案]  [リンク挿入]  [品質レポート]
              │          │             │
              └──────────┼─────────────┘
                         ▼
                  ★ ユーザー確認 ★
              (タイトル選択・修正反映)
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
      ┌──────────┐ ┌──────────┐ ┌──────────┐
      │thumbnail-│ │ sns-     │ │note-image│
      │ gen      │ │ teaser   │ │ -gen     │
      └──────────┘ └──────────┘ └──────────┘
              │          │          │
              ▼          ▼          ▼
        [サムネ指示] [告知文]  [記事内画像]
```

---

## 実行手順

### Step 0: 入力検証

1. 記事ドラフトのパスを確定:
   - `$ARGUMENTS` にパス指定あり → そのファイル
   - 省略時 → `articles/` 内で最新の `.md` ファイル（image_plan.md等は除外）
2. ファイル存在・最低文字数（500文字）を確認
3. `skip:` / `only:` オプションをパースし、実行対象スキルを決定

### Step 1: 並列ブラッシュアップ（3スキル同時）

以下の3スキルを **Agent で並列実行**:

**note-articleで既に実行済みかチェック:**
- note-article経由で作成された記事は、cross-linker と article-review が実行済みの場合がある
- 記事と同ディレクトリに `quality_report.md` が存在する → article-review スキップ
- 記事内にシリーズ内リンクが既に挿入されている → cross-linker スキップ

**Agent A: title-optimizer**
```
記事ドラフト「{ファイルパス}」のタイトルを最適化してください。
/title-optimizer {ファイルパス}
```

**Agent B: cross-linker**（未実行の場合のみ）
```
記事ドラフト「{ファイルパス}」に関連記事リンクを提案してください。
/cross-linker {ファイルパス}
```

**Agent C: article-review**（未実行の場合のみ）
```
記事ドラフト「{ファイルパス}」の品質チェックを実行してください。
/article-review {ファイルパス}
```

### Step 1.5: note-image-gen (plan-only) — Step 1と並列で実行可

**Agent D: note-image-gen (plan-only)**
```
記事ドラフト「{ファイルパス}」の画像配置計画とプロンプトを生成してください。
/note-image-gen {ファイルパス} plan-only
```

### Step 2: ユーザー確認ゲート

Step 1 の結果をまとめて報告:

```markdown
## パイプライン Step 1 完了

### タイトル候補（title-optimizer）
| # | タイトル案 | 文字数 | 特徴 |
|---|-----------|--------|------|
| 1 | ... | ... | ... |

### 品質チェック結果（article-review）
- 総合判定: {PASS/WARN/FAIL}
- {主要な指摘があれば1-2点}

### リンク挿入（cross-linker）
- {挿入したリンク数}件のリンクを提案/挿入済み

### 画像計画（note-image-gen）
- {枚数}枚の画像配置を計画済み

---
**次のステップに進みますか？**
タイトル番号の選択、修正指示があればここで。
「進めて」で Step 3 に進みます。
```

ユーザーの指示を待つ。修正があれば反映してから Step 3 へ。

### Step 3: 販促・ビジュアル生成（3スキル同時）

ユーザー確認後、以下を **並列実行**:

**Agent E: thumbnail-gen**
```
記事「{ファイルパス}」のサムネイルデザイン指示書を生成してください。
/thumbnail-gen {ファイルパス}
```

**Agent F: sns-teaser**
```
記事「{ファイルパス}」のSNS告知文を生成してください。
/sns-teaser {ファイルパス}
```

**Agent G: note-image-gen (generate-only)**
```
記事「{ファイルパス}」の画像を生成してください。
/note-image-gen {ファイルパス} generate-only
```

### Step 4: 最終報告

全スキルの出力をまとめて報告:

```markdown
## パイプライン完了

### 生成物一覧
| 成果物 | パス | 状態 |
|--------|------|------|
| 記事ドラフト | articles/{file} | ✅ |
| タイトル | （記事メタデータに反映済み） | ✅ |
| 品質レポート | articles/quality_report.md | ✅ |
| 記事内画像 | articles/images/{slug}/ | ✅ {N}枚 |
| サムネイル指示書 | articles/thumbnail_spec.md | ✅ 3パターン |
| SNS告知文 | articles/promotion_kit.md | ✅ |
| リンク挿入 | 記事内に反映済み | ✅ |

### 次のアクション
1. 画像・サムネを確認し、必要なら再生成を指示
2. PR作成 → レビュー
3. note公開 → SNS告知文を使って拡散
```

---

## 重複実行の防止

note-article スキルが内包している後工程:
- Phase 3.5: cross-linker（自動実行済み）
- Phase 4: article-review 相当の品質チェック（内蔵済み）
- Phase 5: sns-teaser（promotion_kit.md として出力済み）

note-article 経由の記事に対してパイプラインを実行する場合:
- cross-linker → **スキップ**（quality_report.md / リンク存在で判定）
- article-review → **スキップ**
- sns-teaser → 既存の promotion_kit.md があれば**スキップ**（`--force` で上書き可）
- title-optimizer, note-image-gen, thumbnail-gen → **常に実行**

---

## エラー対応

| エラー | 対応 |
|--------|------|
| ドラフト未検出 | ユーザーにファイルパスを確認 |
| 個別スキル失敗 | 失敗スキルを報告し、残りは続行。後から単独リトライ可 |
| GEMINI_API_KEY なし | note-image-gen をスキップし、他スキルを続行 |
| ユーザーが Step 2 で中断 | Step 1 の成果物は保持。再開時は Step 2 から |
