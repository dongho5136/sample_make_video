SEGMENT_SCENARIO = ["후킹", "문제상황", "제품소개", "사용장면", "혜택강조", "CTA"]

TEMPLATES = [
    {"id": 1, "name": "뼈순이 D-30일 스타일", "style": "캐릭터 챌린지",
     "base_prompt": "귀여운 캐릭터가 30일 변화를 기록하는 톤",
     "subtitle_prompt": "굵은 노란 자막, 카운트다운 강조",
     "scene_prompt": "일자별 비포/애프터 컷 전환",
     "narration_tone": "발랄하고 친근한", "rec_length": 30,
     "rec_model": "Veo", "active": True},
    {"id": 2, "name": "실사 인터뷰 스타일", "style": "다큐/인터뷰",
     "base_prompt": "실제 사용자 인터뷰 형식의 신뢰감 있는 톤",
     "subtitle_prompt": "하단 자막바, 이름/직함 표기",
     "scene_prompt": "정면 인터뷰 + 제품 클로즈업 인서트",
     "narration_tone": "차분하고 진솔한", "rec_length": 30,
     "rec_model": "Google Flow", "active": True},
    {"id": 3, "name": "숏폼 바이럴 스타일", "style": "숏폼",
     "base_prompt": "3초 안에 시선을 잡는 빠른 컷 편집",
     "subtitle_prompt": "화면 중앙 큰 텍스트, 임팩트 효과",
     "scene_prompt": "빠른 장면 전환, 트렌디 BGM 싱크",
     "narration_tone": "에너지 넘치는", "rec_length": 15,
     "rec_model": "Seedance", "active": True},
    {"id": 4, "name": "후기형 광고 스타일", "style": "리뷰",
     "base_prompt": "구매 후기를 읽어주는 형식",
     "subtitle_prompt": "별점/후기 인용 자막",
     "scene_prompt": "제품 언박싱 + 사용 장면",
     "narration_tone": "친근한 수다체", "rec_length": 30,
     "rec_model": "Veo", "active": True},
    {"id": 5, "name": "Before & After 스타일", "style": "비교",
     "base_prompt": "사용 전후를 극적으로 대비",
     "subtitle_prompt": "'BEFORE'/'AFTER' 대비 자막",
     "scene_prompt": "분할 화면 비교 연출",
     "narration_tone": "설득력 있는", "rec_length": 15,
     "rec_model": "Higgsfield", "active": True},
    {"id": 6, "name": "프리미엄 브랜드 스타일", "style": "브랜딩",
     "base_prompt": "고급스럽고 미니멀한 브랜드 무드",
     "subtitle_prompt": "얇은 세리프 자막, 절제된 사용",
     "scene_prompt": "슬로우 모션, 제품 디테일 강조",
     "narration_tone": "고급스럽고 절제된", "rec_length": 60,
     "rec_model": "Google Flow", "active": False},
    {"id": 7, "name": "애니메이션 광고 스타일", "style": "애니메이션",
     "base_prompt": "일러스트/모션그래픽 기반 설명형",
     "subtitle_prompt": "말풍선/키네틱 타이포",
     "scene_prompt": "캐릭터 애니메이션 + 아이콘 모션",
     "narration_tone": "경쾌하고 명료한", "rec_length": 30,
     "rec_model": "Figma Weave", "active": True},
]

ASSETS = [
    {"id": 1, "name": "뼈순이 캐릭터", "type": "캐릭터", "image_url": "",
     "description": "다이어트 챌린지 마스코트, 흰색 캐릭터",
     "ref_prompt": "cute white bone character, energetic pose", "active": True},
    {"id": 2, "name": "메인 제품컷", "type": "제품 이미지", "image_url": "",
     "description": "제품 정면 누끼 이미지",
     "ref_prompt": "product front shot, clean background", "active": True},
    {"id": 3, "name": "브랜드 로고", "type": "브랜드 로고", "image_url": "",
     "description": "1:1 정사각 로고",
     "ref_prompt": "brand logo, transparent bg", "active": True},
    {"id": 4, "name": "스튜디오 배경", "type": "배경 이미지", "image_url": "",
     "description": "밝은 스튜디오 배경",
     "ref_prompt": "bright studio backdrop", "active": True},
    {"id": 5, "name": "경쟁사 참고영상", "type": "참고 영상", "image_url": "",
     "description": "톤 참고용 레퍼런스",
     "ref_prompt": "reference footage", "active": False},
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
    return {
        "total": len(JOBS),
        "completed": sum(1 for j in JOBS if j["status"] == "완료"),
        "generating": sum(1 for j in JOBS if j["status"] in ("생성 중", "합본 생성 중", "구간 생성 완료")),
        "failed": sum(1 for j in JOBS if j["status"] == "실패"),
        "templates": len(TEMPLATES),
        "assets": len(ASSETS),
        "recent_jobs": JOBS[:5],
    }
