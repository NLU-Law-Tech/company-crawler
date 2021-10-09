import os,wget
import csv

def download_file(url,f_name):
    os.makedirs('./gov_data',exist_ok=True)
    wget.download(url,os.path.join('./gov_data',f_name))

if __name__ == "__main__":
    download_file('https://www.fia.gov.tw/download/9bc4de1485014443b518beb37d8f35fe','gov_data.csv')
    out_f = open('gov_list.txt','w',encoding='utf-8')
    with open('gov_data/gov_data.csv','r',encoding='utf-8') as f:
        rows = csv.DictReader(f)

        for row in rows:
            gov_unit = row['機關單位名稱                                            ']
            gov_unit = gov_unit.strip()
            out_f.write(f"{gov_unit}\n")


    