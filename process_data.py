import gzip
import glob
import os
from loguru import logger
import json
import re

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
        
if __name__ == "__main__":
    # deccompress data
    os.makedirs('./company_data/decompress',exist_ok=True)
    save_path = './company_data/decompress'
    files = glob.glob("./company_data/*.jsonl.gz")
    for file in files:
        f_name = os.path.basename(file)
        new_f_name = f_name[:-3]
        decompress_file = os.path.join(save_path,new_f_name)
        logger.info(f"{file} -> {decompress_file}")
        decompress(infile=file,tofile=decompress_file)
    
    #
    company_set = set()
    files = glob.glob(os.path.join(save_path,"*.jsonl"))
    for file in files:
        logger.info(f"porcessing file: {file}")
        with open(file,'r',encoding='utf-8') as f:
            json_lines = f.readlines()
            for line in json_lines:
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
                try:
                    assert type(company_name) is str
                    if company_name != '':
                        company_set.add(company_name)
                except Exception as e:
                    logger.warning(e)
                    logger.warning(line)
                    logger.warning(company_name)
                # logger.debug(company_name)
                # logger.info(f"{line}")

    out_file = './company_list.txt'
    with open(out_file,'w',encoding='utf-8') as f:
        logger.info("wrting file...")
        for company_name in company_set:
            f.write(f"{company_name}\n")
        
