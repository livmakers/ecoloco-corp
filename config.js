/* ECOLOCO コーポレートサイト 設定（ここだけ書き換えればOK）
   【要確認】公開前に ECOLOCO_URL と GAS_ENDPOINT を実際の値に差し替えてください */
window.ECO_CONFIG = {
  RAKUTEN_SHOP_URL: "https://www.rakuten.co.jp/auc-ecoloco/",
  YAHOO_SHOP_URL: "https://store.shopping.yahoo.co.jp/ecoloco/", // Yahoo!ショッピング公式店（ecoloco(エコロコ)Yahoo店）
  ECOLOCO_URL: "https://livmakers.github.io/ecoloco-corp/", // 【要確認】公開後のHPのURL（バナーのリンク先）
  INSTAGRAM_URL: "https://www.instagram.com/ecoloco.official/", // 公式Instagram（ecoloco.official）
  NOTIFY_EMAIL: "ecoloco-yahoo@ysfree.jp",       // 通知先（GAS側 Code.gs の NOTIFY_EMAIL と同じ値に）
  FORM_KEY: "",                  // FormSubmit有効化後のランダム文字列（入れるとメールアドレスがページから消える）
  MIN_FILL_SECONDS: 4,           // 迷惑対策：表示から送信までの最短秒数
  SUBMIT_INTERVAL_SECONDS: 60    // 迷惑対策：連続送信の間隔
};
