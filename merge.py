if __name__ == '__main__':
    files = ['company_list.txt','gov_list.txt']
    with open('unit_list.txt','w',encoding='utf-8') as out_f:
        for file in files:
            data = open(file,'r',encoding='utf-8').read().strip().split()
            for d in data:
                out_f.write(f"{d}\n")
