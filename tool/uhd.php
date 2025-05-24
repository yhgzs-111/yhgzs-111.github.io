<?php
$apiUrl = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN";
$curl = curl_init($apiUrl);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_HTTPHEADER, ["Accept: application/json"]);
$json = curl_exec($curl);
curl_close($curl);

$data = json_decode($json, true);
if (empty($data['images'][0]['urlbase'])) {
    header('HTTP/1.1 500 Internal Server Error');
    exit('Error fetching Bing image metadata');
}
$urlBase = $data['images'][0]['urlbase'];

$imageUrl = 'https://cn.bing.com' . $urlBase . '_UHD.jpg';

header('Content-Type: image/jpeg');
readfile($imageUrl);
exit;
?>
