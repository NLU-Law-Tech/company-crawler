import gzip
import glob
import os
from loguru import logger
import json
import re
import csv

def decompress(infile, tofile):
    with open(infile, 'rb') as inf, open(tofile, 'w', encoding='utf8') as tof:
        decom_str = gzip.decompress(inf.read()).decode('utf-8')
        tof.write(decom_str)

def get_company_name(data):
    company_name = None
    if '商業名稱' in data:
        company_name = data['商業名稱']
    elif '分公司名稱' in data:
        company_name = data['分公司名稱']
    elif '名稱' in data:
        company_name = data['名稱']
    elif '公司名稱' in data:
        company_name = data['公司名稱']
    else:
        assert False,'get company name fail'
    
    while type(company_name) is list:
        company_name = company_name[0]
    return company_name

def get_value_by_similar_key(data,similar_key,default_value):
    for k,v in data.items():
        # logger.debug(re.match(similar_key,k))
        if re.match(similar_key,k):
            # logger.debug(f"{k} {v}")
            if v is None or v == '':
                # logger.warning('skip key:{key} due to null or none')
                continue
            return v
    return default_value

def to_date_string(date_obj):
    date_obj = list(date_obj.values())
    date_obj = [str(x) for x in date_obj]
    return '/'.join(date_obj)

if __name__ == "__main__":
    # # deccompress data
    # os.makedirs('./company_data/decompress',exist_ok=True)
    save_path = './company_data/decompress'
    # files = glob.glob("./company_data/*.jsonl.gz")
    # for file in files:
    #     f_name = os.path.basename(file)
    #     new_f_name = f_name[:-3]
    #     decompress_file = os.path.join(save_path,new_f_name)
    #     logger.info(f"{file} -> {decompress_file}")
    #     decompress(infile=file,tofile=decompress_file)
    #

    csv_file = open('company_list.csv', 'w', newline='')
    fieldnames = [
        'company_name', 
        'address',
        'company_tax_id',
        'company_stats',
        'company_capital',
        'company_setup_date',
        'company_last_stats_change_date',
        'is_branch_office'
        ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    files = glob.glob(os.path.join(save_path,"*.jsonl"))
    for file in files:
        logger.info(f"porcessing file: {file}")
        with open(file,'r',encoding='utf-8') as f:
            json_lines = f.readlines()
            for i,line in enumerate(json_lines):
                try:
                    line = re.sub(r"^[0-9]+,","",line)
                    line = json.loads(line)
                except Exception as e:
                    logger.warning(e)
                    logger.warning(file)
                    logger.warning(line)
                    logger.warning('some error happend, skip this data')
                    continue
                # 取得`公司名稱`或`商業名稱`
                company_name = get_company_name(line)
                if company_name:
                    company_info = {
                        'company_name': company_name,
                        'address': get_value_by_similar_key(line,'地址|所在地',''),
                        'company_tax_id': get_value_by_similar_key(line,'統一編號',''),
                        'company_stats': get_value_by_similar_key(line,'公司狀況',''),
                        'company_capital': get_value_by_similar_key(line,'資本額',''),
                        'company_setup_date': to_date_string(get_value_by_similar_key(line,'核准設立日期',{})),
                        'company_last_stats_change_date': to_date_string(get_value_by_similar_key(line,'最後核准變更日期',{})),
                        'is_branch_office': True if get_value_by_similar_key(line,'分公司名稱',False) else False
                    }
                    writer.writerow(company_info)
                else:
                    logger.warning('skip due to company name is null or none')
                    continue
                
                print(f"{file} {i}/{len(json_lines)} ({int(i/len(json_lines)*100)}%)",end='\r')