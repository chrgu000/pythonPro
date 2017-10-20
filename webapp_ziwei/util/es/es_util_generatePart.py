#! -*- coding:utf-8 -*-

def generateQuery(searchFilter,should_list):
    clean_filter            =generate_clean_filter()
    province                =generate_province(searchFilter["province"])
    city                    =generate_city(searchFilter["city"])
    comname                 =generate_companyNameMust(searchFilter["comname"])
    comnameMustNot_list1    =generate_companyNameMustNotList(searchFilter["comname_mustnot"])
    position                =generate_position(searchFilter["position"])
    employeeNum             =generate_employeeNum(searchFilter["employeeNum"])
    geo                     =generate_geo(searchFilter["geo"])
    registrationYear        =generate_registrationYear(searchFilter["registrationYear"])
    called_filter           =generate_called_filter(searchFilter["companyCode"])
    cominfoRequired         =generate_cominfoRequired(searchFilter["cominfoRequired"])
    return {"bool": {
                "must_not": comnameMustNot_list1+clean_filter+called_filter,
                "must": [comname],
                "filter": [province,city,geo,employeeNum,position,registrationYear,cominfoRequired],
                "should": should_list
                }
            }

def generate_province(province):
    province={"term":{"param4":province}} if province!='' else {}
    return province

def generate_city(city):
    city={"term":{"param5":city}} if city!='' else {}
    return city

def generate_companyNameMust(comnameMust):
    comnameMust={"match_phrase":{"Clue_Entry_Com_Name": comnameMust }} if comnameMust!='' else {}
    return comnameMust

def generate_companyNameMustNotList(comnameMustNot_list):
    comnameMustNot_list1=[]
    if len(comnameMustNot_list)>=1:
        for name in comnameMustNot_list:
            if len(name.strip(' '))==0:continue
            comnameMustNot_list1.append({"match":{"Clue_Entry_Com_Name": name }})
    return comnameMustNot_list1


def generate_geo(geo):#[1,2,3,4]
    geo={} if len(geo)!=4 else {"geo_bounding_box" : {
                                    "location" : {
                                        "top_left" : {
                                            "lat" : float(geo[0].strip(' ')),
                                            "lon" : float(geo[1].strip(' '))
                                        },
                                        "bottom_right" : {
                                            "lat" : float(geo[2].strip(' ')),
                                            "lon" : float(geo[3].strip(' '))
                                        }
                                    }
                                }}
    return geo

def generate_position(position):
    position={
                "multi_match" : {
                  "query":    position,
                  "fields": [ "param1", "Clue_Entry_Major" ]
                }}if position!='' else {}
    return position

def generate_employeeNum(employeeNum):
    employeeNum={
                    "range" : {
                        "employees_num_ceilling" : {
                            "gte" : int(employeeNum)
                        }
                    }
                } if employeeNum!='' else  {}
    return employeeNum

def generate_registrationYear(registrationYear):
    registrationYear={
                    "range" : {
                        "registrationdate" : {
                            "gte" : str(registrationYear).strip(' ')+'-01-01'
                        }
                    }
                } if registrationYear!='' else  {}
    return registrationYear

def generate_clean_filter():
    clean_filter=[{"term":{"param2": -9 }}]
    return clean_filter

def generate_called_filter(companyCode):
    called_filter=[] if companyCode=='' else [{'match':{'alreadyDownload':companyCode}}]
    return called_filter

def generate_cominfoRequired(required):
    cominfoRequired = {} if not required else {"exists": {"field": "cominfo_vector"}}
    return cominfoRequired

def calc_maxnum_each_scroll(num_required,scroll_times):
    scroll_times=1 if scroll_times<=1 else int(scroll_times)
    return int(num_required/float(scroll_times))

def adjust_num_required(num_required):
    num_required=8000 if num_required>=8000 else num_required
    return num_required

def adjust_num_required_by_candiate(num_required,num_candidate):
    num_required=num_required if num_candidate>=num_required else num_candidate
    return num_required
