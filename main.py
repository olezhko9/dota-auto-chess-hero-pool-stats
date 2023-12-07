from dota_auto_chess.hero_stat import get_stat_from_files_with_ocr, get_stat_from_screen_with_ocr, get_stat_from_screen_with_cnn

if __name__ == '__main__':
    # get_stat_from_files_with_ocr()
    get_stat_from_screen_with_ocr()
    # get_stat_from_screen_with_cnn()

    # TODO: implement algorithm similar to
    # while True:
    #     sleep(1)
    #     img = get_image()
    #     heroes = get_heroes_from_image()
    #     append_to_plot()