import logging

from cool_game.logger import setup_logging
from cool_game.views.game import Game


def main():
    setup_logging()
    logger = logging.getLogger("game")
    logging.getLogger("arcade").setLevel(logging.INFO)
    # logging.getLogger("PIL").setLevel(logging.INFO)

    Game.get_instance().start()
