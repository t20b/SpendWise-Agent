from app.db.init_db import DEFAULT_CATEGORIES

KEYWORD_CATEGORY_MAP = {
    "식비": ["식당", "김밥", "치킨", "피자", "버거", "분식", "마트", "이마트", "홈플러스", "롯데마트", "배달"],
    "카페/간식": ["스타벅스", "투썸", "커피", "카페", "디저트", "베이커리", "빵", "편의점", "세븐", "gs25", "cu"],
    "교통": ["택시", "버스", "지하철", "교통", "주유", "주차", "카카오t"],
    "쇼핑": ["쿠팡", "무신사", "쇼핑", "백화점", "올리브영"],
    "생활용품": ["다이소", "생활", "세탁", "청소"],
    "주거": ["월세", "관리비", "전기", "가스", "수도"],
    "통신": ["통신", "휴대폰", "인터넷", "kt", "skt", "lg유플러스"],
    "구독": ["넷플릭스", "유튜브", "멜론", "스포티파이", "구독", "디즈니"],
    "의료": ["병원", "약국", "치과", "의원"],
    "문화/여가": ["영화", "공연", "게임", "노래방", "헬스"],
    "교육": ["강의", "학원", "책", "도서", "교육"],
    "여행": ["호텔", "항공", "기차", "숙박", "여행"],
    "금융/보험": ["보험", "대출", "이자", "수수료"],
}


def normalize_category(category: str | None) -> str:
    if category in DEFAULT_CATEGORIES:
        return category
    return "기타"


def categorize_text(text: str) -> str:
    lowered = text.lower()
    for category, keywords in KEYWORD_CATEGORY_MAP.items():
        if any(keyword.lower() in lowered for keyword in keywords):
            return category
    return "기타"
