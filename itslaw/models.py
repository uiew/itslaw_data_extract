from django.db import models


# 关键词
class Keywords(models.Model):
    keyword = models.CharField(verbose_name="关键词", max_length = 121)


# 法律相关的人物事, 通过Type区分
class LawTypes(models.Model):
    # law_type_id = models.IntegerField(verbose_name="机构或个人", default=0)
    name = models.CharField(verbose_name="机构或个人案例事名称", max_length=222)
    law_type = models.CharField(verbose_name="类型", max_length=222)


# 段落; 段落里面可以有多条；
class Paragraphs(models.Model):
    number = models.IntegerField("代表数值")
    text = models.TextField("内容")

# 详情页段落中的呈现内容; 内容ID； 判断内容为唯一ID
class SubParagraph(models.Model):
    paragraphs = models.ManyToManyField(Paragraphs, verbose_name="段落")
    typetext = models.CharField(verbose_name="H1", max_length=111, default="待填充H1")
    typenum= models.IntegerField(verbose_name="type数", default=111111)

"""
# 相似的判决
class similarJudgement(models.Model):
    similarLevel = models.IntegerField(verbose_name="相关性等级")
    attitude = models.IntegerField(verbose_name="相关性态势")
    name = models.CharField(verbose_name="代理法院", max_length=222)
    score = models.IntegerField(verbose_name="分数")
    title = models.CharField(verbose_name="相关条目标题", max_length=222)
    sj_id = models.CharField(verbose_name="相关条目ID", max_length=222)

# 法律法规分条目描述
class LawItem(models.Model):
    isHit = models.BooleanField(verbose_name="法律类型ID", default=False)
    text = models.TextField(verbose_name="法律条目内容")
    item_type_num = models.IntegerField(verbose_name="类型数量")


# 法规
class Regulation(models.Model):
    regulation_id = models.IntegerField(verbose_name="法规条目ID")
    section_paragraphs = models.ManyToManyField(LawItem, verbose_name = "法规分条目")
    judgementCount = models.IntegerField(verbose_name="判决数量统计")
    trialRoundText = models.IntegerField(verbose_name="审理程序|几审")
"""

# [{'lawFirm': '陕西夏洲律师事务所', 'isClaimed': False, 'originalLawFirm': '陕西夏洲律师事务所', 'name': '刘利兵', 'originalLawyerName': '刘利兵', 'status': 4}]
class LawFirmInfo(models.Model):
    lawFirm = models.CharField(verbose_name="事务所", max_length=123)
    isClaimed = models.BooleanField(verbose_name=False)
    originalLawFirm = models.CharField(verbose_name="事务所2", max_length=123)
    name = models.CharField(verbose_name="名字", max_length=123)
    originalLawyerName = models.CharField(verbose_name=";;;", max_length=223)


class OriginalOpponentLawyer(models.Model):
    layerInfo = models.ForeignKey(LawTypes, verbose_name='被告代理律师信息', related_name="oolli")
    lawFirmInfo = models.ForeignKey(LawTypes, verbose_name='被告代理事务所信息', related_name="oollfi")		


from datetime import datetime
## proponents, originalOpponentLawyers, judges, court, reason, opponents
class CaseDetail(models.Model):
    judgementExperienceInfos = models.TextField(verbose_name='法院观点|', default=None)	
    proponents = models.ManyToManyField(LawTypes, verbose_name='上诉人|原告', related_name = "proponent", default=None)	
    originalOpponentLawyer = models.ManyToManyField(OriginalOpponentLawyer, verbose_name='原告代理律师', related_name="ool", default=None)	
    judgementDate = models.DateField(verbose_name="裁决日期", default=datetime.now().date())
    # nextArea =  models.IntegerField(verbose_name="未知类型的 nextArea_ID")	
    # isWatched =  models.BooleanField("是否被观看", default=False)	
    # canAddCaseAnalysis = models.BooleanField("能否添加案件分析", default=False)
    previousArea = models.IntegerField(verbose_name="严重等级", default=None)		
    caseType =  models.CharField(verbose_name="案件类型", max_length=256, default=None)		
    judgementType = models.CharField(verbose_name="文书性质", max_length=256, default=None)		
    case_id = models.CharField(verbose_name="案件ID", max_length=256, default=None)	
    judges =  models.ManyToManyField(LawTypes, verbose_name='合议庭', related_name = "judge", default=None)	
    # similar_judgement = models.ManyToManyField(similarJudgement, verbose_name='相似判决|用于搜索')	
    keywords = models.ManyToManyField(Keywords, verbose_name = "关键词", default=None)
    trialRound = models.IntegerField(verbose_name="几审", default=0)
    # sourceType = models.IntegerField(verbose_name="未知类型的 sourceType_ID", default=0)
    court = models.ForeignKey(LawTypes, verbose_name='审理法院', related_name = "court", default=None)	
    reason = models.ForeignKey(LawTypes, verbose_name='案由', related_name = "reason", default=None)	
    paragraphs = models.ManyToManyField(SubParagraph, verbose_name='内容段落条目', default=None)	
    # publishType = models.IntegerField(verbose_name="出版类型", default=0)
    # canAddExperience = models.BooleanField("能否添加经验", default=False) 
    # regulation_groupBy_TrialRound_Infos = models.ManyToManyField(Regulation, verbose_name='引用法规')	
    caseNumber = models.CharField(verbose_name="案号", max_length=111, default=None)	
    opponentLawyers = models.ManyToManyField(LawFirmInfo, verbose_name='被告代理律师', default=None)	
    opponents = models.ManyToManyField(LawTypes, verbose_name='被告', default=None, related_name = "opponent")	
    title = models.CharField(verbose_name="标题", max_length=256, default=None)	
    publishDate = models.DateField(verbose_name="出版日期", default=datetime.now().date())
    sourceName =  models.CharField(verbose_name="来源名称", max_length=256, default="")	
    sourceUrl = models.CharField(verbose_name="来源URL", max_length=256, default="")	
    # 省略历史审讯字段; historicalJudgement