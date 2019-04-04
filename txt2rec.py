# -*- coding: utf-8 -*-
import json
import sys
import os
import dbs
import weapon_name

def export_weapon_name():
    w = open("test.txt", "r", encoding = 'UTF-8')
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
    
    nu = open("weapon_name.txt", "w", encoding = 'UTF-8')
    nu.write(str(da))
    nu.close()

def player_record(m):
    w = weapon_name.weapon_name_en[int(m["weapon"][1:])]
    l = [m["name"], m["kill"], m["kill_or_assist"] - m["kill"], m["death"], m["special"], m["point"], w]
    return ", ".join(str(s) for s in l)

def main():
    files = [f for f in os.listdir("Battles") if os.path.isfile(os.path.join("Battles", f))]
    i = 0
    for name in files:
        f = open(os.path.join("Battles", name), "r")
        data = json.load(f)

        os.makedirs("Records", exist_ok=True)
        sys.stdout = open(os.path.join("Records", str(i) + ".txt"), "w", encoding = 'UTF-8')
        
        print("Mode: ", data["rule"])
        print("Result: ", data["result"])
        print("Duration:", data["duration"])
        print("Count: ", data["my_team_count"], " vs ", data["his_team_count"])
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
