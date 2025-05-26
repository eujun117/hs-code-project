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

def calculate_bmr(gender, kg, age):
    if gender == '남':
        return 66 + (13.7 * kg) + (5 * 17) - (6.8 * age)
    elif gender == '여':
        return 65.5 + (9.6 * kg) + (1.8 * 16) - (4.7 * age)
    else:
        return None

def recommend_meals(meals, allergies, bmr):
    results = [] #식단 결과 리스트
    for meal in meals:
        has_allergy = False#알러지 확인을 위한 변수
        for ingredient in meal["ingredients"]:
            if ingredient in allergies:
                has_allergy = True
                break
        if not has_allergy:
            # 칼로리가 목표보다 오차범위 200 안에 있으면 추천
            if bmr - 200 <= meal["calories"] <= bmr + 200:
                results.append(meal)
    return results

gender = input("성별을 입력하세요 (남/여): ")
age = int(input("나이를 입력하세요: "))
weight = float(input("몸무게를 입력하세요 (kg): "))
allergy_input = input("알러지 정보를 입력하세요 (예: 우유,계란,땅콩) : ")

allergies = [a.strip() for a in allergy_input.split(",")]

bmr = calculate_bmr(gender, weight, age)

if bmr is None:
    print("성별 입력이 잘못되었습니다. 프로그램을 종료합니다.")
else:
    print(f"당신의 추천 섭취 칼로리는 약 {int(bmr)} kcal입니다.")

recommended = recommend_meals(meals, allergies, bmr)

if len(recommended) == 0:
    print("죄송합니다. 조건에 맞는 식단이 없습니다.")
else:
    print("추천된 식단:")
    for meal in recommended:
        print(f"\n[{meal['name']}]")
        print("음식:", ", ".join(meal["items"]))
        print(f"총 칼로리: {meal['calories']} kcal")
