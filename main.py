import time
from dota_auto_chess.util import screenshot
from dota_auto_chess.ocr import recognize_heroes as recognize_heroes_ocr, recognize_battle_state, recognize_round
from dota_auto_chess.stat import update_heroes_stat, plot_bar

if __name__ == '__main__':
    prev_heroes = []
    current_round = 0
    last_battle_state = None

    while True:
        time.sleep(0.1)
        screen = screenshot.take_screenshot()

        # TODO: раунд не всегда распознается верно
        # if current_round < 10:
        #     round_box = (795, 10, 20, 20)
        # else:
        #     round_box = (795, 10, 20, 20)
        #
        # round_on_screen = recognize_round(screen, round_box)
        # if round_on_screen is not None and (round_on_screen - 1 == current_round or current_round == 0):
        #     current_round = round_on_screen

        battle_state_box = (885, 32, 145, 35)
        battle_state = recognize_battle_state(screen, battle_state_box)
        
        if battle_state is not None:
            if battle_state == 'PREPARE' and last_battle_state != 'PREPARE':
                current_round += 1
                print('NEW ROUND:', current_round)

            last_battle_state = battle_state

        heroes_names_box = (360, 380, 1210, 25)
        heroes = recognize_heroes_ocr(screen, heroes_names_box)

        if len(heroes) and prev_heroes != heroes:
            print(current_round, heroes)

            if len(heroes) == 5:
                stat = update_heroes_stat(heroes)
                plot_bar('heroes.html', *stat)

            prev_heroes = heroes
