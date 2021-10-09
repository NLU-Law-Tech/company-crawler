import gzip
import glob
import os
from loguru import logger

def decompress(infile, tofile):
    with open(infile, 'rb') as inf, open(tofile, 'w', encoding='utf8') as tof:
        decom_str = gzip.decompress(inf.read()).decode('utf-8')
        tof.write(decom_str)

if __name__ == "__main__":
    os.makedirs('./company_data/decompress',exist_ok=True)
    save_path = './company_data/decompress'
    files = glob.glob("./company_data/*.jsonl.gz")
    for file in files:
        f_name = os.path.basename(file)
        new_f_name = f_name[:-3]
        decompress_file = os.path.join(save_path,new_f_name)
        logger.info(f"{file} -> {decompress_file}")
        decompress(infile=file,tofile=decompress_file)
