SEGMENT_SCENARIO = ["후킹", "문제상황", "제품소개", "사용장면", "혜택강조", "CTA"]

TEMPLATES = [
    {"id": 1, "name": "뼈순이 D-30일 스타일", "style": "캐릭터 챌린지",
     "narration_tone": "발랄하고 친근한", "rec_length": 30, "rec_model": "Veo", "active": True,
     "categories": [
        {"id": 11, "name": "캐릭터", "type": "asset", "items": [
            {"id": 111, "name": "뼈순이", "prompt": "cute white bone character, energetic", "image_url": ""},
            {"id": 112, "name": "근육이", "prompt": "muscular mascot, confident pose", "image_url": ""},
        ]},
        {"id": 12, "name": "후킹 문구", "type": "prompt", "items": [
            {"id": 121, "name": "D-30 시작", "prompt": "오늘부터 D-30, 함께 시작해요", "image_url": ""},
            {"id": 122, "name": "변화 예고", "prompt": "30일 뒤 달라진 나를 만나보세요", "image_url": ""},
        ]},
        {"id": 13, "name": "장면 구성", "type": "prompt", "items": [
            {"id": 131, "name": "비포애프터", "prompt": "일자별 비포/애프터 컷 전환", "image_url": ""},
            {"id": 132, "name": "일기형", "prompt": "매일 기록하는 일기 형식 구성", "image_url": ""},
        ]},
     ]},
    {"id": 2, "name": "실사 인터뷰 스타일", "style": "다큐/인터뷰",
     "narration_tone": "차분하고 진솔한", "rec_length": 30, "rec_model": "Google Flow", "active": True,
     "categories": [
        {"id": 21, "name": "인터뷰이", "type": "asset", "items": [
            {"id": 211, "name": "20대 여성", "prompt": "young woman interview, natural light", "image_url": ""},
            {"id": 212, "name": "30대 남성", "prompt": "man interview, office backdrop", "image_url": ""},
        ]},
        {"id": 22, "name": "질문 스크립트", "type": "prompt", "items": [
            {"id": 221, "name": "첫인상", "prompt": "처음 써봤을 때 느낌은 어땠나요?", "image_url": ""},
            {"id": 222, "name": "재구매", "prompt": "다시 구매할 의향이 있나요? 이유는?", "image_url": ""},
        ]},
     ]},
    {"id": 3, "name": "숏폼 바이럴 스타일", "style": "숏폼",
     "narration_tone": "에너지 넘치는", "rec_length": 15, "rec_model": "Seedance", "active": True,
     "categories": [
        {"id": 31, "name": "훅 문구", "type": "prompt", "items": [
            {"id": 311, "name": "3초 훅", "prompt": "3초 안에 시선을 잡는 강한 첫 문장", "image_url": ""},
            {"id": 312, "name": "궁금증", "prompt": "이거 모르면 손해예요", "image_url": ""},
        ]},
        {"id": 32, "name": "BGM 무드", "type": "prompt", "items": [
            {"id": 321, "name": "트렌디", "prompt": "trendy upbeat short-form bgm", "image_url": ""},
            {"id": 322, "name": "긴장감", "prompt": "tension build-up beat", "image_url": ""},
        ]},
     ]},
    {"id": 4, "name": "후기형 광고 스타일", "style": "리뷰",
     "narration_tone": "친근한 수다체", "rec_length": 30, "rec_model": "Veo", "active": True,
     "categories": [
        {"id": 41, "name": "후기 문구", "type": "prompt", "items": [
            {"id": 411, "name": "별점 5점", "prompt": "★★★★★ 인생템 찾았어요", "image_url": ""},
        ]},
     ]},
    {"id": 5, "name": "Before & After 스타일", "style": "비교",
     "narration_tone": "설득력 있는", "rec_length": 15, "rec_model": "Higgsfield", "active": True,
     "categories": [
        {"id": 51, "name": "비교 대상", "type": "asset", "items": [
            {"id": 511, "name": "제품컷", "prompt": "product front shot, clean bg", "image_url": ""},
        ]},
     ]},
    {"id": 6, "name": "프리미엄 브랜드 스타일", "style": "브랜딩",
     "narration_tone": "고급스럽고 절제된", "rec_length": 60, "rec_model": "Google Flow", "active": False,
     "categories": []},
    {"id": 7, "name": "애니메이션 광고 스타일", "style": "애니메이션",
     "narration_tone": "경쾌하고 명료한", "rec_length": 30, "rec_model": "Figma Weave", "active": True,
     "categories": [
        {"id": 71, "name": "캐릭터", "type": "asset", "items": [
            {"id": 711, "name": "마스코트", "prompt": "brand mascot, flat illustration", "image_url": ""},
        ]},
     ]},
]

