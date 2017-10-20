# -*- coding: utf-8 -*

'''
将线索关键词转成向量
get_keywords_lexicon():将所有线索词作为词库，存储
get_vector():读取词库，读取线索关键词，给出对应的位置向量
'''

import pickle
import os

def get_keywords_lexicon():
    kw_dict = {}
    files = os.listdir("filter_keywords")
    for i in range(0, len(files)):
        file_name = files[i]
        print(file_name)
        file = open("./filter_keywords/" + file_name,errors='ignore')
        lines = file.readlines()
        for j in range(0, len(lines)):
            company_id = lines[j].split(":")[0]
            words = lines[j].split(":")[1]
            word_list = words.split(" ")
            for k in range(0, len(word_list)):
                if word_list[k] not in kw_dict:
                    kw_dict[word_list[k]] = 1
        print("第" + file_name + "完成！")
    idf_dic = open("kw_dict.pkl", 'wb')
    pickle.dump(kw_dict,idf_dic)


def get_vector(num):
    file = open("lexicon.csv",errors='ignore')
    key_value = file.readlines()
    lexcion=[]
    for k in range(0,len(key_value)):
        lexcion.append(key_value[k].replace("\n",""))

    vector_file=[]
    file = open("./filter_keywords/keyword"+str(num)+".csv",errors='ignore')
    lines = file.readlines()
    for j in range(0,len(lines)):
        sig_list=[]
        company_id=lines[j].split(":")[0]
        words=lines[j].split(":")[1]
        word_list=words.split(" ")
        for k in range(0,len(word_list)):
            if word_list[k] in lexcion and word_list[k]!="\n":
                sig_list.append(lexcion.index(word_list[k]))
        # print(company_id+";"+ str(sig_list))
        vector_file.append(company_id+";"+ str(sig_list))

    file = open("vectors"+str(num)+".csv", 'a')
    for i in range(0, len(vector_file)):
        file.write(str(vector_file[i]))
        file.write('\n')
    file.close()


if __name__=='__main__':
    # 获取关键词字典表
    # get_keywords_lexicon()
    for i in range(50,100):
        if os.path.exists("./filter_keywords/keyword"+str(i)+".csv"):
            print(i)
            get_vector(i)
    pass