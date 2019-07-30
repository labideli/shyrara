# -*- coding: utf-8 -*-

MAP = {
    (-1, -1): {
        "site": "hospital",
        "valid_action": ["cure"]
    },
    (0, 0): {
        "site": "home",
        "valid_action": ["study", "sport", "sleep", "play"]
    },
    (0, 1): {
        "site": "street",
        "valid_action": ["play", "walk"]
    },
    (1, 0): {
        "site": "street",
        "valid_action": ["play", "walk"]
    },
    (1, 1): {
        "site": "school",
        "valid_action": ["study", "sport", "sleep", "play"]
    }
}


class RunDailyAction(object):
    __attrs__ = [
        "study", "sport", "sleep", "play", "walk", "cure"
    ]

    def __init__(self, character):
        self.character = character

    def __call__(self, location, action):
        assert action in self.__attrs__
        if self.character["POW"] < 50:
            print("warning: {} is too tired, need to go hospital and be cured"
                  .format(self.character["name"]))
            self.character["location"] = (-1, -1)
            self.run_cure()
            status = "tired"
        else:
            self.character["location"] = location
            getattr(self, "run_{}".format(action))()
            status = "normal"
        return status

    def run_study(self):
        self.character["INT"] += 1
        self.character["POW"] -= 2

    def run_sport(self):
        self.character["ATK"] += 1
        self.character["POW"] -= 3

    def run_play(self):
        self.character["DEF"] += 1
        self.character["POW"] -= 2

    def run_walk(self):
        self.character["AGI"] += 1
        self.character["POW"] -= 2

    def run_sleep(self):
        self.character["POW"] += 3

    def run_cure(self):
        self.character["POW"] += 5
        self.character["INT"] -= 0.5
        self.character["ATK"] -= 0.5
        self.character["DEF"] -= 0.5
        self.character["AGI"] -= 0.5


class DailyAction(object):
    def __init__(self, character):
        self.blocks_count = 4
        self.action_plan = []
        self.character = character
        self.pre_location = self.character["location"]
        self.run_action = RunDailyAction(self.character)

    def add_action(self, pre_location, action):
        if len(self.action_plan) >= self.blocks_count:
            print("warning: at most {} actions in the plan".format(
                self.blocks_count))
        elif pre_location not in MAP:
            print("warning: unknown location")
        elif abs((self.pre_location[0] - pre_location[0]) ** 2
                 + (self.pre_location[1] - pre_location[1]) ** 2) > 1:
            print("warning: cannot reach the location")
        elif action not in MAP[pre_location]["valid_action"]:
            print("warning: cannot do the action {} on {}".format(
                action, MAP[pre_location]["site"]
            ))
        else:
            self.action_plan.append((pre_location, action))
            self.pre_location = pre_location

    def del_action(self, index):
        if index < len(self.action_plan):
            self.action_plan = self.action_plan[:index]
            if len(self.action_plan) == 0:
                self.pre_location = self.character["location"]
            else:
                self.pre_location = self.action_plan[-1][0]
        else:
            print("warning: invalid operation")

    def run_action_plan(self):
        if len(self.action_plan) == self.blocks_count:
            for index, (pre_location, action) in enumerate(self.action_plan):
                print("action {}: do {} at {}".format(
                    index, action, MAP[pre_location]["site"]))
                status = self.run_action(pre_location, action)
                if status == "tired":
                    for i in range(index, self.blocks_count):
                        self.action_plan[i] = ((-1, -1), "cure")
                print("action plan:", self.action_plan)
                print("character:", self.character)
            self.action_plan = []
            self.pre_location = self.character["location"]
        else:
            print("warning: action plan is not ready")

    def main(self):
        while True:
            cmd = str(raw_input("operate: ")).strip()
            if cmd.startswith("add"):
                loc_action = cmd.replace("add", "").strip()
                pre_location, action = loc_action.split(" ")
                self.add_action(eval(pre_location), action)
            elif cmd.startswith("del"):
                index = int(cmd.replace("del", "").strip())
                self.del_action(index)
            elif cmd == "run":
                self.run_action_plan()
            elif cmd == "save":
                pass
            elif cmd == "exit":
                return
            else:
                print("warning: unknown command")
            print("action plan:", self.action_plan)
            print("pre_location:", self.pre_location)


if __name__ == "__main__":
    character_info = {
        "name": "tsuna",
        "location": (0, 0),
        "POW": 55,
        "INT": 10,
        "ATK": 10,
        "DEF": 10,
        "AGI": 10
    }
    DailyAction(character_info).main()
    print(character_info)
