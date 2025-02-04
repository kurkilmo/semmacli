import requests
import json
import time

def request_menu(cost_number: int, lang="fi") -> dict:
    url = f"https://www.semma.fi/menuapi/feed/json?costNumber={cost_number}&language={lang}"
    response = requests.get(url)
    return json.loads(response.text)

if __name__ == "__main__":
    restaurants = {
        "Piato": 1408,
        "Maija": 1402,
        "Ilokivi": 1419,
        "Syke": 1405,
        "Tilia": 1413,
        "Belvedere": 1404,
        "Lozzi": 1401,
        "Uno": 1414,
        "Kvarkki": 140301,
        "Ylisto": 1403,
        "Rentukka": 1416,
        "Norssi": 1411,
        "Novelli": 1409
    }

    piato_data = request_menu(restaurants["Piato"])
    #for day in piato_data["MenusForDays"]:
    #    for key in day.keys():
    #        print(f"{key} {day[key]}")
    #        print("\n")
    for day in piato_data["MenusForDays"]:
        print(day["Date"].split("T")[0] + "\n")
        for item in day["SetMenus"]:
            if not item["Name"]: continue
            print("    " + item["Name"])
            print("    " + item["Price"])
            for component in item["Components"]:
                print("      " + component)
            print("\n")
        print("-------------------\n")

    
