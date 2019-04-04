# -*- coding: utf-8 -*-
import json
import sys
import os
import dbs
import weapon_name
if sys.version_info[0] < 3:
    import codecs

def export_weapon_name():
    w = openfile("test.txt", "r")
    weapon = json.loads(w.read()[1:])
    db = {}
    da = {}

    for i in weapon:
        db[i["key"]] = i["name"]["ja_JP"]

    for k, v in dbs.weapons.items():
        try:
            da[k] = db[v]
        except KeyError:
            pass

    print(da)

    nu = openfile("weapon_name.txt", "w")
    nu.write(str(da))
    nu.close()

def player_record(m):
    w = weapon_name.weapon_name_en[int(m["weapon"][1:])]
    l = [m["name"], m["kill"], m["kill_or_assist"] - m["kill"], m["death"], m["special"], m["point"], w]
    return ", ".join(decodevalue(s) for s in l)

def openfile(path, readwrite):
    if sys.version_info[0] < 3:
        return codecs.open(path, readwrite, "utf-8")
    else:
        return open(path, readwrite, encoding = "utf-8")

def decodevalue(value):
    try:
        return str(value)
    except UnicodeEncodeError:
        return value

def main():
    files = [f for f in os.listdir("Battles") if os.path.isfile(os.path.join("Battles", f))]
    i = 0
    for name in files:
        f = openfile(os.path.join("Battles", name), "r")
        data = json.load(f)

        try:
            os.mkdir("Records")
        except:
            pass
        sys.stdout = openfile(os.path.join("Records", name), "w")

        print("Mode: ", data["rule"])
        print("Result: ", data["result"])
        print("Duration:", data["duration"])
        if ("my_team_count" in data):
            print("Count: ", data["my_team_count"], " vs ", data["his_team_count"])
        else:
            # Turf War case
            print("Percentage: ", data["my_team_percent"], " vs ", data["his_team_percent"])
        print("")

        allies = [m for m in data["players"] if m["team"] == "my"]
        foes = [m for m in data["players"] if m["team"] == "his"]
        print(", ".join(str(s) for s in ["Player","K","A","D","SP","P","Weapon"]))
        print("")

        for m in allies:
            print(player_record(m))

        print("")

        for m in foes:
            print(player_record(m))

        i += 1

main()
