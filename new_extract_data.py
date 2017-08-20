import pandas as pd
import numpy as np

import json

# Cases = [] ## CaseDetails 对象的存储
import os
from os.path import join, dirname, abspath
PROJECT_DIR = dirname(dirname(dirname(abspath(__file__))))
import sys
sys.path.insert(0, PROJECT_DIR)
os.environ["DJANGO_SETTINGS_MODULE"] = "minicms.settings"
import django
django.setup()

from itslaw.models import CaseDetail, LawTypes, Keywords, Paragraphs, SubParagraph, LawFirmInfo, OriginalOpponentLawyer
#

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
                print("Json强转出错.")
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
   
    if type(x) == type([]) and x != []:
        x = x[0]
    """
    在单个 LawType 中插入对象
    """
    g_gaim = None
    _id = _name = _law_type = None 
    if x:
        # print(x)
        g_gaim = LawTypes.objects.get_or_create(name = x["name"], law_type = x["type"])[0]
    return g_gaim

def put_item_to_db(gaims, k):
    """
    LawTypes 中写入数据, 返回对象的数组;
    """
    gaim = gaims[k]
    if type(gaim) == type({}):
        gaim = list(gaim)

    g_gaims = []
    for x in gaim:
        g_gaim = put_x_into_LawType(x)
        if g_gaim:
            g_gaims.append(g_gaim)
    if not g_gaim or g_gaims == []:
        return [] 
    return g_gaims


def put_data():

    # bulk_create 一个 List

    # 写入表格; LawType 写入；LawItem写入;  Keywords 写入,  subParagraphs, similarJudgement, Regulation 写入,
    ## 逐个写入; keywords; 标识 keyword
    ##### 字段的逐个写入
    
    df = main()
    # k = 23
    def get_casedetail_item(df, k):
        # 直接填充为None
        judgementExperienceInfo = None
        ### 写入原告字段
        proponents = df["proponents"]
        g_proponent = put_item_to_db(proponents, k)
        
        ## 写入原告代理律师
        g_originalOpponentLawyer = []
        if df["originalOpponentLawyers"][k]:
            for gaim in df["originalOpponentLawyers"][k]:
                if gaim["lawyerInfo"] and gaim["lawFirmInfo"]:
                    loc_originalOpponentLawyer = OriginalOpponentLawyer.objects.get_or_create(
                            layerInfo = put_x_into_LawType(gaim["lawyerInfo"]),
                            lawFirmInfo = put_x_into_LawType(gaim["lawFirmInfo"]),
                            )[0]
                    g_originalOpponentLawyer.append(loc_originalOpponentLawyer)

        ## 审判日期处理
        judgementDate = df["judgementDate"]
        g_judgementDate = judgementDate[k]

        ## 写入严重等级
        previousArea =df["previousArea"]
        g_previousArea = previousArea[k]

        ## 写入 CaseType
        caseType = df["caseType"]
        g_caseType = caseType[k]

        ## 判决类型
        judgementType =df["judgementType"]
        g_judgementType = judgementType[k]

        ## 写入ID
        case_id = df["_id"]
        g_case_id = case_id[k]["$oid"]

        g_caseNumber = df["caseNumber"][k]

        ## 写入合议庭
        judges =  df["judges"]
        g_judges = put_item_to_db(judges, k)

        #0# 写入关键词
        keywords = df["keywords"]
        g_keywords = []
        for kw in keywords[k][0]:
            g_kw = Keywords.objects.get_or_create(keyword=kw)[0]
            g_keywords.append(g_kw)

        ## 写入审判轮次; 几审
        trialRound = df["trialRound"]
        g_trialRound = trialRound[k]

        ## 写入法院对象
        court = df["court"]
        g_court = put_x_into_LawType(df["court"][k])

        ## 写入案由
        reason = df["reason"]
        g_reason = put_x_into_LawType(df["court"][k])
        ## 写入正文
        paragraphs = df["paragraphs"]
        g_paragraphs = []
        for x in paragraphs[k]:
            # 获取正文条目 H1->typeText
            ### 获取text
            loc_paragraphs = []
            for p in x["subParagraphs"]:
                loc_paragraph = Paragraphs.objects.get_or_create(
                        number = p["number"],
                        text = p["text"],
                        )[0]
                loc_paragraphs.append(loc_paragraph)
            #print(x["typeText"])
            summary_para = SubParagraph.objects.get_or_create(
                    #paragraphs = loc_paragraphs,
                    typetext = x["typeText"],
                    typenum = x["type"],
                    )[0]
            summary_para.paragraphs = loc_paragraphs
            summary_para.save()
            g_paragraphs.append(summary_para)
    

        ## 写入被告律师
        opponentLawyers = df["opponentLawyers"]
        g_opponentLawyers = []
        for x in opponentLawyers[k]:
            loc_LawFirmInfo = LawFirmInfo.objects.get_or_create(
                    lawFirm = x["lawFirm"],
                    isClaimed = x["isClaimed"],
                    originalLawFirm  = x["originalLawFirm"],
                    name = x["name"],
                    originalLawyerName = x["originalLawyerName"],
                    )[0]
            g_opponentLawyers.append(loc_LawFirmInfo)

        ## 写入被告方
        opponents = df["opponents"]
        g_opponents = []

        g_opponents = put_item_to_db(opponents, k)

        ## 来源
        g_sourceUrl = df["sourceUrl"][k]
        g_sourceName = df["sourceName"][k]
        ## 标题
        g_title = df["title"][k]

        # 发布日期
        g_publishDate = df["publishDate"][k]
        Case = CaseDetail.objects.get_or_create(
            judgementExperienceInfos = "",
            # proponents = g_proponent,
            # originalOpponentLawyer = g_originalOpponentLawyer,
            judgementDate = g_judgementDate,
            previousArea = g_previousArea,
            caseType = g_caseType,
            judgementType = g_judgementType,
            case_id = g_case_id,
            # judges = g_judges,
            # keywords = g_keywords,
            trialRound = g_trialRound,
            court = g_court,
            reason = g_reason,
            # paragraphs = g_paragraphs,
            caseNumber = g_caseNumber,
            # opponentLawyers = g_opponentLawyers,
            # opponents = g_opponents,
            title = g_title,
            publishDate = g_publishDate,
            sourceName = g_sourceName,
            sourceUrl = g_sourceUrl,
        )[0]

        Case.proponents = g_proponent
        Case.originalOpponentLawyer = g_originalOpponentLawyer
        Case.judges = g_judges
        Case.keywords = g_keywords
        Case.paragraphs = g_paragraphs
        Case.opponentLawyers = g_opponentLawyers
        Case.opponents = g_opponents
        # Case.save()
        
        return Case 
    cases = []
    for i in range(len(df)):
        try:
            cases.append(get_casedetail_item(df, i))
        except:
            print("第 "+str(i)+" 个写入失败，请进行调试和在Excel中查询结构")
    CaseDetail.bulk_create(cases)
# main()
put_data()



