/* ECOLOCO コーポレートサイト 設定（ここだけ書き換えればOK）
   【要確認】公開前に ECOLOCO_URL と GAS_ENDPOINT を実際の値に差し替えてください */
window.ECO_CONFIG = {
  RAKUTEN_SHOP_URL: "https://www.rakuten.co.jp/auc-ecoloco/",
  YAHOO_SHOP_URL: "",            // Yahoo!ショッピングのURLが確認できたら入れる（空なら非表示）
  ECOLOCO_URL: "https://livmakers.github.io/ecoloco-corp/", // 【要確認】公開後のHPのURL（バナーのリンク先）
  NOTIFY_EMAIL: "ecoloco-yahoo@ysfree.jp",       // 通知先（GAS側 Code.gs の NOTIFY_EMAIL と同じ値に）
  GAS_ENDPOINT: "",              // 【要設定】Google Apps Script のウェブアプリURL（docs/gas-setup.md 参照）
  MIN_FILL_SECONDS: 4,           // 迷惑対策：表示から送信までの最短秒数
  SUBMIT_INTERVAL_SECONDS: 60    // 迷惑対策：連続送信の間隔
};
