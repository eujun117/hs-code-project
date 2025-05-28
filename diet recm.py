import csv
import streamlit as st

# CSV에서 식단 데이터 불러오기
meals = []
with open("meals_50.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        meal = {
            "name": row["name"],
            "items": [item.strip() for item in row["items"].split(",")],
            "calories": int(row["calories"]),
            "ingredients": [ing.strip() for ing in row["ingredients"].split(",")]
        }
        meals.append(meal)

# BMR 계산 함수
def calculate_bmr(gender, kg, height, age):
    if gender == '남':
        return 66 + (1.37 * kg) + (5 * height) - (6.8 * age)
    elif gender == '여':
        return 65.5 + (0.96 * kg) + (1.8 * height) - (4.7 * age)
    else:
        return None

# 식단 추천 함수
def recommend_meals(meals, allergies, bmr):
    results = []
    for meal in meals:
        has_allergy = any(ingredient in allergies for ingredient in meal["ingredients"])
        if not has_allergy and (bmr - 200 <= meal["calories"] <= bmr + 200):
            results.append(meal)
    return results

# Streamlit UI 시작
st.title("식단 추천 웹앱 🍽️")
st.markdown("당신의 건강과 알러지를 고려한 맞춤 식단을 추천해드립니다.")

# 사용자 입력 받기
gender = st.selectbox("성별을 선택하세요", ["남", "여"])
age = st.number_input("나이", min_value=1, max_value=120, value=25)
height = st.number_input("키 (cm)", min_value=100.0, max_value=250.0, value=170.0)
weight = st.number_input("몸무게 (kg)", min_value=30.0, max_value=200.0, value=70.0)
allergy_input = st.text_input("알러지 정보를 입력하세요 (예: 우유,계란,땅콩)", "")

# 입력값 정리
allergies = [a.strip() for a in allergy_input.split(",") if a.strip() != ""]

# 버튼 클릭 시 실행
if st.button("식단 추천받기"):
    bmr = calculate_bmr(gender, weight, height, age)

    if bmr is None:
        st.error("성별 정보가 올바르지 않습니다.")
    else:
        st.success(f"추천 섭취 칼로리는 약 {int(bmr)} kcal입니다.")
        recommended = recommend_meals(meals, allergies, bmr)

        if len(recommended) == 0:
            st.warning("조건에 맞는 식단이 없습니다.")
        else:
            st.subheader("추천된 식단 리스트 🥗")
            for meal in recommended:
                st.markdown(f"### {meal['name']}")
                st.write("음식:", ", ".join(meal["items"]))
                st.write("총 칼로리:", f"{meal['calories']} kcal")
                st.markdown("---")
