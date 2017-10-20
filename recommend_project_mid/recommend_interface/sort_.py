'''
排序模块:
    1、根据模型评分排序，由高到低
    2、根据惊喜度，覆盖率等调整评分（待做）
'''
def sort_recommend_result(result_filter):
    sort_result = []
    temp = {}
    for i in range(0, len(result_filter)):
        temp[result_filter[i].split(":")[0]] = result_filter[i].split(":")[1]
        sort_result = sort_dict(temp)
    return sort_result

#对字典排序,返回结果是list
def sort_dict(dict):
    dict_sort = sorted(dict.items(), key=lambda item: item[1], reverse=True)
    return dict_sort


if __name__ == '__main__':
    pass
