# 公司清單爬蟲
爬取並匯出公司清單

## 資料來源
政府開放資料僅有提供營運中公司＆異動，並不包含已解散公司。
查詢後有部分資料無法取得，故使用第三方蒐集資料。

- https://github.com/ronnywang/twcompany
- http://ronnywang-twcompany.s3-website-ap-northeast-1.amazonaws.com/files

## 使用
### 安裝套件
```
pip install -r requirements
```
### 爬取並匯出
```sh
sh start.sh
```