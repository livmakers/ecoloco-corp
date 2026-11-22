<?php
declare(strict_types=1);
function eco_session(): void {
  if (session_status() === PHP_SESSION_ACTIVE) return;
  session_name('ecoform');
  session_set_cookie_params(['lifetime' => 0, 'path' => '/', 'secure' => !empty($_SERVER['HTTPS']), 'httponly' => true, 'samesite' => 'Strict']);
  session_start();
}
function eco_json(array $a, int $code = 200): void {
  http_response_code($code);
  header('Content-Type: application/json; charset=utf-8');
  header('Cache-Control: no-store');
  header('X-Content-Type-Options: nosniff');
  echo json_encode($a, JSON_UNESCAPED_UNICODE);
  exit;
}
/* ヘッダーインジェクション対策：改行と制御文字を除去 */
function eco_line(string $s, int $max = 200): string {
  $s = preg_replace('/[\x00-\x1F\x7F]/u', ' ', $s) ?? '';
  return mb_substr(trim($s), 0, $max);
}
function eco_text(string $s, int $max = 5000): string {
  $s = str_replace(["\r\n", "\r"], "\n", $s);
  $s = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $s) ?? '';
  return mb_substr(trim($s), 0, $max);
}
/* 同一IPの送信回数制限（ファイルで記録。公開フォルダ外の一時領域を使用） */
function eco_rate_ok(int $maxPerHour): bool {
  $ip = $_SERVER['REMOTE_ADDR'] ?? '0';
  $f = sys_get_temp_dir() . '/ecoform_' . hash('sha256', $ip . __DIR__);
  $now = time();
  $list = is_file($f) ? array_filter(array_map('intval', explode(',', (string)file_get_contents($f))), fn($t) => $t > $now - 3600) : [];
  if (count($list) >= $maxPerHour) return false;
  $list[] = $now;
  file_put_contents($f, implode(',', $list), LOCK_EX);
  return true;
}
