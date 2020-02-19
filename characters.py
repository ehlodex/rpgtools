#!/usr/bin/env python3
"""Characters Module for RPG Tools.

RPG Tools is a basic framework for Role-Playing Games.
Includes Characters, Weapons, Armour, and Game Objects.
"""

# __all__ = []
__version__ = '0.1'
__author__ = 'Joshua Burkholder [ehlodex]'

import random


def get_random(r1, r2=None):
    r1, r2 = r1[0], r1[1]
    # TODO: validation, exception
    return random.randint(r1, r2)


class Attribute:
    def __init__(self, name, injury_class, remove_class, hp, mp):
        self.name = name
        self.injury_class = injury_class
        self.remove_class = remove_class
        self.hp = random.choice(hp)
        self.mp = random.choice(mp)


race = {
    'h': Attribute('human', 'physical', None, (50, 55, 60), (40, 45, 50)),
    'e': Attribute('elf', 'physical', None, (50, 55, 60), (40, 45, 50)),
    'd': Attribute('dwarf', 'physical', None, (50, 55, 60), (40, 45, 50)),
    'g': Attribute('gnome', 'physical', None, (50, 55, 60), (40, 45, 50)),
    'o': Attribute('orc', 'physical', None, (60, 65, 70), (15, 20, 25, 30))
}

role = {
    'wa': Attribute('warrior', None, None, (10, 15), (0, 5)),
    'ra': Attribute('ranger', None, None, (10, 15), (0, 5)),
    'mo': Attribute('monk', None, None, (10, 15), (0, 5)),
    'ne': Attribute('necromancer', None, None, (10, 15), (0, 5)),
    'me': Attribute('mesmer', None, None, (10, 15), (0, 5)),
    'el': Attribute('elementalist', None, None, (10, 15), (0, 5))
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
        self._holding1 = None
        self._holding2 = None
        self.raw = Raw()
        self.raw.damage_value = (0, 1)
        self.raw.damage_bonus = (0, 0)
        self.raw.damage_class = 'physical'
        self.raw.hands_needed = 0
        self.raw.hp_bonus = 0
        self.raw.mp_bonus = 0
        self.raw.name = 'nothing'

    def status(self):
        print('{} is a {} {} with {} hp and {} mp.'
              .format(self.name, self.gender, self.race, self.hp, self.mp))

        print('{} deals {} damage, wielding {} as {} primary weapon, and '
              'holding {} as a secondary.'
              .format(self._gender[1].capitalize(), self.damage,
                      self.weapon.name, self._gender[3], self.offhand.name))

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
        return self._race.hp + self._role1.hp + self.weapon.hp_bonus + self.offhand.hp_bonus

    @property
    def injury_class(self):
        injured_by = [self._race.injury_class, self._role1.injury_class]
        # TODO: if armour_value > threshold: injured_by.remove['physical']
        while None in injured_by:
            injured_by.remove(None)
        return injured_by

    @property
    def mp(self):
        return self._race.mp + self._role1.mp + self.weapon.mp_bonus + self.offhand.mp_bonus

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

    @property  # _holding2
    def offhand(self):
        return self.raw if self._holding2 is None else self._holding2


# THIS SECTION USED FOR TESTING ONLY!
if __name__ == '__main__':
    q = Character('John Q. Public', race['h'], role['wa'], gender['m'], align['ng'])
    q.status()
    print(q.injury_class)
