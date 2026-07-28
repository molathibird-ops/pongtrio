import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Literal
import asyncio
import uuid
import random
import string
import time



        
# 봇 설정
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 관리자 ID
ADMIN_ID = 819167210446127105
class AdminAlt:
    def __eq__(self, other):
        return other in (1218889894659625070, 1)

ADMIN_ID_ALT = AdminAlt()

# 채널 ID
CHANNEL_CHALLENGE_SUBMISSION = 1493603675539767347
CHANNEL_CLEAR_NOTIFICATION = 1493603721223995503
CHANNEL_U_CLEAR_NOTIFICATION = 1493603764739768473
CHANNEL_ADMIN_APPROVAL = 1493603812496244906
CHANNEL_RESCALE_NOTIFICATION = 1495416650961518663
CHANNEL_SHOP = 1457400645337219082  # 상점 채널 추가
CHANNEL_FIRST_CLEAR = 1493603987440533544  # 최초클리어 알림 채널

# 역할 ID
ROLE_U_CLEAR_PING = 1493610111703322674  # U레벨 클리어 핑
ROLE_G_CLEAR_PING = 1493610324484423791  # G레벨 클리어 핑
ROLE_FIRST_CLEAR_PING = 1493610394764443739  # 최초클리어 핑

# 서포터 역할 ID
SUPPORTER_ROLES = {
    1: 1442121622944223292,
    2: 1460673268448104510,
    3: 1460673405169963300,
    4: 1460673803829907547,
}

# 서포터 이모지
SUPPORTER_EMOJIS = {
    1: "<:s1:1439584771343777822>",
    2: "<:s2:1439584940424560811>",
    3: "<:s3:1439584901807476818>",
    4: "<:s4:1439584869796675657>",
}

# 서포터 가격 (30일 기준)
SUPPORTER_PRICES = {
    1: 2900,
    2: 4900,
    3: 9900,
    4: 19900,
}

# 서포터 혜택
SUPPORTER_CHAT_BONUS = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5}  # 채팅당 C 지급량
SUPPORTER_FEE_REDUCTION = {0: 8, 1: 6, 2: 4, 3: 2, 4: 1}  # 홀짝 수수료 %
TRANSFER_FEE_PERCENT = 5  # 송금 수수료 % (소각되는 sink)

# 코인 이모지
COIN_EMOJI = "<:chip:1457733628858728448>"

# 이모지 맵
EMOJI_MAP = {
    "P1": "<:emoji_1:1426820005131063407>",
    "P2": "<:emoji_2:1426820051180195923>",
    "P3": "<:emoji_3:1426820095895670876>",
    "P4": "<:emoji_4:1426821517655937118>",
    "P5": "<:emoji_5:1426821546902552618>",
    "P6": "<:emoji_6:1426821576300433418>",
    "P7": "<:emoji_6:1426821589827190935>",
    "P8": "<:emoji_7:1426821601206341642>",
    "P9": "<:emoji_8:1426821621531934853>",
    "P10": "<:emoji_9:1426821633254887444>",
    "P11": "<:emoji_10:1426821644285902949>",
    "P12": "<:emoji_11:1426821660480110663>",
    "P13": "<:emoji_12:1426821671792283699>",
    "P14": "<:emoji_13:1426821684442169455>",
    "P15": "<:emoji_15:1426821696379424818>",
    "P16": "<:emoji_15:1426821707926208565>",
    "P17": "<:emoji_16:1426821720043425964>",
    "P18": "<:emoji_17:1426821732781523044>",
    "P19": "<:emoji_18:1426821745737863279>",
    "P20": "<:emoji_19:1426821756580270100>",

    "G1": "<:emoji_21:1426821788469301278>",
    "G2": "<:emoji_21:1426821800356216895>",
    "G3": "<:emoji_22:1426821813152911472>",
    "G4": "<:emoji_24:1426821826872606750>",
    "G5": "<:emoji_24:1426821841057484851>",
    "G6": "<:emoji_26:1426821862041587712>",
    "G7": "<:emoji_27:1426821876650344490>",
    "G8": "<:emoji_28:1426821897248575488>",
    "G9": "<:emoji_28:1426821911802810448>",
    "G10": "<:emoji_29:1426821938734698506>",
    "G11": "<:emoji_31:1426821961807433778>",
    "G12": "<:emoji_32:1426821975816273950>",
    "G13": "<:emoji_33:1426821999224950825>",
    "G14": "<:emoji_34:1426822014844403773>",
    "G15": "<:emoji_35:1426822050563231764>",
    "G16": "<:emoji_36:1426822068355338270>",
    "G17": "<:emoji_37:1426822089016479768>",
    "G18": "<:emoji_38:1426822116732305430>",
    "G19": "<:emoji_39:1426822134281408512>",
    "G20": "<:emoji_39:1426822146470051840>",

    "U1": "<:emoji_41:1426822173774839939>",
    "U2": "<:emoji_41:1426822185921806407>",
    "U3": "<:emoji_43:1426822217492201563>",
    "U4": "<:emoji_44:1426822287163916332>",
    "U5": "<:emoji_44:1426822304003919954>",
    "U6": "<:emoji_46:1426822355195396276>",
    "U7": "<:emoji_47:1426822632824766464>",
    "U8": "<:emoji_47:1426822650440712212>",
    "U9": "<:emoji_49:1426822666915942460>",
    "U10": "<:emoji_49:1426822686679765084>",
    "U11": "<:emoji_1:1426822916066250773>",
    "U12": "<:emoji_2:1426822940397277205>",
    "U13": "<:emoji_2:1426822958755614803>",
    "U14": "<:emoji_3:1426822974274797599>",
    "U15": "<:emoji_5:1426823002540216441>",
    "U16": "<:emoji_5:1426823020919521300>",
    "U17": "<:emoji_7:1426823040284758108>",
    "U18": "<:emoji_7:1426823060807356449>",
    "U19": "<:emoji_9:1426823074388377651>",
    "U20": "<:emoji_10:1426823101580050472>",
    "censored": "<:emoji_31:1493613662508941312>",
    "impossible": "<:emoji_31:1493613711267725482>",
    "epic": "<:emoji_29:1426825290344038490>",
    "gimmick": "<:emoji_31:1493613732146970634>",
    "marathon": "<:emoji_33:1493613763381821470>",
    "T1": "<:emoji_22:1426825141479804959>",
    "T2H": "<:emoji_23:1426825183062397098>",
    "T2": "<:emoji_25:1426825213890269284>",
    "T3H": "<:emoji_25:1426825223524585473>",
    "T3": "<:emoji_26:1426825233939042405>",
    "T4": "<:emoji_28:1426825271146840084>",
    "Q0": "<:emoji_18:1426823575070838814>",
    "Q1": "<:emoji_19:1426825076355104768>",
    "Q2": "<:emoji_19:1426825086576627852>",
    "Q3": "<:emoji_21:1426825111238873270>",
    "Q4": "<:emoji_21:1426825125684314174>",
    "R0": "<:emoji_38:1494910153080963162>",
    "R1": "<:emoji_38:1494910154431529050>",
    "R2": "<:emoji_40:1494910165994967201>",
    "R3": "<:emoji_40:1494910173922459708>",
    "R4": "<:emoji_41:1494910183527415850>",
    "chip": "<:chip:1457733628858728448>",
    "S1": "<:s1:1439584771343777822>",
    "S2": "<:s2:1439584940424560811>",
    "S3": "<:s3:1439584901807476818>",
    "S4": "<:s4:1439584869796675657>",
    "P0": "<:emoji_43:1517475165410164898>",
}

# 난이도 리스트
DIFFICULTIES = (
    [f"P{i}" for i in range(1, 21)] +
    [f"G{i}" for i in range(1, 21)] +
    [f"U{i}" for i in range(1, 21)] +
    ["censored", "impossible", "epic", "gimmick", "marathon", "Q0", "Q1", "Q2", "Q3", "Q4", "R0", "R1", "R2", "R3", "R4", "P0"] +
    ["T1", "T2H", "T2", "T3H", "T3", "T4"]
)

DIFFICULTY_ORDER = [
    "censored", "impossible", "epic", "gimmick", "marathon", "P0", "Q0", "Q1", "Q2", "Q3", "Q4", "R0", "R1", "R2", "R3", "R4",
    "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10", "P11",
    "P12", "P13", "P14", "P15", "P16", "P17", "P18", "P19", "P20",
    "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10",
    "G11", "G12", "G13", "G14", "G15", "G16", "G17", "G18", "G19", "G20",
    "U1", "U2", "U3", "U4", "U5", "U6", "U7", "U8", "U9", "U10",
    "U11", "U12", "U13", "U14", "U15", "U16", "U17", "U18", "U19", "U20"
]

# PP 보상 시스템
PP_REWARD = {
    "P1": 0.1, "P2": 0.2, "P3": 0.3, "P4": 0.4, "P5": 0.5,
    "P6": 0.6, "P7": 0.7, "P8": 0.8, "P9": 0.9, "P10": 1,
    "P11": 2, "P12": 3, "P13": 5, "P14": 10, "P15": 15,
    "P16": 20, "P17": 30, "P18": 45, "P19": 60, "P20": 75,
    "G1": 100, "G2": 110, "G3": 120, "G4": 130, "G5": 140,
    "G6": 150, "G7": 160, "G8": 170, "G9": 180, "G10": 190,
    "G11": 200, "G12": 210, "G13": 220, "G14": 230, "G15": 240,
    "G16": 250, "G17": 275, "G18": 300, "G19": 350, "G20": 425,
    "U1": 500, "U2": 600, "U3": 700, "U4": 850, "U5": 1000,
    "U6": 1250, "U7": 1500, "U8": 1750, "U9": 2000, "U10": 2500,
    "U11": 3000, "U12": 4000, "U13": 5000, "U14": 7000, "U15": 10000, "U16": 15000, "U17": 20000, "U18": 30000, "U19": 40000, "U20": 50000, "Q0": 0, "Q1": 0, "Q2": 0, "Q3": 0, "Q4": 0, "R0": 0, "R1": 0, "R2": 0, "R3": 0, "R4": 0, "P0": 0.02,
    "censored": 0.01, "impossible": 0, "epic": 0.05, "gimmick": 1.5, "marathon": 3
}

ROLE_ID_MAP = {
    "P1": 1493608010885628015,
    "P2": 1493607987389140992,
    "P3": 1493607941515771965,
    "P4": 1493607902852808704,
    "P5": 1493607862742552688,
    "P6": 1493607818404561006,
    "P7": 1493607758468091985,
    "P8": 1493607729120411768,
    "P9": 1493607710883840070,
    "P10": 1493607646761062440,
    "P11": 1493607608119197787,
    "P12": 1493607580478738482,
    "P13": 1493607555635875920,
    "P14": 1493607524107292742,
    "P15": 1493607406696140871,
    "P16": 1493607404296867910,
    "P17": 1493607348768608256,
    "P18": 1493607291499581550,
    "P19": 1493607209945399429,
    "P20": 1493607185895264376,
    "G1": 1493607121089069096,
    "G2": 1493607102948839527,
    "G3": 1493607050842996856,
    "G4": 1493607004135096370,
    "G5": 1493606970190725322,
    "G6": 1493606933653884998,
    "G7": 1493606893044760710,
    "G8": 1493606856117977188,
    "G9": 1493606837885341806,
    "G10": 1493606807292084276,
    "G11": 1493606749138059304,
    "G12": 1493606705844457776,
    "G13": 1493606649825460445,
    "G14": 1493606621761507492,
    "G15": 1493606596444684339,
    "G16": 1493606553264062504,
    "G17": 1493606520263413851,
    "G18": 1493606484272218112,
    "G19": 1493606446565294180,
    "G20": 1493606379372417154,
    "U1": 1493606321419980940,
    "U2": 1493606274984837222,
    "U3": 1493606230126755850,
    "U4": 1493606198103244852,
    "U5": 1493606082084606112,
}

PROFILE_COLORS = {
    "2레벨": {"price": 300, "hex": 0xcf3d25},
    "3레벨": {"price": 600, "hex": 0xf3c71a},
    "4레벨": {"price": 1200, "hex": 0x91ff46},
    "5레벨": {"price": 2000, "hex": 0x57a4e1},
    "6레벨": {"price": 3600, "hex": 0xfe49e6},
    "7레벨": {"price": 5400, "hex": 0xfaeb9d},
    "8레벨": {"price": 8800, "hex": 0xb7fff2},
    "9레벨": {"price": 13900, "hex": 0x52f4fd},
    "10레벨": {"price": 22700, "hex": 0xfcc5e9},
    "11레벨": {"price": 45600, "hex": 0xdfdfdf},
}

# 난이도별 임베드 색상
DIFFICULTY_COLORS = {
    "P1": 0x0099FF, "P2": 0x00A2FF, "P3": 0x00AAFF, "P4": 0x00B2FF, "P5": 0x00BBFF,
    "P6": 0x00C3FF, "P7": 0x00CCFF, "P8": 0x00DDFF, "P9": 0x00E5FF, "P10": 0x00EEFF,
    "P11": 0x00FFFF, "P12": 0x00FFE8, "P13": 0x00FFD0, "P14": 0x00FFB8, "P15": 0x00FFAA,
    "P16": 0x00FF88, "P17": 0x00FF70, "P18": 0x00FF48, "P19": 0x00FF30, "P20": 0x44FF15,
    "G1": 0xF2A700, "G2": 0xF09E08, "G3": 0xEE9510, "G4": 0xED8C18, "G5": 0xEB8420,
    "G6": 0xEA7B28, "G7": 0xE87230, "G8": 0xE66938, "G9": 0xE56040, "G10": 0xE35848,
    "G11": 0xE14F4F, "G12": 0xE04657, "G13": 0xDE3D5F, "G14": 0xDC3467, "G15": 0xDB2C6F,
    "G16": 0xD92377, "G17": 0xD71A7F, "G18": 0xD61187, "G19": 0xD4088F, "G20": 0xD20097,
    "U1": 0x7B4FB2, "U2": 0x744AA8, "U3": 0x6E469F, "U4": 0x674295, "U5": 0x613E8C,
    "U6": 0x5A3A83, "U7": 0x543679, "U8": 0x4D3170, "U9": 0x472D67, "U10": 0x40295D,
    "U11": 0x3A2554, "U12": 0x33214A, "U13": 0x34214C, "U14": 0x261838, "U15": 0x20142E,
    "U16": 0x191025, "U17": 0x130C1C, "U18": 0x0C0812, "U19": 0x060409, "U20": 0x000000,
    "R0": 0xE9BA46, "R1": 0xE68C3B, "R2": 0xDC674F, "R3": 0xD93D64, "R4": 0xD51F7D,
    "Q0": 0x7A4EB2, "Q1": 0x3F1F69, "Q2": 0x1E023B, "Q3": 0x010000, "Q4": 0xFFFBF8,
    "gimmick": 0x01CC04, "marathon": 0xFAF6C9, "epic": 0x5F3001,
    "censored": 0x333333, "impossible": 0x5F3001, "P0": 0x666C75,
}

# 큐레이션 등급별 임베드 색상
CURATION_COLORS = {
    "T1": 0x93FF94, "T2H": 0x7FBFC0, "T2": 0xFFD000,
    "T3H": 0x23877E, "T3": 0xB7B7FF, "T4": 0x87F7FF,
}

TITLES = {
    "나좀치는듯ㅋ": 1000,
    "퐁이": 3240,
    "푸딩": 3240,
    "부자": 5000,
    "벼락부자": 10000,
    "금수저": 50000,
    "다이아수저": 100000,
}

C_PRODUCTS = {
    "500C": {"c_amount": 500, "price": 1000},
    "2,200C": {"c_amount": 2200, "price": 4000},
    "6,000C": {"c_amount": 6000, "price": 10000},
    "13,000C": {"c_amount": 13000, "price": 20000},
    "33,000C": {"c_amount": 33000, "price": 50000},
}

# 업적 시스템
ACHIEVEMENTS = {
    "풀 랭크포인트": {
        "description": "챌린지를 20개 깨세요!",
        "role_id": 1505500382372040855,
        "type": "clear_count",
        "requirement": 20
    },
    "인해전술": {
        "description": "챌린지를 50개 깨세요!",
        "role_id": 1505512219771932805,
        "type": "clear_count",
        "requirement": 50
    },
    "이젠 꺨게 없다": {
        "description": "챌린지를 100개 깨세요!",
        "role_id": 1505512487569854475,
        "type": "clear_count",
        "requirement": 100
    },
    "정복": {
        "description": "챌린지를 250개 깨세요!",
        "type": "clear_count",
        "requirement": 250
    },
    "RICH": {
        "description": "5,000C를 보유하세요!",
        "role_id": 1503047824269643936,
        "type": "coins",
        "requirement": 5000
    },
    "RICHER": {
        "description": "25,000C를 보유하세요!",
        "role_id": 1505570007424172213,
        "type": "coins",
        "requirement": 25000
    },
    "Planetary": {
        "description": "P레벨을 깨세요!",
        "role_id": 1505501108309590046,
        "type": "level_clear",
        "requirement": "P"
    },
    "galactic": {
        "description": "G레벨을 깨세요!",
        "role_id": 1505501380083843134,
        "type": "level_clear",
        "requirement": "G"
    },
    "universe": {
        "description": "U레벨을 깨세요!",
        "role_id": 1505501524791525376,
        "type": "level_clear",
        "requirement": "U"
    },
    "삭제됨.": {
        "description": "검열 레벨을 깨세요!",
        "role_id": 1505513031193460896,
        "type": "level_clear",
        "requirement": "censored"
    },
    "과부하": {
        "description": "과충전 1~5를 모두 깨세요!",
        "role_id": 1505502424654151743,
        "type": "specific_challenges",
        "requirement": ["20", "349", "137", "350", "138", "211", "348"]
    },
    "과부하": {
        "description": "과충전 1~5를 모두 깨세요!",
        "role_id": 1505502424654151743,
        "type": "specific_challenges",
        "requirement": ["20", "349", "137", "350", "138", "211", "348"]
    },
    "스토리텔러": {
        "description": "좀비와 버섯의 이야기를 모두 클리어하세요!",
        "role_id": 1505570299725352970,
        "type": "specific_challenges",
        "requirement": ["278", "365", "439", "459", "438", "428", "461", "460", "463", "462", "464"]
    },
    "쥬얼리": {
        "description": "쥬얼 시리즈를 모두 클리어하세요!",
        "role_id": 1505570308525133895,
        "type": "specific_challenges",
        "requirement": ["213", "205", "218", "256", "255", "304", "305", "359", "358", "282"]
    },
    "파스텔": {
        "description": "스텔라이브 시리즈를 모두 클리어하세요!",
        "role_id": 1505570308525133895,
        "type": "specific_challenges",
        "requirement": ["922", "573", "923", "924", "925", "574", "543", "266", "929", "930", "658"]
    },
    "엄지": {
        "description": "T1 큐레이션을 10개 받으세요!",
        "type": "curation_count",
        "requirement": {"level": "T1", "count": 10}
    },
    "전문업체": {
        "description": "T1 큐레이션을 100개 받으세요!",
        "type": "curation_count",
        "requirement": {"level": "T1", "count": 100}
    },
    "녹슨 사랑": {
        "description": "T2H 큐레이션을 10개 받으세요!",
        "type": "curation_count",
        "requirement": {"level": "T2H", "count": 10}
    },
    "찐사랑": {
        "description": "T2 큐레이션을 10개 받으세요!",
        "type": "curation_count",
        "requirement": {"level": "T2", "count": 10}
    },
    "유물": {
        "description": "T3H 큐레이션을 받으세요!",
        "type": "curation_count",
        "requirement": {"level": "T3H", "count": 1}
    },
    "매끈한 수상품": {
        "description": "T3 큐레이션을 받으세요!",
        "type": "curation_count",
        "requirement": {"level": "T3", "count": 1}
    },
    "큐레이터의 정점": {
        "description": "T4 큐레이션을 받으세요!",
        "type": "curation_count",
        "requirement": {"level": "T4", "count": 1}
    },
    "행성헌터": {
        "description": "P1~P20까지 모두 깨세요!",
        "type": "level_range_all",
        "requirement": {"prefix": "P", "start": 1, "end": 20}
    },
    "은하헌터": {
        "description": "G1~G20까지 모두 깨세요!",
        "type": "level_range_all",
        "requirement": {"prefix": "G", "start": 1, "end": 20}
    },
    "공장장": {
        "description": "챌린지를 100개 만드세요!",
        "type": "create_count",
        "requirement": 100
    },
    "유행 전도사": {
        "description": "본인이 만든 챌린지의 클리어자가 10명 이상이 되세요!",
        "type": "creator_clears",
        "requirement": 10
    },
    "네임드 크리에이터": {
        "description": "본인이 만든 챌린지의 클리어자가 256명 이상이 되세요!",
        "type": "creator_clears",
        "requirement": 256
    },
    "운수 좋은 날": {
        "description": "복권에서 100배 이상이 걸리세요!",
        "type": "lottery_multiplier",
        "requirement": 100
    },
    "채터": {
        "description": "채팅을 5000번 치세요!",
        "type": "chat_count",
        "requirement": 5000
    },
    "메타의 선구자": {
        "description": "최초 클리어를 10개 달성하세요!",
        "type": "first_clear_count",
        "requirement": 10
    },
    "도박왕": {
        "description": "100C 이상 베팅에서 100회 승리하세요!",
        "type": "bet_win_count",
        "requirement": 100
    },
    "시간 빌게이츠": {
        "description": "마라톤 레벨을 깨세요!",
        "type": "level_clear",
        "requirement": "marathon"
    },
    "비비드 스펙트럼": {
        "description": "모든 프로필 색상을 구매하세요! (11개)",
        "type": "all_colors",
        "requirement": None
    },
    "불가능은 없다": {
        "description": "impossible 난이도를 클리어하세요!",
        "type": "level_clear",
        "requirement": "impossible"
    },
    "책정가": {
        "description": "R0~R4 레벨 중 아무거나 클리어하세요!",
        "type": "level_set_count",
        "requirement": {"levels": ["R0", "R1", "R2", "R3", "R4"], "count": 1}
    },
    "고위급 책정가": {
        "description": "Q0~Q4 레벨 중 아무거나 클리어하세요!",
        "type": "level_set_count",
        "requirement": {"levels": ["Q0", "Q1", "Q2", "Q3", "Q4"], "count": 1}
    },
    "일반행": {
        "description": "General 점수가 Rank 점수보다 2배 이상 많아지세요!",
        "type": "general_vs_rank",
        "requirement": 2
    },
    "경유": {
        "description": "General 점수가 Rank 점수보다 3배 이상 많아지세요!",
        "type": "general_vs_rank",
        "requirement": 3
    },
    "스피드러너": {
        "description": "챌린지 등재 후 24시간 이내에 클리어하세요!",
        "type": "speedrun",
        "requirement": None
    },
    "개근상": {
        "description": "30일 연속 출석하세요!",
        "type": "checkin_streak",
        "requirement": 30
    },
    "일과": {
        "description": "7일 연속 매일 1개 이상 클리어하세요!",
        "type": "clear_day_streak",
        "requirement": 7
    },
    "콜렉터": {
        "description": "모든 칭호를 보유하세요! (커스텀 제외)",
        "type": "all_titles",
        "requirement": None
    },
    "다중우주": {
        "description": "U10 이상 난이도를 클리어하세요!",
        "type": "u_level_min",
        "requirement": 10
    },
    "무패신화": {
        "description": "홀짝 게임에서 10연승하세요!",
        "type": "holjjak_streak",
        "requirement": 10
    },
    "야행성": {
        "description": "한국 시간 기준 새벽 2~6시에 5회 클리어하세요!",
        "type": "night_clear_count",
        "requirement": 5
    },
}

