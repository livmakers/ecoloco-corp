/**
 * ECOLOCO フォーム受信（Google Apps Script ウェブアプリ）
 * 受信 → スプレッドシートに記録 → 担当者へGmail通知 → 送信者へ自動返信
 * 無料（個人のGoogleアカウントの1日あたりの送信上限の範囲内）。設定手順は docs/gas-setup.md
 */
var NOTIFY_EMAIL = 'ecoloco-yahoo@ysfree.jp';   // 通知先（config.js の NOTIFY_EMAIL と同じ値に）
var SENDER_NAME  = 'ECOLOCO（株式会社ワイズフリー）';
var SHEET_ID     = '';                             // 空なら「このスクリプトに紐づくスプレッドシート」を使う
var MIN_INTERVAL_SEC = 20;                         // 同じメールアドレスからの連続送信を弾く間隔

var COLUMNS = {
  contact: ['受付日時','種別','お名前','会社名','メール','電話','お問い合わせ種別','内容','送信元ページ'],
  recruit: ['受付日時','種別','お名前','ふりがな','メール','電話','希望職種','希望雇用形態','都道府県','ポートフォリオURL','経験・自己PR','希望の連絡方法','送信元ページ']
};

function doPost(e) {
  try {
    var d = JSON.parse(e.postData.contents);
    var kind = d.kind === 'recruit' ? 'recruit' : 'contact';

    // 検証（サーバー側でも必ず確認する）
    if (d.website) return out({ ok: true });                          // ハニーポットが入っていたら黙って終了
    if (!d.name || !d.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(d.email)) return out({ ok: false, error: 'invalid' });
    if (!d.agree) return out({ ok: false, error: 'agree' });
    if (kind === 'contact' && (!d.type || !d.body)) return out({ ok: false, error: 'invalid' });
    if (kind === 'recruit' && (!d.kana || !d.tel || !d.job || !d.employment || !d.prefecture)) return out({ ok: false, error: 'invalid' });
    ['name','company','email','tel','type','body','kana','job','employment','prefecture','portfolio','pr','contact_method','page'].forEach(function (k) {
      if (d[k] && String(d[k]).length > 5000) d[k] = String(d[k]).slice(0, 5000);
    });

    // 連続送信の制限
    var cache = CacheService.getScriptCache(), ck = 'last_' + Utilities.base64Encode(d.email);
    if (cache.get(ck)) return out({ ok: false, error: 'rate' });
    cache.put(ck, '1', MIN_INTERVAL_SEC);

    var now = Utilities.formatDate(new Date(), 'Asia/Tokyo', 'yyyy/MM/dd HH:mm:ss');
    var row, label = kind === 'recruit' ? '採用応募' : 'お問い合わせ';
    if (kind === 'recruit') {
      row = [now, label, d.name, d.kana, d.email, d.tel, d.job, d.employment, d.prefecture, d.portfolio || '', d.pr || '', d.contact_method || '', d.page || ''];
    } else {
      row = [now, label, d.name, d.company || '', d.email, d.tel || '', d.type, d.body, d.page || ''];
    }

    // 1) スプレッドシートに記録（先頭が「=」「+」「-」「@」の文字列は数式として実行されないよう無害化）
    var ss = SHEET_ID ? SpreadsheetApp.openById(SHEET_ID) : SpreadsheetApp.getActiveSpreadsheet();
    var sh = ss.getSheetByName(label) || ss.insertSheet(label);
    if (sh.getLastRow() === 0) { sh.appendRow(COLUMNS[kind]); sh.setFrozenRows(1); }
    sh.appendRow(row.map(function (v) { v = String(v); return /^[=+\-@]/.test(v) ? "'" + v : v; }));

    // 2) 担当者へ通知
    var body = COLUMNS[kind].map(function (c, i) { return '■' + c + '\n' + row[i]; }).join('\n\n');
    MailApp.sendEmail({ to: NOTIFY_EMAIL, replyTo: d.email, name: SENDER_NAME, subject: '【ECOLOCO HP】' + label + '：' + d.name + ' 様', body: body });

    // 3) 送信者へ自動返信
    var intro = kind === 'recruit'
      ? 'このたびは、ECOLOCOの採用にご応募いただき、ありがとうございます。\n内容を確認のうえ、担当者よりメールまたはお電話でご連絡いたします。'
      : 'このたびは、お問い合わせいただき、ありがとうございます。\n内容を確認のうえ、担当者よりご連絡いたします。';
    MailApp.sendEmail({
      to: d.email, name: SENDER_NAME, replyTo: NOTIFY_EMAIL,
      subject: '【ECOLOCO】' + label + 'を受け付けました',
      body: d.name + ' 様\n\n' + intro + '\n\n※このメールは自動送信です。\n\n――――――――――――――――\n■送信内容\n' + body +
            '\n――――――――――――――――\n株式会社ワイズフリー（ecoloco）\n〒541-0056 大阪府大阪市中央区久太郎町3丁目5番5号 丸忠第一ビル5F\nTEL 06-6281-0800（平日 10:00〜13:00）\n'
    });
    return out({ ok: true });
  } catch (err) {
    console.error(err);
    return out({ ok: false, error: 'server' });
  }
}

function doGet() { return out({ ok: true, service: 'ecoloco-form' }); }
function out(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
