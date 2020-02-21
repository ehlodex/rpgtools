import random
import time
from rpgtools.characters import Character, race, role, gender, align

hero = Character('Sir Robin',
                 race['h'], role['wa'], gender['m'], align['lg'])

enemy = Character(random.choice(['Vohrsoth', 'Cthulhu', 'Kaiju']),
                  race[random.choice(list(race))],
                  role[random.choice(list(role))],
                  gender[random.choice(list(gender))],
                  align['ce'])

# cheat mode!
hero.raw.damage_value = (50, 100)
enemy.raw.damage_value = (75, 100)

print('Before you stands {}, the fearsome {}-class {}.'.format(enemy.name, enemy.role[0], enemy.race))

while enemy.hp_left > 0 and hero.hp_left > 0:
    action = input('Will you attack, run, or interact? [A/r/i] ') or 'a'
    action = action.lower()[0]
    if action == 'a':
        damage = hero.attack(enemy)
        if damage:
            print('You inflict {} damage! '.format(damage), end='')
        elif not damage:
            print('You cannot attack that!')
        else:
            print('ERROR: Damage was not returned correctly!')

        if enemy.alive:
            time.sleep(1)
            damage = enemy.attack(hero)
            print('... {} strikes back for {} damage!\n'.format(enemy.name, damage))
        else:
            print(' \n')

    elif action == 'r':
        damage = False
        if random.randint(0, 2) == random.randint(0, 2):
            damage = enemy.attack(hero)
        if damage:
            print('{} takes a cheap shot as you run away! (-{})'.format(enemy.name, damage))
        else:
            print('{} bravely runs away! (-0)'.format(hero.name))
        break

    elif action == 'i':
        interact = hero.interact(enemy)
        if interact:
            pass
        else:
            print('You cannot interact with that.')

    print('{:<15}: {:>4} / {:>4}'.format(hero.name, hero.hp_left, hero.hp))
    print('{:<15}: {:>4} / {:>4}'.format(enemy.name, enemy.hp_left, enemy.hp))

if hero.alive and not enemy.alive:
    print('You are victorious!')
elif not hero.alive:
    print('You are dead.')
elif hero.alive and enemy.alive:
    print('Brave {} turned about, and gallantly {} chickened out!'.format(hero.name, hero._gender[1]))
else:
    print("Hmm... that wasn't supposed to happen...")
