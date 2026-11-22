<?php
/* CSRFトークン発行：フォーム表示時にJSが取得 */
require __DIR__ . '/lib.php';
eco_session();
$_SESSION['csrf'] = bin2hex(random_bytes(32));
$_SESSION['csrf_at'] = time();
eco_json(['ok' => true, 'token' => $_SESSION['csrf']]);