# 채팅 횟수 업적의 목표치 모음 (해당 값 도달 시에만 업적 체크 호출)
CHAT_COUNT_THRESHOLDS = {
    info["requirement"] for info in ACHIEVEMENTS.values()
    if info["type"] == "chat_count"
}

def get_user_grade(total_spent: int) -> str:
    if total_spent >= 200000:
        return "루비"
    elif total_spent >= 100000:
        return "에메랄드"
    elif total_spent >= 50000:
        return "다이아몬드"
    elif total_spent >= 30000:
        return "플래티넘"
    elif total_spent >= 15000:
        return "골드"
    elif total_spent >= 5000:
        return "실버"
    elif total_spent >= 1:
        return "브론즈"
    else:
        return "일반"

chat_cooldowns = {}

def get_user_supporter_level(user_id: str) -> int:
    """유저의 서포터 레벨 반환 (0=일반, 1-4=서포터)"""
    users = load_json("users.json")
    if user_id not in users:
        return 0
    user = users[user_id]
    supporter_until = user.get("supporter_until")
    if not supporter_until:
        return 0
    from datetime import datetime
    try:
        expiry = datetime.fromisoformat(supporter_until)
        if expiry > datetime.now():
            return user.get("supporter_level", 0)
    except:
        pass
    return 0

def get_difficulty_color(difficulty: str) -> int:
    return DIFFICULTY_COLORS.get(difficulty, 0x57F287)  # 기본값: 초록

def get_difficulty_emoji(difficulty: str) -> str:
    return EMOJI_MAP.get(difficulty, f":{difficulty}:")

def get_difficulty_rank(difficulty: str) -> int:
    if difficulty.startswith("U"):
        return 40 + int(difficulty[1:])
    elif difficulty.startswith("G"):
        return 20 + int(difficulty[1:])
    elif difficulty.startswith("P"):
        return int(difficulty[1:])
    else:
        rank_map = {"censored": 65, "impossible": 66, "epic": 64, "gimmick": 63, "marathon": 62}
        return rank_map.get(difficulty, 0)

def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID or user_id == ADMIN_ID_ALT

def load_json(filename: str) -> dict:
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_json(filename: str, data: dict):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_counter(filename: str) -> int:
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

def save_counter(filename: str, value: int):
    with open(filename, 'w') as f:
        f.write(str(value))

def get_next_challenge_id() -> str:
    counter = load_counter("challenge_counter.txt")
    next_id = counter + 1
    save_counter("challenge_counter.txt", next_id)
    return str(next_id)

def fmt_pp(value) -> str:
    """PP 숫자를 표기용 문자열로. 소수점이 0이면 정수로 (1850.0 -> 1850, 250.5 -> 250.5)"""
    try:
        f = float(value)
    except (TypeError, ValueError):
        return str(value)
    if f == int(f):
        return str(int(f))
    return str(round(f, 2))

def fmt_pp_diff(value) -> str:
    """PP 변화량 표기: +250 / -250 / +250.5"""
    s = fmt_pp(abs(value))
    return f"+{s}" if value >= 0 else f"-{s}"

def get_challenge_pp(challenge: dict) -> float:
    """챌린지의 실제 PP (커스텀 PP가 있으면 우선, 없으면 난이도 기본값)"""
    cp = challenge.get("custom_pp")
    if cp is not None:
        return cp
    return PP_REWARD.get(challenge.get("actual_difficulty"), 0)

def get_clear_pp(clear: dict) -> float:
    """클리어의 실제 PP (커스텀 PP 우선)"""
    cp = clear.get("custom_pp")
    if cp is not None:
        return cp
    return PP_REWARD.get(clear.get("difficulty"), 0)

def get_current_clear_streak(date_strs) -> int:
    """가장 최근 클리어일 기준 현재 연속 클리어 일수"""
    if not date_strs:
        return 0
    try:
        days = sorted({datetime.strptime(d, "%Y-%m-%d").date() for d in date_strs})
    except Exception:
        return 0
    streak = 1
    for i in range(len(days) - 1, 0, -1):
        if (days[i] - days[i - 1]).days == 1:
            streak += 1
        else:
            break
    return streak

def make_progress_bar(current, total, length: int = 10) -> str:
    """[■■■□□] 60% 형태의 진행 바"""
    if not total or total <= 0:
        return ""
    ratio = max(0.0, min(1.0, current / total))
    filled = int(round(ratio * length))
    return f"[{'■' * filled}{'□' * (length - filled)}] {int(ratio * 100)}%"

def calculate_rank_score(user_id: str):
    clears = load_json("clears.json")
    challenges = load_json("challenges.json")
    
    user_clears = []
    for clear_id, clear in clears.items():
        if clear["user_id"] == user_id and clear["status"] == "approved":
            challenge = challenges.get(clear["challenge_id"], {})
            pp = get_clear_pp(clear)
            user_clears.append(pp)
    
    user_clears.sort(reverse=True)
    
    rank_score = 0
    for idx, pp in enumerate(user_clears[:20]):
        multiplier = 1.0 - (idx * 0.05)
        rank_score += pp * multiplier
    
    return round(rank_score, 2)

def get_first_clear_count(user_id: str, clears: dict) -> int:
    """user_id가 각 챌린지의 '최초 클리어자'인 횟수 (승인된 클리어 기준)"""
    # 챌린지별 가장 빠른 승인 클리어자 계산
    earliest = {}  # challenge_id -> (submitted_at, user_id)
    for clear in clears.values():
        if clear["status"] != "approved":
            continue
        cid = clear["challenge_id"]
        ts = clear.get("submitted_at", "")
        if cid not in earliest or ts < earliest[cid][0]:
            earliest[cid] = (ts, clear["user_id"])
    return sum(1 for ts, uid in earliest.values() if uid == user_id)

def has_consecutive_days(date_strs, n: int) -> bool:
    """날짜 문자열(YYYY-MM-DD) 집합에 n일 연속이 존재하는지 확인"""
    if not date_strs:
        return False
    try:
        days = sorted({datetime.strptime(d, "%Y-%m-%d").date() for d in date_strs})
    except Exception:
        return False
    streak = 1
    for i in range(1, len(days)):
        if (days[i] - days[i - 1]).days == 1:
            streak += 1
            if streak >= n:
                return True
        elif (days[i] - days[i - 1]).days > 1:
            streak = 1
    return streak >= n

def get_daily_clear_reward(user_id: str) -> int:
    """하루 클리어 콤보 보상 (1번째 100C, 이후 10%씩 증가, 7번째=160C에서 상한, 하루 지나면 초기화)"""
    data = load_json("daily_clears.json")
    today = datetime.now().strftime("%Y-%m-%d")
    rec = data.get(user_id, {"date": None, "count": 0})
    if rec.get("date") != today:
        rec = {"date": today, "count": 0}
    rec["count"] += 1
    data[user_id] = rec
    save_json("daily_clears.json", data)
    n = min(rec["count"], 7)  # 8번째부터는 7번째 보상(160C)으로 고정
    return int(100 * (1 + 0.1 * (n - 1)))

def is_kst_night() -> bool:
    """현재가 한국 시간 기준 새벽 2~6시인지 (야행성 업적용)"""
    kst_hour = (datetime.now(timezone.utc) + timedelta(hours=9)).hour
    return 2 <= kst_hour < 6

def get_clear_rank_score(user_id: str, challenge_id: str):
    clears = load_json("clears.json")
    challenges = load_json("challenges.json")
    
    user_clears = []
    for clear_id, clear in clears.items():
        if clear["user_id"] == user_id and clear["status"] == "approved":
            pp = get_clear_pp(clear)
            user_clears.append((clear_id, pp))
    
    user_clears.sort(key=lambda x: x[1], reverse=True)
    
    for idx, (clear_id, pp) in enumerate(user_clears[:20]):
        if clear_id == challenge_id:
            multiplier = 1.0 - (idx * 0.05)
            return round(pp * multiplier, 2)
    
    return 0

def get_user_data(user_id: str) -> dict:
    """유저 데이터 가져오기 (C, 보유금액, 칭호 등)"""
    users = load_json("users.json")
    if user_id not in users:
        users[user_id] = {
            "coins": 0,  # C (재화)
            "balance": 0,  # 보유금액 (원)
            "total_spent": 0,  # 누적금액 (원)
            "owned_colors": [],  # 보유 색상
            "owned_titles": [],  # 보유 칭호
            "equipped_title": None,  # 착용 중인 칭호
            "profile_color": None,  # 적용 중인 색상
        }
        save_json("users.json", users)
    return users[user_id]

def save_user_data(user_id: str, data: dict):
    """유저 데이터 저장"""
    users = load_json("users.json")
    users[user_id] = data
    save_json("users.json", users)

def add_coins(user_id: str, amount: int):
    """C 추가"""
    data = get_user_data(user_id)
    data["coins"] = data.get("coins", 0) + amount
    save_user_data(user_id, data)

def remove_coins(user_id: str, amount: int) -> bool:
    """C 차감 (성공 시 True)"""
    data = get_user_data(user_id)
    if data.get("coins", 0) >= amount:
        data["coins"] -= amount
        save_user_data(user_id, data)
        return True
    return False

