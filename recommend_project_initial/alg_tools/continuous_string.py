# -*- coding: utf-8 -*
#查找两个字符串的连续子串
def get_child(data1, data2):
    maxLength = end = tempLength = 0
    tempData = {}

    # 选择出比较长字符串
    largest = data1
    other = data2
    if len(data2) > len(data1):
        largest = data2
        other = data1

    # 将比较长的字符串每个字符及位置存在字典中，便于查找
    for i in range(len(largest)):
        if largest[i] not in tempData: tempData[largest[i]] = []
        tempData[largest[i]].append(i)

    # 遍历较短字符串准备找相同字符串
    for i in range(len(other)):
        # 如果较长字符串中没有就丢弃
        if other[i] not in tempData: continue
        # 字符重复出现，其下标存在字典中List中
        indexList = tempData[other[i]]
        # 对重复字符遍历比较，查找字串
        for index in indexList:
            firsti = i + 1
            tempLength = 1
            j = index + 1
            # 字串查找
            while firsti < len(other) and j < len(largest) and other[firsti] == largest[j]:
                tempLength += 1
                firsti += 1
                j += 1
            # 如果本次子串最长纪录下来
            if tempLength > maxLength:
                maxLength = tempLength
                end = j
        print(largest[end - maxLength:end])
    return largest[end - maxLength:end]

if __name__ == '__main__':
    #print(kmp_match("BBC ABCDAB ABCDABCDABDE", "ABCDABD"))
    print(get_child('经济永昌中路8天津-19号楼', '北京市北京经济永昌中路8'))
    pass