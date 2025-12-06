from datetime import date
import math
import random
import hashlib

def hash_password(password: str) -> str:
    hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed

def generate_meal_id(meal_foods,meal_type):
    meal_id = meal_type
    meal_foods = dict(sorted(meal_foods.items()))
    for food , quantity in meal_foods.items():
        meal_id += str(quantity)
        meal_id += food
    print(meal_id)
    return meal_id
def generate_recommend_id(user_id,rdate):
    date_str = rdate.strftime("%d")
    return f"{user_id}{date_str}"
def generate_meal_level(gender, age, weight_lbs, height_feet, height_inches=0):
    if weight_lbs <= 0 or age <= 0 or height_feet < 0 or height_inches < 0:
        raise ValueError("Age, weight, and height must be positive numbers")
    
    weight_kg = weight_lbs * 0.453592
    height_cm = height_feet * 30.48 + height_inches * 2.54

    gender = gender.lower()
    if gender == 'male':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    elif gender == 'female':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    else:
        raise ValueError("Gender must be 'male' or 'female'")

    if bmr < 1800:
        return "small"
    elif bmr <= 2500:
        return "medium"
    else:
        return "large"

def get_meal_nutrition(meal_type, size):
    nutrition_estimate_data = {
        "Breakfast": {
            "Small":  {"Calcium":0.2,  "Carbohydrates":30, "Fat":8,  "Fiber":3, "Iron":0.003, "Protein":12, "Sugar":8,  "Vitamin A":0.0003, "Vitamin C":0.02},
            "Medium": {"Calcium":0.4,  "Carbohydrates":45, "Fat":12, "Fiber":4, "Iron":0.005, "Protein":18, "Sugar":12, "Vitamin A":0.0005, "Vitamin C":0.04},
            "Large":  {"Calcium":0.6,  "Carbohydrates":60, "Fat":16, "Fiber":5, "Iron":0.007, "Protein":24, "Sugar":16, "Vitamin A":0.0007, "Vitamin C":0.06}
        },
        "Lunch": {
            "Small":  {"Calcium":0.25, "Carbohydrates":50, "Fat":10, "Fiber":4, "Iron":0.004, "Protein":15, "Sugar":6,  "Vitamin A":0.0004, "Vitamin C":0.03},
            "Medium": {"Calcium":0.5,  "Carbohydrates":70, "Fat":15, "Fiber":6, "Iron":0.006, "Protein":22, "Sugar":9,  "Vitamin A":0.0006, "Vitamin C":0.05},
            "Large":  {"Calcium":0.75, "Carbohydrates":90, "Fat":20, "Fiber":8, "Iron":0.008, "Protein":30, "Sugar":12, "Vitamin A":0.0008, "Vitamin C":0.07}
        },
        "Dinner": {
            "Small":  {"Calcium":0.2,  "Carbohydrates":40, "Fat":9,  "Fiber":3, "Iron":0.0035,"Protein":14, "Sugar":5,  "Vitamin A":0.00035,"Vitamin C":0.02},
            "Medium": {"Calcium":0.45, "Carbohydrates":65, "Fat":14, "Fiber":5, "Iron":0.0055,"Protein":22, "Sugar":8,  "Vitamin A":0.00055,"Vitamin C":0.04},
            "Large":  {"Calcium":0.7,  "Carbohydrates":85, "Fat":18, "Fiber":6, "Iron":0.0075,"Protein":30, "Sugar":10, "Vitamin A":0.00075,"Vitamin C":0.06}
        }
    }
    meal_type = meal_type.title()
    size = size.title()
    return nutrition_estimate_data[meal_type][size]

def score_food(food, current, targets):
    score = 0
    REWARD_FACTOR = 2.0
    #sum up nutrient score
    if food['Avoid']:
        return score
    for nutrient, target_val in targets.items():
        current_val = current.get(nutrient, 0)
        food_val = food.get(nutrient, 0)

        delta = target_val - current_val
        if delta > 0:
            if food_val> delta:
                score -= (food_val -delta)/ target_val
                score += (delta ) / target_val *REWARD_FACTOR
            else:
                score += food_val / target_val*REWARD_FACTOR
        else:
            score -= food_val / target_val
            

    today = date.today()
    for rdate in food.get('rdates'):
        delta = (today - rdate).days
        score -= math.exp(-delta)
    return score
def fill_meal(foods, targets):
    meal = {}
    totals = {n: 0 for n in targets}
    
    while True:

        scores = {}
        for food in foods:
            scores[food['f_name']] = score_food(food, totals, targets)
    

        positive_scores = {f: s for f, s in scores.items() if s > 0}
        if not positive_scores:
            break
        total_score = sum(positive_scores.values())
        probabilities = [s / total_score for s in positive_scores.values()]
        chosen_food_name = random.choices(list(positive_scores.keys()), weights=probabilities, k=1)[0]
        meal[chosen_food_name] = meal.get(chosen_food_name, 0) + 1
        food = next(f for f in foods if f['f_name'] == chosen_food_name)
        for nutrient in totals:
            totals[nutrient] += food.get(nutrient, 0) 
    #print(totals,targets)
    return meal