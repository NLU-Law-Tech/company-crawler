# 單位清單爬蟲
爬取並匯出單位清單(公部門+公司)

## 匯出檔案
- company_list.txt: 公司清單
- gov_list.txt: 公部門清單
- unit_list.txt: 公司+公部門清單

## 資料來源
政府開放資料僅有提供營運中公司＆異動，並不包含已解散公司。
查詢後有部分資料無法取得，故公司資料使用第三方蒐集資料。

- https://github.com/ronnywang/twcompany
- http://ronnywang-twcompany.s3-website-ap-northeast-1.amazonaws.com/files
- https://data.gov.tw/dataset/44806

## 使用
### 安裝套件
```
pip install -r requirements
```
### 爬取並匯出
```sh
sh start.sh
```