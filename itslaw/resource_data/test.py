import pandas as pd
import numpy as np

import json

class DataView():

    def __init__(self, db_file):
        self.db_file = db_file

    def get_data(self):
        with open(self.db_file, "r+", encoding="UTF-8") as f:
            strings = f.read()
            f.close()
        str_ls = strings.split("\n")
        # print(str_ls[2])
        res = []
        for x in str_ls:
            try:
                res.append(dict(json.loads(x)))
            except json.decoder.JSONDecodeError:
                print("Json强转出错。")
                print(x)
        return res


def main():
    
    import os
    fu_file = os.path.dirname(os.path.abspath(__file__))
    data_file = str(os.path.join(fu_file, "db_data")) + "//" + "itslaw_detail.dat"
    dics = DataView(data_file).get_data()
    # print("dics的长度: "+str(len(dics)))
    columns = dics[0].keys()
    df = pd.DataFrame(dics)
    # [print(x) for x in columns]
    # df.to_csv(str(os.path.join(fu_file, "temp")) + "//" + "temp2.csv")

    return df


def put_x_into_LawType(x):
    """
    在单个 LawType 中插入对象
    """
    g_gaim = None
    if x:
        g_gaim = LawTypes.objects.get_or_create(
                law_type_id = x["id"],
                name = x["name"],
                law_type = x["type"],)
    return g_gaim

def put_item_to_db(gaims, k):
    """
    LawTypes 中写入数据, 返回对象的数组; 
    """
    gaim = list(gaims[k])
    g_gaims = []
    for x in gaims():
        g_gaim = put_x_into_LawType(x)
        g_gaims.append(g_gaim)
    return g_gaims


def put_data():
    
    # bulk_create 一个 List
    Cases = [] ## CaseDetails 对象的存储
    import os
    from os.path import join, dirname, abspath
    PROJECT_DIR = dirname(dirname(dirname(abspath(__file__))))
    import sys
    sys.path.insert(0, PROJECT_DIR)
    os.environ["DJANGO_SETTINGS_MODULE"] = "minicms.settings"  
    import django
    django.setup()

    df = main()
    from itslaw.models import CaseDetail, LawTypes, Keywords, SubParagraph, LawFirmInfo, OriginalOpponentLawyer
    # 
    # 写入表格; LawType 写入；LawItem写入;  Keywords 写入,  subParagraphs, similarJudgement, Regulation 写入,
    ## 逐个写入; keywords; 标识 keyword
    ##### 字段的逐个写入

    k = 20

    # 直接填充为None
    judgementExperienceInfo = None 
    proponents = df["proponents"]
    print("原告")
    g_proponent = put_item_to_db(proponents, k)
    print(g_proponent)

    originalOpponentLawyers = df["originalOpponentLawyers"]
    print("原告代理律师")
    originalOpponentLawyer = OriginalOpponentLawyer.objects.get_or_create(
        layerInfo = ,
        lawFirmInfo
    )
        
    judgementDate = df["judgementDate"]
    print("审判日期")
    print(judgementDate[k])

    previousArea =df["previousArea"]
    print("严重等级")
    print(previousArea[k])
    caseType = df["caseType"]
    print("类型")
    print(caseType[k])		
    judgementType =df["judgementType"]
    print("审判类型")
    print(judgementType[k])
    case_id = df["_id"]
    print("ID")
    print(case_id[k])

    judges =  df["judges"] 
    print("合议庭")
    print(judges[k])

    keywords = df["keywords"]
    print("guanjianci")
    print(keywords[k])

    trialRound = df["trialRound"]
    print("几审")
    print(trialRound[k])

    court = df["court"]
    print("法院")
    print(court[k])

    reason = df["reason"]
    print("原因")
    print(reason[k])

    paragraphs = df["paragraphs"]	
    print("段落")
    print(paragraphs[k])

    opponentLawyers = df["opponentLawyers"]
    print("被告律师")
    print(opponentLawyers[k])
    opponents = df["opponents"]

    print("被告方")
    print(opponents[k])

    sourceUrl = df["sourceUrl"]
    print("SourceUrl")
    print(sourceUrl[k])

    title = df["title"]
    print("title")
    print(title[k])


# main()
put_data()


