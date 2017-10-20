
from ..util.NLP_tool import matchCellphone,removeSpace

def postProcess(cidlist,all_cid_source,sample_number):
    dataDict=[]
    unique_comname=[]
    for cid in cidlist:
        source=all_cid_source[cid]

        # avoid repeat comname
        comName=source['Clue_Entry_Com_Name']
        if comName in unique_comname:
            continue
        unique_comname.append(comName)

        # avoid wrong Cellphone number
        if 'Clue_Entry_Cellphone' not in source or not matchCellphone(source['Clue_Entry_Cellphone']):
            continue
        attList_clueDB = source.keys()
        for att in attList_clueDB:
            if type(source[att]) == str:
                source[att] = removeSpace(source[att])

        dataDict.append(source)
        if(len(dataDict)==sample_number):break

    return dataDict