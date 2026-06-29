# 画像生成プロンプト — 記事#7 (slug: 07_ai-adoption-gap)

NanoBanana Pro / Gemini image 用。16:9 (1280×720)。ネイビー #1A237E ベースのシリーズ統一トーン。

---

## img_01 ― 「2つの壁」概念図（L41）

### 日本語ラベル版（推奨・本命）

```
Create a clean, minimal infographic illustration for a business article. 16:9, 1280x720.

Concept: A simple abstract figure (a single faceless person silhouette) tries to move along a horizontal path from LEFT to RIGHT. The left side is labeled as "tool delivered / 導入", the right side is the goal "定着 (adoption & results)". Two distinct vertical WALLS block the path between them.

- Wall 1 (closer to the start, before trying): a solid wall labeled "試す前の壁". Small sub-caption: "心理的ハードル". A small dice / gacha-capsule icon hints at unpredictability ("ガチャ").
- Wall 2 (after the first wall, after trying): a solid wall labeled "試した後の壁". Small sub-caption: "アウトプットの品質".
- Above the two walls, a slender BRIDGE arc spans across both walls connecting start to goal, subtly labeled "橋渡し" — it is the only way through. Render the bridge in the accent color so it reads as the solution.

Style: flat design with subtle gradients, clean infographic, professional business-magazine quality, lots of negative space but fill the whole canvas (no empty gray areas). Dark navy (#1A237E) background. Accent color: warm amber/orange (#FFB300) for the walls, bright teal (#00BCD4) for the bridge and path.
Japanese text must be rendered cleanly and correctly; keep total text to the few labels listed only.
No stock-photo aesthetics, no generic business clip art, no handshakes, no globe, no literal gears, no device frames or browser UI.
```

### 英語ラベル版（日本語が崩れる場合のフォールバック）

```
Same composition as above, but use ENGLISH labels only:
- Left start: "DELIVERED"  / Right goal: "ADOPTED"
- Wall 1: "WALL 1 — Before trying" sub: "Psychological barrier (unpredictable / 'gacha')"
- Wall 2: "WALL 2 — After trying" sub: "Output quality (direction skill)"
- Bridge arc label: "THE BRIDGE"
Clean minimal infographic, 16:9, navy #1A237E background, amber walls, teal bridge. No stock-photo look, no clip art.
```

---

## （任意）img_02 ― 打ち手マトリクス

```
Create a clean 2x2-style infographic matrix. 16:9, navy (#1A237E) background.
Two columns: "試すハードルを下げる（見通し）" and "品質を上げる".
Under quality, two sub-areas: "プロダクト側" and "人側＝ディレクション".
Place 2 minimal icon+keyword cards under each: ハンズオン / 可視化 ; 入り口設計 / フィードバック循環 ; ロールモデル伴走 / 事例共有.
Flat minimal infographic, teal & amber accents, clean Japanese labels, no clip art, fill canvas.
```

---

## 生成コマンド（APIキー設定後）

```bash
pip install google-genai
export GEMINI_API_KEY="..."
python3 - <<'PY'
from google import genai
from google.genai import types
c = genai.Client()
p = open("articles/drafts/image_prompts.md").read()  # or paste a single prompt
r = c.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents="<paste img_01 prompt here>",
    config=types.GenerateContentConfig(response_modalities=["IMAGE","TEXT"]),
)
for part in r.candidates[0].content.parts:
    if part.inline_data:
        open("articles/drafts/images/07_ai-adoption-gap/img_01.png","wb").write(part.inline_data.data)
PY
```
