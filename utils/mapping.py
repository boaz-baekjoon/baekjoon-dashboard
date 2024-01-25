# 등급을 숫자로 변환하는 함수
def tier_to_num(tier):
    division = 1
    for char in tier[::-1]:
        if char.isdigit():
            division = int(char)
            break
    
    if tier.startswith("Bronze"):
        return 6.0 - division
    elif tier.startswith("Silver"):
        return 11.0 - division
    elif tier.startswith("Gold"):
        return 16.0 - division
    elif tier.startswith("Platinum"):
        return 21.0 - division
    elif tier.startswith("Diamond"):
        return 26.0 - division
    elif tier.startswith("Ruby"):
        return 31.0 - division
    elif tier == "Master":
        return 31.0
    else:
        return 1.0


# 등급 범위에 따라 텍스트로 변환하는 함수 정의
def tier_avg_to_text(avg_tier):
    if avg_tier < 2.0:
        return "Bronze 5"
    elif 2.0 <= avg_tier < 3.0:
        return "Bronze 4"
    elif 3.0 <= avg_tier < 4.0:
        return "Bronze 3"
    elif 4.0 <= avg_tier < 5.0:
        return "Bronze 2"
    elif 5.0 <= avg_tier < 6.0:
        return "Bronze 1"
    elif 6.0 <= avg_tier < 7.0:
        return "Silver 5"
    elif 7.0 <= avg_tier < 8.0:
        return "Silver 4"
    elif 8.0 <= avg_tier < 9.0:
        return "Silver 3"
    elif 9.0 <= avg_tier < 10.0:
        return "Silver 2"
    elif 10.0 <= avg_tier < 11.0:
        return "Silver 1"
    elif 11.0 <= avg_tier < 12.0:
        return "Gold 5"
    elif 12.0 <= avg_tier < 13.0:
        return "Gold 4"
    elif 13.0 <= avg_tier < 14.0:
        return "Gold 3"
    elif 14.0 <= avg_tier < 15.0:
        return "Gold 2"
    elif 15.0 <= avg_tier < 16.0:
        return "Gold 1"
    elif 16.0 <= avg_tier < 17.0:
        return "Platinum 5"
    elif 17.0 <= avg_tier < 18.0:
        return "Platinum 4"
    elif 18.0 <= avg_tier < 19.0:
        return "Platinum 3"
    elif 19.0 <= avg_tier < 20.0:
        return "Platinum 2"
    elif 20.0 <= avg_tier < 21.0:
        return "Platinum 1"
    elif 21.0 <= avg_tier < 22.0:
        return "Diamond 5"
    elif 22.0 <= avg_tier < 23.0:
        return "Diamond 4"
    elif 23.0 <= avg_tier < 24.0:
        return "Diamond 3"
    elif 24.0 <= avg_tier < 25.0:
        return "Diamond 2"
    elif 25.0 <= avg_tier < 26.0:
        return "Diamond 1"
    elif 26.0 <= avg_tier < 27.0:
        return "Ruby 5"
    elif 27.0 <= avg_tier < 28.0:
        return "Ruby 4"
    elif 28.0 <= avg_tier < 29.0:
        return "Ruby 3"
    elif 29.0 <= avg_tier < 30.0:
        return "Ruby 2"
    elif 30.0 <= avg_tier < 31.0:
        return "Ruby 1"
    elif avg_tier >= 31.0:
        return "Master"
    else:
        return 1.0

# 등급 범위에 따라 텍스트로 변환하는 함수 정의
def tier_avg_to_text(avg_tier):
    if avg_tier < 2.0:
        return "Bronze 5"
    elif 2.0 <= avg_tier < 3.0:
        return "Bronze 4"
    elif 3.0 <= avg_tier < 4.0:
        return "Bronze 3"
    elif 4.0 <= avg_tier < 5.0:
        return "Bronze 2"
    elif 5.0 <= avg_tier < 6.0:
        return "Bronze 1"
    elif 6.0 <= avg_tier < 7.0:
        return "Silver 5"
    elif 7.0 <= avg_tier < 8.0:
        return "Silver 4"
    elif 8.0 <= avg_tier < 9.0:
        return "Silver 3"
    elif 9.0 <= avg_tier < 10.0:
        return "Silver 2"
    elif 10.0 <= avg_tier < 11.0:
        return "Silver 1"
    elif 11.0 <= avg_tier < 12.0:
        return "Gold 5"
    elif 12.0 <= avg_tier < 13.0:
        return "Gold 4"
    elif 13.0 <= avg_tier < 14.0:
        return "Gold 3"
    elif 14.0 <= avg_tier < 15.0:
        return "Gold 2"
    elif 15.0 <= avg_tier < 16.0:
        return "Gold 1"
    elif 16.0 <= avg_tier < 17.0:
        return "Platinum 5"
    elif 17.0 <= avg_tier < 18.0:
        return "Platinum 4"
    elif 18.0 <= avg_tier < 19.0:
        return "Platinum 3"
    elif 19.0 <= avg_tier < 20.0:
        return "Platinum 2"
    elif 20.0 <= avg_tier < 21.0:
        return "Platinum 1"
    elif 21.0 <= avg_tier < 22.0:
        return "Diamond 5"
    elif 22.0 <= avg_tier < 23.0:
        return "Diamond 4"
    elif 23.0 <= avg_tier < 24.0:
        return "Diamond 3"
    elif 24.0 <= avg_tier < 25.0:
        return "Diamond 2"
    elif 25.0 <= avg_tier < 26.0:
        return "Diamond 1"
    elif 26.0 <= avg_tier < 27.0:
        return "Ruby 5"
    elif 27.0 <= avg_tier < 28.0:
        return "Ruby 4"
    elif 28.0 <= avg_tier < 29.0:
        return "Ruby 3"
    elif 29.0 <= avg_tier < 30.0:
        return "Ruby 2"
    elif 30.0 <= avg_tier < 31.0:
        return "Ruby 1"
    elif avg_tier >= 31.0:
        return "Master"
    else:
        return 1.0
    
def tier_num_to_text(tier_num):
    tier_mapping = {
        1: "Bronze 5", 2: "Bronze 4", 3: "Bronze 3", 4: "Bronze 2", 5: "Bronze 1",
        6: "Silver 5", 7: "Silver 4", 8: "Silver 3", 9: "Silver 2", 10: "Silver 1",
        11: "Gold 5", 12: "Gold 4", 13: "Gold 3", 14: "Gold 2", 15: "Gold 1",
        16: "Platinum 5", 17: "Platinum 4", 18: "Platinum 3", 19: "Platinum 2", 20: "Platinum 1",
        21: "Diamond 5", 22: "Diamond 4", 23: "Diamond 3", 24: "Diamond 2", 25: "Diamond 1",
        26: "Ruby 5", 27: "Ruby 4", 28: "Ruby 3", 29: "Ruby 2", 30: "Ruby 1",
        31: "Master"
    }
    return tier_mapping.get(tier_num, "Unknown Tier")