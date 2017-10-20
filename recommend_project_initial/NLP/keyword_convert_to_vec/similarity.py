# -*- coding: utf-8 -*

'''
对每一个线索提取出了关键词，如果用户输入一部分感兴趣的词，那么可通过这些词找到相关线索
在寻找线索过程中，使用多层查询
'''
def simi_clue(s):
    start_list=s.split(" ")
    index_list=[]
    file = open("lexicon.csv", errors='ignore')
    key_value = file.readlines()
    lexcion = []
    for k in range(0, len(key_value)):
        lexcion.append(key_value[k].replace("\n", ""))

    for k in range(0, len(start_list)):
        if start_list[k] in lexcion and start_list[k] != "\n":
            index_list.append(lexcion.index(start_list[k]))

    print(index_list)

    file = open("vectors2.csv", errors='ignore')
    lines = file.readlines()
    vec_dict={}
    for i in range(0,5000):
        cid_i = lines[i].split(";")[0]
        vec_i = lines[i].split(";")[1].replace("[","").replace("]","")
        vec_dict[cid_i]=vec_i

    simi={}
    for i in range(0,2):
        if len(simi)==0:
            temp={}
            for k,v in vec_dict.items():
                vec_i_list=v.split(",")
                count=0
                for k1 in range(0,len(index_list)):
                    for k2 in range(0,len(vec_i_list)):
                        if int(index_list[k1]) == int(vec_i_list[k2]):
                            count+=1
                if count>=1 :
                    temp[k]=count
            c=0
            for k1,v1 in temp.items():
                if k1 not in simi.keys():
                    simi[k1]=v1
                    c+=1
            if c==0:
                break
        else:
            temp={}
            for key,value in simi.items():
                vec_1_list =vec_dict[key].split(",")
                for k,v in vec_dict.items():
                    vec_i_list=v.split(",")
                    count=0
                    for k1 in range(0,len(vec_1_list)):
                        for k2 in range(0,len(vec_i_list)):
                            if int(vec_1_list[k1])==int(vec_i_list[k2]):
                                count+=1
                    if count>2 :
                        temp[k]=count
            c=0
            for k1,v1 in temp.items():
                if k1 not in simi.keys():
                    simi[k1]=v1
                    c+=1
            if c==0:break
        print(str(simi))
        print(len(simi))


if __name__=='__main__':
    s=input("keywords(不少于1个):")
    simi_clue(s)
    pass