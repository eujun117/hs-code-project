import streamlit as st

# 식단 데이터
meals = [
    {"name": "한식 A", "items": ["불고기", "밥", "김치"], "calories": 700, "ingredients": ["소고기", "쌀", "배추"]},
    {"name": "양식 B", "items": ["스파게티", "샐러드"], "calories": 650, "ingredients": ["밀가루", "계란", "토마토"]},
    {"name": "채식 C", "items": ["샐러드", "두부스테이크"], "calories": 500, "ingredients": ["두부", "양상추", "오이"]},
    {"name": "간편식 D", "items": ["김밥", "계란찜"], "calories": 600, "ingredients": ["쌀", "계란", "당근"]},
    {"name": "한식 E", "items": ["된장찌개", "밥", "나물"], "calories": 550, "ingredients": ["된장", "두부", "시금치", "쌀"]},
    {"name": "양식 F", "items": ["치킨샐러드", "감자수프"], "calories": 720, "ingredients": ["닭고기", "감자", "우유"]},
    {"name": "분식 G", "items": ["떡볶이", "순대"], "calories": 800, "ingredients": ["쌀떡", "고추장", "돼지내장"]},
    {"name": "일식 H", "items": ["초밥", "미소국"], "calories": 650, "ingredients": ["생선", "쌀", "된장"]},
    {"name": "간편식 I", "items": ["샌드위치", "과일주스"], "calories": 580, "ingredients": ["밀가루", "햄", "사과"]},
    {"name": "한식 J", "items": ["잡곡밥", "닭가슴살", "브로콜리"], "calories": 630, "ingredients": ["현미", "닭고기", "브로콜리"]}
]

# BMR 계산 함수
def calculate_bmr(gender, kg, age):
    if gender == '남':
        return 66 + (13.7 * kg) + (5 * 17) - (6.8 * age)
    elif gender == '여':
        return 65.5 + (9.6 * kg) + (1.8 * 16) - (4.7 * age)
    else:
        return None

# 식단 추천 함수
def recommend_meals(meals, allergies, bmr):
    results = []
    for meal in meals:
        if any(ingredient in allergies for ingredient in meal["ingredients"]):
            continue
        if bmr - 200 <= meal["calories"] <= bmr + 200:
            results.append(meal)
    return results

# Streamlit UI
st.title("🍱 식단 추천 웹앱")
st.write("간단한 정보를 입력하면 알러지를 피하고 칼로리에 맞는 식단을 추천해드려요!")

# 사용자 입력
gender = st.selectbox("성별을 선택하세요", ["남", "여"])
age = st.number_input("나이", min_value=1, max_value=120, value=25, step=1)
weight = st.number_input("몸무게 (kg)", min_value=30.0, max_value=200.0, value=70.0, step=1.0)
allergy_input = st.text_input("알러지 정보를 입력하세요 (예: 우유, 계란, 땅콩)")

# 버튼 누르면 결과 출력
if st.button("식단 추천받기"):
    allergies = [a.strip() for a in allergy_input.split(",") if a.strip()]
    bmr = calculate_bmr(gender, weight, age)

    if bmr is None:
        st.error("성별 입력 오류. 다시 시도해주세요.")
    else:
        st.success(f"🎯 추천 섭취 칼로리: 약 {int(bmr)} kcal")

        recommended = recommend_meals(meals, allergies, bmr)

        if not recommended:
            st.warning("조건에 맞는 식단이 없습니다.")
        else:
            st.subheader("🥗 추천된 식단:")
            for meal in recommended:
                st.markdown(f"### {meal['name']}")
                st.markdown(f"- 음식: {', '.join(meal['items'])}")
                st.markdown(f"- 총 칼로리: {meal['calories']} kcal")
                st.markdown("---")
