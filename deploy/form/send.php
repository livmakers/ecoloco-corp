<?php
/* フォーム送信（採用応募・お問い合わせ共通）
   JSONで受け取り → 検証 → BOSSへ通知メール → 送信者へ自動返信 */
declare(strict_types=1);
require __DIR__ . '/lib.php';
$cfg = require __DIR__ . '/mail-config.php';
mb_language('uni'); // UTF-8で送信（文字化け防止）
mb_internal_encoding('UTF-8');
date_default_timezone_set('Asia/Tokyo');

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') eco_json(['ok' => false, 'error' => 'method'], 405);
// 同じサイトからの送信のみ受け付け
$host = $_SERVER['HTTP_HOST'] ?? '';
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
$oport = parse_url($origin, PHP_URL_PORT);
$ohost = (string)parse_url($origin, PHP_URL_HOST) . ($oport ? ':' . $oport : '');
if ($origin !== '' && strcasecmp($ohost, $host) !== 0) eco_json(['ok' => false, 'error' => 'origin'], 403);

$raw = file_get_contents('php://input', false, null, 0, 64000);
$in = json_decode((string)$raw, true);
if (!is_array($in)) eco_json(['ok' => false, 'error' => 'format'], 400);

eco_session();
$token = (string)($in['_token'] ?? '');
if (empty($_SESSION['csrf']) || !hash_equals((string)$_SESSION['csrf'], $token)) eco_json(['ok' => false, 'error' => 'token'], 403);
if (time() - (int)($_SESSION['csrf_at'] ?? 0) < (int)$cfg['min_seconds']) eco_json(['ok' => false, 'error' => 'fast'], 429);
if (!empty($in['_honey'])) eco_json(['ok' => true]); // ボットには成功を装う
if (time() - (int)($_SESSION['last_send'] ?? 0) < (int)$cfg['interval_seconds']) eco_json(['ok' => false, 'error' => 'interval'], 429);
if (!eco_rate_ok((int)$cfg['max_per_hour_ip'])) eco_json(['ok' => false, 'error' => 'rate'], 429);

$kind = eco_line((string)($in['_kind'] ?? 'contact'), 40);
$email = eco_line((string)($in['email'] ?? ''), 254);
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) eco_json(['ok' => false, 'error' => 'email'], 422);
$name = eco_line((string)($in['お名前'] ?? $in['name'] ?? ''), 100);
if ($name === '') eco_json(['ok' => false, 'error' => 'name'], 422);

// 本文（_で始まる制御用項目は除外）
$lines = [];
$count = 0;
foreach ($in as $k => $v) {
  if (!is_string($k) || $k === '' || $k[0] === '_' || is_array($v)) continue;
  if (++$count > 40) break;
  $lines[] = '■' . eco_line($k, 40) . "\n" . eco_text((string)$v) . "\n";
}
$lines[] = "■送信元ページ\n" . eco_line((string)($_SERVER['HTTP_REFERER'] ?? ''), 300) . "\n";
$lines[] = "■受信日時（サーバー）\n" . date('Y-m-d H:i:s') . "\n";
$body = implode("\n", $lines);

$label = $kind === 'recruit' ? '採用応募' : ($kind === 'question' ? '採用の質問・相談' : 'お問い合わせ');
$subject = '【ecoloco】' . $label . '：' . $name . ' 様';
$fromHeader = 'From: ' . mb_encode_mimeheader($cfg['from_name'], 'UTF-8', 'B') . ' <' . $cfg['from'] . '>';
$headers = $fromHeader . "\r\nReply-To: " . $email;
$ok = mb_send_mail($cfg['to'], $subject, $body, $headers, '-f' . $cfg['from']);
if (!$ok) eco_json(['ok' => false, 'error' => 'mail'], 500);

if ($cfg['autoreply']) {
  $ar = $name . " 様\n\n" .
    "このたびは ecoloco（株式会社ワイズフリー）へ" . $label . "いただき、ありがとうございます。\n" .
    "以下の内容で受け付けました。内容を確認のうえ、担当者よりメールでご連絡いたします。\n" .
    "数日たっても連絡がない場合は、迷惑メールフォルダもご確認ください。\n\n" .
    "--------------------------------\n" . $body . "--------------------------------\n\n" .
    "※このメールは送信専用アドレスから自動でお送りしています。\n株式会社ワイズフリー（ecoloco）\n";
  mb_send_mail($email, '【ecoloco】' . $label . 'を受け付けました', $ar, $fromHeader, '-f' . $cfg['from']);
}
$_SESSION['last_send'] = time();
unset($_SESSION['csrf']); // トークンは使い捨て
eco_json(['ok' => true]);
