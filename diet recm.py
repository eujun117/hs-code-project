import streamlit as st

# 더미 식단 데이터 (태그 포함)
meals = [
    {"name": "한식 A", "items": ["불고기", "밥", "김치"], "calories": 700,
     "ingredients": ["소고기", "쌀", "배추"], "tags": ["고단백", "고탄수화물"]},
    {"name": "양식 B", "items": ["스파게티", "샐러드"], "calories": 650,
     "ingredients": ["밀가루", "계란", "토마토"], "tags": ["중단백", "고탄수화물"]},
    {"name": "채식 C", "items": ["샐러드", "두부스테이크"], "calories": 500,
     "ingredients": ["두부", "양상추", "오이"], "tags": ["고단백", "저탄수화물"]},
    {"name": "간편식 D", "items": ["김밥", "계란찜"], "calories": 600,
     "ingredients": ["쌀", "계란", "당근"], "tags": ["중단백", "중탄수화물"]},
    {"name": "한식 E", "items": ["된장찌개", "밥", "나물"], "calories": 550,
     "ingredients": ["된장", "두부", "시금치", "쌀"], "tags": ["저단백", "고탄수화물"]},
    {"name": "헬스 F", "items": ["닭가슴살", "현미", "브로콜리"], "calories": 630,
     "ingredients": ["닭고기", "현미", "브로콜리"], "tags": ["고단백", "저탄수화물"]},
    {"name": "다이어트 G", "items": ["샐러드", "계란"], "calories": 450,
     "ingredients": ["양상추", "계란", "당근"], "tags": ["고단백", "저탄수화물"]},
    {"name": "양식 H", "items": ["치킨스테이크", "감자샐러드"], "calories": 680,
     "ingredients": ["닭고기", "감자", "양상추"], "tags": ["고단백", "중탄수화물"]},
    {"name": "분식 I", "items": ["떡볶이", "오뎅"], "calories": 800,
     "ingredients": ["쌀떡", "고추장", "어묵"], "tags": ["저단백", "고탄수화물"]},
    {"name": "일식 J", "items": ["초밥", "미소국"], "calories": 620,
     "ingredients": ["생선", "쌀", "된장"], "tags": ["중단백", "중탄수화물"]},
    {"name": "채식 K", "items": ["현미밥", "콩조림"], "calories": 530,
     "ingredients": ["현미", "강낭콩", "간장"], "tags": ["고단백", "저탄수화물"]},
    {"name": "브런치 L", "items": ["오트밀", "아보카도"], "calories": 510,
     "ingredients": ["귀리", "아보카도", "우유"], "tags": ["중단백", "저탄수화물"]},
    {"name": "건강식 M", "items": ["닭가슴살", "고구마"], "calories": 560,
     "ingredients": ["닭고기", "고구마", "브로콜리"], "tags": ["고단백", "중탄수화물"]},
    {"name": "다이어트 N", "items": ["샐러드", "두부"], "calories": 480,
     "ingredients": ["양상추", "두부", "당근"], "tags": ["고단백", "저탄수화물"]},
    {"name": "양식 O", "items": ["파스타", "크림수프"], "calories": 750,
     "ingredients": ["밀가루", "크림", "양파"], "tags": ["저단백", "고탄수화물"]},
    {"name": "분식 P", "items": ["라면", "김치"], "calories": 720,
     "ingredients": ["밀가루", "계란", "배추"], "tags": ["저단백", "고탄수화물"]},
    {"name": "한식 Q", "items": ["잡곡밥", "닭갈비"], "calories": 680,
     "ingredients": ["현미", "닭고기", "양파"], "tags": ["고단백", "중탄수화물"]},
    {"name": "건강식 R", "items": ["연어스테이크", "샐러드"], "calories": 640,
     "ingredients": ["연어", "양상추", "토마토"], "tags": ["고단백", "저탄수화물"]},
    {"name": "일식 S", "items": ["우동", "야채튀김"], "calories": 700,
     "ingredients": ["밀가루", "야채", "간장"], "tags": ["저단백", "고탄수화물"]},
    {"name": "브런치 T", "items": ["계란오믈렛", "통밀빵"], "calories": 610,
     "ingredients": ["계란", "통밀", "치즈"], "tags": ["중단백", "중탄수화물"]}
]

# BMR 계산 함수
def calculate_bmr(gender, kg, height, age):
    if gender == '남':
        return 66 + (1.37 * kg) + (5 * height) - (6.8 * age)
    elif gender == '여':
        return 65.5 + (0.96 * kg) + (1.8 * height) - (4.7 * age)
    else:
        return None
# 추천 함수
def recommend_meals(meals, allergies, bmr, selected_tags):
    results = []
    for meal in meals:
        if any(ing in allergies for ing in meal["ingredients"]):
            continue
        if not (bmr - 200 <= meal["calories"] <= bmr + 200):
            continue
        if selected_tags and not any(tag in meal["tags"] for tag in selected_tags):
            continue
        results.append(meal)
    return results

# --- Streamlit UI ---
st.title("태그 기반 식단 추천 앱")

gender = st.selectbox("성별", ["남", "여"])
age = st.number_input("나이", 1, 120, step=1)
weight = st.number_input("몸무게 (kg)", 30.0, 200.0, step=1.0)
allergy_input = st.text_input("알러지 정보를 입력하세요 (예: 우유,계란,땅콩)")

# 식단 태그 선택
all_tags = sorted({tag for meal in meals for tag in meal["tags"]})
selected_tags = st.multiselect("원하는 식단 특징을 선택하세요", all_tags)

if st.button("추천 식단 보기"):
    allergies = [a.strip() for a in allergy_input.split(",") if a.strip()]
    bmr = calculate_bmr(gender, weight, age)

    if bmr is None:
        st.error("BMR 계산 오류 발생")
    else:
        st.success(f"BMR 기준 섭취 칼로리: 약 {int(bmr)} kcal")
        recommended = recommend_meals(meals, allergies, bmr, selected_tags)

        if not recommended:
            st.warning("조건에 맞는 식단이 없습니다.")
        else:
            st.subheader("추천 식단")
            for meal in recommended:
                st.markdown(f"### {meal['name']}")
                st.markdown(f"- 음식: {', '.join(meal['items'])}")
                st.markdown(f"- 칼로리: {meal['calories']} kcal")
                st.markdown(f"- 태그: {', '.join(meal['tags'])}")
                st.markdown("---")
