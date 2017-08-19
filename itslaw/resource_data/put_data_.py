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
                law_type = x["type"],)[0]
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

    def get_case(df, k):
        # 直接填充为None
        judgementExperienceInfo = None
        ### 写入原告字段
        proponents = df["proponents"]
        g_proponent = put_item_to_db(proponents, k)
        ## 写入原告代理律师
        originalOpponentLawyers = df["originalOpponentLawyers"]
        g_originalOpponentLawyer = []
        for gaim in originalOpponentLawyers[k]:
            if gaim["layerInfo"]:
                law_info = lawFirmInfo = None
                loc_originalOpponentLawyer = OriginalOpponentLawyer.objects.get_or_create(
                        law_info = put_x_into_LawType(gaim["layerInfo"]),
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

        ## 写入合议庭
        judges =  df["judges"]
        g_proponent = put_item_to_db(judges, k)

        #0# 写入关键词
        keywords = df["keywords"]
        g_keywords = []
        for kw in keywords:
            g_kw = Keywords.objects.get_or_create(keyword=kw)[0]
            g_keywords.append(g_kw)

        ## 写入审判轮次; 几审
        trialRound = df["trialRound"]
        g_trialRound = trialRound[k]

        ## 写入法院对象
        court = df["court"]
        g_court = put_item_to_db(court, k)

        ## 写入案由
        reason = df["reason"]
        g_reason = put_item_to_db(reason, k)

        ## 写入正文
        paragraphs = df["paragraphs"]
        o_paragraphs = []
        for x in paragraphs[k]:
            # 获取正文条目 H1->text
            ### 获取text
            loc_paragraphs = []
            for p in x["paragraphs"]:
                loc_paragraph = Paragraphs.objects.get_or_create(
                        number = p["number"],
                        text = p["text"],
                        )[0]
                loc_paragraphs.append(loc_paragraph)
                summary_para = SubParagraph.objects.get_or_create(
                        paragraphs = loc_paragraphs,
                        typetext = x["typetext"],
                        typenum = x["typenum"],
                        )
                o_paragraphs.append(summary_para)

        ## 写入被告律师
        opponentLawyers = df["opponentLawyers"]
        print("被告律师")
        print(opponentLawyers[k])
        g_opponentLawyers = []
        for x in opponentLawyers[k]:
            loc_LawFirmInfo = LawFirmInfo.objects.get_or_create(
                    lawFirm = x["lawFirm"],
                    isClaimed = x["isClaimed"],
                    originalLawFirm  = x["originalLawFirm"],
                    name = x["name"],
                    originalLawyerName = x["originalLawyerName"],
                    )
            g_opponentLawyers.append(loc_LawFirmInfo)

        ## 写入被告方
        opponents = df["opponents"]
        g_opponents = put_item_to_db(opponents, k)

        ## 来源
        sourceUrl = df["sourceUrl"]
        g_sourceUrl = sourceUrl[k]

        ## 标题
        title = df["title"]
        g_title = title[k]

        Case = CaseDetail(
		proponents = g_proponents,
			originalOpponentLawyer = g_originalOpponentLawyer,
			judgementDate = g_judgementDate,
			previousArea = g_previousArea,
			caseType = g_caseType,
			judgementType = g_judgementType,
			case_id = g_case_id,
			judges = g_judges,
			keywords = g_keywords,
			trialRound = g_trialRound,
			court = g_court,
			reason = g_reason,
			paragraphs = g_paragraphs,
			caseNumber = g_caseNumber,
			opponentLawyers = g_opponentLawyers,
			opponents = g_opponents,
			title=g_title,
			publishDate = g_publishDate,
			sourceName = g_sourceName,
			sourceUrl = g_sourceUrl,
		)
        
        return Case

    CaseDetails = []
    for i in range(len(df)):
  
        try:
            print("执行过")
            g_case = get_case(df, i)
            CaseDetails.append(g_case)
        except:
            pass
   
    CaseDetail.objects.bulk_create(CaseDetails)


# main()
put_data()



