# Lighthouse 計測記録

**状態：未計測。** この環境にNode.js（Lighthouse実行に必要）が入っておらず、数値を取得できませんでした。数値は創作しません。

## 計測手順（公開後、Chromeで1分）
1. 公開URLをChromeで開く → F12 → 「Lighthouse」タブ → モバイル／全カテゴリ → 「分析」
2. 各ページ（TOP・ABOUT・RECRUIT・CONTACT）の Performance／Accessibility／SEO を下表に記入（目標：各90以上）

| ページ | Performance | Accessibility | SEO | 計測日 |
|---|---|---|---|---|
| TOP | | | | |
| ABOUT US | | | | |
| RECRUIT | | | | |
| CONTACT | | | | |

## 代わりに実施済みの検査（tools/verify.py・docs/verify-log.txt）
- コントラスト比：本文9.9:1／リンク・ボタン7.5〜7.95:1／補助文字5.5〜6:1（AA以上）
- 画像alt欠落：全ページ0／モバイル横スクロール：全ページ0／コンソールエラー：0
- 懸念点（計測時に見る）：Google Fontsの外部読込、楽天画像の元サイズ、JS描画のリスト
