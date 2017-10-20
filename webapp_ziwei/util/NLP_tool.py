#! -*- coding:utf-8 -*-

import jieba
from jieba import analyse
import re


def calculate_capital(raw):

    if raw is None:
        return 0.0
    numbers = re.findall('\d*\.\d+|\d+', raw)# 0.4 or 4

    ret = 0.0
    if numbers:
        ret = float(numbers[-1])
        if '万' in raw:
            ret *= 1e4
        elif '亿' in raw:
            ret *= 1e8
    if ret == 0.0:
        ret += 1.0
    return math.log10(ret)

def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring

def remove_brace_content(string):
    string=re.sub("[\(（].*?[\)）]",' ',string)  # ? means not greedy, not match as many as possible
    return string

def calculate_text(raw_str): #return wordlist
    try:
        ### quanjia banjiao
        raw_str=raw_str

        raw_str=strQ2B(raw_str)
        #####
        raw_str = re.sub("[\s+\.\!\/_,$%^*()+\"\']+|[+——！，。;,#$%^&_？、~@#￥%……&*（）:“”【】]+", " ",raw_str)
        raw_str=re.sub("[\d]+","",raw_str)
        #raw_str=re.sub(u'和',' ',raw_str.decode('utf8'))
        #raw_str=re.sub(u'及',' ',raw_str.decode('utf8'))

        ####
        split_pattern = '[\\s;,/#|]+' #s->space
        words = re.split(split_pattern, raw_str)
        words = [w for w in words if w and len(w) > 0]
        return [word for word in words]
    except:
        if isinstance(raw_str,str)==False and isinstance(raw_str,str)==False:return []

def extract_tag(stri_list):
    ll=[]

    for stri in stri_list:
        for x, w in jieba.analyse.textrank(stri, withWeight=True):
            if w>=0.0 and x not in ll:
                ll.append(x);
    return ll

def wordParsing(string):
    seg_list = jieba.cut_for_search(string)
    seg_list = [w for w in seg_list if len(w)>0]
    return seg_list

def wordParsingCut(string,cut_all = False):
    seg_list = jieba.cut(string,cut_all=cut_all)
    seg_list = [w for w in seg_list if len(w)>0]
    return seg_list

def remove_allegedNotParticipate(ll):
    ll_rst=[]
    allegedWords=['除外','不含','不包括','但','不得','未经']
    for w in ll:
        if any(aWord in w for aWord in allegedWords):
            continue
        else:ll_rst.append(w)
    return ll_rst

def getStopWord():
    stopWordList=['技术推广','研究院','研究','电子','电子产品','预包装食品',\
                  '贸易','咨询服务','工程','无一般经营项目','中心','信息','咨询',\
                  '管理','科技','研发','推广','设计','制造','制作','生产','加工','销售',\
                  '代销','许可经营项目','一般经营项目','标准','规程','定额','零售','配件','服务',\
                  '发展','开发','电子科','电子科技','批发']
    return stopWordList

def remove_digit_english_punct(str):

    raw_str=strQ2B(str)
    raw_str = re.sub("[\s+\.\!\/_,$%^*()+\"\']+|[+——！，。;,#$%^&_？、~@#￥%……&*（）:“”【】]+", " ",raw_str)
    raw_str=re.sub("[\d]+","",raw_str)
    raw_str=re.sub("[\w]+","",raw_str)
    return raw_str


def strip_word(s):
    s_origin=s
    s=s
    wordList1=['经营','从事','提供','批发','业务','制造','销售','从事','等']
    wordList2=['的','以及','和','及']
    for w in wordList1:

        s=re.sub(r"(%s)"%w,"",s);


    for w in wordList2:

        s=re.sub(r"(%s)"%w," ",s)

    return s+' '+s_origin if s!=s_origin else s_origin

def combine_parsed(ll):
    n=len(ll);
    ll_ret=[]
    for i in range(n)[:-1]:

        pair=ll[i]+ll[i+1];
        ll_ret.append(pair)
    return ll_ret
    
def getNumber(string):
    return re.sub(r'[^\+\-\d.\s]+','',string)

def getChinese(string):
    # 提取所有汉字字符    
    return re.sub(r'[^\u4e00-\u9fbf]+',' ',string)

def removeSpace(string):
    # 去掉空白字符
    return re.sub(r'\s','',string)

def simple2tradition(line):  
    # TODO 将简体转换成繁体 
    return line

def splitParagraph2Sentences(paragraph):
    # 去掉回车换行符（使用常用的标点符号分句）
    return re.split('[\r\n，、；。！？——……～,.~!?]+',paragraph)

# SSS(Space separated string)
def passage2SSS_1(strList):
    retStrList=[]
    for stri in strList:#for each doc
        if stri in ['null','NULL',None,'']:continue
        # wordListRaw = jieba.analyse.textrank(stri, withWeight=False)

        sentences = [getChinese(sentence) for sentence in splitParagraph2Sentences(stri)]
        wordListRaw = []
        [wordListRaw.extend(wordParsingCut(sentence,False)) for sentence in sentences]
        yield ' '.join(wordListRaw)

# SSS(Space separated string)
def passage2SSS_2(strList):
    retStrList=[]
    # keyword_list=[]
    for string in strList:#product str
        if isinstance(string,str):
            string = remove_brace_content(string)
            ll = [getChinese(sentence) for sentence in splitParagraph2Sentences(string)]
            ll=remove_allegedNotParticipate(ll);
            parseWord=[]
            for w in ll:
                wlist=wordParsingCut(w,True)
                wlist=[w for w in wlist if len(w)>1]
                parseWord+=wlist
            #### parsewordList ->idf high word

    #         keyword=idf_keyword(' '.join(parseWord),10);
    #         keyword_list+=keyword
    #         ####
            retStrList.append(' '.join(parseWord))

    return retStrList

def matchCellphone(numbers):
    return False if None == re.match('^1\d{10}$',str(numbers)) else True