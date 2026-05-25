"""
共享内容过滤模块 v5
- robotaxi公司账号：宽松过滤（运营/技术/合作相关内容都保留）
- 其他账号：严格过滤（只通过1个关键词匹配，但先过负面关键词兜底）
"""
import re

# ==================== 严格关键词（非robotaxi公司账号用）====================
STRICT_KEYWORDS = [
    "robotaxi", "robo-taxi", "cybercab",
    "autonomous vehicle", "autonomous driving", "autonomous fleet",
    "autonomous ride", "autonomous taxi", "autonomous mobility",
    "self-driving vehicle", "self-driving car", "self-driving taxi",
    "self driving vehicle", "self driving car", "self driving taxi",
    "driverless ride", "driverless taxi", "driverless car",
    "driverless vehicle", "driverless miles", "driverless fleet",
    "fsd", "full self-driving", "full self driving",
    "lidar", "motion planning", "perception system",
    "l4 autonomous", "level 4 autonomous",
    "robotaxi service", "autonomous ride-hail",
    "commercial autonomous", "autonomous operation",
    "无人驾驶", "自动驾驶", "萝卜快跑",
    "文远知行", "小马智行", "元戎启行", "黑芝麻智能", "滴滴自动驾驶",
    "智能驾驶",
]

# ==================== 宽松关键词（robotaxi公司账号额外匹配）====================
LIGHT_KEYWORDS = [
    # 运营扩展
    "destination", "new route", "service area",
    "offer rides", "book a ride", "ride-hail",
    "launch", "expansion", "fleet",
    # 里程/规模
    "miles", "trips", "riders", "passengers",
    "million miles", "thousand miles",
    # 合作/商业
    "partnership", "partner", "collaborat",
    "deploy", "commercial",
    # 安全/技术
    "safety", "permits", "approval", "testing",
    "ai driver", "software", "update",
    # 产品
    "app", "download", "sign up",
    "free", "available",
]

# ==================== 负面关键词（所有账号通用，匹配即过滤）====================
BLOCK_KEYWORDS = [
    # 商品/周边/活动（非robotaxi业务）
    "merchandise", "shop now", "shop.tesla", "buy now",
    "jersey", "snapback hat", "socks", "cap",
    "soccer", "fifa", "world cup", "football",
    # 纯捐赠/慈善话题
    "donated his wealth", "charities", "donation",
    # 股价/非业务讨论
    "stock price", "stock market", "share price",
    # 纯庆祝/节日/问候
    "happy mother", "happy father", "merry christmas",
    "happy new year", "happy holidays", "happy birthday",
    "good morning", "good night", "happy thanksgiving",
    "happy halloween", "for journeys",
    "subscribe now", "subscribe today", "sign up now",
]

# ==================== robotaxi 公司名单（这些公司用宽松过滤）====================
ROBOTAXI_COMPANIES = {
    "waymo", "zoox", "wayve", "aurora", "nuro", "motional",
    "weride", "we ride", "pony.ai",
}


def has_keyword(text, keywords):
    """检查文本是否包含任意关键词"""
    if not text: return False
    tl = text.lower()
    return any(kw in tl for kw in keywords)


def should_keep(text, company=""):
    if not text: return False
    tl = text.lower()

    # 0. 所有账号先过负面关键词
    if has_keyword(tl, BLOCK_KEYWORDS):
        return False

    # 1. robotaxi公司账号 → 宽松过滤（运营/技术/安全相关保留）
    if company.lower() in ROBOTAXI_COMPANIES:
        return has_keyword(tl, STRICT_KEYWORDS) or has_keyword(tl, LIGHT_KEYWORDS)

    # 2. 其他账号 → 严格过滤（匹配任意1个关键词即可，负面词已在第0步兜底）
    return has_keyword(tl, STRICT_KEYWORDS)
