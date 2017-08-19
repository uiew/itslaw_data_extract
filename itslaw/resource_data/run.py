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
        print(str_ls[2])
        res = []
        for x in str_ls:
            try:
                res.append(dict(json.loads(x)))
            except json.decoder.JSONDecodeError:
                print("Json强转出错。")
                print(x)
        return res

    def view_obj(self, num):
        obj = self.get_data()[num]
        for key in obj.keys():
            print(obj[key])

        return


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

def put_data():
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
    judgementExperienceInfos = df["judgementExperienceInfos"]
    print("法院观点")
    print(judgementExperienceInfos)
    # 直接填充为None
    proponents = df["proponents"]
    print("审理法院")
    originalOpponentLawyer = df["originalOpponentLawyers"]
    print("被告代理律师")
    print(originalOpponentLawyer)
    judgementDate = df["judgementDate"]
    print("审判日期")
    print(judgementDate)
    nextArea = df["nextArea"]
    print("下一个")
    print(nextArea)
    isWatched = df["isWatched"]
    print("观看过")
    print(isWatched)
    canAddCaseAnalysis = df["canAddCaseAnalysis"]
    print("能不家")
    print(canAddCaseAnalysis)
    previousArea =df["previousArea"]
    print("严重等级")
    print(previousArea)
    caseType = df["caseType"]
    print("类型")
    print(caseType)		
    judgementType =df["judgementType"]
    print("审判类型")
    print(judgementType)
    case_id = df["_id"]
    print("ID")
    print(case_id)
    """
    judges =  df["judges"]
    
    print("合议庭")
    print(judges)
    keywords = df["keywords"]
    print("guanjianci")
    print(keywords)
    trialRound = df["trialRound"]
    print("几审")
    print(trialRound)
    sourceType = df["sourceType"]
    print("来源类型")
    print(sourceType)
    court = df["court"]
    print("原告")
    print(court)
    reason = df["reason"]
    print("原因")
    print(reason)
    paragraphs = df["paragraphs"]	
    print("段落")
    print(paragraphs)
    publishType = df["publishType"]
    print("出版类型")
    print(publishType)
    canAddExperience = df["canAddExperience"]
    print("能添加经验")
    print(canAddExperience)
    caseNumber = df["caseNumber"]	
    print("示例数量")
    print(caseNumber)
    opponentLawyers = df["opponentLawyers"]
    print("被告律师")
    print(opponentLawyers)
    opponents = df["opponents"]
    print("被告方")
    print(opponents)
    sourceUrl = df["sourceUrl"]
    print("SourceUrl")
    print(sourceUrl)
    """

# main()
put_data()


