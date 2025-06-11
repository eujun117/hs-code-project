import csv
import streamlit as st

# CSV 파일 불러오기
meals = []
with open("meals_50_nutrition.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        meal = {
            "name": row["name"],
            "items": [item.strip() for item in row["items"].split(",")],
            "calories": int(row["calories"]),
            "ingredients": [ing.strip() for ing in row["ingredients"].split(",")],
            "carbs": int(row["carbs"]),
            "protein": int(row["protein"]),
            "fat": int(row["fat"]),
            "tags": [tag.strip() for tag in row["tags"].split(",")]
        }
        meals.append(meal)

# BMR 계산
def calculate_bmr(gender, kg, height, age):
    if gender == '남':
        return 66 + (1.37 * kg) + (5 * height) - (6.8 * age)
    elif gender == '여':
        return 65.5 + (0.96 * kg) + (1.8 * height) - (4.7 * age)
    else:
        return None

# 식단 추천
def recommend_meals(meals, allergies, bmr, carb_range, protein_range, fat_range, selected_tags):
    results = []
    for meal in meals:
        if any(ingredient in allergies for ingredient in meal["ingredients"]):
            continue
        if not (bmr - 200 <= meal["calories"] <= bmr + 200):
            continue
        if not (carb_range[0] <= meal["carbs"] <= carb_range[1]):
            continue
        if not (protein_range[0] <= meal["protein"] <= protein_range[1]):
            continue
        if not (fat_range[0] <= meal["fat"] <= fat_range[1]):
            continue
        if selected_tags and not any(tag in meal["tags"] for tag in selected_tags):
            continue
        results.append(meal)
    return results

# Streamlit UI
st.title("식단 추천 웹앱")
st.write("영양소 범위와 알러지 정보 기반으로 개인 맞춤 식단을 추천해드립니다.")

# 사용자 입력
gender = st.selectbox("성별", ["남", "여"])

# int형: 나이 (전부 int로 통일)
age = st.number_input("나이", min_value=1, max_value=120, value=25, step=1)

# float형: 키, 몸무게 (전부 float로 통일)
height = st.number_input("키 (cm)", min_value=100.0, max_value=250.0, value=170.0, step=1.0)
weight = st.number_input("몸무게 (kg)", min_value=30.0, max_value=200.0, value=70.0, step=1.0)

# 알러지 입력 (문자열)
allergy_input = st.text_input("알러지 정보를 입력하세요 (예: 우유,계란,땅콩)")

# 영양소 필터 범위 설정
st.subheader("영양소 필터 설정 (선택사항)")
carb_range = st.slider("탄수화물 (g)", 0, 200, (0, 200))
protein_range = st.slider("단백질 (g)", 0, 100, (0, 100))
fat_range = st.slider("지방 (g)", 0, 100, (0, 100))
all_tags = sorted(set(tag for meal in meals for tag in meal["tags"]))
selected_tags = st.multiselect("식단 태그 선택", all_tags)

if st.button("식단 추천받기"):
    allergies = [a.strip() for a in allergy_input.split(",") if a.strip()]
    bmr = calculate_bmr(gender, weight, height, age)

    if bmr is None:
        st.error("BMR 계산 중 오류가 발생했습니다.")
    else:
        st.success(f"계산된 추천 섭취 칼로리: 약 {int(bmr)} kcal")
        recommended = recommend_meals(
            meals, allergies, bmr,
            carb_range, protein_range, fat_range,
            selected_tags
        )
        if not recommended:
            st.warning("조건에 맞는 식단이 없습니다.")
        else:
            st.subheader("추천 식단 목록")
            for meal in recommended:
                st.markdown(f"### {meal['name']}")
                st.markdown(f"- 음식: {', '.join(meal['items'])}")
                st.markdown(f"- 칼로리: {meal['calories']} kcal")
                st.markdown(f"- 탄수화물: {meal['carbs']}g, 단백질: {meal['protein']}g, 지방: {meal['fat']}g")
                st.markdown(f"- 태그: {', '.join(meal['tags'])}")
                st.markdown("---")