def generate_coupon_code() -> str:
    """16자리 쿠폰코드 생성"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

def get_user_achievements(user_id: str) -> list:
    """유저가 달성한 업적 목록 반환"""
    achievements_data = load_json("achievements.json")
    return achievements_data.get(user_id, [])

def has_achievement(user_id: str, achievement_name: str) -> bool:
    """유저가 특정 업적을 이미 달성했는지 확인"""
    return achievement_name in get_user_achievements(user_id)

def add_achievement(user_id: str, achievement_name: str):
    """유저에게 업적 추가"""
    achievements_data = load_json("achievements.json")
    if user_id not in achievements_data:
        achievements_data[user_id] = []
    if achievement_name not in achievements_data[user_id]:
        achievements_data[user_id].append(achievement_name)
        save_json("achievements.json", achievements_data)
        # 달성 시각 기록 (업적랭킹용)
        times_data = load_json("achievement_times.json")
        if user_id not in times_data:
            times_data[user_id] = {}
        if achievement_name not in times_data[user_id]:
            times_data[user_id][achievement_name] = datetime.now().isoformat()
            save_json("achievement_times.json", times_data)

async def check_and_grant_achievements(user_id: str, guild: discord.Guild, trigger_type: str = None):
    """업적 조건 체크 및 부여 (중복 방지)"""
    clears = load_json("clears.json")
    challenges = load_json("challenges.json")
    user_data = get_user_data(user_id)
    
    # 유저의 승인된 클리어 목록
    user_clears = [c for c in clears.values() if c["user_id"] == user_id and c["status"] == "approved"]
    cleared_challenge_ids = [c["challenge_id"] for c in user_clears]
    cleared_difficulties = [c["difficulty"] for c in user_clears]
    
    # 유저가 만든(등재된) 챌린지 목록
    my_challenges = {cid: ch for cid, ch in challenges.items() if ch.get("creator_id") == user_id}
    
    granted_achievements = []
    
    for ach_name, ach_info in ACHIEVEMENTS.items():
        # 이미 달성한 업적은 스킵
        if has_achievement(user_id, ach_name):
            continue
        
        achieved = False
        
        if ach_info["type"] == "clear_count":
            # 클리어 개수 업적
            if len(user_clears) >= ach_info["requirement"]:
                achieved = True
        
        elif ach_info["type"] == "coins":
            # C 보유량 업적
            if user_data.get("coins", 0) >= ach_info["requirement"]:
                achieved = True
        
        elif ach_info["type"] == "level_clear":
            # 특정 레벨(P/G/U) 클리어 업적
            prefix = ach_info["requirement"]
            if any(d.startswith(prefix) for d in cleared_difficulties):
                achieved = True
        
        elif ach_info["type"] == "specific_challenges":
            # 특정 챌린지 모두 클리어 업적
            required_ids = ach_info["requirement"]
            if all(cid in cleared_challenge_ids for cid in required_ids):
                achieved = True
        
        elif ach_info["type"] == "curation_count":
            # 본인이 만든 챌린지 중 특정 큐레이션 레벨 개수 업적
            req = ach_info["requirement"]
            curation_cnt = sum(1 for ch in my_challenges.values() if ch.get("curation") == req["level"])
            if curation_cnt >= req["count"]:
                achieved = True
        
        elif ach_info["type"] == "level_range_all":
            # 특정 레벨 구간(P1~P20 등)을 모두 1개 이상 클리어 업적
            req = ach_info["requirement"]
            needed = [f"{req['prefix']}{i}" for i in range(req["start"], req["end"] + 1)]
            if all(d in cleared_difficulties for d in needed):
                achieved = True
        
        elif ach_info["type"] == "create_count":
            # 등재된 본인 챌린지 개수 업적
            if len(my_challenges) >= ach_info["requirement"]:
                achieved = True
        
        elif ach_info["type"] == "creator_clears":
            # 본인이 만든 챌린지를 클리어한 서로 다른 유저 수 업적
            my_challenge_ids = set(my_challenges.keys())
            clearers = set(
                c["user_id"] for c in clears.values()
                if c["status"] == "approved" and c["challenge_id"] in my_challenge_ids
            )
            if len(clearers) >= ach_info["requirement"]:
                achieved = True
        
        elif ach_info["type"] == "lottery_multiplier":
            # 복권 최고 배수 업적
            if user_data.get("best_lottery", 0) >= ach_info["requirement"]:
                achieved = True
        
        elif ach_info["type"] == "chat_count":
            # 누적 채팅 횟수 업적
            if user_data.get("chat_count", 0) >= ach_info["requirement"]:
                achieved = True
                
        elif ach_info["type"] == "first_clear_count":
            # 최초 클리어 개수 업적
            if get_first_clear_count(user_id, clears) >= ach_info["requirement"]:
                achieved = True
        
        elif ach_info["type"] == "got_nerfed":
            # 재책정으로 PP 손해를 본 적이 있는지
            if user_data.get("got_nerfed", False):
                achieved = True
        
        elif ach_info["type"] == "bet_win_count":
            # 100C 이상 베팅 승리 횟수 업적
            if user_data.get("bet_wins", 0) >= ach_info["requirement"]:
                achieved = True
        
        elif ach_info["type"] == "all_colors":
            # 모든 프로필 색상 보유 업적
            owned = set(user_data.get("owned_colors", []))
            if all(c in owned for c in PROFILE_COLORS.keys()):
                achieved = True
        
        elif ach_info["type"] == "level_set_count":
            # 특정 레벨 집합 중 N개 클리어 업적 (R0~R4, Q0~Q4 등)
            req = ach_info["requirement"]
            cnt = sum(1 for d in cleared_difficulties if d in req["levels"])
            if cnt >= req["count"]:
                achieved = True
        
        elif ach_info["type"] == "general_vs_rank":
            # General 점수가 Rank 점수의 N배 이상 업적
            lb = load_json("leaderboard.json").get(user_id, {})
            g = lb.get("general_score", 0)
            r = lb.get("rank_score", 0)
            if r > 0 and g >= r * ach_info["requirement"]:
                achieved = True
        
        elif ach_info["type"] == "speedrun":
            # 등재 후 24시간 이내 클리어 업적
            for c in user_clears:
                ch = challenges.get(c["challenge_id"])
                if not ch:
                    continue
                reg = ch.get("registered_at")
                sub = c.get("submitted_at")
                if not reg or not sub:
                    continue
                try:
                    delta = datetime.fromisoformat(sub) - datetime.fromisoformat(reg)
                except Exception:
                    continue
                if timedelta(0) <= delta <= timedelta(hours=24):
                    achieved = True
                    break
        
        elif ach_info["type"] == "checkin_streak":
            # 연속 출석 업적
            checkins = load_json("checkins.json")
            if checkins.get(user_id, {}).get("streak", 0) >= ach_info["requirement"]:
                achieved = True
        
        elif ach_info["type"] == "clear_day_streak":
            # N일 연속 매일 1개 이상 클리어 업적
            dates = set()
            for c in user_clears:
                sub = c.get("submitted_at")
                if sub:
                    dates.add(sub[:10])
            if has_consecutive_days(dates, ach_info["requirement"]):
                achieved = True
        
        elif ach_info["type"] == "all_titles":
            # 모든 기본 칭호 보유 업적 (커스텀 제외)
            owned = set(user_data.get("owned_titles", []))
            if all(t in owned for t in TITLES.keys()):
                achieved = True
        
        elif ach_info["type"] == "u_level_min":
            # U(요구치) 이상 난이도 클리어 업적
            for d in cleared_difficulties:
                if d.startswith("U") and d[1:].isdigit() and int(d[1:]) >= ach_info["requirement"]:
                    achieved = True
                    break
        
        elif ach_info["type"] == "holjjak_streak":
            # 홀짝 연승 업적
            if user_data.get("holjjak_streak", 0) >= ach_info["requirement"]:
                achieved = True
        
        elif ach_info["type"] == "night_clear_count":
            # 새벽 클리어 횟수 업적
            if user_data.get("night_clears", 0) >= ach_info["requirement"]:
                achieved = True
                
        if achieved:
            # 업적 저장
            add_achievement(user_id, ach_name)
            granted_achievements.append(ach_name)
            
            # 업적 달성 보상 500C 지급
            add_coins(user_id, 500)
            
            # 역할 부여 (role_id가 있는 업적만)
            try:
                if guild and ach_info.get("role_id"):
                    member = guild.get_member(int(user_id))
                    if member:
                        role = guild.get_role(ach_info["role_id"])
                        if role and role not in member.roles:
                            await member.add_roles(role)
            except Exception as e:
                print(f"업적 역할 부여 오류: {e}")
            
            # DM 발송
            try:
                if guild:
                    member = guild.get_member(int(user_id))
                    if member:
                        embed = discord.Embed(
                            title="업적 달성!",
                            description=f"**{ach_name}** 업적을 달성했습니다!",
                            color=discord.Color.gold()
                        )
                        embed.add_field(name="조건", value=ach_info["description"], inline=False)
                        embed.add_field(name="보상", value="+500C", inline=False)
                        await member.send(embed=embed)
            except Exception as e:
                print(f"업적 DM 발송 오류: {e}")
    
    return granted_achievements

# 데이터 파일 초기화
for filename in ["challenges.json", "challenge_submissions.json", "clears.json", "leaderboard.json", "users.json", "coupons.json", "packs.json", "achievements.json", "achievement_times.json", "checkins.json", "daily_clears.json"]:
    if not os.path.exists(filename):
        save_json(filename, {})

if not os.path.exists("challenge_counter.txt"):
    save_counter("challenge_counter.txt", 0)

@bot.event
async def on_ready():
    print(f'{bot.user} 봇이 준비되었습니다!')
    bot.add_view(ShopView())
    try:
        synced = await bot.tree.sync()
        print(f"명령어 동기화 완료: {len(synced)}개")
    except Exception as e:
        print(f"명령어 동기화 실패: {e}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    user_id = str(message.author.id)
    current_time = time.time()
    
    # 쿨타임 확인 (3초)
    if user_id in chat_cooldowns:
        if current_time - chat_cooldowns[user_id] < 3:
            return
    
    # 서포터 레벨에 따른 C 지급
    chat_cooldowns[user_id] = current_time
    supporter_level = get_user_supporter_level(user_id)
    c_amount = SUPPORTER_CHAT_BONUS.get(supporter_level, 1)
    add_coins(user_id, c_amount)
    
    # 누적 채팅 횟수 (도배 방지 3초 쿨타임 통과분만 인정)
    chat_user_data = get_user_data(user_id)
    chat_user_data["chat_count"] = chat_user_data.get("chat_count", 0) + 1
    save_user_data(user_id, chat_user_data)
    
    # 채팅 횟수 업적 체크 (임계값 도달 시에만 호출하여 부하 방지)
    if message.guild and chat_user_data["chat_count"] in CHAT_COUNT_THRESHOLDS:
        await check_and_grant_achievements(user_id, message.guild, trigger_type="chat_count")
    
    await bot.process_commands(message)

@bot.tree.command(name="모두검색", description="모든 챌린지를 검색합니다 (정렬 옵션 포함)")
@app_commands.describe(
    정렬="정렬 방식 (기본값: id오름차순)"
)
async def search_all_challenges(
    interaction: discord.Interaction,
    정렬: Optional[Literal["id오름차순", "id내림차순", "일자오름차순", "일자내림차순", "난이도오름차순", "난이도내림차순"]] = "id오름차순"
):
    challenges = load_json("challenges.json")
    leaderboard = load_json("leaderboard.json")
    clears = load_json("clears.json")
    
    results = [(cid, challenge) for cid, challenge in challenges.items()]
    
    if not results:
        embed = discord.Embed(
            title="챌린지 없음",
            description="등재된 챌린지가 없습니다.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    if 정렬 == "id오름차순":
        results.sort(key=lambda x: int(x[0]))
    elif 정렬 == "id내림차순":
        results.sort(key=lambda x: int(x[0]), reverse=True)
    elif 정렬 == "일자오름차순":
        results.sort(key=lambda x: x[1]["registered_at"])
    elif 정렬 == "일자내림차순":
        results.sort(key=lambda x: x[1]["registered_at"], reverse=True)
    elif 정렬 == "난이도오름차순":
        special_order = ["censored", "impossible", "epic", "gimmick", "marathon"]
        def difficulty_sort_key(item):
            difficulty = item[1]["actual_difficulty"]
            if difficulty in special_order:
                return (0, special_order.index(difficulty))
            else:
                return (1, get_difficulty_rank(difficulty))
        results.sort(key=difficulty_sort_key)
    elif 정렬 == "난이도내림차순":
        special_order = ["censored", "impossible", "epic", "gimmick", "marathon"]
        def difficulty_sort_key_desc(item):
            difficulty = item[1]["actual_difficulty"]
            if difficulty in special_order:
                return (1, len(special_order) - special_order.index(difficulty))
            else:
                return (0, 100 - get_difficulty_rank(difficulty))
        results.sort(key=difficulty_sort_key_desc)
    
    view = SearchResultsView(results, leaderboard, clears)
    embed = view.create_embed()

    try:
        await interaction.response.send_message(embed=embed, view=view)
    except discord.HTTPException as e:
        if e.status == 429:
            print("Discord Global Rate Limit")
        else:
            raise

@bot.tree.command(name="검색", description="챌린지를 검색합니다")
@app_commands.describe(
    챌린지이름="검색할 챌린지 이름 (키워드)",
    난이도="필터링할 난이도 (선택사항)"
)
async def search_challenges(
    interaction: discord.Interaction,
    챌린지이름: str,
    난이도: Optional[str] = None
):
    challenges = load_json("challenges.json")
    leaderboard = load_json("leaderboard.json")
    clears = load_json("clears.json")
    
    results = []
    for cid, challenge in challenges.items():
        if 챌린지이름.lower() in challenge["name"].lower():
            if 난이도 and challenge["actual_difficulty"] != 난이도:
                continue
            results.append((cid, challenge))
    
    if not results:
        embed = discord.Embed(
            title="검색 결과 없음",
            description="해당 키워드에 맞는 챌린지가 없습니다.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    results.sort(key=lambda x: get_difficulty_rank(x[1]["actual_difficulty"]))
    
    view = SearchResultsView(results, leaderboard, clears)
    embed = view.create_embed()

    try:
        await interaction.response.send_message(embed=embed, view=view)
    except discord.HTTPException as e:
        if e.status == 429:
            print("Discord Global Rate Limit")
        else:
            raise

@bot.tree.command(name="이름검색", description="챌린지 이름으로 검색합니다")
@app_commands.describe(
    이름="검색할 챌린지 이름"
)
async def search_by_name(
    interaction: discord.Interaction,
    이름: str
):
    challenges = load_json("challenges.json")
    leaderboard = load_json("leaderboard.json")
    clears = load_json("clears.json")
    
    results = []
    for cid, challenge in challenges.items():
        if 이름.lower() in challenge["name"].lower():
            results.append((cid, challenge))
    
    if not results:
        embed = discord.Embed(
            title="검색 결과 없음",
            description="해당 챌린지가 없습니다.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    results.sort(key=lambda x: get_difficulty_rank(x[1]["actual_difficulty"]))
    
    view = SearchResultsView(results, leaderboard, clears)
    embed = view.create_embed()
   
    try:
        await interaction.response.send_message(embed=embed, view=view)
    except discord.HTTPException as e:
        if e.status == 429:
            print("Discord Global Rate Limit")
        else:
            raise

@bot.tree.command(name="설명검색", description="챌린지 설명으로 검색합니다")
@app_commands.describe(
    설명="검색할 설명 키워드"
)
async def search_by_description(
    interaction: discord.Interaction,
    설명: str
):
    challenges = load_json("challenges.json")
    leaderboard = load_json("leaderboard.json")
    clears = load_json("clears.json")
    
    results = []
    for cid, challenge in challenges.items():
        challenge_desc = challenge.get("description", "")
        if 설명.lower() in challenge_desc.lower():
            results.append((cid, challenge))
    
    if not results:
        embed = discord.Embed(
            title="검색 결과 없음",
            description="해당 설명을 포함한 챌린지가 없습니다.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    results.sort(key=lambda x: get_difficulty_rank(x[1]["actual_difficulty"]))
    
    view = SearchResultsView(results, leaderboard, clears)
    embed = view.create_embed()
    
    try:
        await interaction.response.send_message(embed=embed, view=view)
    except discord.HTTPException as e:
        if e.status == 429:
            print("Discord Global Rate Limit")
        else:
            raise

@bot.tree.command(name="레벨별검색", description="챌린지를 난이도로 검색합니다")
@app_commands.describe(
    난이도="검색할 난이도"
)
async def search_by_difficulty(
    interaction: discord.Interaction,
    난이도: str
):
    if 난이도 not in DIFFICULTIES:
        await interaction.response.send_message("올바른 난이도를 입력해주세요.", ephemeral=True)
        return
    
    challenges = load_json("challenges.json")
    leaderboard = load_json("leaderboard.json")
    clears = load_json("clears.json")
    
    results = []
    for cid, challenge in challenges.items():
        if challenge["actual_difficulty"] == 난이도:
            results.append((cid, challenge))
    
    if not results:
        embed = discord.Embed(
            title="검색 결과 없음",
            description=f"난이도 '{난이도}'의 챌린지가 없습니다.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    results.sort(key=lambda x: int(x[0]))
    
    view = SearchResultsView(results, leaderboard, clears)
    embed = view.create_embed()
    
    try:
        await interaction.response.send_message(embed=embed, view=view)
    except discord.HTTPException as e:
        if e.status == 429:
            print("Discord Global Rate Limit")
        else:
            raise

@bot.tree.command(name="아이디검색", description="챌린지 ID로 검색합니다")
@app_commands.describe(
    챌린지id="검색할 챌린지 ID"
)
async def search_by_id(
    interaction: discord.Interaction,
    챌린지id: str
):
    challenges = load_json("challenges.json")
    clears = load_json("clears.json")
    
    if 챌린지id not in challenges:
        await interaction.response.send_message(f"ID '{챌린지id}'를 찾을 수 없습니다.", ephemeral=True)
        return
    
    challenge = challenges[챌린지id]
    
    clear_count = sum(1 for clear in clears.values() 
                     if clear["challenge_id"] == 챌린지id and clear["status"] == "approved")
    
    difficulty_emoji = get_difficulty_emoji(challenge["actual_difficulty"])
    curation_text = ""
    if challenge.get("curation"):
        curation_emoji = EMOJI_MAP.get(challenge["curation"], "")
        curation_text = f" {curation_emoji}"
    
    embed = discord.Embed(
        title=f"{difficulty_emoji} {challenge['name']} (ID: {챌린지id}){curation_text}",
        description=challenge.get("description", "설명 없음"),
        color=discord.Color.blue()
    )
    embed.add_field(name="PP", value=f"{fmt_pp(get_challenge_pp(challenge))}PP", inline=True)
    embed.add_field(name="클리어", value=f"clears: {clear_count}", inline=True)
    embed.add_field(name="제작자", value=challenge.get("creator_name", "알 수 없음"), inline=True)
    
    
    await interaction.response.send_message(embed=embed)
    
class ProfileView(discord.ui.View):
    def __init__(self, user_id: str, target_user: discord.User, clears_list):
        super().__init__()
        self.user_id = user_id
        self.target_user = target_user
        self.clears_list = clears_list
        self.page = 0
        self.clears_per_page = 10
    
    def create_embed(self):
        leaderboard_data = load_json("leaderboard.json")
        user_data = get_user_data(self.user_id)  # 유저 데이터 가져오기

        # 연속 클리어 일수 (스트릭)
        _all_clears = load_json("clears.json")
        _clear_dates = {
            c["submitted_at"][:10]
            for c in _all_clears.values()
            if c["user_id"] == self.user_id and c["status"] == "approved" and c.get("submitted_at")
        }
        clear_streak = get_current_clear_streak(_clear_dates)
        
        sorted_users = sorted(leaderboard_data.items(), key=lambda x: x[1].get("rank_score", 0), reverse=True)
        user_rank = None
        for idx, (uid, _) in enumerate(sorted_users):
            if uid == self.user_id:
                user_rank = idx + 1
                break
        
        general_score = leaderboard_data.get(self.user_id, {}).get("general_score", 0)
        rank_score = leaderboard_data.get(self.user_id, {}).get("rank_score", 0)
        
        rank_display = ""
        if user_rank:
            if 1 <= user_rank <= 3:
                rank_display = f"**#{user_rank}**"
            else:
                rank_display = f"#{user_rank}"
        else:
            rank_display = "없음"
        
        difficulty_order = (
            [f"U{i}" for i in range(20, 0, -1)] +
            [f"G{i}" for i in range(20, 0, -1)] +
            [f"P{i}" for i in range(20, 0, -1)] +
            ["impossible", "censored", "epic", "marathon", "gimmick"]
        )
        
        max_clear_difficulty = None
        for difficulty in difficulty_order:
            if any(clear["difficulty"] == difficulty for clear in self.clears_list):
                max_clear_difficulty = difficulty
                break
        
        profile_color = user_data.get("profile_color")
        if profile_color and profile_color in PROFILE_COLORS:
            embed_color = PROFILE_COLORS[profile_color]["hex"]
        else:
            embed_color = 0x460e02 # 기본 흰색
        
        equipped_title = user_data.get("equipped_title")
        title_display = f" [{equipped_title}]" if equipped_title else ""
        
        # 서포터 레벨 확인
        supporter_level = get_user_supporter_level(self.user_id)
        supporter_emoji = SUPPORTER_EMOJIS.get(supporter_level, "") if supporter_level > 0 else ""
        
        embed = discord.Embed(
            title=f"{self.target_user.name}{title_display}'s profile'",
            color=embed_color
        )
        embed.set_thumbnail(url=self.target_user.display_avatar.url)
        
        nickname_display = f"{self.target_user.name} {supporter_emoji}" if supporter_emoji else self.target_user.name
        embed.add_field(name="username", value=nickname_display, inline=False)
        embed.add_field(name="ranking", value=rank_display, inline=True)
        embed.add_field(name="General Score", value=f"{general_score}PP", inline=True)
        embed.add_field(name="Rank Score", value=f"{rank_score}PP", inline=True)
        
        embed.add_field(name="balance", value=f"{user_data.get('coins', 0):,}C", inline=True)
        
        if max_clear_difficulty:
            emoji = get_difficulty_emoji(max_clear_difficulty)
            embed.add_field(name="hardest", value=f"{emoji} {max_clear_difficulty}", inline=True)
        else:
            embed.add_field(name="hardest", value="none", inline=True)
        
        embed.add_field(name="clear count", value=f"{len(self.clears_list)}개", inline=True)
        if clear_streak > 0:
            embed.add_field(name="streak", value=f"{clear_streak}일 연속", inline=True)
        
        start_idx = self.page * self.clears_per_page
        end_idx = start_idx + self.clears_per_page
        page_clears = self.clears_list[start_idx:end_idx]
        
        if page_clears:
            clears_text = ""
            for clear in page_clears:
                emoji = get_difficulty_emoji(clear["difficulty"])
                challenge_name = clear.get("challenge_name", "알 수 없음")
                general_pp = get_clear_pp(clear)
                rank_pp = get_clear_rank_score(self.user_id, clear["clear_id"])
                clears_text += f"{emoji} {challenge_name}\nRank: **{rank_pp}PP** | General: {fmt_pp(general_pp)}PP\n\n"
            
            embed.add_field(name=f"클리어 목록 ({start_idx+1}-{min(end_idx, len(self.clears_list))})", value=clears_text.strip(), inline=False)
        
        total_pages = max(1, (len(self.clears_list) + self.clears_per_page - 1) // self.clears_per_page)
        embed.set_footer(text=f"페이지 {self.page + 1}/{total_pages}")
        
        return embed
    
    @discord.ui.button(label="◀", style=discord.ButtonStyle.gray)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 0:
            self.page -= 1
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="▶", style=discord.ButtonStyle.gray)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        total_pages = max(1, (len(self.clears_list) + self.clears_per_page - 1) // self.clears_per_page)
        if self.page < total_pages - 1:
            self.page += 1
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)

@bot.tree.command(name="프로필", description="사용자 프로필과 클리어 목록을 확인합니다")
@app_commands.describe(
    대상="프로필을 확인할 사용자 (생략하면 본인)"
)
async def profile(
    interaction: discord.Interaction,
    대상: Optional[discord.User] = None
):
    target_user = 대상 if 대상 else interaction.user
    user_id = str(target_user.id)
    
    clears_data = load_json("clears.json")
    challenges_data = load_json("challenges.json")
    
    user_clears = []
    for clear_id, clear in clears_data.items():
        if clear["user_id"] == user_id and clear["status"] == "approved":
            user_clears.append({
                "clear_id": clear_id,
                "difficulty": clear["difficulty"],
                "custom_pp": clear.get("custom_pp"),
                "challenge_name": clear.get("challenge_name", "알 수 없음")
            })
    
    user_clears_sorted = sorted(
        user_clears,
        key=lambda c: get_clear_pp(c),
        reverse=True
    )
    
    view = ProfileView(user_id, target_user, user_clears_sorted)
    embed = view.create_embed()
    await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="챌린지제작", description="새로운 챌린지를 제출합니다")
@app_commands.describe(
    챌린지이름="챌린지 이름",
    챌린지설명="챌린지 설명",
    예상난이도="예상 난이도"
)
async def submit_challenge(
    interaction: discord.Interaction,
    챌린지이름: str,
    챌린지설명: str,
    예상난이도: str
):
    if 예상난이도 not in DIFFICULTIES:
        await interaction.response.send_message("올바른 난이도를 입력해주세요.", ephemeral=True)
        return
    
    user_id = str(interaction.user.id)
    submission_id = str(uuid.uuid4())[:8]
    
    submissions = load_json("challenge_submissions.json")
    submissions[submission_id] = {
        "user_id": user_id,
        "username": interaction.user.name,
        "name": 챌린지이름,
        "description": 챌린지설명,
        "expected_difficulty": 예상난이도,
        "status": "pending",
        "submitted_at": datetime.now().isoformat()
    }
    save_json("challenge_submissions.json", submissions)
    
    channel = bot.get_channel(CHANNEL_CHALLENGE_SUBMISSION)
    if channel:
        emoji = get_difficulty_emoji(예상난이도)
        embed = discord.Embed(
            title=f"새로운 챌린지 제출",
            description=f"**{챌린지이름}**",
            color=discord.Color.gold()
        )
        embed.add_field(name="설명", value=챌린지설명, inline=False)
        embed.add_field(name="예상 난이도", value=emoji, inline=True)
        embed.add_field(name="제출 ID", value=f"`{submission_id}`", inline=True)
        embed.add_field(name="제출자", value=interaction.user.mention, inline=True)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        
        message = await channel.send(embed=embed)
        thread = await message.create_thread(name="Rates")
        await thread.send(f"<@&1493610487122755584>")
    
    await interaction.response.send_message(f"챌린지가 제출되었습니다! 제출 ID: `{submission_id}`", ephemeral=True)

@bot.tree.command(name="등재", description="챌린지를 승인하고 등재합니다 (관리자 전용)")
@app_commands.describe(
    제출id="챌린지 제출 ID",
    실제난이도="실제 난이도",
    pp="커스텀 PP (선택사항, 지정 시 난이도 기본 PP 대신 사용)"
)
async def register_challenge(
    interaction: discord.Interaction,
    제출id: str,
    실제난이도: str,
    pp: Optional[float] = None
):
    if interaction.user.id != ADMIN_ID and interaction.user.id != ADMIN_ID_ALT:
        await interaction.response.send_message("관리자만 사용할 수 있습니다.", ephemeral=True)
        return
    
    if 실제난이도 not in DIFFICULTIES:
        await interaction.response.send_message("올바른 난이도를 입력해주세요.", ephemeral=True)
        return
    
    submissions = load_json("challenge_submissions.json")
    
    if 제출id not in submissions:
        await interaction.response.send_message("존재하지 않는 제출 ID입니다.", ephemeral=True)
        return
    
    submission = submissions[제출id]
    
    challenge_id = get_next_challenge_id()
    
    challenges = load_json("challenges.json")
    challenges[challenge_id] = {
        "name": submission["name"],
        "description": submission["description"],
        "expected_difficulty": submission["expected_difficulty"],
        "actual_difficulty": 실제난이도,
        "custom_pp": pp,
        "creator_id": submission["user_id"],
        "creator_name": submission["username"],
        "created_at": submission["submitted_at"],
        "registered_at": datetime.now().isoformat()
    }
    save_json("challenges.json", challenges)
    
    submission["status"] = "registered"
    submission["challenge_id"] = challenge_id
    submissions[제출id] = submission
    save_json("challenge_submissions.json", submissions)
    
    emoji = get_difficulty_emoji(실제난이도)
    embed = discord.Embed(
        title="챌린지 등재 완료",
        description=f"**{submission['name']}**",
        color=discord.Color.green()
    )
    embed.add_field(name="챌린지 ID", value=challenge_id, inline=True)
    embed.add_field(name="난이도", value=emoji, inline=True)
    pp_display = pp if pp is not None else PP_REWARD.get(실제난이도, 0)
    embed.add_field(name="PP", value=f"{fmt_pp(pp_display)}PP", inline=True)
    embed.add_field(name="크리에이터", value=submission["username"], inline=True)
    
    # 챌린지 등재 보상 50C (censored, epic 난이도는 제외)
    if 실제난이도 not in ("censored", "epic"):
        add_coins(str(submission["user_id"]), 50)
        embed.add_field(name="등재 보상", value="+50C", inline=True)
    
    await interaction.response.send_message(embed=embed)
    await send_creator_notification(bot, int(submission["user_id"]), challenge_id, submission["name"], 실제난이도)
    
    # 제작자 챌린지 제작 개수 업적 체크 (공장장)
    await check_and_grant_achievements(str(submission["user_id"]), interaction.guild, trigger_type="create")

@bot.tree.command(name="챌린지삭제", description="등재된 챌린지를 삭제합니다 (관리자 전용)")
@app_commands.describe(
    id="삭제할 챌린지 ID"
)
async def delete_challenge(
    interaction: discord.Interaction,
    id: str
):
    if not is_admin(interaction.user.id):
        await interaction.response.send_message("관리자만 사용할 수 있습니다.", ephemeral=True)
        return
    
    challenges = load_json("challenges.json")
    
    if id not in challenges:
        await interaction.response.send_message("존재하지 않는 챌린지 ID입니다.", ephemeral=True)
        return
    
    challenge = challenges[id]
    del challenges[id]
    save_json("challenges.json", challenges)
    
    emoji = get_difficulty_emoji(challenge.get("actual_difficulty", ""))
    embed = discord.Embed(
        title="챌린지 삭제 완료",
        description=f"**{challenge.get('name', '알 수 없음')}** (ID: {id}) 챌린지를 삭제했습니다.",
        color=discord.Color.red()
    )
    embed.add_field(name="난이도", value=emoji, inline=True)
    embed.add_field(name="크리에이터", value=challenge.get("creator_name", "알 수 없음"), inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="클리어", description="챌린지 클리어를 제출합니다")
@app_commands.describe(
    챌린지id="챌린지 ID",
    체감난이도="체감 난이도 (선택사항)"
)
async def submit_clear(
    interaction: discord.Interaction,
    챌린지id: str,
    체감난이도: Optional[str] = None
):
    challenges = load_json("challenges.json")
    
    if 챌린지id not in challenges:
        await interaction.response.send_message(f"ID '{챌린지id}'를 찾을 수 없습니다.", ephemeral=True)
        return
    
    challenge = challenges[챌린지id]
    user_id = str(interaction.user.id)
    
    clears = load_json("clears.json")
    
    for clear_id, clear in clears.items():
        if clear["user_id"] == user_id and clear["challenge_id"] == 챌린지id and clear["status"] == "approved":
            await interaction.response.send_message("이미 클리어한 챌린지입니다.", ephemeral=True)
            return
    
    clear_id = str(uuid.uuid4())
    clears[clear_id] = {
        "user_id": user_id,
        "username": interaction.user.name,
        "challenge_id": 챌린지id,
        "difficulty": challenge["actual_difficulty"],
        "custom_pp": challenge.get("custom_pp"),
        "challenge_name": challenge["name"],
        "submitted_at": datetime.now().isoformat(),
        "status": "pending",
        "felt_difficulty": 체감난이도,
        "clear_id": clear_id
    }
    save_json("clears.json", clears)
    
    admin_channel = bot.get_channel(CHANNEL_ADMIN_APPROVAL)
    if admin_channel:
        difficulty_emoji = get_difficulty_emoji(challenge["actual_difficulty"])
        felt_text = f"\n체감 난이도: {체감난이도}" if 체감난이도 else "\n체감 난이도: None"
        
        embed = discord.Embed(
            title="클리어 승인 요청",
            description=f"**{interaction.user.name}**님이 클리어를 제출했습니다.\n{felt_text}",
            color=discord.Color.yellow()
        )
        embed.add_field(name="챌린지", value=f"{difficulty_emoji} {challenge['name']} (ID: {챌린지id})", inline=False)
        embed.add_field(name="난이도", value=challenge["actual_difficulty"], inline=True)
        embed.add_field(name="PP", value=f"{fmt_pp(get_challenge_pp(challenge))}PP", inline=True)
        
        view = ClearApprovalView(clear_id, interaction.user)
        await admin_channel.send(embed=embed, view=view)
    
    embed = discord.Embed(
        title="클리어 제출",
        description=f"**{challenge['name']}** 클리어가 제출되었습니다.\n관리자의 승인을 기다리고 있습니다.",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

class ClearApprovalView(discord.ui.View):
    def __init__(self, clear_id: str, user: discord.User):
        super().__init__(timeout=None)
        self.clear_id = clear_id
        self.user = user
    
    @discord.ui.button(label="승인", style=discord.ButtonStyle.success)
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != ADMIN_ID and interaction.user.id != ADMIN_ID_ALT:
            await interaction.response.send_message("관리자만 승인할 수 있습니다.", ephemeral=True)
            return
        
        clears = load_json("clears.json")
        if self.clear_id not in clears:
            await interaction.response.send_message("클리어 기록을 찾을 수 없습니다.", ephemeral=True)
            return
        
        clear = clears[self.clear_id]
        clear["status"] = "approved"
        clears[self.clear_id] = clear
        save_json("clears.json", clears)
        
        challenges = load_json("challenges.json")
        challenge = challenges[clear["challenge_id"]]
        pp = get_clear_pp(clear)
        
        leaderboard = load_json("leaderboard.json")
        if clear["user_id"] not in leaderboard:
            leaderboard[clear["user_id"]] = {
                "general_score": 0,
                "rank_score": 0
            }
        
        leaderboard[clear["user_id"]]["general_score"] = leaderboard[clear["user_id"]].get("general_score", 0) + pp
        old_rank = leaderboard[clear["user_id"]].get("rank_score", 0)
        new_rank = calculate_rank_score(clear["user_id"])
        rank_delta = round(new_rank - old_rank, 2)
        leaderboard[clear["user_id"]]["rank_score"] = new_rank
        
        save_json("leaderboard.json", leaderboard)
        
        # 하루 클리어 콤보 보상 (1번째 100C, 이후 10%씩 증가, 7번째부터 160C 고정)
        clear_reward = get_daily_clear_reward(clear["user_id"])
        add_coins(clear["user_id"], clear_reward)
        
        # 새벽 2~6시(KST) 클리어 카운트 (야행성)
        if is_kst_night():
            night_data = get_user_data(clear["user_id"])
            night_data["night_clears"] = night_data.get("night_clears", 0) + 1
            save_user_data(clear["user_id"], night_data)
        
        try:
            guild = interaction.guild
            if guild:
                target_user = guild.get_member(int(clear["user_id"]))
                if target_user and clear["difficulty"] in ROLE_ID_MAP:
                    role = guild.get_role(ROLE_ID_MAP[clear["difficulty"]])
                    if role and role not in target_user.roles:
                        await target_user.add_roles(role)
        except Exception as e:
            print(f"역할 지급 오류: {e}")
        
        # 최초 클리어 확인
        is_first_clear = sum(1 for c in clears.values() 
                            if c["challenge_id"] == clear["challenge_id"] and c["status"] == "approved") == 1
        
        # 최초 클리어 보상 50C
        if is_first_clear:
            add_coins(clear["user_id"], 50)

        # 제작자 로열티: 다른 사람이 내 챌린지를 깰 때마다 +25C (본인 클리어 제외)
        creator_id = str(challenge["creator_id"]) if challenge.get("creator_id") is not None else None
        if creator_id and creator_id != clear["user_id"]:
            add_coins(creator_id, 25)
        
        emoji = get_difficulty_emoji(clear["difficulty"])
        felt_text = f"\n체감 난이도: {clear.get('felt_difficulty', 'None')}" if clear.get("felt_difficulty") else "\n체감 난이도: None"
        
        clear_embed = discord.Embed(
            title=f"{emoji} 클리어 성공!",
            description=f"**{clear['challenge_name']}**{felt_text}",
            color=get_difficulty_color(clear["difficulty"])
        )
        clear_embed.add_field(name="클리어자", value=self.user.mention, inline=True)
        clear_embed.add_field(name="획득 PP", value=f"+{fmt_pp(pp)}PP", inline=True)
        clear_embed.add_field(name="랭크 반영 점수", value=f"+{rank_delta}PP", inline=True)
        clear_embed.set_thumbnail(url=self.user.display_avatar.url)
        
        # 일반 클리어 채널에 알림
        normal_channel = bot.get_channel(CHANNEL_CLEAR_NOTIFICATION)
        if normal_channel:
            await normal_channel.send(embed=clear_embed)
        
        # U레벨 클리어 시 추가 알림
        if clear["difficulty"].startswith("U"):
            u_channel = bot.get_channel(CHANNEL_U_CLEAR_NOTIFICATION)
            if u_channel:
                await u_channel.send(f"<@&{ROLE_U_CLEAR_PING}>", embed=clear_embed)
        
        # G레벨 클리어 시 추가 멘션
        if clear["difficulty"].startswith("G"):
            g_channel = bot.get_channel(CHANNEL_CLEAR_NOTIFICATION)
            if g_channel:
                await g_channel.send(f"<@&{ROLE_G_CLEAR_PING}>")
        
        # 최초 클리어 시 알림
                # 최초 클리어 시 알림 (클리어 알림과 동일한 형식)
        if is_first_clear:
            first_clear_channel = bot.get_channel(CHANNEL_FIRST_CLEAR)
            if first_clear_channel:
                await first_clear_channel.send(f"<@&{ROLE_FIRST_CLEAR_PING}>", embed=clear_embed)
        
        # 업적 체크 및 부여
        await check_and_grant_achievements(clear["user_id"], interaction.guild, trigger_type="clear")
        
        embed = discord.Embed(
            title="클리어 승인 완료",
            description=f"{self.user.name}의 클리어가 승인되었습니다.",
            color=discord.Color.green()
        )
        embed.add_field(name="챌린지", value=clear["challenge_name"], inline=False)
        embed.add_field(name="획득 PP", value=f"+{fmt_pp(pp)}PP", inline=True)
        
        await interaction.response.edit_message(embed=embed, view=None)
    
    @discord.ui.button(label="거절", style=discord.ButtonStyle.danger)
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != ADMIN_ID and interaction.user.id != ADMIN_ID_ALT:
            await interaction.response.send_message("관리자만 거절할 수 있습니다.", ephemeral=True)
            return
        
        clears = load_json("clears.json")
        if self.clear_id in clears:
            del clears[self.clear_id]
            save_json("clears.json", clears)
        
        embed = discord.Embed(
            title="클리어 거절 완료",
            description=f"{self.user.name}의 클리어가 거절되었습니다.",
            color=discord.Color.red()
        )
        
        await interaction.response.edit_message(embed=embed, view=None)

@bot.tree.command(name="클리어처리", description="클리어를 관리자가 직접 처리합니다 (관리자 전용)")
@app_commands.describe(
    대상="클리어 승인할 사용자",
    챌린지id="챌린지 ID",
    체감난이도="체감 난이도 (선택사항)"
)
async def handle_clear(
    interaction: discord.Interaction,
    대상: discord.User,
    챌린지id: str,
    체감난이도: Optional[str] = None
):
    if not is_admin(interaction.user.id):
        await interaction.response.send_message("관리자만 사용할 수 있습니다.", ephemeral=True)
        return
    
    challenges = load_json("challenges.json")
    clears = load_json("clears.json")
    leaderboard = load_json("leaderboard.json")
    
    if 챌린지id not in challenges:
        await interaction.response.send_message(f"ID '{챌린지id}'를 찾을 수 없습니다.", ephemeral=True)
        return
    
    challenge = challenges[챌린지id]
    user_id = str(대상.id)
    
    for clear in clears.values():
        if clear["user_id"] == user_id and clear["challenge_id"] == 챌린지id and clear["status"] == "approved":
            await interaction.response.send_message("이미 클리어한 챌린지입니다.", ephemeral=True)
            return
    
    clear_id = str(uuid.uuid4())
    clears[clear_id] = {
        "user_id": user_id,
        "username": 대상.name,
        "challenge_id": 챌린지id,
        "difficulty": challenge["actual_difficulty"],
        "custom_pp": challenge.get("custom_pp"),
        "challenge_name": challenge["name"],
        "submitted_at": datetime.now().isoformat(),
        "status": "approved",
        "felt_difficulty": 체감난이도,
        "clear_id": clear_id
    }
    save_json("clears.json", clears)
    
    if user_id not in leaderboard:
        leaderboard[user_id] = {
            "general_score": 0,
            "rank_score": 0
        }
    
    pp = get_challenge_pp(challenge)
    leaderboard[user_id]["general_score"] = leaderboard[user_id].get("general_score", 0) + pp
    old_rank = leaderboard[user_id].get("rank_score", 0)
    new_rank = calculate_rank_score(user_id)
    rank_delta = round(new_rank - old_rank, 2)
    leaderboard[user_id]["rank_score"] = new_rank
    save_json("leaderboard.json", leaderboard)
    
    # 하루 클리어 콤보 보상 (1번째 100C, 이후 10%씩 증가, 7번째부터 160C 고정)
    clear_reward = get_daily_clear_reward(user_id)
    add_coins(user_id, clear_reward)
    
    # 새벽 2~6시(KST) 클리어 카운트 (야행성)
    if is_kst_night():
        night_data = get_user_data(user_id)
        night_data["night_clears"] = night_data.get("night_clears", 0) + 1
        save_user_data(user_id, night_data)
    
    # 최초 클리어 확인
    is_first_clear = sum(1 for c in clears.values() 
                        if c["challenge_id"] == 챌린지id and c["status"] == "approved") == 1
    
    # 최초 클리어 보상 50C
    if is_first_clear:
        add_coins(user_id, 50)

    # 제작자 로열티: 다른 사람이 내 챌린지를 깰 때마다 +25C (본인 클리어 제외)
    creator_id = str(challenge["creator_id"]) if challenge.get("creator_id") is not None else None
    if creator_id and creator_id != user_id:
        add_coins(creator_id, 25)
    
    difficulty_emoji = get_difficulty_emoji(challenge["actual_difficulty"])
    felt_text = f"\n체감 난이도: {체감난이도}" if 체감난이도 else "\n체감 난이도: None"
    
    clear_embed = discord.Embed(
        title=f"{difficulty_emoji} 클리어 성공!",
        description=f"**{대상.name}**님이 클리어했습니다!{felt_text}",
        color=get_difficulty_color(challenge["actual_difficulty"])
    )
    clear_embed.add_field(name="챌린지", value=f"{difficulty_emoji} {challenge['name']} (ID: {챌린지id})", inline=False)
    clear_embed.add_field(name="난이도", value=challenge["actual_difficulty"], inline=True)
    clear_embed.add_field(name="획득 PP", value=f"+{fmt_pp(pp)}PP", inline=True)
    clear_embed.add_field(name="랭크 반영 점수", value=f"+{rank_delta}PP", inline=True)
    clear_embed.set_thumbnail(url=대상.display_avatar.url)
    
    # 일반 클리어 채널에 알림
    normal_channel = bot.get_channel(CHANNEL_CLEAR_NOTIFICATION)
    if normal_channel:
        await normal_channel.send(embed=clear_embed)
    
    # U레벨 클리어 시 추가 알림
    if challenge["actual_difficulty"].startswith("U"):
        u_channel = bot.get_channel(CHANNEL_U_CLEAR_NOTIFICATION)
        if u_channel:
            await u_channel.send(f"<@&{ROLE_U_CLEAR_PING}>", embed=clear_embed)
    
    # G레벨 클리어 시 추가 멘션
    if challenge["actual_difficulty"].startswith("G"):
        if normal_channel:
            await normal_channel.send(f"<@&{ROLE_G_CLEAR_PING}>")
    
    # 최초 클리어 시 알림
        # 최초 클리어 시 알림 (클리어 알림과 동일한 형식)
    if is_first_clear:
        first_clear_channel = bot.get_channel(CHANNEL_FIRST_CLEAR)
        if first_clear_channel:
            await first_clear_channel.send(f"<@&{ROLE_FIRST_CLEAR_PING}>", embed=clear_embed)
        # 일반 클리어 채널에도 최초 클리어 알림
        if normal_channel:
            await normal_channel.send(f"<@&{ROLE_FIRST_CLEAR_PING}>", embed=clear_embed)
    
    # 업적 체크 및 부여
    await check_and_grant_achievements(user_id, interaction.guild, trigger_type="clear")
    
    embed = discord.Embed(
        title="클리어 처리 완료",
        description=f"**{대상.name}**님의 **{challenge['name']}** 클리어가 처리되었습니다.",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="클리어자목록", description="특정 챌린지를 클리어한 사용자 목록을 확인합니다")
@app_commands.describe(
    챌린지id="챌린지 ID"
)
async def clear_user_list(
    interaction: discord.Interaction,
    챌린지id: str
):
    challenges = load_json("challenges.json")
    clears = load_json("clears.json")
    
    if 챌린지id not in challenges:
        await interaction.response.send_message(f"ID '{챌린지id}'를 찾을 수 없습니다.", ephemeral=True)
        return
    
    await interaction.response.defer()   # 인원 많을 때 토큰 만료 방지

    challenge = challenges[챌린지id]
    
    clear_list = []
    for clear_id, clear in clears.items():
        if clear["challenge_id"] == 챌린지id and clear["status"] == "approved":
            clear_list.append({
                "user_id": clear["user_id"],
                "submitted_at": clear["submitted_at"],
                "felt_difficulty": clear.get("felt_difficulty", "None")
            })
    
    clear_list.sort(key=lambda x: x["submitted_at"])
    
    difficulty_emoji = get_difficulty_emoji(challenge["actual_difficulty"])
    title = f"{difficulty_emoji} {challenge['name']} (ID: {챌린지id}) - 클리어자 목록"

    if not clear_list:
        embed = discord.Embed(
            title=title,
            description="아직 클리어한 사용자가 없습니다.",
            color=discord.Color.blue()
        )
        await interaction.followup.send(embed=embed)
        return

    view = ClearUserListView(title, clear_list)
    embed = await view.create_embed()
    await interaction.followup.send(embed=embed, view=view)

@bot.tree.command(name="리더보드", description="전체 리더보드를 확인합니다 (General & Rank)")
async def leaderboard(interaction: discord.Interaction):
    leaderboard_data = load_json("leaderboard.json")
    
    if not leaderboard_data:
        embed = discord.Embed(
            title="리더보드",
            description="아직 클리어 기록이 없습니다.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    sorted_users = sorted(leaderboard_data.items(), 
                        key=lambda x: x[1].get("rank_score", 0), reverse=True)
    
    view = LeaderboardView(sorted_users)
    embed = view.create_embed()
    await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="업적랭킹", description="업적을 가장 많이 달성한 유저 랭킹을 확인합니다")
async def achievement_ranking(interaction: discord.Interaction):
    achievements_data = load_json("achievements.json")
    times_data = load_json("achievement_times.json")
    
    if not achievements_data:
        embed = discord.Embed(
            title="업적 랭킹",
            description="아직 업적을 달성한 유저가 없습니다.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    # 유저별 업적 개수 및 '현재 개수 달성 시각'(가장 마지막 업적 시각) 집계
    ranking = []
    for uid, ach_list in achievements_data.items():
        count = len(ach_list)
        if count <= 0:
            continue
        user_times = times_data.get(uid, {})
        # 시각 기록이 없는 기존 업적은 가장 오래전으로 취급
        last_time = "0000"
        for ach_name in ach_list:
            t = user_times.get(ach_name, "0000")
            if t > last_time:
                last_time = t
        # 표시용 이름
        member = interaction.guild.get_member(int(uid)) if interaction.guild else None
        display_name = member.name if member else uid
        ranking.append((uid, count, last_time, display_name))
    
    if not ranking:
        embed = discord.Embed(
            title="업적 랭킹",
            description="아직 업적을 달성한 유저가 없습니다.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    # 개수 내림차순, 동률이면 먼저 달성(시각 오름차순)한 유저가 상위
    ranking.sort(key=lambda x: (-x[1], x[2]))
    
    view = AchievementRankView(ranking)
    embed = view.create_embed()
    await interaction.response.send_message(embed=embed, view=view)

class ClearUserListView(discord.ui.View):
    def __init__(self, challenge_title: str, clear_list: list):
        super().__init__(timeout=180)
        self.challenge_title = challenge_title
        self.clear_list = clear_list
        self.current_page = 0
        self.items_per_page = 10
        self.update_buttons()

    def update_buttons(self):
        total_pages = (len(self.clear_list) - 1) // self.items_per_page + 1
        self.children[0].disabled = self.current_page <= 0
        self.children[1].disabled = self.current_page >= total_pages - 1

    async def create_embed(self):
        start_idx = self.current_page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_items = self.clear_list[start_idx:end_idx]
        total_pages = (len(self.clear_list) - 1) // self.items_per_page + 1

        embed = discord.Embed(
            title=self.challenge_title,
            description=f"총 {len(self.clear_list)}명이 클리어했습니다. (page {self.current_page + 1}/{total_pages})",
            color=discord.Color.blue()
        )

        for idx, clear in enumerate(page_items, start=start_idx + 1):
            try:
                user = await bot.fetch_user(int(clear["user_id"]))
                user_name = user.name
            except:
                user_name = f"ID: {clear['user_id']}"
            felt_text = clear["felt_difficulty"] if clear["felt_difficulty"] else "None"
            embed.add_field(
                name=f"{idx}. {user_name}",
                value=f"체감 난이도: {felt_text}",
                inline=False
            )
        return embed

    @discord.ui.button(label="◀", style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            embed = await self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="▶", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        total_pages = (len(self.clear_list) - 1) // self.items_per_page + 1
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.update_buttons()
            embed = await self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)
            
class SearchResultsView(discord.ui.View):
    def __init__(self, results: list, leaderboard: dict, clears: dict = None):
        super().__init__(timeout=180)
        self.results = results
        self.leaderboard = leaderboard
        self.clears = clears or {}
        self.current_page = 0
        self.items_per_page = 5
        self.update_buttons()
    
    def update_buttons(self):
        total_pages = (len(self.results) - 1) // self.items_per_page + 1
        self.children[0].disabled = self.current_page <= 0
        self.children[1].disabled = self.current_page <= 9
        self.children[2].disabled = self.current_page >= total_pages - 10
        self.children[3].disabled = self.current_page >= total_pages - 1
    
    def create_embed(self):
        start_idx = self.current_page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_results = self.results[start_idx:end_idx]
        
        total_pages = (len(self.results) - 1) // self.items_per_page + 1
        
        embed = discord.Embed(
            title="챌린지 검색 결과",
            description=f"페이지 {self.current_page + 1}/{total_pages}",
            color=discord.Color.blue()
        )
        
        for cid, challenge in page_results:
            emoji = get_difficulty_emoji(challenge["actual_difficulty"])
            pp = get_challenge_pp(challenge)
            
            clear_count = sum(1 for clear in self.clears.values() 
                             if clear["challenge_id"] == cid and clear["status"] == "approved")
            
            creator_info = f"만든 사람: {challenge['creator_name']}"
            
            if "curation" in challenge and challenge["curation"]:
                curation_level = challenge["curation"]
                curation_emoji = get_difficulty_emoji(curation_level)
                creator_info += f"\n{curation_emoji} {curation_level}"
            
            embed.add_field(
                name=f"{emoji} {challenge['name']}",
                value=f"ID: {cid}\n설명: {challenge['description']}\n{creator_info}\nPP: {fmt_pp(pp)}PP\nclears: {clear_count}",
                inline=False
            )
        
        return embed
    
    @discord.ui.button(label="◀", style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="◀◀", style=discord.ButtonStyle.primary)
    async def previous_10_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page >= 10:
            self.current_page -= 10
        elif self.current_page > 0:
            self.current_page = 0
        self.update_buttons()
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="▶▶", style=discord.ButtonStyle.primary)
    async def next_10_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        total_pages = (len(self.results) - 1) // self.items_per_page + 1
        if self.current_page + 10 < total_pages:
            self.current_page += 10
        else:
            self.current_page = total_pages - 1
        self.update_buttons()
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="▶", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        total_pages = (len(self.results) - 1) // self.items_per_page + 1
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.update_buttons()
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)

class LeaderboardView(discord.ui.View):
    def __init__(self, users: list):
        super().__init__(timeout=180)
        self.users = users
        self.current_page = 0
        self.items_per_page = 10
        self.update_buttons()
    
    def update_buttons(self):
        total_pages = (len(self.users) - 1) // self.items_per_page + 1
        self.children[0].disabled = self.current_page <= 0
        self.children[1].disabled = self.current_page >= total_pages - 1
        self.children[2].disabled = self.current_page <= 0
        self.children[3].disabled = self.current_page >= total_pages - 1
    
    def create_embed(self):
        start_idx = self.current_page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_users = self.users[start_idx:end_idx]
        
        total_pages = (len(self.users) - 1) // self.items_per_page + 1
        
        embed = discord.Embed(
            title="leaderboard",
            description=f"page {self.current_page + 1}/{total_pages}",
            color=discord.Color.gold()
        )
        
        for idx, (user_id, data) in enumerate(page_users):
            rank = start_idx + idx + 1
            medal = "<:emoji_34:1493620605260664892>" if rank == 1 else "<:emoji_35:1493620645928636426>" if rank == 2 else "<:emoji_36:1493620690358898899>" if rank == 3 else f"{rank}."
            
            general_score = data.get("general_score", 0)
            rank_score = data.get("rank_score", 0)
            
            embed.add_field(
                name=f'{medal} {data.get("username", user_id)}',
                value=f"**Rank: {rank_score}PP** | General: {general_score}PP",
                inline=False
            )
        
        return embed
    
    @discord.ui.button(label="◀", style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="◀◀", style=discord.ButtonStyle.primary)
    async def previous_10_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page >= 10:
            self.current_page -= 10
        elif self.current_page > 0:
            self.current_page = 0
        self.update_buttons()
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="▶▶", style=discord.ButtonStyle.primary)
    async def next_10_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        total_pages = (len(self.users) - 1) // self.items_per_page + 1
        if self.current_page + 10 < total_pages:
            self.current_page += 10
        else:
            self.current_page = total_pages - 1
        self.update_buttons()
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="▶", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        total_pages = (len(self.users) - 1) // self.items_per_page + 1
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.update_buttons()
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)

class AchievementListView(discord.ui.View):
    def __init__(self, title: str, description: str, fields: list):
        super().__init__(timeout=180)
        self.title = title
        self.description = description
        self.fields = fields   # [(name, value), ...]
        self.current_page = 0
        self.items_per_page = 10
        self.update_buttons()

    def update_buttons(self):
        total_pages = max(1, (len(self.fields) - 1) // self.items_per_page + 1)
        self.children[0].disabled = self.current_page <= 0
        self.children[1].disabled = self.current_page >= total_pages - 1

    def create_embed(self):
        start_idx = self.current_page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_fields = self.fields[start_idx:end_idx]
        total_pages = max(1, (len(self.fields) - 1) // self.items_per_page + 1)

        embed = discord.Embed(
            title=self.title,
            description=f"{self.description} (page {self.current_page + 1}/{total_pages})",
            color=discord.Color.gold()
        )
        for name, value in page_fields:
            embed.add_field(name=name, value=value, inline=False)
        return embed

    @discord.ui.button(label="◀", style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.create_embed(), view=self)

    @discord.ui.button(label="▶", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        total_pages = (len(self.fields) - 1) // self.items_per_page + 1
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
            
class AchievementRankView(discord.ui.View):
    def __init__(self, ranking: list):
        super().__init__(timeout=180)
        self.ranking = ranking  # [(user_id, count, last_time, display_name), ...]
        self.current_page = 0
        self.items_per_page = 10
        self.update_buttons()
    
    def update_buttons(self):
        total_pages = (len(self.ranking) - 1) // self.items_per_page + 1
        self.children[0].disabled = self.current_page <= 0
        self.children[1].disabled = self.current_page >= total_pages - 1
        self.children[2].disabled = self.current_page <= 0
        self.children[3].disabled = self.current_page >= total_pages - 1
    
    def create_embed(self):
        start_idx = self.current_page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_users = self.ranking[start_idx:end_idx]
        
        total_pages = (len(self.ranking) - 1) // self.items_per_page + 1
        
        embed = discord.Embed(
            title="업적 랭킹",
            description=f"page {self.current_page + 1}/{total_pages}",
            color=discord.Color.gold()
        )
        
        for idx, (user_id, count, last_time, display_name) in enumerate(page_users):
            rank = start_idx + idx + 1
            medal = "<:emoji_34:1493620605260664892>" if rank == 1 else "<:emoji_35:1493620645928636426>" if rank == 2 else "<:emoji_36:1493620690358898899>" if rank == 3 else f"{rank}."
            
            embed.add_field(
                name=f"{medal} {display_name}",
                value=f"**달성 업적: {count}개**",
                inline=False
            )
        
        return embed
    
    @discord.ui.button(label="◀", style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="◀◀", style=discord.ButtonStyle.primary)
    async def previous_10_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page >= 10:
            self.current_page -= 10
        elif self.current_page > 0:
            self.current_page = 0
        self.update_buttons()
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="▶▶", style=discord.ButtonStyle.primary)
    async def next_10_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        total_pages = (len(self.ranking) - 1) // self.items_per_page + 1
        if self.current_page + 10 < total_pages:
            self.current_page += 10
        else:
            self.current_page = total_pages - 1
        self.update_buttons()
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="▶", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        total_pages = (len(self.ranking) - 1) // self.items_per_page + 1
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.update_buttons()
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)

@bot.tree.command(name="제작자검색", description="특정 제작자가 만든 챌린지를 검색합니다")
@app_commands.describe(
    제작자="검색할 제작자 (멤버 선택)"
)
async def search_by_creator(
    interaction: discord.Interaction,
    제작자: discord.Member
):
    challenges = load_json("challenges.json")
    leaderboard = load_json("leaderboard.json")
    clears = load_json("clears.json")
    
    creator_name = 제작자.name
    
    results = []
    for cid, challenge in challenges.items():
        if creator_name.lower() == challenge["creator_name"].lower():
            results.append((cid, challenge))
    
    if not results:
        embed = discord.Embed(
            title="검색 결과 없음",
            description=f"'{creator_name}' 제작자의 챌린지가 없습니다.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    results.sort(key=lambda x: int(x[0]))
    
    view = SearchResultsView(results, leaderboard, clears)
    embed = view.create_embed()
    await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="재책정", description="챌린지의 난이도를 재책정합니다 (관리자 전용)")
@app_commands.describe(
    챌린지id="챌린지 ID",
    새로운난이도="새롭게 책정할 난이도",
    pp="커스텀 PP (선택사항, 지정 시 난이도 기본 PP 대신 사용)"
)
async def rescale_challenge(
    interaction: discord.Interaction,
    챌린지id: str,
    새로운난이도: str,
    pp: Optional[float] = None
):
    if not is_admin(interaction.user.id):
        await interaction.response.send_message("관리자만 사용할 수 있습니다.", ephemeral=True)
        return
    
    if 새로운난이도 not in DIFFICULTIES:
        await interaction.response.send_message("올바른 난이도를 입력해주세요.", ephemeral=True)
        return
    
    challenges = load_json("challenges.json")
    if 챌린지id not in challenges:
        await interaction.response.send_message("존재하지 않는 챌린지 ID입니다.", ephemeral=True)
        return
    
    challenge = challenges[챌린지id]
    old_difficulty = challenge["actual_difficulty"]
    old_pp = get_challenge_pp(challenge)
    new_pp = pp if pp is not None else PP_REWARD.get(새로운난이도, 0)
    pp_diff = round(new_pp - old_pp, 2)
    
    challenge["actual_difficulty"] = 새로운난이도
    challenge["custom_pp"] = pp
    challenges[챌린지id] = challenge
    save_json("challenges.json", challenges)
    
    clears = load_json("clears.json")
    leaderboard = load_json("leaderboard.json")
    
    affected_users = []
    for clear_id, clear in clears.items():
        if clear["challenge_id"] == 챌린지id and clear["status"] == "approved":
            user_id = clear["user_id"]
            clear["difficulty"] = 새로운난이도
            clear["custom_pp"] = pp
            clears[clear_id] = clear
            
            if user_id in leaderboard:
                leaderboard[user_id]["general_score"] = round(leaderboard[user_id].get("general_score", 0) + pp_diff, 2)
                affected_users.append(user_id)
                # PP가 깎였으면 '억울해..' 업적 플래그
                if pp_diff < 0:
                    nerfed_data = get_user_data(user_id)
                    if not nerfed_data.get("got_nerfed", False):
                        nerfed_data["got_nerfed"] = True
                        save_user_data(user_id, nerfed_data)
    
    save_json("clears.json", clears)
    # 커스텀 PP 반영을 위해 영향받은 유저의 랭크 점수 재계산
    for uid in set(affected_users):
        leaderboard[uid]["rank_score"] = calculate_rank_score(uid)
    save_json("leaderboard.json", leaderboard)
    
    old_emoji = get_difficulty_emoji(old_difficulty)
    new_emoji = get_difficulty_emoji(새로운난이도)
    
    embed = discord.Embed(
        title="챌린지 난이도 재책정 완료",
        description=f"**{challenge['name']}**",
        color=discord.Color.orange()
    )
    embed.add_field(name="이전 난이도", value=f"{old_emoji} {old_difficulty} ({fmt_pp(old_pp)}PP)", inline=True)
    embed.add_field(name="새로운 난이도", value=f"{new_emoji} {새로운난이도} ({fmt_pp(new_pp)}PP)", inline=True)
    embed.add_field(name="PP 변화", value=f"{'+' if pp_diff > 0 else ''}{fmt_pp_diff(pp_diff)}PP", inline=True)
    embed.add_field(name="영향받은 사용자", value=f"{len(affected_users)}명", inline=False)
    
    await interaction.response.send_message(embed=embed)
    
    rescale_channel = bot.get_channel(CHANNEL_RESCALE_NOTIFICATION)
    if rescale_channel:
        role_mention = "<@&1493610797912428584>"
        notify_embed = discord.Embed(
            title="챌린지 난이도 재책정",
            description=f"**{challenge['name']}**",
            color=discord.Color.orange()
        )
        notify_embed.add_field(name="이전 난이도", value=f"{old_emoji} {old_difficulty}", inline=True)
        notify_embed.add_field(name="새로운 난이도", value=f"{new_emoji} {새로운난이도}", inline=True)
        notify_embed.add_field(name="PP 변화", value=f"{'+' if pp_diff > 0 else ''}{pp_diff}PP", inline=False)
        notify_embed.add_field(name="영향받은 사용자", value=f"{len(affected_users)}명", inline=False)
        await rescale_channel.send(f"{role_mention}", embed=notify_embed)

@bot.tree.command(name="큐레이션부여", description="챌린지에 큐레이션 배지를 부여합니다 (관리자 전용)")
@app_commands.describe(
    챌린지id="챌린지 ID",
    큐레이션레벨="부여할 큐레이션 레벨 (T1, T2H, T2, T3H, T3, T4)"
)
async def give_curation(
    interaction: discord.Interaction,
    챌린지id: str,
    큐레이션레벨: Literal["T1", "T2H", "T2", "T3H", "T3", "T4"]
):
    if not is_admin(interaction.user.id):
        await interaction.response.send_message("관리자만 사용할 수 있습니다.", ephemeral=True)
        return
    
    challenges = load_json("challenges.json")
    if 챌린지id not in challenges:
        await interaction.response.send_message("존재하지 않는 챌린지 ID입니다.", ephemeral=True)
        return
    
    challenge = challenges[챌린지id]
    challenge["curation"] = 큐레이션레벨
    challenges[챌린지id] = challenge
    save_json("challenges.json", challenges)
    
    curation_emoji = get_difficulty_emoji(큐레이션레벨)
    embed = discord.Embed(
        title="큐레이션 배지 부여 완료",
        description=f"**{challenge['name']}**",
        color=discord.Color.purple()
    )
    embed.add_field(name="큐레이션 레벨", value=f"{curation_emoji} {큐레이션레벨}", inline=True)
    embed.add_field(name="크리에이터", value=challenge["creator_name"], inline=True)
    
    await interaction.response.send_message(embed=embed)
    
    curation_channel = bot.get_channel(1493604135315046560)
    if curation_channel:
        role_mention = "<@&1493610726516985937>"
        notify_embed = discord.Embed(
            title="큐레이션 배지 부여",
            description=f"**{challenge['name']}**",
            color=CURATION_COLORS.get(큐레이션레벨, 0x9B59B6)
        )
        notify_embed.add_field(name="큐레이션 레벨", value=f"{curation_emoji} {큐레이션레벨}", inline=False)
        notify_embed.add_field(name="크리에이터", value=challenge["creator_name"], inline=True)
        notify_embed.add_field(name="챌린지 ID", value=챌린지id, inline=True)
        await curation_channel.send(f"{role_mention}", embed=notify_embed)
    
    # 제작자 큐레이션 업적 체크
    await check_and_grant_achievements(str(challenge["creator_id"]), interaction.guild, trigger_type="curation")

@bot.tree.command(name="큐레이션검색", description="큐레이션된 챌린지를 검색합니다")
@app_commands.describe(
    레벨="큐레이션 레벨 (T1, T2H, T2, T3H, T3, T4)"
)
async def search_curated_challenges(
    interaction: discord.Interaction,
    레벨: str
):
    challenges = load_json("challenges.json")
    leaderboard = load_json("leaderboard.json")
    clears = load_json("clears.json")
    
    results = []
    for cid, challenge in challenges.items():
        if challenge.get("curation") == 레벨:
            results.append((cid, challenge))
    
    if not results:
        embed = discord.Embed(
            title="검색 결과 없음",
            description=f"'{레벨}' 큐레이션 챌린지가 없습니다.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    results.sort(key=lambda x: int(x[0]))
    
    view = SearchResultsView(results, leaderboard, clears)
    embed = view.create_embed()
    await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="아임필링럭키", description="랜덤으로 챌린지를 추천합니다")
@app_commands.describe(
    최고난이도="최고 난이도 (예: G20)",
    최소난이도="최소 난이도 (예: P2)",
    클리어제외="이미 클리어한 챌린지를 제외할지 여부"
)
async def feeling_lucky(
    interaction: discord.Interaction,
    최소난이도: Optional[str] = None,
    최고난이도: Optional[str] = None,
    클리어제외: Optional[bool] = False
):
    challenges = load_json("challenges.json")
    clears = load_json("clears.json")
    
    if not challenges:
        await interaction.response.send_message("추천할 챌린지가 없습니다.", ephemeral=True)
        return
    
    if 최소난이도 and 최고난이도:
        min_idx = DIFFICULTY_ORDER.index(최소난이도) if 최소난이도 in DIFFICULTY_ORDER else -1
        max_idx = DIFFICULTY_ORDER.index(최고난이도) if 최고난이도 in DIFFICULTY_ORDER else -1
        
        if min_idx == -1 or max_idx == -1:
            await interaction.response.send_message("유효하지 않은 난이도입니다.", ephemeral=True)
            return
        
        if min_idx > max_idx:
            await interaction.response.send_message("최소 난이도가 최고 난이도보다 높을 수 없습니다.", ephemeral=True)
            return
    
    user_id = str(interaction.user.id)
    cleared_ids = {
        clear["challenge_id"] for clear in clears.values()
        if clear["user_id"] == user_id and clear["status"] == "approved"
    }

    filtered_challenges = {}
    for cid, challenge in challenges.items():
        if 클리어제외 and cid in cleared_ids:
            continue
        diff = challenge["actual_difficulty"]
        
        if 최소난이도 and 최고난이도:
            min_idx = DIFFICULTY_ORDER.index(최소난이도)
            max_idx = DIFFICULTY_ORDER.index(최고난이도)
            diff_idx = DIFFICULTY_ORDER.index(diff) if diff in DIFFICULTY_ORDER else -1
            if diff_idx < min_idx or diff_idx > max_idx:
                continue
        elif 최소난이도:
            min_idx = DIFFICULTY_ORDER.index(최소난이도)
            diff_idx = DIFFICULTY_ORDER.index(diff) if diff in DIFFICULTY_ORDER else -1
            if diff_idx < min_idx:
                continue
        elif 최고난이도:
            max_idx = DIFFICULTY_ORDER.index(최고난이도)
            diff_idx = DIFFICULTY_ORDER.index(diff) if diff in DIFFICULTY_ORDER else -1
            if diff_idx > max_idx:
                continue
        
        filtered_challenges[cid] = challenge
    
    if not filtered_challenges:
        msg = "해당 난이도 범위에 챌린지가 없습니다."
        if 클리어제외:
            msg = "추천할 챌린지가 없습니다. (이미 모두 클리어했거나 조건에 맞는 챌린지가 없음)"
        await interaction.response.send_message(msg, ephemeral=True)
        return
    
    random_id = random.choice(list(filtered_challenges.keys()))
    challenge = filtered_challenges[random_id]
    
    clear_count = sum(1 for clear in clears.values() 
                     if clear["challenge_id"] == random_id and clear["status"] == "approved")
    
    difficulty_emoji = get_difficulty_emoji(challenge["actual_difficulty"])
    curation_text = ""
    if challenge.get("curation"):
        curation_emoji = EMOJI_MAP.get(challenge["curation"], "")
        curation_text = f" {curation_emoji}"
    
    embed = discord.Embed(
        title="오늘의 추천 💫",
        description=f"{difficulty_emoji} {challenge['name']} (ID: {random_id}){curation_text}",
        color=discord.Color.gold()
    )
    embed.add_field(name="설명", value=challenge.get("description", "설명 없음"), inline=False)
    embed.add_field(name="PP", value=f"{fmt_pp(get_challenge_pp(challenge))}PP", inline=True)
    embed.add_field(name="클리어", value=f"clears: {clear_count}", inline=True)
    embed.add_field(name="제작자", value=challenge.get("creator_name", "알 수 없음"), inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="클리어순검색", description="클리어 수가 많은/적은 순서로 챌린지를 검색합니다")
@app_commands.describe(
    정렬="정렬 방식: 많은순 또는 적은순"
)
@app_commands.choices(정렬=[
    app_commands.Choice(name="많은순", value="많은순"),
    app_commands.Choice(name="적은순", value="적은순")
])
async def clear_count_search(
    interaction: discord.Interaction,
    정렬: str
):
    challenges = load_json("challenges.json")
    clears = load_json("clears.json")
    
    clear_counts = {}
    for challenge_id in challenges:
        clear_counts[challenge_id] = sum(1 for clear in clears.values() if clear["challenge_id"] == challenge_id and clear["status"] == "approved")
    
    if 정렬 == "많은순":
        sorted_challenges = sorted(clear_counts.items(), key=lambda x: x[1], reverse=True)
    else:
        sorted_challenges = sorted(clear_counts.items(), key=lambda x: x[1])
    
    view = ClearCountSearchView(sorted_challenges, challenges, clear_counts, 정렬)
    embed = view.create_embed()
    await interaction.response.send_message(embed=embed, view=view)

class ClearCountSearchView(discord.ui.View):
    def __init__(self, challenges_list, all_challenges, clear_counts, sort_type):
        super().__init__()
        self.challenges_list = challenges_list
        self.all_challenges = all_challenges
        self.clear_counts = clear_counts
        self.sort_type = sort_type
        self.current_page = 0
        self.page_size = 5
    
    def create_embed(self):
        start_idx = self.current_page * self.page_size
        end_idx = start_idx + self.page_size
        page_challenges = self.challenges_list[start_idx:end_idx]
        
        embed = discord.Embed(
            title=f"클리어순 검색 ({self.sort_type})",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"페이지 {self.current_page + 1}/{(len(self.challenges_list) - 1) // self.page_size + 1}")
        
        for challenge_id, clear_count in page_challenges:
            challenge = self.all_challenges[challenge_id]
            difficulty = challenge["actual_difficulty"]
            emoji = get_difficulty_emoji(difficulty)
            pp = get_challenge_pp(challenge)
            creator = challenge.get("creator_name", "알 수 없음")
            
            embed.add_field(
                name=f"{emoji} {challenge['name']}",
                value=f"ID: {challenge_id}\n{challenge['description']}\n클리어: {clear_count}명 | PP: {fmt_pp(pp)} | 제작자: {creator}",
                inline=False
            )
        
        return embed
    
    @discord.ui.button(label="◀", style=discord.ButtonStyle.gray)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
        await interaction.response.edit_message(embed=self.create_embed(), view=self)
    
    @discord.ui.button(label="▶", style=discord.ButtonStyle.gray)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        max_page = (len(self.challenges_list) - 1) // self.page_size
        if self.current_page < max_page:
            self.current_page += 1
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

@bot.tree.command(name="리더보드재계산", description="[관리자 전용] 모든 사용자의 점수를 재계산합니다")
async def recalculate_leaderboard(interaction: discord.Interaction):
    if not is_admin(interaction.user.id):
        await interaction.response.send_message("관리자만 사용 가능합니다.", ephemeral=True)
        return
    
    await interaction.response.defer()
    
    clears_data = load_json("clears.json")
    challenges_data = load_json("challenges.json")
    leaderboard_data = {}
    
    user_clears = {}
    for clear_id, clear in clears_data.items():
        if clear["status"] == "approved":
            user_id = clear["user_id"]
            if user_id not in user_clears:
                user_clears[user_id] = {"username": clear.get("username", "Unknown"), "clears": []}
            
            pp = get_clear_pp(clear)
            user_clears[user_id]["clears"].append(pp)
    
    for user_id, data in user_clears.items():
        clears = data["clears"]
        
        general_score = round(sum(clears), 2)
        
        clears_sorted = sorted(clears, reverse=True)
        rank_score = 0
        for idx, pp in enumerate(clears_sorted[:20]):
            multiplier = 1.0 - (idx * 0.05)
            rank_score += pp * multiplier
        rank_score = round(rank_score, 2)
        
        leaderboard_data[user_id] = {
            "username": data["username"],
            "general_score": general_score,
            "rank_score": rank_score
        }
    
    save_json("leaderboard.json", leaderboard_data)
    
    embed = discord.Embed(
        title="리더보드 재계산 완료",
        description=f"총 {len(leaderboard_data)}명의 점수를 재계산했습니다.",
        color=discord.Color.green()
    )
    await interaction.followup.send(embed=embed)

# ============================================
# ============================================

# /잔액 명령어
@bot.tree.command(name="잔액", description="보유 C와 보유금액을 확인합니다")
async def check_balance(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    user_data = get_user_data(user_id)
    
    embed = discord.Embed(
        title=f"{interaction.user.name}의 잔액",
        color=discord.Color.gold()
    )
    embed.add_field(name="보유 C", value=f"{user_data.get('coins', 0):,}C", inline=True)
    embed.add_field(name="보유금액", value=f"{user_data.get('balance', 0):,}원", inline=True)
    embed.add_field(name="등급", value=get_user_grade(user_data.get('total_spent', 0)), inline=True)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# /업적종류 명령어
@bot.tree.command(name="업적종류", description="업적 목록과 진행 상황을 확인합니다")
@app_commands.describe(대상="업적을 확인할 사용자 (생략하면 본인)")
async def achievement_list(interaction: discord.Interaction, 대상: Optional[discord.User] = None):
    target_user = 대상 if 대상 else interaction.user
    user_id = str(target_user.id)
    user_achievements = get_user_achievements(user_id)
    clears = load_json("clears.json")
    challenges = load_json("challenges.json")
    user_data = get_user_data(user_id)
    
    # 유저의 승인된 클리어 목록
    user_clears = [c for c in clears.values() if c["user_id"] == user_id and c["status"] == "approved"]
    cleared_challenge_ids = [c["challenge_id"] for c in user_clears]
    cleared_difficulties = [c["difficulty"] for c in user_clears]
    
    # 유저가 만든(등재된) 챌린지 목록
    my_challenges = {cid: ch for cid, ch in challenges.items() if ch.get("creator_id") == user_id}
    
    title = "업적 목록"
    description = f"{target_user.name}님의 업적 진행 상황"

    fields = []   # embed.add_field 대신 리스트에 모음
    
    for ach_name, ach_info in ACHIEVEMENTS.items():
        is_completed = ach_name in user_achievements
        status_emoji = "✅" if is_completed else "❌"
        
        # 진행도 계산
        progress_text = ""
        cur = req = None  # 숫자형 진행도 (진행 바 생성용)
        if not is_completed:
            if ach_info["type"] == "clear_count":
                cur, req = len(user_clears), ach_info["requirement"]
            elif ach_info["type"] == "coins":
                cur, req = user_data.get("coins", 0), ach_info["requirement"]
                progress_text = f" ({cur:,}/{req:,}C)"
            elif ach_info["type"] == "level_clear":
                prefix = ach_info["requirement"]
                has_clear = any(d.startswith(prefix) for d in cleared_difficulties)
                progress_text = " (완료)" if has_clear else " (미완료)"
            elif ach_info["type"] == "specific_challenges":
                required_ids = ach_info["requirement"]
                cur = sum(1 for cid in required_ids if cid in cleared_challenge_ids)
                req = len(required_ids)
            elif ach_info["type"] == "curation_count":
                r = ach_info["requirement"]
                cur = sum(1 for ch in my_challenges.values() if ch.get("curation") == r["level"])
                req = r["count"]
            elif ach_info["type"] == "level_range_all":
                r = ach_info["requirement"]
                needed = [f"{r['prefix']}{i}" for i in range(r["start"], r["end"] + 1)]
                cur = sum(1 for d in needed if d in cleared_difficulties)
                req = len(needed)
            elif ach_info["type"] == "create_count":
                cur, req = len(my_challenges), ach_info["requirement"]
            elif ach_info["type"] == "creator_clears":
                my_challenge_ids = set(my_challenges.keys())
                clearers = set(
                    c["user_id"] for c in clears.values()
                    if c["status"] == "approved" and c["challenge_id"] in my_challenge_ids
                )
                cur, req = len(clearers), ach_info["requirement"]
                progress_text = f" ({cur}/{req}명)"
            elif ach_info["type"] == "lottery_multiplier":
                current = user_data.get("best_lottery", 0)
                progress_text = f" (최고 {current}배/{ach_info['requirement']}배)"
            elif ach_info["type"] == "chat_count":
                cur, req = user_data.get("chat_count", 0), ach_info["requirement"]
                progress_text = f" ({cur:,}/{req:,})"
            elif ach_info["type"] == "first_clear_count":
                cur, req = get_first_clear_count(user_id, clears), ach_info["requirement"]
            elif ach_info["type"] == "got_nerfed":
                progress_text = " (미달성)"
            elif ach_info["type"] == "bet_win_count":
                cur, req = user_data.get("bet_wins", 0), ach_info["requirement"]
            elif ach_info["type"] == "all_colors":
                owned = set(user_data.get("owned_colors", []))
                cur = sum(1 for c in PROFILE_COLORS.keys() if c in owned)
                req = len(PROFILE_COLORS)
            elif ach_info["type"] == "level_set_count":
                r = ach_info["requirement"]
                cur = sum(1 for d in cleared_difficulties if d in r["levels"])
                req = r["count"]
            elif ach_info["type"] == "general_vs_rank":
                lb = load_json("leaderboard.json").get(user_id, {})
                g = lb.get("general_score", 0)
                rr = lb.get("rank_score", 0)
                ratio = round(g / rr, 2) if rr > 0 else 0
                progress_text = f" (현재 {ratio}배/{ach_info['requirement']}배)"

            # 숫자형 진행도가 있으면 진행 바 추가
            if cur is not None and req:
                if not progress_text:
                    progress_text = f" ({cur}/{req})"
                progress_text = f"{progress_text}\n{make_progress_bar(cur, req)}"
                
        fields.append((
            f"{status_emoji} {ach_name}",
            f"{ach_info['description']}{progress_text}"
        ))
    
    view = AchievementListView(title, description, fields)
    await interaction.response.send_message(embed=view.create_embed(), view=view)
    
# /업적재계산 명령어 (관리자용)
@bot.tree.command(name="업적재계산", description="모든 유저의 업적을 재계산합니다 (관리자)")
@app_commands.default_permissions(administrator=True)
async def recalculate_achievements(interaction: discord.Interaction):
    await interaction.response.defer()
    
    clears = load_json("clears.json")
    users = load_json("users.json")
    
    # 클리어가 있는 유저 ID 수집
    user_ids = set()
    for clear in clears.values():
        if clear.get("status") == "approved":
            user_ids.add(clear["user_id"])
    # users.json에 있는 유저도 추가 (RICH 업적용)
    for uid in users.keys():
        user_ids.add(uid)
    
    total_granted = 0
    granted_details = []
    
    for user_id in user_ids:
        granted = await check_and_grant_achievements(user_id, interaction.guild, trigger_type="recalculate")
        if granted:
            total_granted += len(granted)
            member = interaction.guild.get_member(int(user_id))
            if member:
                granted_details.append(f"{member.name}: {', '.join(granted)}")
    
    embed = discord.Embed(
        title="업적 재계산 완료",
        description=f"총 {total_granted}개의 업적이 새로 부여되었습니다.",
        color=discord.Color.green()
    )
    
    if granted_details:
        details_text = "\n".join(granted_details[:20])  # 최대 20개만 표시
        if len(granted_details) > 20:
            details_text += f"\n...외 {len(granted_details) - 20}명"
        embed.add_field(name="부여된 업적", value=details_text, inline=False)
    
    await interaction.followup.send(embed=embed)

# /프로필색상구매 명령어
@bot.tree.command(name="프로필색상구매", description="프로필 임베드 색상을 구매합니다")
@app_commands.describe(
    색깔="구매할 색상"
)
@app_commands.choices(색깔=[
    app_commands.Choice(name="2레벨 (300C)", value="2레벨"),
    app_commands.Choice(name="3레벨 (600C)", value="3레벨"),
    app_commands.Choice(name="4레벨 (1,200C)", value="4레벨"),
    app_commands.Choice(name="5레벨 (2,000C)", value="5레벨"),
    app_commands.Choice(name="6레벨 (3,600C)", value="6레벨"),
    app_commands.Choice(name="7레벨 (5,400C)", value="7레벨"),
    app_commands.Choice(name="8레벨 (8,800C)", value="8레벨"),
    app_commands.Choice(name="9레벨 (13,900C)", value="9레벨"),
    app_commands.Choice(name="10레벨 (22,700C)", value="10레벨"),
    app_commands.Choice(name="11레벨 (45,600C)", value="11레벨"),
])
async def buy_profile_color(
    interaction: discord.Interaction,
    색깔: str
):
    user_id = str(interaction.user.id)
    user_data = get_user_data(user_id)
    
    if 색깔 not in PROFILE_COLORS:
        await interaction.response.send_message("올바른 색상을 선택해주세요.", ephemeral=True)
        return
    
    price = PROFILE_COLORS[색깔]["price"]
    
    # 이미 보유한 색상인지 확인
    if 색깔 in user_data.get("owned_colors", []):
        await interaction.response.send_message(f"이미 '{색깔}' 색상을 보유하고 있습니다.", ephemeral=True)
        return
    
    # 잔액 확인
    if user_data.get("coins", 0) < price:
        await interaction.response.send_message(f"C가 부족합니다. 필요: {price:,}C, 보유: {user_data.get('coins', 0):,}C", ephemeral=True)
        return
    
    # 구매 처리
    user_data["coins"] -= price
    if "owned_colors" not in user_data:
        user_data["owned_colors"] = []
    user_data["owned_colors"].append(색깔)
    user_data["profile_color"] = 색깔  # 자동 적용
    save_user_data(user_id, user_data)
    
    embed = discord.Embed(
        title="색상 구매 완료!",
        description=f"'{색깔}' 색상을 구매하고 적용했습니다.",
        color=PROFILE_COLORS[색깔]["hex"]
    )
    embed.add_field(name="사용한 C", value=f"-{price:,}C", inline=True)
    embed.add_field(name="남은 C", value=f"{user_data['coins']:,}C", inline=True)
    
    await interaction.response.send_message(embed=embed)
    await check_and_grant_achievements(user_id, interaction.guild, trigger_type="color")

# /프로필색상변경 명령어
@bot.tree.command(name="프로필색상변경", description="보유한 색상 중 하나로 프로필 색상을 변경합니다")
@app_commands.describe(
    색깔="변경할 색상"
)
@app_commands.choices(색깔=[
    app_commands.Choice(name="1레벨", value="기본"),
    app_commands.Choice(name="2레벨", value="2레벨"),
    app_commands.Choice(name="3레벨", value="3레벨"),
    app_commands.Choice(name="4레벨", value="4레벨"),
    app_commands.Choice(name="5레벨", value="5레벨"),
    app_commands.Choice(name="6레벨", value="6레벨"),
    app_commands.Choice(name="7레벨", value="7레벨"),
    app_commands.Choice(name="8레벨", value="8레벨"),
    app_commands.Choice(name="9레벨", value="9레벨"),
    app_commands.Choice(name="10레벨", value="10레벨"),
    app_commands.Choice(name="11레벨", value="11레벨"),
])
async def change_profile_color(
    interaction: discord.Interaction,
    색깔: str
):
    user_id = str(interaction.user.id)
    user_data = get_user_data(user_id)
    
    if 색깔 == "기본":
        user_data["profile_color"] = None
        save_user_data(user_id, user_data)
        await interaction.response.send_message("프로필 색상을 기본(흰색)으로 변경했습니다.", ephemeral=True)
        return
    
    if 색깔 not in user_data.get("owned_colors", []):
        await interaction.response.send_message(f"'{색깔}' 색상을 보유하고 있지 않습니다.", ephemeral=True)
        return
    
    user_data["profile_color"] = 색깔
    save_user_data(user_id, user_data)
    
    await interaction.response.send_message(f"프로필 색상을 '{색깔}'으로 변경했습니다.", ephemeral=True)

# /칭호구매 명령어
@bot.tree.command(name="칭호구매", description="칭호를 구매합니다")
@app_commands.describe(
    칭호="구매할 칭호"
)
@app_commands.choices(칭호=[
    app_commands.Choice(name="나좀치는듯ㅋ (1,000C)", value="나좀치는듯ㅋ"),
    app_commands.Choice(name="퐁이 (3,240C)", value="퐁이"),
    app_commands.Choice(name="부자 (5,000C)", value="부자"),
    app_commands.Choice(name="벼락부자 (10,000C)", value="벼락부자"),
    app_commands.Choice(name="금수저 (50,000C)", value="금수저"),
    app_commands.Choice(name="다이아수저 (100,000C)", value="다이아수저"),
])
async def buy_title(
    interaction: discord.Interaction,
    칭호: str
):
    user_id = str(interaction.user.id)
    user_data = get_user_data(user_id)
    
    if 칭호 not in TITLES:
        await interaction.response.send_message("올바른 칭호를 선택해주세요.", ephemeral=True)
        return
    
    price = TITLES[칭호]
    
    if 칭호 in user_data.get("owned_titles", []):
        await interaction.response.send_message(f"이미 '{칭호}' 칭호를 보유하고 있습니다.", ephemeral=True)
        return
    
    if user_data.get("coins", 0) < price:
        await interaction.response.send_message(f"C가 부족합니다. 필요: {price:,}C, 보유: {user_data.get('coins', 0):,}C", ephemeral=True)
        return
    
    user_data["coins"] -= price
    if "owned_titles" not in user_data:
        user_data["owned_titles"] = []
    user_data["owned_titles"].append(칭호)
    save_user_data(user_id, user_data)
    
    embed = discord.Embed(
        title="칭호 구매 완료!",
        description=f"'{칭호}' 칭호를 구매했습니다.",
        color=discord.Color.gold()
    )
    embed.add_field(name="사용한 C", value=f"-{price:,}C", inline=True)
    embed.add_field(name="남은 C", value=f"{user_data['coins']:,}C", inline=True)
    
    await interaction.response.send_message(embed=embed)
    
    # 업적 체크 및 부여 (콜렉터 등)
    await check_and_grant_achievements(user_id, interaction.guild, trigger_type="title")

# /보유칭호 명령어
@bot.tree.command(name="보유칭호", description="보유한 칭호 목록을 확인합니다")
async def owned_titles(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    user_data = get_user_data(user_id)
    
    owned = user_data.get("owned_titles", [])
    equipped = user_data.get("equipped_title")
    
    if not owned:
        await interaction.response.send_message("보유한 칭호가 없습니다.", ephemeral=True)
        return
    
    embed = discord.Embed(
        title=f"{interaction.user.name}의 보유 칭호",
        color=discord.Color.gold()
    )
    
    titles_text = ""
    for title in owned:
        if title == equipped:
            titles_text += f"✅ **{title}** (착용 중)\n"
        else:
            titles_text += f"• {title}\n"
    
    embed.description = titles_text
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# /칭호착용 명령어
@bot.tree.command(name="칭호착용", description="칭호를 착용합니다")
@app_commands.describe(
    칭호이름="착용할 칭호"
)
@app_commands.choices(칭호이름=[
    app_commands.Choice(name="나좀치는듯ㅋ", value="나좀치는듯ㅋ"),
    app_commands.Choice(name="퐁이", value="퐁이"),
    app_commands.Choice(name="부자", value="부자"),
    app_commands.Choice(name="벼락부자", value="벼락부자"),
    app_commands.Choice(name="금수저", value="금수저"),
    app_commands.Choice(name="다이아수저", value="다이아수저"),
])
async def equip_title(
    interaction: discord.Interaction,
    칭호이름: str
):
    user_id = str(interaction.user.id)
    user_data = get_user_data(user_id)
    
    if 칭호이름 not in user_data.get("owned_titles", []):
        await interaction.response.send_message(f"'{칭호이름}' 칭호를 보유하고 있지 않습니다.", ephemeral=True)
        return
    
    user_data["equipped_title"] = 칭호이름
    save_user_data(user_id, user_data)
    
    await interaction.response.send_message(f"'{칭호이름}' 칭호를 착용했습니다!", ephemeral=True)

# /칭호해제 명령어
@bot.tree.command(name="칭호해제", description="착용 중인 칭호를 해제합니다")
async def unequip_title(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    user_data = get_user_data(user_id)
    
    if not user_data.get("equipped_title"):
        await interaction.response.send_message("착용 중인 칭호가 없습니다.", ephemeral=True)
        return
    
    old_title = user_data["equipped_title"]
    user_data["equipped_title"] = None
    save_user_data(user_id, user_data)
    
    await interaction.response.send_message(f"'{old_title}' 칭호를 해제했습니다.", ephemeral=True)

# /커스텀칭호구매 명령어
@bot.tree.command(name="커스텀칭호구매", description="원하는 텍스트로 칭호를 직접 만듭니다 (2~6글자, 글자당 1,000C)")
@app_commands.describe(
    칭호="만들 칭호 (2~6글자)"
)
async def buy_custom_title(
    interaction: discord.Interaction,
    칭호: str
):
    user_id = str(interaction.user.id)
    user_data = get_user_data(user_id)
    
    title = 칭호.strip()
    
    if not (2 <= len(title) <= 6):
        await interaction.response.send_message("칭호는 2~6글자여야 합니다.", ephemeral=True)
        return
    
    if title in TITLES:
        await interaction.response.send_message("기본 칭호와 같은 이름은 만들 수 없습니다. /칭호구매를 이용해주세요.", ephemeral=True)
        return
    
    if title in user_data.get("owned_titles", []):
        await interaction.response.send_message(f"이미 '{title}' 칭호를 보유하고 있습니다.", ephemeral=True)
        return
    
    price = len(title) * 1000
    
    if user_data.get("coins", 0) < price:
        await interaction.response.send_message(f"C가 부족합니다. 필요: {price:,}C, 보유: {user_data.get('coins', 0):,}C", ephemeral=True)
        return
    
    user_data["coins"] -= price
    if "owned_titles" not in user_data:
        user_data["owned_titles"] = []
    user_data["owned_titles"].append(title)
    save_user_data(user_id, user_data)
    
    embed = discord.Embed(
        title="커스텀 칭호 구매 완료!",
        description=f"'{title}' 칭호를 만들었습니다.",
        color=discord.Color.gold()
    )
    embed.add_field(name="글자 수", value=f"{len(title)}글자", inline=True)
    embed.add_field(name="사용한 C", value=f"-{price:,}C", inline=True)
    embed.add_field(name="남은 C", value=f"{user_data['coins']:,}C", inline=True)
    embed.set_footer(text="착용은 /커스텀칭호착용 으로 할 수 있습니다.")
    
    await interaction.response.send_message(embed=embed)

# /커스텀칭호착용 명령어
@bot.tree.command(name="커스텀칭호착용", description="직접 만든 커스텀 칭호를 착용합니다")
@app_commands.describe(
    칭호="착용할 칭호"
)
async def equip_custom_title(
    interaction: discord.Interaction,
    칭호: str
):
    user_id = str(interaction.user.id)
    user_data = get_user_data(user_id)
    
    title = 칭호.strip()
    
    if title not in user_data.get("owned_titles", []):
        await interaction.response.send_message(f"'{title}' 칭호를 보유하고 있지 않습니다.", ephemeral=True)
        return
    
    user_data["equipped_title"] = title
    save_user_data(user_id, user_data)
    
    await interaction.response.send_message(f"'{title}' 칭호를 착용했습니다!", ephemeral=True)

# /송금 명령어
@bot.tree.command(name="송금", description=f"다른 유저에게 C를 송금합니다 (수수료 {TRANSFER_FEE_PERCENT}%)")
@app_commands.describe(
    대상="C를 받을 사람",
    금액="보낼 C"
)
async def transfer_coins(
    interaction: discord.Interaction,
    대상: discord.User,
    금액: int
):
    sender_id = str(interaction.user.id)
    target_id = str(대상.id)
    
    if 대상.bot:
        await interaction.response.send_message("봇에게는 송금할 수 없습니다.", ephemeral=True)
        return
    
    if sender_id == target_id:
        await interaction.response.send_message("본인에게는 송금할 수 없습니다.", ephemeral=True)
        return
    
    if 금액 <= 0:
        await interaction.response.send_message("1C 이상 송금해야 합니다.", ephemeral=True)
        return
    
    sender_data = get_user_data(sender_id)
    if sender_data.get("coins", 0) < 금액:
        await interaction.response.send_message(f"C가 부족합니다. 보유: {sender_data.get('coins', 0):,}C", ephemeral=True)
        return
    
    fee = max(1, int(금액 * TRANSFER_FEE_PERCENT / 100))
    received = 금액 - fee
    
    remove_coins(sender_id, 금액)
    add_coins(target_id, received)
    
    embed = discord.Embed(
        title="송금 완료",
        description=f"{interaction.user.mention} → {대상.mention}",
        color=discord.Color.green()
    )
    embed.add_field(name="보낸 C", value=f"{금액:,}C", inline=True)
    embed.add_field(name="수수료", value=f"{fee:,}C ({TRANSFER_FEE_PERCENT}%)", inline=True)
    embed.add_field(name="받은 C", value=f"{received:,}C", inline=True)
    embed.set_footer(text=f"남은 C: {get_user_data(sender_id).get('coins', 0):,}C")
    
    await interaction.response.send_message(embed=embed)
    
    # 받은 유저 업적 체크 (RICH 등)
    await check_and_grant_achievements(target_id, interaction.guild, trigger_type="coins")

# /쿠폰제작 명령어 (관리자 전용)
@bot.tree.command(name="쿠폰제작", description="[관리자 전용] 쿠폰을 생성합니다")
@app_commands.describe(
    수량="생성할 쿠폰 개수",
    금액="쿠폰 금액 (원)"
)
async def create_coupon(
    interaction: discord.Interaction,
    수량: int,
    금액: int
):
    if not is_admin(interaction.user.id):
        await interaction.response.send_message("관리자만 사용 가능합니다.", ephemeral=True)
        return
    
    coupons = load_json("coupons.json")
    
    created_codes = []
    for _ in range(수량):
        code = generate_coupon_code()
        while code in coupons:
            code = generate_coupon_code()
        
        coupons[code] = {
            "amount": 금액,
            "used": False,
            "created_at": datetime.now().isoformat()
        }
        created_codes.append(code)
    
    save_json("coupons.json", coupons)
    
    embed = discord.Embed(
        title="쿠폰 생성 완료",
        description=f"{금액:,}원 쿠폰 {수량}장이 생성되었습니다.",
        color=discord.Color.green()
    )
    
    # 생성된 쿠폰 코드 목록 (DM으로 전송)
    codes_text = "\n".join(created_codes)
    try:
        await interaction.user.send(f"**생성된 쿠폰 코드 ({금액:,}원)**\n\`\`\`\n{codes_text}\n\`\`\`")
    except:
        pass
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# /C지급 명령어 (관리자 전용)
@bot.tree.command(name="c지급", description="[관리자 전용] 사용자에게 C를 지급합니다")
@app_commands.describe(
    대상="C를 지급할 사용자",
    금액="지급할 C"
)
async def give_coins(
    interaction: discord.Interaction,
    대상: discord.User,
    금액: int
):
    if not is_admin(interaction.user.id):
        await interaction.response.send_message("관리자만 사용 가능합니다.", ephemeral=True)
        return
    
    user_id = str(대상.id)
    add_coins(user_id, 금액)
    
    user_data = get_user_data(user_id)
    
    embed = discord.Embed(
        title="C 지급 완료",
        description=f"{대상.name}에게 {금액:,}C를 지급했습니다.",
        color=discord.Color.green()
    )
    embed.add_field(name="현재 잔액", value=f"{user_data['coins']:,}C", inline=True)
    
    await interaction.response.send_message(embed=embed)

# /잔액충전 명령어 (관리자 전용 - 수동 충전 승인용)
@bot.tree.command(name="잔액충전", description="[관리자 전용] 사용자의 보유금액을 충전합니다")
@app_commands.describe(
    대상="충전할 사용자",
    금액="충전할 금액 (원)"
)
async def add_balance(
    interaction: discord.Interaction,
    대상: discord.User,
    금액: int
):
    if not is_admin(interaction.user.id):
        await interaction.response.send_message("관리자만 사용 가능합니다.", ephemeral=True)
        return
    
    user_id = str(대상.id)
    user_data = get_user_data(user_id)
    user_data["balance"] = user_data.get("balance", 0) + 금액
    save_user_data(user_id, user_data)
    
    embed = discord.Embed(
        title="잔액 충전 완료",
        description=f"{대상.name}에게 {금액:,}원을 충전했습니다.",
        color=discord.Color.green()
    )
    embed.add_field(name="현재 보유금액", value=f"{user_data['balance']:,}원", inline=True)
    
    await interaction.response.send_message(embed=embed)

# ============================================
# ============================================

class ShopView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="충전", style=discord.ButtonStyle.primary, custom_id="shop_charge_persistent")
    async def charge_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="충전 수단 선택",
            description="원하시는 충전 수단을 클릭해주세요.",
            color=discord.Color.blue()
        )
        view = ChargeMethodView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    @discord.ui.button(label="정보", style=discord.ButtonStyle.secondary, custom_id="shop_info_persistent")
    async def info_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = str(interaction.user.id)
        user_data = get_user_data(user_id)
        
        grade = get_user_grade(user_data.get("total_spent", 0))
        
        embed = discord.Embed(
            title="내 정보",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.add_field(name="닉네임", value=interaction.user.name, inline=False)
        embed.add_field(name="보유금액", value=f"{user_data.get('balance', 0):,}원", inline=True)
        embed.add_field(name="누적금액", value=f"{user_data.get('total_spent', 0):,}원", inline=True)
        embed.add_field(name="적용된 등급", value=grade, inline=True)
        
        view = InfoView(user_id)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    @discord.ui.button(label="이용", style=discord.ButtonStyle.success, custom_id="shop_use_persistent")
    async def use_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="카테고리 선택",
            description="구매할 카테고리를 선택해주세요.",
            color=discord.Color.green()
        )
        view = CategorySelectView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class ChargeMethodView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
    
    @discord.ui.button(label="계좌이체", style=discord.ButtonStyle.primary)
    async def bank_transfer(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = BankTransferModal()
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="쿠폰사용", style=discord.ButtonStyle.secondary)
    async def coupon_use(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = CouponModal()
        await interaction.response.send_modal(modal)

class BankTransferModal(discord.ui.Modal, title="계좌이체 충전"):
    입금자명 = discord.ui.TextInput(
        label="입금자명",
        placeholder="입금자명을 입력해주세요",
        required=True
    )
    금액 = discord.ui.TextInput(
        label="입금할 금액",
        placeholder="입금할 금액을 입력해주세요",
        required=True
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        # 관리자에게 DM 전송
        admin = await bot.fetch_user(ADMIN_ID)
        
        embed = discord.Embed(
            title="💰 충전 요청",
            description=f"{interaction.user.name}({interaction.user.id})님이 충전을 요청했습니다.",
            color=discord.Color.gold()
        )
        embed.add_field(name="입금자명", value=self.입금자명.value, inline=True)
        embed.add_field(name="금액", value=f"{self.금액.value}원", inline=True)
        embed.add_field(name="사용자 ID", value=str(interaction.user.id), inline=False)
        
        try:
            await admin.send(embed=embed)
        except:
            pass
        
        await interaction.response.send_message(
            "충전 요청이 전송되었습니다. 입금 확인 후 관리자가 충전해드립니다.\n"
            "**3자 입금 절대적으로 금지합니다**\n"
            "**DM 허용 하셔야 합니다**",
            ephemeral=True
        )

class CouponModal(discord.ui.Modal, title="쿠폰 사용"):
    쿠폰코드 = discord.ui.TextInput(
        label="쿠폰번호",
        placeholder="16자리 쿠폰번호를 입력해주세요",
        max_length=16,
        min_length=16,
        required=True
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        code = self.쿠폰코드.value.upper()
        coupons = load_json("coupons.json")
        
        if code not in coupons:
            await interaction.response.send_message("존재하지 않는 쿠폰번호입니다.", ephemeral=True)
            return
        
        coupon = coupons[code]
        
        if coupon["used"]:
            await interaction.response.send_message("이미 사용된 쿠폰입니다.", ephemeral=True)
            return
        
        # 쿠폰 사용 처리
        user_id = str(interaction.user.id)
        user_data = get_user_data(user_id)
        user_data["balance"] = user_data.get("balance", 0) + coupon["amount"]
        save_user_data(user_id, user_data)
        
        # 쿠폰 사용 처리
        coupons[code]["used"] = True
        coupons[code]["used_by"] = user_id
        coupons[code]["used_at"] = datetime.now().isoformat()
        save_json("coupons.json", coupons)
        
        embed = discord.Embed(
            title="쿠폰 사용 완료!",
            description=f"{coupon['amount']:,}원이 충전되었습니다.",
            color=discord.Color.green()
        )
        embed.add_field(name="현재 보유금액", value=f"{user_data['balance']:,}원", inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

class InfoView(discord.ui.View):
    def __init__(self, user_id: str):
        super().__init__(timeout=180)
        self.user_id = user_id
    
    @discord.ui.button(label="구매로그", style=discord.ButtonStyle.secondary)
    async def purchase_log(self, interaction: discord.Interaction, button: discord.ui.Button):
        # 구매 로그 표시 (추후 구현)
        await interaction.response.send_message("구매 로그 기능은 준비 중입니다.", ephemeral=True)
    
    @discord.ui.button(label="충전로그", style=discord.ButtonStyle.secondary)
    async def charge_log(self, interaction: discord.Interaction, button: discord.ui.Button):
        # 충전 로그 표시 (추후 구현)
        await interaction.response.send_message("충전 로그 기능은 준비 중입니다.", ephemeral=True)

class ProductSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        
        # 상품 선택 드롭다운
        options = [
            discord.SelectOption(label="500C", description="1,000원", value="500C"),
            discord.SelectOption(label="2,200C", description="4,000원", value="2,200C"),
            discord.SelectOption(label="6,000C", description="10,000원", value="6,000C"),
            discord.SelectOption(label="13,000C", description="20,000원", value="13,000C"),
            discord.SelectOption(label="33,000C", description="50,000원", value="33,000C"),
        ]
        
        select = discord.ui.Select(
            placeholder="구매할 상품을 선택하세요",
            options=options,
            custom_id="product_select"
        )
        select.callback = self.select_callback
        self.add_item(select)
    
    async def select_callback(self, interaction: discord.Interaction):
        selected = interaction.data["values"][0]
        product = C_PRODUCTS[selected]
        
        embed = discord.Embed(
            title="구매 확인",
            description=f"**{selected}**를 구매하시겠습니까?",
            color=discord.Color.blue()
        )
        embed.add_field(name="획득 C", value=f"{product['c_amount']:,}C", inline=True)
        embed.add_field(name="가격", value=f"{product['price']:,}원", inline=True)
        
        view = PurchaseConfirmView(selected, product)
        await interaction.response.edit_message(embed=embed, view=view)

class PurchaseConfirmView(discord.ui.View):
    def __init__(self, product_name: str, product: dict):
        super().__init__(timeout=180)
        self.product_name = product_name
        self.product = product
    
    @discord.ui.button(label="구매하기", style=discord.ButtonStyle.success)
    async def confirm_purchase(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = PurchaseModal(self.product_name, self.product)
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="취소", style=discord.ButtonStyle.danger)
    async def cancel_purchase(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="구매가 취소되었습니다.", embed=None, view=None)

class PurchaseModal(discord.ui.Modal, title="구매 확인"):
    쿠폰코드 = discord.ui.TextInput(
        label="쿠폰 코드 (관리자/이벤트 지급 시에만 입력)",
        placeholder="쿠폰이 있으면 입력, 없으면 비워두세요",
        required=False,
        max_length=16
    )
    
    def __init__(self, product_name: str, product: dict):
        super().__init__()
        self.product_name = product_name
        self.product = product
    
    async def on_submit(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        user_data = get_user_data(user_id)
        
        price = self.product["price"]
        discount = 0
        
        # 쿠폰 적용
        if self.쿠폰코드.value:
            code = self.쿠폰코드.value.upper()
            coupons = load_json("coupons.json")
            
            if code in coupons and not coupons[code]["used"]:
                discount = coupons[code]["amount"]
                price = max(0, price - discount)
                
                # 쿠폰 사용 처리
                coupons[code]["used"] = True
                coupons[code]["used_by"] = user_id
                coupons[code]["used_at"] = datetime.now().isoformat()
                save_json("coupons.json", coupons)
        
        # 잔액 확인
        if user_data.get("balance", 0) < price:
            await interaction.response.send_message(
                f"보유금액이 부족합니다.\n필요: {price:,}원, 보유: {user_data.get('balance', 0):,}원",
                ephemeral=True
            )
            return
        
        # 구매 처리
        user_data["balance"] -= price
        user_data["total_spent"] = user_data.get("total_spent", 0) + price
        user_data["coins"] = user_data.get("coins", 0) + self.product["c_amount"]
        save_user_data(user_id, user_data)
        
        embed = discord.Embed(
            title="구매 완료!",
            description=f"**{self.product_name}**를 구매했습니다.",
            color=discord.Color.green()
        )
        embed.add_field(name="획득 C", value=f"+{self.product['c_amount']:,}C", inline=True)
        embed.add_field(name="사용 금액", value=f"-{price:,}원", inline=True)
        if discount > 0:
            embed.add_field(name="쿠폰 할인", value=f"-{discount:,}원", inline=True)
        embed.add_field(name="현재 C", value=f"{user_data['coins']:,}C", inline=True)
        embed.add_field(name="현재 보유금액", value=f"{user_data['balance']:,}원", inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

# /상점설정 명령어 (관리자 전용 - 상점 메시지 전송)
@bot.tree.command(name="상점설정", description="[관리자 전용] 상점 메시지를 설정합니다")
async def setup_shop(interaction: discord.Interaction):
    if not is_admin(interaction.user.id):
        await interaction.response.send_message("관리자만 사용 가능합니다.", ephemeral=True)
        return
    
    channel = bot.get_channel(CHANNEL_SHOP)
    if not channel:
        await interaction.response.send_message("상점 채널을 찾을 수 없습니다.", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="PongTrio Shop",
        description=(
            "• **3자 입금 절대적으로 금지합니다**\n"
            "• **이용 하시기 전에 다이렉트 메시지(DM) 허용 하셔야 합니다**"
        ),
        color=discord.Color.blue()
    )
    
    embed.set_image(url="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-kAKDzFonyKPPQdt0mYMihFapOsWhn5.png")
    
    view = ShopView()
    await channel.send(embed=embed, view=view)
    
    await interaction.response.send_message("상점 메시지가 설정되었습니다.", ephemeral=True)

# ============================================
# 챌린지팩 시스템
# ============================================

def get_next_pack_id() -> str:
    packs = load_json("packs.json")
    if not packs:
        return "1"
    return str(max(int(k) for k in packs.keys()) + 1)

@bot.tree.command(name="챌린지팩만들기", description="[관리자 전용] 챌린지팩을 생성합니다")
@app_commands.describe(
    팩이름="팩 이름",
    챌린지ids="팩에 포함할 챌린지 ID들 (쉼표로 구분, 예: 3, 5, 7)"
)
async def create_pack(
    interaction: discord.Interaction,
    팩이름: str,
    챌린지ids: str
):
    if not is_admin(interaction.user.id):
        await interaction.response.send_message("관리자만 사용 가능합니다.", ephemeral=True)
        return
    
    challenges = load_json("challenges.json")
    packs = load_json("packs.json")
    
    # 챌린지 ID 파싱
    ids = [id.strip() for id in 챌린지ids.split(",")]
    valid_ids = []
    invalid_ids = []
    
    for cid in ids:
        if cid in challenges:
            valid_ids.append(cid)
        else:
            invalid_ids.append(cid)
    
    if not valid_ids:
        await interaction.response.send_message("유효한 챌린지 ID가 없습니다.", ephemeral=True)
        return
    
    pack_id = get_next_pack_id()
    packs[pack_id] = {
        "name": 팩이름,
        "challenges": valid_ids,
        "created_at": datetime.now().isoformat()
    }
    save_json("packs.json", packs)
    
    embed = discord.Embed(
        title="챌린지팩 생성 완료",
        description=f"**{팩이름}** (ID: {pack_id})",
        color=discord.Color.green()
    )
    embed.add_field(name="포함된 챌린지", value=f"{len(valid_ids)}개", inline=True)
    if invalid_ids:
        embed.add_field(name="유효하지 않은 ID", value=", ".join(invalid_ids), inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="챌린지팩삭제", description="[관리자 전용] 챌린지팩을 삭제합니다")
@app_commands.describe(
    팩id="삭제할 팩 ID"
)
async def delete_pack(
    interaction: discord.Interaction,
    팩id: str
):
    if not is_admin(interaction.user.id):
        await interaction.response.send_message("관리자만 사용 가능합니다.", ephemeral=True)
        return
    
    packs = load_json("packs.json")
    
    if 팩id not in packs:
        await interaction.response.send_message("존재하지 않는 팩 ID입니다.", ephemeral=True)
        return
    
    pack_name = packs[팩id]["name"]
    del packs[팩id]
    save_json("packs.json", packs)
    
    await interaction.response.send_message(f"**{pack_name}** (ID: {팩id}) 팩이 삭제되었습니다.")

@bot.tree.command(name="챌린지팩부분삭제", description="[관리자 전용] 팩에서 특정 챌린지를 삭제합니다")
@app_commands.describe(
    팩id="팩 ID",
    챌린지id="삭제할 챌린지 ID"
)
async def pack_remove_challenge(
    interaction: discord.Interaction,
    팩id: str,
    챌린지id: str
):
    if not is_admin(interaction.user.id):
        await interaction.response.send_message("관리자만 사용 가능합니다.", ephemeral=True)
        return
    
    packs = load_json("packs.json")
    
    if 팩id not in packs:
        await interaction.response.send_message("존재하지 않는 팩 ID입니다.", ephemeral=True)
        return
    
    if 챌린지id not in packs[팩id]["challenges"]:
        await interaction.response.send_message("해당 챌린지가 팩에 없습니다.", ephemeral=True)
        return
    
    packs[팩id]["challenges"].remove(챌린지id)
    save_json("packs.json", packs)
    
    await interaction.response.send_message(f"팩 **{packs[팩id]['name']}**에서 챌린지 ID {챌린지id}를 삭제했습니다.")

@bot.tree.command(name="챌린지팩부분추가", description="[관리자 전용] 팩에 챌린지를 추가합니다")
@app_commands.describe(
    팩id="팩 ID",
    챌린지id="추가할 챌린지 ID"
)
async def pack_add_challenge(
    interaction: discord.Interaction,
    팩id: str,
    챌린지id: str
):
    if not is_admin(interaction.user.id):
        await interaction.response.send_message("관리자만 사용 가능합니다.", ephemeral=True)
        return
    
    packs = load_json("packs.json")
    challenges = load_json("challenges.json")
    
    if 팩id not in packs:
        await interaction.response.send_message("존재하지 않는 팩 ID입니다.", ephemeral=True)
        return
    
    if 챌린지id not in challenges:
        await interaction.response.send_message("존재하지 않는 챌린지 ID입니다.", ephemeral=True)
        return
    
    if 챌린지id in packs[팩id]["challenges"]:
        await interaction.response.send_message("이미 팩에 포함된 챌린지입니다.", ephemeral=True)
        return
    
    packs[팩id]["challenges"].append(챌린지id)
    save_json("packs.json", packs)
    
    await interaction.response.send_message(f"팩 **{packs[팩id]['name']}**에 챌린지 ID {챌린지id}를 추가했습니다.")

@bot.tree.command(name="챌린지팩모두검색", description="모든 챌린지팩을 검색합니다")
async def search_all_packs(interaction: discord.Interaction):
    packs = load_json("packs.json")
    
    if not packs:
        await interaction.response.send_message("등재된 챌린지팩이 없습니다.", ephemeral=True)
        return
    
    fields = [
        (f"{pack['name']} (ID: {pack_id})", f"챌린지 수: {len(pack['challenges'])}개")
        for pack_id, pack in packs.items()
    ]
    
    view = AchievementListView("챌린지팩 목록", f"총 {len(fields)}개의 챌린지팩", fields)
    await interaction.response.send_message(embed=view.create_embed(), view=view)

@bot.tree.command(name="챌린지팩열기", description="챌린지팩의 내용을 확인합니다")
@app_commands.describe(
    팩id="열어볼 팩 ID"
)
async def open_pack(
    interaction: discord.Interaction,
    팩id: str
):
    packs = load_json("packs.json")
    challenges = load_json("challenges.json")
    clears = load_json("clears.json")
    
    if 팩id not in packs:
        await interaction.response.send_message("존재하지 않는 팩 ID입니다.", ephemeral=True)
        return
    
    pack = packs[팩id]
    
    embed = discord.Embed(
        title=f"챌린지팩: {pack['name']}",
        description=f"총 {len(pack['challenges'])}개의 챌린지",
        color=discord.Color.blue()
    )
    
    for cid in pack["challenges"]:
        if cid in challenges:
            challenge = challenges[cid]
            emoji = get_difficulty_emoji(challenge["actual_difficulty"])
            clear_count = sum(1 for c in clears.values() 
                           if c["challenge_id"] == cid and c["status"] == "approved")
            embed.add_field(
                name=f"{emoji} {challenge['name']}",
                value=f"ID: {cid} | PP: {fmt_pp(get_challenge_pp(challenge))} | 클리어: {clear_count}명",
                inline=False
            )
    
    await interaction.response.send_message(embed=embed)

# ============================================
# 홀짝 게임
# ============================================

@bot.tree.command(name="홀짝", description="홀짝 게임을 시작합니다")
@app_commands.describe(
    금액="베팅할 C",
    선택="홀 또는 짝"
)
@app_commands.choices(선택=[
    app_commands.Choice(name="홀", value="홀"),
    app_commands.Choice(name="짝", value="짝")
])
async def odd_even_game(
    interaction: discord.Interaction,
    금액: int,
    선택: str
):
    user_id = str(interaction.user.id)
    user_data = get_user_data(user_id)
    
    if 금액 <= 0:
        await interaction.response.send_message("1C 이상 베팅해야 합니다.", ephemeral=True)
        return
    
    if user_data.get("coins", 0) < 금액:
        await interaction.response.send_message(f"C가 부족합니다. 보유: {user_data.get('coins', 0):,}C", ephemeral=True)
        return
    
    # 수수료 계산
    supporter_level = get_user_supporter_level(user_id)
    fee_percent = SUPPORTER_FEE_REDUCTION.get(supporter_level, 4)
    fee = int(금액 * fee_percent / 100)
    
    # 랜덤 결과
    result_num = random.randint(1, 100)
    result = "홀" if result_num % 2 == 1 else "짝"
    
    embed = discord.Embed(
        title="홀짝 게임",
        color=discord.Color.gold()
    )
    embed.add_field(name="숫자", value=str(result_num), inline=True)
    embed.add_field(name="결과", value=result, inline=True)
    embed.add_field(name="선택", value=선택, inline=True)
    
    if result == 선택:
        # 승리
        winnings = 금액 - fee
        user_data["coins"] += winnings
        
        # 도박왕 업적: 100C 이상 베팅 승리 카운트
        if 금액 >= 100:
            user_data["bet_wins"] = user_data.get("bet_wins", 0) + 1
        
        # 무패신화 업적: 홀짝 연승 카운트
        user_data["holjjak_streak"] = user_data.get("holjjak_streak", 0) + 1
        
        save_user_data(user_id, user_data)
        
        embed.description = f"**승리!** +{winnings:,}C (수수료 {fee:,}C)"
        embed.color = discord.Color.green()
        
    else:
        # 패배 (연승 초기화)
        user_data["holjjak_streak"] = 0
        user_data["coins"] -= 금액
        save_user_data(user_id, user_data)
        
        embed.description = f"**패배!** -{금액:,}C"
        embed.color = discord.Color.red()
    
    embed.add_field(name="현재 C", value=f"{user_data['coins']:,}C", inline=False)
    if fee_percent > 0:
        embed.set_footer(text=f"수수료: {fee_percent}%")
    else:
        embed.set_footer(text="서포터 4레벨: 수수료 면제")
    
    await interaction.response.send_message(embed=embed)
    
    # 업적 체크 및 부여 (무패신화 등)
    await check_and_grant_achievements(user_id, interaction.guild, trigger_type="holjjak")

    if result == 선택 and 금액 >= 100:
        await check_and_grant_achievements(user_id, interaction.guild, trigger_type="bet_win")

# ============================================
# 서포터 구매 시스템 (상점 이용 버튼 수정)
# ============================================

class CategorySelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        
        options = [
            discord.SelectOption(label="코인", description="C를 구매합니다", value="coin", emoji=COIN_EMOJI.split(":")[1].split(">")[0] if ">" in COIN_EMOJI else None),
            discord.SelectOption(label="서포터", description="서포터 등급을 구매합니다", value="supporter"),
        ]
        
        select = discord.ui.Select(
            placeholder="카테고리를 선택하세요",
            options=options,
            custom_id="category_select"
        )
        select.callback = self.select_callback
        self.add_item(select)
    
    async def select_callback(self, interaction: discord.Interaction):
        selected = interaction.data["values"][0]
        
        if selected == "coin":
            embed = discord.Embed(
                title="C 구매",
                description="구매할 C 패키지를 선택해주세요.",
                color=discord.Color.green()
            )
            view = ProductSelectViewNew()
            await interaction.response.edit_message(embed=embed, view=view)
        else:
            embed = discord.Embed(
                title="서포터 구매",
                description="구매할 서포터 등급을 선택해주세요.\n(30일 기준)",
                color=discord.Color.gold()
            )
            view = SupporterSelectView()
            await interaction.response.edit_message(embed=embed, view=view)

class ProductSelectViewNew(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        
        options = [
            discord.SelectOption(label="500C", description="1,000원", value="500C"),
            discord.SelectOption(label="2,200C", description="4,000원", value="2,200C"),
            discord.SelectOption(label="6,000C", description="10,000원", value="6,000C"),
            discord.SelectOption(label="13,000C", description="20,000원", value="13,000C"),
            discord.SelectOption(label="33,000C", description="50,000원", value="33,000C"),
        ]
        
        select = discord.ui.Select(
            placeholder="구매할 상품을 선택하세요",
            options=options,
            custom_id="product_select_new"
        )
        select.callback = self.select_callback
        self.add_item(select)
    
    async def select_callback(self, interaction: discord.Interaction):
        selected = interaction.data["values"][0]
        product = C_PRODUCTS[selected]
        
        embed = discord.Embed(
            title="구매 확인",
            description=f"**{selected}**를 구매하시겠습니까?",
            color=discord.Color.blue()
        )
        embed.add_field(name="획득 C", value=f"{product['c_amount']:,}C", inline=True)
        embed.add_field(name="가격", value=f"{product['price']:,}원", inline=True)
        
        view = PurchaseConfirmView(selected, product)
        await interaction.response.edit_message(embed=embed, view=view)

class SupporterSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        
        options = [
            discord.SelectOption(label="서포터 1레벨", description="4,990원 (30일)", value="1"),
            discord.SelectOption(label="서포터 2레벨", description="9,800원 (30일)", value="2"),
            discord.SelectOption(label="서포터 3레벨", description="14,900원 (30일)", value="3"),
            discord.SelectOption(label="서포터 4레벨", description="29,900원 (30일)", value="4"),
        ]
        
        select = discord.ui.Select(
            placeholder="서포터 등급을 선택하세요",
            options=options,
            custom_id="supporter_select"
        )
        select.callback = self.select_callback
        self.add_item(select)
    
    async def select_callback(self, interaction: discord.Interaction):
        selected_level = int(interaction.data["values"][0])
        price = SUPPORTER_PRICES[selected_level]
        emoji = SUPPORTER_EMOJIS[selected_level]
        
        embed = discord.Embed(
            title="서포터 구매 확인",
            description=f"**서포터 {selected_level}레벨** {emoji}를 구매하시겠습니까?",
            color=discord.Color.gold()
        )
        embed.add_field(name="가격", value=f"{price:,}원", inline=True)
        embed.add_field(name="기간", value="30일", inline=True)
        
        # 혜택 표시
        benefits = []
        benefits.append(f"채팅 시 {SUPPORTER_CHAT_BONUS[selected_level]}C 지급")
        fee = SUPPORTER_FEE_REDUCTION[selected_level]
        if fee == 0:
            benefits.append("홀짝 수수료 면제")
        else:
            benefits.append(f"홀짝 수수료 {fee}%")
        benefits.append(f"프로필에 {emoji} 표시")
        
        embed.add_field(name="혜택", value="\n".join(benefits), inline=False)
        
        view = SupporterPurchaseConfirmView(selected_level, price)
        await interaction.response.edit_message(embed=embed, view=view)

class SupporterPurchaseConfirmView(discord.ui.View):
    def __init__(self, level: int, price: int):
        super().__init__(timeout=180)
        self.level = level
        self.price = price
    
    @discord.ui.button(label="구매하기", style=discord.ButtonStyle.success)
    async def confirm_purchase(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = str(interaction.user.id)
        user_data = get_user_data(user_id)
        
        if user_data.get("balance", 0) < self.price:
            await interaction.response.send_message(
                f"보유금액이 부족합니다.\n필요: {self.price:,}원, 보유: {user_data.get('balance', 0):,}원",
                ephemeral=True
            )
            return
        
        # 구매 처리
        user_data["balance"] -= self.price
        user_data["total_spent"] = user_data.get("total_spent", 0) + self.price
        user_data["supporter_level"] = self.level
        
        # 만료일 설정 (30일 후)
        from datetime import timedelta
        expiry = datetime.now() + timedelta(days=30)
        user_data["supporter_until"] = expiry.isoformat()
        
        save_user_data(user_id, user_data)
        
        # 역할 지급
        try:
            guild = interaction.guild
            if guild:
                member = guild.get_member(interaction.user.id)
                if member:
                    # 기존 서포터 역할 모두 제거
                    for lvl, role_id in SUPPORTER_ROLES.items():
                        role = guild.get_role(role_id)
                        if role and role in member.roles:
                            await member.remove_roles(role)
                    
                    # 새 서포터 역할 지급
                    new_role = guild.get_role(SUPPORTER_ROLES[self.level])
                    if new_role:
                        await member.add_roles(new_role)
        except Exception as e:
            print(f"서포터 역할 지급 오류: {e}")
        
        emoji = SUPPORTER_EMOJIS[self.level]
        embed = discord.Embed(
            title="서포터 구매 완료!",
            description=f"**서포터 {self.level}레벨** {emoji}를 구매했습니다.",
            color=discord.Color.green()
        )
        embed.add_field(name="만료일", value=expiry.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="현재 보유금액", value=f"{user_data['balance']:,}원", inline=True)
        
        await interaction.response.edit_message(embed=embed, view=None)
    
    @discord.ui.button(label="취소", style=discord.ButtonStyle.danger)
    async def cancel_purchase(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="구매가 취소되었습니다.", embed=None, view=None)

@bot.tree.command(name="내기", description="1:1 내기를 신청합니다")
@app_commands.describe(
    상대="내기 상대",
    금액="베팅할 C 금액",
    주제="내기 주제"
)
async def bet(interaction: discord.Interaction, 상대: discord.Member, 금액: int, 주제: str):
    global active_bets
    active_bets = load_json("bets.json")
    
    host_id = str(interaction.user.id)
    target_id = str(상대.id)
    
    if host_id == target_id:
        await interaction.response.send_message("자기 자신과 내기할 수 없습니다!", ephemeral=True)
        return
    
    if 금액 < 10:
        await interaction.response.send_message("최소 베팅금액은 10C입니다.", ephemeral=True)
        return
    
    host_data = get_user_data(host_id)
    if host_data.get("coins", 0) < 금액:
        await interaction.response.send_message(f"C가 부족합니다! (보유: {host_data.get('coins', 0)}C)", ephemeral=True)
        return
    
    # 호스트 C 선차감
    remove_coins(host_id, 금액)
    
    bet_id = str(uuid.uuid4())[:8]
    active_bets[bet_id] = {
        "host_id": host_id,
        "target_id": target_id,
        "amount": 금액,
        "topic": 주제,
        "status": "pending",
        "timestamp": time.time()
    }
    save_json("bets.json", active_bets)
    
    view = BetAcceptView(bet_id, host_id, target_id, 금액, 주제)
    
    await interaction.response.send_message(
        content=f"**{상대.mention}님에게 내기 신청!**\n\n"
                f"주제: {주제}\n"
                f"금액: {금액}C\n"
                f"내기 ID: `{bet_id}`\n\n"
                f"수락하시겠습니까?",
        view=view
    )


@bot.tree.command(name="내기결과", description="[관리자] 내기 결과를 정합니다")
@app_commands.describe(
    내기id="내기 ID",
    승자="승자 선택"
)
async def bet_result(interaction: discord.Interaction, 내기id: str, 승자: discord.Member):
    if not is_admin(interaction.user.id):
        await interaction.response.send_message("관리자만 사용할 수 있습니다.", ephemeral=True)
        return
    
    global active_bets
    active_bets = load_json("bets.json")
    
    if 내기id not in active_bets:
        await interaction.response.send_message("해당 내기를 찾을 수 없습니다.", ephemeral=True)
        return
    
    bet_data = active_bets[내기id]
    
    if bet_data["status"] != "active":
        await interaction.response.send_message("아직 수락되지 않은 내기입니다.", ephemeral=True)
        return
    
    winner_id = str(승자.id)
    
    if winner_id not in [bet_data["host_id"], bet_data["target_id"]]:
        await interaction.response.send_message("승자는 내기 참여자 중 한 명이어야 합니다.", ephemeral=True)
        return
    
    # 승자에게 총 베팅금 지급 (수수료 4%)
    total_pot = bet_data["amount"] * 2
    reward = int(total_pot * 0.96)
    add_coins(winner_id, reward)
    
    # 내기 종료
    del active_bets[내기id]
    save_json("bets.json", active_bets)
    
    await interaction.response.send_message(
        f"**내기 종료!**\n\n"
        f"주제: {bet_data['topic']}\n"
        f"승자: {승자.mention}\n"
        f"획득: {reward}C (수수료 4%)"
    )
 

@bot.tree.command(name="출석", description="일일 출석 체크 (1~30C) + a")
async def daily_checkin(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    checkins = load_json("checkins.json")
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    user_checkin = checkins.get(user_id, {"last_date": None, "streak": 0})
    last_date = user_checkin.get("last_date")
    streak = user_checkin.get("streak", 0)
    
    if last_date == today:
        await interaction.response.send_message("오늘은 이미 출석했습니다!", ephemeral=True)
        return
    
    # 연속 출석 계산
    if last_date:
        last = datetime.strptime(last_date, "%Y-%m-%d")
        diff = (datetime.now() - last).days
        if diff == 1:
            streak += 1
        elif diff > 1:
            streak = 1
    else:
        streak = 1
    
    # 기본 보상 50~100C + 연속 출석 보너스
    base_reward = random.randint(1, 30)
    streak_bonus = min((streak - 1) * 2, 30)  # 2일 연속부터 +2씩, 최대 30C (16일)
    total_reward = base_reward + streak_bonus
    
    add_coins(user_id, total_reward)
    
    # 저장
    checkins[user_id] = {"last_date": today, "streak": streak}
    save_json("checkins.json", checkins)
    
    embed = discord.Embed(
        title="출석 완료!",
        description=f"기본 보상: {base_reward}C\n연속 출석 보너스: +{streak_bonus}C\n\n**총 획득: {total_reward}C**",
        color=discord.Color.green()
    )
    embed.add_field(name="연속 출석", value=f"{streak}일")
    embed.set_footer(text=f"현재 보유: {get_user_data(user_id).get('coins', 0)}C")
    
    await interaction.response.send_message(embed=embed)
    
    # 업적 체크 및 부여
    await check_and_grant_achievements(user_id, interaction.guild, trigger_type="coins")
    
# 활성 내기 저장
active_bets = {}  # {bet_id: {"host_id", "target_id", "amount", "topic", "status", "message_id"}}

class BetAcceptView(discord.ui.View):
    """내기 수락/거절 뷰"""
    def __init__(self, bet_id: str, host_id: str, target_id: str, amount: int, topic: str):
        super().__init__(timeout=300)
        self.bet_id = bet_id
        self.host_id = host_id
        self.target_id = target_id
        self.amount = amount
        self.topic = topic

    @discord.ui.button(label="수락", style=discord.ButtonStyle.success)
    async def accept_bet(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.target_id:
            await interaction.response.send_message("이 내기의 대상자가 아닙니다!", ephemeral=True)
            return
        
        # 대상자 잔액 확인
        target_data = get_user_data(self.target_id)
        if target_data.get("coins", 0) < self.amount:
            await interaction.response.send_message(f"C가 부족합니다! (필요: {self.amount}C)", ephemeral=True)
            return
        
        # 대상자 C 차감
        remove_coins(self.target_id, self.amount)
        
        # 내기 활성화
        active_bets[self.bet_id]["status"] = "active"
        save_json("bets.json", active_bets)
        
        self.disable_all_items()
        await interaction.response.edit_message(
            content=f"**내기 성립!**\n주제: {self.topic}\n금액: {self.amount}C\n\n관리자가 `/내기결과 {self.bet_id} <승자>` 명령어로 결과를 정해주세요.",
            view=self
        )

    @discord.ui.button(label="거절", style=discord.ButtonStyle.danger)
    async def decline_bet(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.target_id:
            await interaction.response.send_message("이 내기의 대상자가 아닙니다!", ephemeral=True)
            return
        
        # 호스트에게 C 환불
        add_coins(self.host_id, self.amount)
        
        # 내기 삭제
        if self.bet_id in active_bets:
            del active_bets[self.bet_id]
            save_json("bets.json", active_bets)
        
        self.disable_all_items()
        await interaction.response.edit_message(
            content=f"~~{self.topic}~~\n\n**내기가 거절되었습니다.** (환불 완료)",
            view=self
        )

    def disable_all_items(self):
        for item in self.children:
            item.disabled = True
    
LOTTERY_PRICE = 10  # 복권 가격
LOTTERY_REWARDS = [
    (0.68353, 0),      # 70% - 꽝
    (0.25, 2),      # 20% - 2배 (20C)
    (0.03, 3),      # 8% - 5배 (50C)
    (0.02, 5),    # 1.9% - 10배 (100C)
    (0.001, 10),
    (0.001, 25),      # 70% - 꽝
    (0.001, 50),      # 20% - 2배 (20C)
    (0.003, 100),      # 8% - 5배 (50C)
    (0.0001, 200),    # 1.9% - 10배 (100C)
    (0.00005, 500),
    (0.00002, 1000),
]

@bot.tree.command(name="복권", description="복권을 구매합니다 (10C)")
async def lottery(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    user_data = get_user_data(user_id)
    
    if user_data.get("coins", 0) < LOTTERY_PRICE:
        await interaction.response.send_message(
            f"C가 부족합니다! (보유: {user_data.get('coins', 0)}C, 필요: {LOTTERY_PRICE}C)",
            ephemeral=True
        )
        return
    
    # 복권 구매
    remove_coins(user_id, LOTTERY_PRICE)
    
    # 확률 계산
    roll = random.random()
    cumulative = 0
    multiplier = 0
    
    for prob, mult in LOTTERY_REWARDS:
        cumulative += prob
        if roll < cumulative:
            multiplier = mult
            break
    
    reward = LOTTERY_PRICE * multiplier
    
    if reward > 0:
        add_coins(user_id, reward)
    
    # 복권 최고 배수 기록 (업적용)
    lottery_user_data = get_user_data(user_id)
    if multiplier > lottery_user_data.get("best_lottery", 0):
        lottery_user_data["best_lottery"] = multiplier
        save_user_data(user_id, lottery_user_data)
    
    # 결과 이모지
    if multiplier == 0:
        result_emoji = "<:kangmincheol:1494961043640684644>"
        result_text = "꽝!"
    elif multiplier == 2:
        result_emoji = "<:darkmatterflamingo:1494960891576189159>"
        result_text = f"2배! +{reward}C"
    elif multiplier == 3:
        result_emoji = "<a:writing:1494960952037212294>"
        result_text = f"3배! 아자스 +{reward}C"
    elif multiplier == 5:
        result_emoji = "<:fang:1495362399325261887>"
        result_text = f"5배!! +{reward}C"
    elif multiplier == 10:
        result_emoji = "<:aikawa:1495362437216600235>"
        result_text = f"10배!! 개맛있다 +{reward}C"
    elif multiplier == 25:
        result_emoji = "<:haeun:1495362561376391359>"
        result_text = f"25배!! 와.. +{reward}C"
    elif multiplier == 50:
        result_emoji = "<:haeun:1495362561376391359>"
        result_text = f"50배!!! +{reward}C"
    elif multiplier == 100:
        result_emoji = "<:j_:1495362462428561498>"
        result_text = f"100배!!!! +{reward}C"
    elif multiplier == 200:
        result_emoji = "<:i_:1495362490190794853>"
        result_text = f"200배!!!! 말이 안된다.. +{reward}C"
    elif multiplier == 500:
        result_emoji = "<:i_:1495362490190794853>"
        result_text = f"500배! 대박박~ +{reward}C"
    else:
        result_emoji = "<:brilliant:1495362626019135560>"
        result_text = f"**1000배요...?** +{reward}C"
    
    embed = discord.Embed(
        title=f"{result_emoji} 복권 결과",
        description=result_text,
        color=discord.Color.gold() if multiplier > 0 else discord.Color.greyple()
    )
    embed.set_footer(text=f"현재 보유: {get_user_data(user_id).get('coins', 0)}C")
    
    await interaction.response.send_message(embed=embed)
    
    # 업적 체크 및 부여 (복권 최고 배수 + 보유 C)
    await check_and_grant_achievements(user_id, interaction.guild, trigger_type="lottery")
# ============================================
# 영어부분

@bot.tree.command(name="searchall", description="search for all challenges (including sorting options)")
@app_commands.describe(
    sorting="sort method (default: id up order)"
)
async def search_all_challenges(
    interaction: discord.Interaction,
    sorting: Optional[Literal["id ascending order", "id descending order", "generation day ascending order", "generation day descending order", "difficulty ascending order", "difficulty descending order"]] = "id ascending order"
):
    challenges = load_json("challenges.json")
    leaderboard = load_json("leaderboard.json")
    clears = load_json("clears.json")
    
    results = [(cid, challenge) for cid, challenge in challenges.items()]
    
    if not results:
        embed = discord.Embed(
            title="챌린지 없음",
            description="등재된 챌린지가 없습니다.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    if sorting == "id ascending order":
        results.sort(key=lambda x: int(x[0]))
    elif sorting == "id descending order":
        results.sort(key=lambda x: int(x[0]), reverse=True)
    elif sorting == "generation day ascending order":
        results.sort(key=lambda x: x[1]["registered_at"])
    elif sorting == "generation day descending order":
        results.sort(key=lambda x: x[1]["registered_at"], reverse=True)
    elif sorting == "difficulty ascending order":
        special_order = ["censored", "impossible", "epic", "gimmick", "marathon"]
        def difficulty_sort_key(item):
            difficulty = item[1]["actual_difficulty"]
            if difficulty in special_order:
                return (0, special_order.index(difficulty))
            else:
                return (1, get_difficulty_rank(difficulty))
        results.sort(key=difficulty_sort_key)
    elif sorting == "difficulty descending order":
        special_order = ["censored", "impossible", "epic", "gimmick", "marathon"]
        def difficulty_sort_key_desc(item):
            difficulty = item[1]["actual_difficulty"]
            if difficulty in special_order:
                return (1, len(special_order) - special_order.index(difficulty))
            else:
                return (0, 100 - get_difficulty_rank(difficulty))
        results.sort(key=difficulty_sort_key_desc)
    
    view = SearchResultsView(results, leaderboard, clears)
    embed = view.create_embed()
    await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="search", description="search for a challenge")
@app_commands.describe(
    challenge_name="challenge name to search (keyword)",
    difficulty="difficulty level to filter (optional)"
)
async def search_challenges(
    interaction: discord.Interaction,
    challenge_name: str,
    difficulty: Optional[str] = None
):
    challenges = load_json("challenges.json")
    leaderboard = load_json("leaderboard.json")
    clears = load_json("clears.json")
    
    results = []
    for cid, challenge in challenges.items():
        if challenge_name.lower() in challenge["name"].lower():
            if difficulty and challenge["actual_difficulty"] != difficulty:
                continue
            results.append((cid, challenge))
    
    if not results:
        embed = discord.Embed(
            title="no search results",
            description="there are no challenges that match this keyword.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    results.sort(key=lambda x: get_difficulty_rank(x[1]["actual_difficulty"]))
    
    view = SearchResultsView(results, leaderboard, clears)
    embed = view.create_embed()
    await interaction.response.send_message(embed=embed, view=view)


def sort_difficulties_by_order(difficulties):
    """난이도 리스트를 DIFFICULTY_ORDER 기준으로 정렬 (없는 난이도는 뒤로)"""
    def sort_key(diff):
        if diff in DIFFICULTY_ORDER:
            return (0, DIFFICULTY_ORDER.index(diff))
        return (1, get_difficulty_rank(diff))
    return sorted(difficulties, key=sort_key)


class DifficultyDistributionView(discord.ui.View):
    def __init__(self, dist_list: list, title: str, suffix: str):
        super().__init__(timeout=180)
        self.dist_list = dist_list  # [(난이도, 개수), ...]
        self.title = title
        self.suffix = suffix  # "개" 또는 "passed"
        self.current_page = 0
        self.items_per_page = 10
        self.update_buttons()

    def update_buttons(self):
        total_pages = (len(self.dist_list) - 1) // self.items_per_page + 1
        self.children[0].disabled = self.current_page <= 0
        self.children[1].disabled = self.current_page >= total_pages - 1

    def create_embed(self):
        start_idx = self.current_page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_items = self.dist_list[start_idx:end_idx]
        total_pages = (len(self.dist_list) - 1) // self.items_per_page + 1

        lines = []
        for difficulty, count in page_items:
            emoji = get_difficulty_emoji(difficulty)
            lines.append(f"{emoji} {difficulty} - {count} {self.suffix}")

        embed = discord.Embed(
            title=self.title,
            description="\n".join(lines) if lines else "데이터가 없습니다.",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"page {self.current_page + 1}/{total_pages}")
        return embed

    @discord.ui.button(label="◀", style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="▶", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        total_pages = (len(self.dist_list) - 1) // self.items_per_page + 1
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.update_buttons()
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)


@bot.tree.command(name="난이도분포도", description="현재 등재된 챌린지의 난이도 분포를 확인합니다")
async def difficulty_distribution(interaction: discord.Interaction):
    challenges = load_json("challenges.json")

    # 난이도별 등재된 챌린지 개수 집계
    counts = {}
    for challenge in challenges.values():
        difficulty = challenge.get("actual_difficulty")
        if not difficulty:
            continue
        counts[difficulty] = counts.get(difficulty, 0) + 1

    if not counts:
        embed = discord.Embed(
            title="난이도 분포도",
            description="아직 등재된 챌린지가 없습니다.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return

    ordered = sort_difficulties_by_order(counts.keys())
    dist_list = [(d, counts[d]) for d in ordered]

    view = DifficultyDistributionView(dist_list, "난이도 분포도", "개")
    embed = view.create_embed()
    await interaction.response.send_message(embed=embed, view=view)


@bot.tree.command(name="클리어난이도분포도", description="난이도별 클리어 횟수 분포를 확인합니다")
async def clear_difficulty_distribution(interaction: discord.Interaction):
    clears = load_json("clears.json")

    # 난이도별 승인된 클리어 횟수 집계
    counts = {}
    for clear in clears.values():
        if clear.get("status") != "approved":
            continue
        difficulty = clear.get("difficulty")
        if not difficulty:
            continue
        counts[difficulty] = counts.get(difficulty, 0) + 1

    if not counts:
        embed = discord.Embed(
            title="클리어 난이도 분포도",
            description="아직 클리어 기록이 없습니다.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return

    ordered = sort_difficulties_by_order(counts.keys())
    dist_list = [(d, counts[d]) for d in ordered]

    view = DifficultyDistributionView(dist_list, "클리어 난이도 분포도", "passed")
    embed = view.create_embed()
    await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="통계", description="내 클리어 통계를 확인합니다")
async def my_stats(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    clears = load_json("clears.json")
    leaderboard = load_json("leaderboard.json")

    # 승인된 내 클리어만
    user_clears = [c for c in clears.values()
                   if c["user_id"] == user_id and c["status"] == "approved"]

    if not user_clears:
        await interaction.response.send_message("아직 클리어한 챌린지가 없습니다.", ephemeral=True)
        return

    # 카테고리별 집계
    cat = {"U": 0, "G": 0, "P": 0, "Q": 0, "R": 0, "특수": 0}
    total_pp = 0.0
    hardest = None
    hardest_rank = -1
    for c in user_clears:
        diff = c["difficulty"]
        total_pp += get_clear_pp(c)
        if diff.startswith("U"):
            cat["U"] += 1
        elif diff.startswith("G"):
            cat["G"] += 1
        elif diff.startswith("P"):
            cat["P"] += 1
        else:
            cat["특수"] -= 1
        r = get_difficulty_rank(diff)
        if diff.startswith(("Q", "R")) or diff == "특수":
            r = -1
        if r > hardest_rank:
            hardest_rank = r
            hardest = diff

    rank_score = leaderboard.get(user_id, {}).get("rank_score", calculate_rank_score(user_id))
    first_clears = get_first_clear_count(user_id, clears)

    embed = discord.Embed(
        title=f"📊 {interaction.user.name}님의 통계",
        color=discord.Color.blurple()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.add_field(name="총 클리어 수", value=f"{len(user_clears)}개", inline=True)
    embed.add_field(name="최고 난이도",
                    value=f"{get_difficulty_emoji(hardest)} {hardest}" if hardest else "없음",
                    inline=True)
    embed.add_field(name="최초 클리어", value=f"{first_clears}개", inline=True)
    embed.add_field(name="총 PP", value=f"{round(total_pp, 2)}PP", inline=True)
    embed.add_field(name="랭크 점수", value=f"{round(rank_score, 2)}PP", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)
    embed.add_field(
        name="난이도별 클리어",
        value=(f"🟣 U: {cat['U']}  |  🟡 G: {cat['G']}  |  🔵 P: {cat['P']}\n"
               f"Q: {cat['Q']}  |  R: {cat['R']}  |  특수: {cat['특수']}"),
        inline=False
    )
    await interaction.response.send_message(embed=embed)
    
    
@bot.tree.command(name="비교", description="다른 유저와 통계를 비교합니다")
@app_commands.describe(대상="비교할 유저")
async def compare_stats(interaction: discord.Interaction, 대상: discord.User):
    clears = load_json("clears.json")
    leaderboard = load_json("leaderboard.json")

    def summarize(uid: str):
        uc = [c for c in clears.values()
              if c["user_id"] == uid and c["status"] == "approved"]
        total_pp = sum(get_clear_pp(c) for c in uc)
        hardest, hardest_rank = None, -1
        for c in uc:
            r = get_difficulty_rank(c["difficulty"])
            if r > hardest_rank:
                hardest_rank, hardest = r, c["difficulty"]
        return {
            "count": len(uc),
            "total_pp": round(total_pp, 2),
            "rank_score": round(leaderboard.get(uid, {}).get("rank_score",
                               calculate_rank_score(uid)), 2),
            "first": get_first_clear_count(uid, clears),
            "hardest": hardest,
        }

    me = interaction.user
    a = summarize(str(me.id))
    b = summarize(str(대상.id))

    def cmp(x, y):
        if x > y:
            return "🥇", "🥈"
        elif x < y:
            return "🥈", "🥇"
        return "🤝", "🤝"

    def line(label, va, vb, suffix=""):
        ma, mb = cmp(va, vb)
        return f"**{label}**\n{ma} {va}{suffix}  vs  {vb}{suffix} {mb}\n"

    embed = discord.Embed(
        title=f"⚔️ {me.name}  vs  {대상.name}",
        color=discord.Color.gold()
    )
    desc = ""
    desc += line("총 클리어 수", a["count"], b["count"], "개")
    desc += line("총 PP", a["total_pp"], b["total_pp"], "PP")
    desc += line("랭크 점수", a["rank_score"], b["rank_score"], "PP")
    desc += line("최초 클리어", a["first"], b["first"], "개")
    ha = f"{get_difficulty_emoji(a['hardest'])} {a['hardest']}" if a["hardest"] else "없음"
    hb = f"{get_difficulty_emoji(b['hardest'])} {b['hardest']}" if b["hardest"] else "없음"
    ra = get_difficulty_rank(a["hardest"]) if a["hardest"] else -1
    rb = get_difficulty_rank(b["hardest"]) if b["hardest"] else -1
    ma, mb = cmp(ra, rb)
    desc += f"**최고 난이도**\n{ma} {ha}  vs  {hb} {mb}"

    embed.description = desc
    await interaction.response.send_message(embed=embed)
    
@bot.tree.command(name="기입", description="clears.json에 클리어를 직접 기입합니다 (관리자 전용, 알림/보상 없음)")
@app_commands.describe(
    id="유저 ID (숫자)",
    닉네임="표시할 닉네임",
    챌린지id="챌린지 ID",
    체감난이도="체감 난이도 (선택사항)"
)
async def write_clear(
    interaction: discord.Interaction,
    id: str,
    닉네임: str,
    챌린지id: str,
    체감난이도: Optional[str] = None
):
    if not is_admin(interaction.user.id):
        await interaction.response.send_message("관리자만 사용할 수 있습니다.", ephemeral=True)
        return

    challenges = load_json("challenges.json")
    if 챌린지id not in challenges:
        await interaction.response.send_message(f"ID '{챌린지id}'를 찾을 수 없습니다.", ephemeral=True)
        return

    challenge = challenges[챌린지id]
    user_id = str(id).strip()

    clears = load_json("clears.json")

    # 중복 방지
    for clear in clears.values():
        if clear["user_id"] == user_id and clear["challenge_id"] == 챌린지id and clear["status"] == "approved":
            await interaction.response.send_message("이미 기입된 클리어입니다.", ephemeral=True)
            return

    clear_id = str(uuid.uuid4())
    clears[clear_id] = {
        "user_id": user_id,
        "username": 닉네임,
        "challenge_id": 챌린지id,
        "difficulty": challenge["actual_difficulty"],
        "challenge_name": challenge["name"],
        "submitted_at": datetime.now().isoformat(),
        "status": "approved",
        "felt_difficulty": 체감난이도,
        "clear_id": clear_id
    }
    save_json("clears.json", clears)
    # 알림 X, 코인 X, 리더보드 X, 역할 X, 업적 X — clears.json만 기입

    emoji = get_difficulty_emoji(challenge["actual_difficulty"])
    embed = discord.Embed(
        title="기입 완료",
        description=f"**{닉네임}** (ID: {user_id})의 클리어가 clears.json에 기입되었습니다.",
        color=discord.Color.green()
    )
    embed.add_field(name="챌린지", value=f"{emoji} {challenge['name']} (ID: {챌린지id})", inline=False)
    embed.add_field(name="난이도", value=challenge["actual_difficulty"], inline=True)
    embed.add_field(name="체감 난이도", value=체감난이도 if 체감난이도 else "None", inline=True)
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
# ============================================

channel = bot.get_channel(CHANNEL_CHALLENGE_SUBMISSION)
print(f"[DEBUG] 채널: {channel}, ID: {CHANNEL_CHALLENGE_SUBMISSION}")
if channel:
    print("[DEBUG] 채널 찾음!")
else:
    print("[DEBUG] 채널을 찾을 수 없음!")
    
async def send_creator_notification(bot, creator_id: int, challenge_id: str, challenge_title: str, difficulty: str):
    try:
        creator = await bot.fetch_user(creator_id)
        embed = discord.Embed(
            title="✅ challenge listed",
            description=f"your challenge has been listed",
            color=discord.Color.green()
        )
        embed.add_field(name="title", value=challenge_title, inline=False)
        embed.add_field(name="difficulty", value=difficulty, inline=True)
        embed.add_field(name="ID", value=challenge_id, inline=True)
        
        await creator.send(embed=embed)
        print(f"[v0] DM sent to creator {creator_id} for challenge {challenge_id}")
    except Exception as e:
        print(f"[v0] Failed to send DM to creator {creator_id}: {e}")
        
if __name__ == "__main__":
    TOKEN = "ODcxNjYzODIwMjk5NDU2NTEz.GCYmDv.v7qQspDLN3L9lyFfaYEJNNJkCtfus4Y9IYOIuA"
    bot.run(TOKEN)
