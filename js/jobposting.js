/* 構造化データ（JobPosting）を content/content.js から生成して挿入 */
(function(){
  var C=window.ECO_CONTENT||{}, jobs=C.jobs||[];
  var map={"正社員":"FULL_TIME","契約社員":"CONTRACTOR","アルバイト":"PART_TIME","外注":"CONTRACTOR"};
  jobs.forEach(function(j){
    var et=[];(j.type||[]).forEach(function(t){Object.keys(map).forEach(function(k){if(t.indexOf(k)===0&&et.indexOf(map[k])<0)et.push(map[k]);});});
    var ld={"@context":"https://schema.org","@type":"JobPosting","title":j.title,"description":j.work+" "+j.quality,
      "datePosted":"2026-11-19", /* 【要確認】実際の掲載開始日に更新 */
      "hiringOrganization":{"@type":"Organization","name":"株式会社ワイズフリー","sameAs":location.origin+"/"},
      "jobLocation":{"@type":"Place","address":{"@type":"PostalAddress","postalCode":"541-0056","addressRegion":"大阪府","addressLocality":"大阪市中央区","streetAddress":"久太郎町3丁目5番5号 丸忠第一ビル5F","addressCountry":"JP"}}};
    if(et.length)ld.employmentType=et.length>1?et:et[0];
    var s=document.createElement("script");s.type="application/ld+json";s.text=JSON.stringify(ld);document.head.appendChild(s);
  });
})();
