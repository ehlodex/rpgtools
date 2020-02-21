#!/usr/bin/env python3
"""Characters Module for RPG Tools.

RPG Tools is a basic framework for Role-Playing Games.
Includes Characters, Weapons, Armour, and Game Objects.
"""

# __all__ = []
__version__ = '0.2.2020.0220'
__author__ = 'Joshua Burkholder [ehlodex]'

import random


def get_random(r1, r2=None):
    r1, r2 = r1[0], r1[1]
    # TODO: validation, exception
    return random.randint(r1, r2)


class Attribute:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp


race = {
    'h': Attribute('human', (70, 85, 140, 180, 200)),
    'e': Attribute('elf', (70, 85, 140, 180, 200)),
    'd': Attribute('dwarf', (70, 85, 140, 180, 200)),
    'g': Attribute('gnome', (70, 85, 140, 180, 200)),
    'o': Attribute('orc', (70, 85, 140, 180, 200))
}

role = {
    'wa': Attribute('warrior', (28, 70, 140, 210, 280)),
    'ra': Attribute('ranger', (18, 45, 90, 135, 180)),
    'mo': Attribute('monk', (5, 12.5, 25, 37.5, 50)),
    'ne': Attribute('necromancer', (28, 70, 140, 210, 280)),
    'me': Attribute('mesmer', (18, 45, 90, 135, 180)),
    'el': Attribute('elementalist', (5, 12.5, 25, 37.5, 50))
}

gender = {
    'm': ('male', 'he', 'him', 'his', 'his', 'himself'),
    'f': ('female', 'she', 'her', 'her', 'hers', 'herself'),
    'a': ('asexual', 'it', 'it', 'its', 'its', 'itself')
}

align = {
    'lg': ('Lawful', 'Good'),
    'ln': ('Lawful', 'Neutral'),
    'le': ('Lawful', 'Evil'),
    'ng': ('Neutral', 'Good'),
    'nn': ('Neutral', 'Neutral'),
    'ne': ('Neutral', 'Evil'),
    'cg': ('Chaotic', 'Good'),
    'cn': ('Chaotic', 'Neutral'),
    'ce': ('Chaotic', 'Evil')
}


class Raw:
    pass


class Character:
    def __init__(self, c_name, c_race, c_role, c_gender, c_align):
        self.name = c_name
        self._race = c_race
        self._role1 = c_role
        self._role2 = None
        self._gender = c_gender
        self.alignment = c_align
        self.alive = True
        self._holding1 = None
        self._holding2 = None
        self._injury = 0
        self._level = 1
        self.raw = Raw()
        self.raw.damage_value = (0, 2)
        self.raw.hands_needed = 0
        self.raw.name = 'nothing'

    @property  # damage is outgoing
    def damage(self):
        damage_sum = (get_random(self.weapon.damage_value)
                      + get_random(self.offhand.damage_value))
        return max(damage_sum, 1)

    @property
    def free_hands(self):
        return 2 - self.weapon.hands_needed - self.offhand.hands_needed

    @property
    def gender(self):
        return self._gender[0]

    @property
    def hp(self):
        base = 0
        vita = 370 if self.level > 1 else 300
        for i in range(1, self.level + 1):
            b = int(i // 20)
            base = base + self._role1.hp[b]
            vita = vita + self._race.hp[b]
        return int(base + vita)

    @property
    def hp_left(self):
        return max((self.hp - self.injury), 0)

    @property
    def injury(self):
        return self._injury

    @injury.setter
    def injury(self, new_value):
        self._injury = new_value
        if self.injury >= self.hp:
            self.alive = False

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, new_value):
        new_value = new_value if new_value < 80 else 80
        self._level = new_value

    @property  # _holding2
    def offhand(self):
        return self.raw if self._holding2 is None else self._holding2

    @property
    def race(self):
        return self._race.name

    @property
    def role(self):
        role1 = self._role1.name
        role2 = None if self._role2 is None else self._role2.name
        return [role1, role2]

    @property  # _holding1
    def weapon(self):
        return self.raw if self._holding1 is None else self._holding1

    def attack(self, other):
        if other == self:
            return None
        try:
            return other.on_attack(self)
        except AttributeError:
            pass
        return False

    def interact(self, other):
        if other == self:
            return None
        try:
            return other.on_interact(self)
        except AttributeError:
            pass
        return False

    def kick(self, other):
        if other == self:
            return None
        try:
            return other.on_kick(self)
        except AttributeError:
            pass
        return False

    def level_up(self):
        self.level = self.level + 1
        print('{} has advanced to level {}!'.format(self.name, self.level))

    def on_attack(self, other):
        injury = other.damage
        self.injury = self.injury + injury
        return injury

    def punch(self, other):
        if other == self:
            return None
        try:
            return other.on_punch(self)
        except AttributeError:
            pass
        return False

    def status(self):
        print('{} is a level {} {} {} with {} hp, dealing {} damage.'
              .format(self.name, self.level, self.gender, self.race, self.hp, self.damage))

        print('{} wields {} as {} primary weapon, and '
              'holds {} as a secondary.'
              .format(self._gender[1].capitalize(),
                      self.weapon.name, self._gender[3], self.offhand.name))


# THIS SECTION USED FOR TESTING ONLY!
if __name__ == '__main__':
    q = Character('John Q. Public',
                  race['h'], role['wa'], gender['m'], align['ng'])
    q.status()
