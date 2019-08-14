# -*- coding: utf-8 -*-

"""
  adjust and add move action
  metrics: "ENERGY", "FIRE", "CON", "INT", "WIL", "AGI": 10
"""

MAP = {
    (-1, -1): {
        "site": "hospital",
        "valid_action": ["cure"]
    },
    (0, 0): {
        "site": "home",
        "valid_action": ["study", "sport", "image", "walk", "sleep"]
    },
    (0, 1): {
        "site": "street",
        "valid_action": ["walk"]
    },
    (1, 0): {
        "site": "street",
        "valid_action": ["walk"]
    },
    (1, 1): {
        "site": "school",
        "valid_action": ["study", "sport", "image", "walk", "sleep"]
    }
}


class RunDailyAction(object):
    __attrs__ = [
        "move", "study", "sport", "image", "battle", "walk", "sleep",
        "cure", "talk", "together"
    ]

    def __init__(self, character):
        self.character = character

    def __call__(self, action, location=None):
        assert action in self.__attrs__
        if self.character["ENERGY"] < 50:
            print("warning: {} is too tired, need to go hospital and be cured"
                  .format(self.character["name"]))
            self.character["location"] = (-1, -1)
            self.run_cure()
            status = "tired"
        elif action == "move":
            self.run_move(location)
            status = "normal"
        else:
            getattr(self, "run_{}".format(action))()
            status = "normal"
        return status

    def run_move(self, location):
        self.character["ENERGY"] -= 1
        self.character["AGI"] += 0.5
        self.character["location"] = location

    def run_study(self):
        self.character["ENERGY"] -= 2
        self.character["INT"] += 2

    def run_sport(self):
        self.character["ENERGY"] -= 3
        self.character["CON"] += 2
        self.character["AGI"] += 1

    def run_image(self):
        self.character["ENERGY"] -= 2
        self.character["WIL"] += 2

    def run_battle(self):
        pass  # turn to battle scene

    def run_walk(self):
        self.character["ENERGY"] -= 1
        pass  # turn to events

    def run_sleep(self):
        self.character["ENERGY"] += 3

    def run_cure(self):
        self.character["ENERGY"] += 5
        self.character["INT"] -= 0.5
        self.character["ATK"] -= 0.5
        self.character["DEF"] -= 0.5
        self.character["AGI"] -= 0.5


class DailyAction(object):
    def __init__(self, character):
        self.character = character
        self.run_action = RunDailyAction(self.character)

        self.blocks_count = 4
        self.action_plan = []  # [(action, location)]
        self.pre_location = self.character["location"]

    def _change_location(self, pre_location):
        if pre_location not in MAP:
            print("warning: unknown location")
        elif abs((self.pre_location[0] - pre_location[0]) ** 2
                 + (self.pre_location[1] - pre_location[1]) ** 2) > 1:
            print("warning: cannot reach the location")
        else:
            self.pre_location = pre_location

    def add_action(self, action):
        if len(self.action_plan) >= self.blocks_count:
            print("warning: at most {} actions in the plan".format(
                self.blocks_count))
        elif (action != "move"
              and action not in MAP[self.pre_location]["valid_action"]):
            print("warning: cannot do the action {} on {}".format(
                action, MAP[self.pre_location]["site"]))
        else:
            self.action_plan.append((action, self.pre_location))

    def del_action(self, index):
        if index < len(self.action_plan):
            self.action_plan = self.action_plan[:index]
            if len(self.action_plan) == 0:
                self.pre_location = self.character["location"]
            else:
                self.pre_location = self.action_plan[-1][1]
        else:
            print("warning: invalid operation")

    def run_action_plan(self):
        if len(self.action_plan) == self.blocks_count:
            for index, (action, pre_location) in enumerate(self.action_plan):
                print("action {}: {} at/in/to {}".format(
                    index, action, MAP[pre_location]["site"]))
                status = self.run_action(action, pre_location)
                if status == "tired":
                    for i in range(index, self.blocks_count):
                        self.action_plan[i] = ("cure", (-1, -1))
                print("action plan:", self.action_plan)
                print("character:", self.character)
            self.action_plan = []
            self.pre_location = self.character["location"]
        else:
            print("warning: action plan is not ready")

    def main(self):
        while True:
            cmd = str(input("operation: ")).strip()
            if cmd.startswith("move"):
                pre_location = eval(cmd.replace("move", "").strip())
                self._change_location(pre_location)
                self.add_action("move")
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
                self.add_action(cmd)
            print("action plan:", self.action_plan)
            print("pre_location:", self.pre_location)


if __name__ == "__main__":
    character_info = {
        "name": "tsuna",
        "location": (0, 0),
        "ENERGY": 55,
        "FIRE": 10000,
        "CON": 10,
        "INT": 10,
        "WIL": 10,
        "AGI": 10
    }
    DailyAction(character_info).main()
    print(character_info)
