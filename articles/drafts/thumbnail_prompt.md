# サムネイル — 記事#7「AIは『作って配る』だけでは使われない ― 橋渡しという仕事」

採用：**パターンA（テキスト中心型）**
slug: `07_ai-adoption-gap` / サイズ: **1280×670px**（note推奨 1.91:1）
カテゴリ：組織・人材論 → アンバー #D97706 / アクセント=ダークブラウン #5C2E0A

## レイアウト
```
┌─────────────────────────────────┐
│ ◾BizDev公開日誌                      │  ← 左上：シリーズロゴ（小・白）
│                                     │
│     「作って配る」だけでは            │  ← 中央：メイン2行（太ゴシック）
│        使われない。                  │     「使われない」をダークブラウンで強調
│                                     │
│        ── 橋渡しという仕事            │  ← 下：細字サブコピー（白）
│                                  #7 │  ← 右下：円形 #7 バッジ
└─────────────────────────────────┘
```

## デザイン指示（Canva / Figma）
- 背景：アンバーの斜めグラデーション #D97706 →（右下）#B45309
- メインコピー：和文太ゴシック、約72pt級、白。「使われない」のみ #5C2E0A で強調
- サブコピー：「橋渡しという仕事」細字・白・約28pt、メインの下に余白を取って配置
- 左上：「BizDev公開日誌」16〜18pt、白、字間広め
- 右下：円形バッジに「#7」（白フチ／半透明ダークブラウン地）
- 全体に余白を多めに、editorial（雑誌的）でミニマルに

## テキスト（30字以内・3行）
- メイン：`「作って配る」だけでは / 使われない。`
- サブ：`── 橋渡しという仕事`

## 画像生成AIプロンプト（NanoBanana Pro / Gemini, 1280×670）
```
Minimal typographic thumbnail for a business article, 1280x670 px (1.91:1).
Warm amber diagonal gradient background (#D97706 to #B45309).
Centered bold Japanese gothic headline on two lines: 「作って配る」だけでは / 使われない。
Render the word 使われない in dark brown (#5C2E0A) for emphasis, the rest in white.
Below it, a thin white sub-line: 橋渡しという仕事.
Top-left small white series label: BizDev公開日誌.
Bottom-right circular badge: #7.
Clean, editorial, generous negative space. Japanese text rendered cleanly and correctly.
No photo, no stock imagery, no clip art, no gears, fill the whole canvas.
```

## 生成方法（GEMINI_API_KEY 入手後）
`articles/drafts/image_prompts.md` 末尾の生成コマンドを流用。出力先 `assets/drafts/07_ai-adoption-gap_thumbnail.png`。
※ 和文がAI生成で崩れる場合は、背景だけAIで作り、文字は Canva/Figma で上から組むのが確実。
