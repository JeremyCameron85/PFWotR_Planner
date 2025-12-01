class Character:
    def __init__(self, name="", race=None, char_class=None):
        self.name = name
        self.race = race
        self.level = 1
        self.feats = []

    def level_up(self):
        self.level += 1