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
            {"id": 121, "name": "D-30 시작", "image_url": "",
             "prompt": "3초 안에 시청자의 스크롤을 멈추게 할 강렬한 첫 문장으로 시작한다. "
                       "'오늘부터 D-30, 당신의 30일 후는 어떻게 달라질까요?'라는 질문을 화면 중앙 굵은 "
                       "노란 자막으로 띄우고, 카운트다운 숫자 30을 임팩트 있게 확대 애니메이션한다. "
                       "배경음은 경쾌한 비트, 캐릭터가 손을 흔들며 프레임 안으로 통통 튀어 들어온다."},
            {"id": 122, "name": "변화 예고", "image_url": "",
             "prompt": "'30일 뒤 달라진 나를 미리 만나보세요'라는 카피를 속삭이듯 시작해 점점 볼륨을 높인다. "
                       "화면은 흐릿한 실루엣에서 또렷한 애프터 컷으로 서서히 포커스가 맞춰지며, "
                       "하단에 진행률 바가 0%에서 100%로 차오르는 모션을 넣는다. "
                       "마지막에 캐릭터가 엄지를 치켜세우며 시선을 사로잡는다."},
            {"id": 123, "name": "공감형 오프닝", "image_url": "",
             "prompt": "'다이어트, 작심삼일로 끝난 적 있으신가요?'라는 공감 질문으로 문을 연다. "
                       "실패했던 순간들을 빠른 컷으로 몽타주하며 시청자의 고개를 끄덕이게 만든 뒤, "
                       "'이번엔 다릅니다'라는 반전 자막으로 전환한다. 톤은 친근하되 진지하게."},
        ]},
        {"id": 13, "name": "장면 구성", "type": "prompt", "items": [
            {"id": 131, "name": "비포애프터", "image_url": "",
             "prompt": "일자별 비포/애프터 컷을 좌우 분할 화면으로 전환하며 변화를 극적으로 대비시킨다. "
                       "각 컷 상단에 'DAY 01', 'DAY 15', 'DAY 30' 라벨을 붙이고, 넘어갈 때마다 "
                       "가벼운 스와이프 트랜지션과 셔터음을 넣어 리듬감을 준다."},
            {"id": 132, "name": "일기형", "image_url": "",
             "prompt": "매일의 기록을 손글씨 다이어리 페이지가 넘어가는 형식으로 구성한다. "
                       "캐릭터의 하루 루틴(운동·식단·컨디션)을 짧은 클립으로 보여주고, "
                       "페이지 모서리에 도장처럼 완료 스탬프가 찍히는 만족감 있는 모션을 반복한다."},
            {"id": 133, "name": "챌린지 인증형", "image_url": "",
             "prompt": "실사용자들의 인증샷을 콜라주처럼 빠르게 이어 붙여 신뢰감을 쌓는다. "
                       "화면 곳곳에 '나도 성공', 'D-30 완주' 같은 손글씨 스티커를 흩뿌리고, "
                       "마지막엔 모든 인증샷이 하트 모양으로 모이는 그리드 애니메이션으로 마무리한다."},
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
            {"id": 221, "name": "첫인상", "image_url": "",
             "prompt": "'처음 써보셨을 때 솔직히 어떠셨어요?'라고 편안하게 물으며 인터뷰이의 표정 변화를 "
                       "클로즈업으로 담는다. 답변 중 핵심 문장은 하단 자막으로 강조하고, 제품 클로즈업 "
                       "인서트를 자연스럽게 교차 편집해 진정성을 살린다."},
            {"id": 222, "name": "재구매", "image_url": "",
             "prompt": "'다시 구매하실 의향이 있나요? 그 이유는 무엇인가요?'라는 질문으로 신뢰를 증폭한다. "
                       "인터뷰이가 망설임 없이 '네'라고 답하는 순간을 슬로우 모션으로 잡고, "
                       "실제 재구매 화면(장바구니·주문내역)을 근거 인서트로 붙인다."},
            {"id": 223, "name": "비교 경험", "image_url": "",
             "prompt": "'다른 제품과 비교했을 때 가장 큰 차이는요?'라고 물어 차별점을 인터뷰이의 입으로 "
                       "말하게 한다. 경쟁 상황을 은근히 암시하는 B롤을 깔되 비방은 피하고, "
                       "'이건 확실히 다르더라고요'라는 자연스러운 멘트로 설득력을 높인다."},
        ]},
     ]},
    {"id": 3, "name": "숏폼 바이럴 스타일", "style": "숏폼",
     "narration_tone": "에너지 넘치는", "rec_length": 15, "rec_model": "Seedance", "active": True,
     "categories": [
        {"id": 31, "name": "훅 문구", "type": "prompt", "items": [
            {"id": 311, "name": "3초 훅", "image_url": "",
             "prompt": "영상 시작 3초 안에 시선을 붙잡는 강한 첫 문장을 화면 정중앙 초대형 자막으로 띄운다. "
                       "'이거 모르면 진짜 손해예요'를 빠른 줌인과 함께 던지고, 곧바로 제품의 핵심 장면으로 "
                       "컷 전환해 궁금증이 식기 전에 몰입시킨다."},
            {"id": 312, "name": "궁금증 유발", "image_url": "",
             "prompt": "'왜 다들 이걸 사재기하는지 아세요?'라는 질문으로 호기심을 자극한다. "
                       "답을 바로 주지 않고 관련 없어 보이는 장면들을 빠르게 나열하다가, "
                       "마지막에 제품을 공개하며 '바로 이것 때문입니다' 반전으로 마무리한다."},
            {"id": 313, "name": "숫자 임팩트", "image_url": "",
             "prompt": "'재고 300개, 3시간 만에 완판'처럼 구체적인 숫자를 화면 가득 카운터 애니메이션으로 "
                       "보여준다. 숫자가 빠르게 올라가는 효과음과 함께 긴박감을 조성하고, "
                       "'지금이 마지막 기회'라는 자막으로 행동을 촉구한다."},
        ]},
        {"id": 32, "name": "BGM 무드", "type": "prompt", "items": [
            {"id": 321, "name": "트렌디", "image_url": "",
             "prompt": "요즘 숏폼에서 유행하는 업템포 비트를 깔되 저작권 안전한 트랙으로 선택한다. "
                       "비트 드롭 지점에 맞춰 제품 클로즈업 컷을 배치해 리듬과 편집을 싱크시키고, "
                       "후렴 구간에서 자막이 튀어오르는 키네틱 타이포로 흥을 끌어올린다."},
            {"id": 322, "name": "긴장감", "image_url": "",
             "prompt": "낮은 베이스가 서서히 고조되는 텐션 빌드업 트랙으로 기대감을 쌓는다. "
                       "제품 공개 직전 0.5초 무음을 넣어 시선을 집중시키고, 공개 순간 강한 임팩트음과 "
                       "함께 화면을 플래시로 전환해 카타르시스를 준다."},
        ]},
     ]},
    {"id": 4, "name": "후기형 광고 스타일", "style": "리뷰",
     "narration_tone": "친근한 수다체", "rec_length": 30, "rec_model": "Veo", "active": True,
     "categories": [
        {"id": 41, "name": "후기 문구", "type": "prompt", "items": [
            {"id": 411, "name": "별점 5점", "image_url": "",
             "prompt": "'★★★★★ 인생템 찾았어요'라는 리뷰를 실제 쇼핑몰 후기 화면처럼 재현해 신뢰를 준다. "
                       "별 다섯 개가 하나씩 채워지는 애니메이션과 함께 후기 텍스트를 타이핑 효과로 띄우고, "
                       "작성자 닉네임과 구매 인증 배지를 붙여 진짜 후기 같은 디테일을 살린다."},
            {"id": 412, "name": "재구매 후기", "image_url": "",
             "prompt": "'벌써 세 번째 재구매예요'라는 멘트로 반복 구매의 만족을 강조한다. "
                       "주문 내역 세 건을 스크롤하며 보여주고, '이젠 없으면 불안할 정도'라는 솔직한 코멘트로 "
                       "제품 의존도를 유쾌하게 표현한다."},
            {"id": 413, "name": "선물 후기", "image_url": "",
             "prompt": "'친구 선물했다가 저까지 재구매했어요'라는 확산형 후기로 입소문 효과를 노린다. "
                       "선물 포장을 여는 장면과 받은 사람의 놀란 반응을 담고, '주변에 다 추천했다'는 "
                       "멘트로 자연스러운 바이럴을 유도한다."},
        ]},
     ]},
    {"id": 5, "name": "Before & After 스타일", "style": "비교",
     "narration_tone": "설득력 있는", "rec_length": 15, "rec_model": "Higgsfield", "active": True,
     "categories": [
        {"id": 51, "name": "비교 대상", "type": "asset", "items": [
            {"id": 511, "name": "제품컷", "prompt": "product front shot, clean bg", "image_url": ""},
        ]},
        {"id": 52, "name": "대비 연출", "type": "prompt", "items": [
            {"id": 521, "name": "분할 비교", "image_url": "",
             "prompt": "화면을 좌(BEFORE)/우(AFTER)로 정확히 반 나눠 동일한 각도·조명에서 촬영한 "
                       "두 상태를 동시에 보여준다. 가운데 분할선을 좌우로 슬라이드시키며 변화 정도를 "
                       "인터랙티브하게 드러내고, 'BEFORE'/'AFTER' 라벨을 큼직하게 고정한다."},
            {"id": 522, "name": "타임랩스", "image_url": "",
             "prompt": "사용 전부터 후까지의 과정을 빠른 타임랩스로 압축해 극적인 변화를 한 컷에 담는다. "
                       "경과 시간을 화면 모서리 타이머로 표시하고, 변화가 두드러지는 구간에서 잠시 "
                       "속도를 늦춰 시청자가 차이를 확실히 인지하게 한다."},
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
        {"id": 72, "name": "모션 컨셉", "type": "prompt", "items": [
            {"id": 721, "name": "키네틱 타이포", "image_url": "",
             "prompt": "핵심 메시지를 글자 하나하나가 튀고 늘어나고 회전하는 키네틱 타이포그래피로 "
                       "표현한다. 색상은 브랜드 팔레트로 통일하고, 리듬감 있는 등장/퇴장 모션으로 "
                       "정보 전달과 시각적 즐거움을 동시에 잡는다."},
            {"id": 722, "name": "아이콘 설명형", "image_url": "",
             "prompt": "제품의 기능을 단순한 아이콘 애니메이션으로 하나씩 시각화해 이해를 돕는다. "
                       "각 기능이 등장할 때 짧은 효과음과 말풍선 설명을 붙이고, 마지막에 아이콘들이 "
                       "제품 로고로 모여드는 통합 모션으로 마무리한다."},
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
