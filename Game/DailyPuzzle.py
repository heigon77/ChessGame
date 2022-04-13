import chessdotcom as chcom


class DailyPuzzle:

    def __init__(self):
        pass

    def get_daily_puzzle(self):
        dailypuzzle = chcom.get_random_daily_puzzle()
        return dailypuzzle