# 상태값: 대기 중 / 생성 중 / 구간 생성 완료 / 합본 생성 중 / 완료 / 실패
JOBS = [
    {"id": 101, "name": "여름 다이어트 챌린지", "template": "뼈순이 D-30일 스타일",
     "model": "Veo", "length": 30, "status": "완료",
     "requested_at": "2026-07-01 10:12", "completed_at": "2026-07-01 10:41",
     "segments": [{"name": n, "status": "완료"} for n in SEGMENT_SCENARIO[:4]]},
    {"id": 102, "name": "신제품 런칭 티저", "template": "숏폼 바이럴 스타일",
     "model": "Seedance", "length": 15, "status": "생성 중",
     "requested_at": "2026-07-04 09:30", "completed_at": "",
     "segments": [{"name": "후킹", "status": "완료"}, {"name": "문제상황", "status": "생성 중"}]},
    {"id": 103, "name": "브랜드 무드 필름", "template": "프리미엄 브랜드 스타일",
     "model": "Google Flow", "length": 60, "status": "실패",
     "requested_at": "2026-07-03 15:00", "completed_at": "2026-07-03 15:22",
     "segments": [{"name": n, "status": "실패" if i == 2 else "완료"}
                  for i, n in enumerate(SEGMENT_SCENARIO[:5])]},
    {"id": 104, "name": "고객 후기 모음", "template": "후기형 광고 스타일",
     "model": "Veo", "length": 30, "status": "대기 중",
     "requested_at": "2026-07-04 11:00", "completed_at": "",
     "segments": [{"name": n, "status": "대기 중"} for n in SEGMENT_SCENARIO[:4]]},
]

RESULTS = [
    {"id": 201, "name": "여름 다이어트 챌린지", "final_video": "",
     "template": "뼈순이 D-30일 스타일", "assets": ["뼈순이 캐릭터", "메인 제품컷"],
     "model": "Veo", "created_at": "2026-07-01 10:41",
     "segments": [{"name": n, "video": "", "thumbnail": ""} for n in SEGMENT_SCENARIO[:4]]},
    {"id": 202, "name": "가을 시즌 프로모션", "final_video": "",
     "template": "Before & After 스타일", "assets": ["메인 제품컷", "브랜드 로고"],
     "model": "Higgsfield", "created_at": "2026-06-28 14:05",
     "segments": [{"name": n, "video": "", "thumbnail": ""} for n in SEGMENT_SCENARIO[:6]]},
]

SETTINGS = {
    "ip_restrict_enabled": True,
    "allowed_ips": ["203.0.113.10", "203.0.113.11"],
    "last_access_ip": "203.0.113.10",
    "access_logs": [
        {"ip": "203.0.113.10", "time": "2026-07-04 11:02", "result": "허용"},
        {"ip": "198.51.100.7", "time": "2026-07-04 08:41", "result": "차단"},
    ],
    "admin_account": "admin@company.com",
    "default_ratio": "9:16",
    "default_model": "Veo",
    "save_path": "/videos/output",
}

MODELS = ["Veo", "Google Flow", "Seedance", "Grok", "Higgsfield", "Figma Weave"]
RATIOS = ["16:9", "9:16", "1:1", "4:5"]


def get_stats():
    total_items = sum(len(c["items"]) for t in TEMPLATES for c in t["categories"])
    return {
        "total": len(JOBS),
        "completed": sum(1 for j in JOBS if j["status"] == "완료"),
        "generating": sum(1 for j in JOBS if j["status"] in ("생성 중", "합본 생성 중", "구간 생성 완료")),
        "failed": sum(1 for j in JOBS if j["status"] == "실패"),
        "templates": len(TEMPLATES),
        "pool_items": total_items,
        "recent_jobs": JOBS[:5],
    }
