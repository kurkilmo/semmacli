import requests
import json
import sys
import os
import getopt
import time
import locale
from termcolor import colored, cprint

restaurant_info = {
    "piato":        ("semma", "1408"),
    "bistro":       ("compass-group", 3081),
    "syke":         ("semma", "1405"),
    "tilia":        ("semma", "1413"),
    "belvedere":    ("semma", "1404"),
    "lozzi":        ("semma", "1401"),
    "uno":          ("semma", "1414"),
    "kvarkki":      ("semma", "140301"),
    "ylistö":       ("semma", "1403"),
    "rentukka":     ("semma", "1416"),
    "norssi":       ("semma", "1411"),
    "taide":        ("compass-group", "0301")
}

def request_menu(restaurant_name, lang="fi") -> dict:
    info = restaurant_info[restaurant_name]
    url = f"https://www.{info[0]}.fi/menuapi/feed/json?costNumber={info[1]}&language={lang}"
    response = requests.get(url)
    return json.loads(response.text)

def format_date(original_date: str):
    time_struct = time.strptime(original_date.split("T")[0], "%Y-%m-%d")
    return time.strftime("%A %d.%m.%Y", time_struct).capitalize()


def print_restaurants(restaurants: list, week=False):
    rest_datas = list(map(lambda r: request_menu(r), restaurants))
    
    if week:
        days_amount = max(map(lambda rest: len(rest["MenusForDays"]), rest_datas))
    else:
        days_amount = 1

    for day in range(days_amount):
        cprint(format_date(rest_datas[0]["MenusForDays"][day]["Date"]), "light_yellow")

        for index, restaurant in enumerate(rest_datas):
            restaurant_name = restaurants[index].capitalize()
            menu = dict()
            try:
                menu = restaurant["MenusForDays"][day]
            except IndexError:
                pass

            if menu and len(menu["SetMenus"]) != 0:
                name_text = colored(restaurant_name, "light_green")
                open_times = menu["LunchTime"]
                if open_times:
                    open_text = ": avoinna " + open_times
                else:
                    open_text = ""
                print(f"{name_text}{open_text}")

                for item in menu["SetMenus"]:
                    if not item["Name"] and not item["Price"]: continue
                    price = item["Price"] or ""
                    name = item["Name"] or ""
                    print(f"  {colored(name, "light_cyan")} {price}")
                    for component in item["Components"]:
                        split = component.replace("\n", " ").split(" (")
                        title = split[0]
                        allergens = "(" + split[1]
                        print(f"      {title} {colored(allergens, "dark_grey")}")
                    print()
            else:
                print(f"{colored(restaurant_name, "light_green")}: {colored("suljettu", "red")}\n")


config_file = f"{os.environ["HOME"]}/.config/semmacli.json"
def set_default(default):
    json_str = json.dumps({ "default_restaurant": default })
    try:
        with open(config_file, "w") as file:
            file.write(json_str)
            return True
    except FileNotFoundError:
        return False

def get_default():
    try:
        data = json.loads(open(config_file, "r").read())
        return data["default_restaurant"]
    except:
        return ""

def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def main():
    locale.setlocale(locale.LC_TIME, "fi_FI")
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "wlda", ["set-default=", "week", "list", "all"])
    except getopt.GetoptError as er:
        print(f"Tuntematon argumentti {colored(er.opt, "light_red")}")
        exit(2)

    show_week = False
    omit_default = False
    for option, value in opts:
        match option:
            case "-w" | "--week":
                show_week = True
            case "--set-default":
                if set_default(value):
                    print(f"{value} asetettiin oletusravintolaksi")
                else:
                    print("Oletusravintolan asettaminen epäonnistui")
            case "-l" | "--list":
                print("Saatavilla olevat ravintolat:")
                for restaurant in restaurant_info.keys():
                    print(f"  { restaurant.capitalize() }")
                omit_default = True
            case "-d":
                default = get_default()
                if default:
                    args = [get_default()] + args
            case "-a" | "all":
                args = list(restaurant_info.keys())

    deleted = False
    for arg in args.copy():
        if arg not in restaurant_info.keys():
            print(f"Ravintolaa {arg} ei löydy")
            deleted = True
            args.remove(arg)

    if len(args) == 0 and not omit_default:
        default = get_default()
        if not default:
            if not deleted:
                print("Ravintolaa ei annettu eikä oletusravintolaa asetettu.")
                print(f"Voit asettaa oletusravintolan komennolla {colored("semmacli --set-default <ravintola>", "light_yellow")}")
            exit(1)
        args = [default]

    if len(args) == 0: exit(0)
    print_restaurants(remove_duplicates(args), show_week)


if __name__ == "__main__":
    main()