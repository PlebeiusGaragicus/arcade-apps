import os
from time import sleep

from PIL import Image, ImageDraw, ImageFont

from seedsigner.hardware.buttons import HardwareButtonsConstants
from seedsigner.gui.screens import BaseTopNavScreen, WarningEdgesThread, WarningEdgesMixin
from seedsigner.views.view import View, Destination, NotYetImplementedView, BackStackView

from seedsigner.views.module_views import ModuleExecutionHandlerView

from modules.games.color import *

class BaseGameScreen(ModuleExecutionHandlerView, BaseTopNavScreen, WarningEdgesMixin, View):
    intro_image_filename: str = None

    def __post_init__(self):
        self.title = ""
        self.show_back_button = False
        # self.resolution = (96, 96)
        self.framerate = 30
        self.instructions_text = None

        # self.alive = True # done inside self._run() now
        self.score = 0
        self.won_the_game: bool = None
        super().__post_init__()

    def run(self):
        """
            NOTE: THIS IS THE ENTRYPOINT FOR THE GAME WHEN IT TAKES OVER FULL CONTROL
            NOTE: THIS CLASS SATISFIES THE ModuleHandler INTERFACE
                -->> it defines a run function that calls `self.display()`
                -->> it defines a _run() function that actually draws to the screen using PIL
                -->> it may return control to run() which may self.display()

            As a BasePausableGameScreen, this class checks or KEY1 input and pauses the game via pause_screen()
            Also, it runs results_screen() when the game is over and returns control to run() which may run self.display(), depending on user input

            Care is taken to wait for the user to release buttons in order for screens not to flash too quickly.
        """
        self.hw_inputs.block_for_all_buttons_release()

        self.intro()

        while True:
            play_again = self.display()

            if play_again is False:
                break
        
        return Destination( BackStackView )
    
    def intro(self):
        """
            Display the intro image for the game.

            Fails gracefully if there's no intro image.
        """
        try:
            image_url = os.path.join(self.my_directory, "img", "splash_screen.png")
            logo = Image.open(image_url).convert("RGB")

        except FileNotFoundError:
            return
        img = Image.new('RGB', logo.size, (255, 255, 255))
        img.paste(logo)
        with self.renderer.lock:
            self.renderer.disp.ShowImage(img, 0, 0)
        sleep(1.3)

    def setup(self):
        raise Exception("setup() not implemented in the child class!")

    def update(self):
        raise Exception("update() not implemented in the child class!")

    def input(self, input = None):
        raise Exception("input() not implemented in the child class!")

    def draw(self):
        raise Exception("draw() not implemented in the child class!")

    def _run(self):
        self.alive = True
        self.setup()

        while self.alive is True:
            self.update()

            input = self.hw_inputs.has_any_input(ret_list=True)
            if HardwareButtonsConstants.KEY1 in input:
                user_quits = self.pause_screen()
                self.hw_inputs.block_for_all_buttons_release()
                if user_quits:
                    return False
            self.input(input=input)
            self.draw()

        return self.results_screen(self.won_the_game)
    
    def pause_screen(self) -> bool:
        from seedsigner.controller import Controller
        unlocked = Controller.get_instance().is_unlocked

        from seedsigner.models.settings import Settings, SettingsConstants
        able_to_unlock = Settings.get_instance()._data[SettingsConstants.SETTING__ONLY_GAMES] is SettingsConstants.OPTION__DISABLED

        def draw_pause_screen():
            FONT_SIZE = 40
            image = Image.new("RGB", (240, 240), DEEP_GREY)
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("./src/seedsigner/resources/fonts/Inconsolata-SemiBold.ttf", 34)
            large_font = ImageFont.truetype("./src/seedsigner/resources/fonts/Inconsolata-SemiBold.ttf", FONT_SIZE)

            draw.text((10, 15), "GAME PAUSED", font=large_font, fill=BRIGHT_GOLD)
            draw.text((68, 115), "CONTINUE >", font=font, fill=GREEN_1)
            draw.text((136, 180), "QUIT >", font=font, fill=GREEN_2)

            with self.renderer.lock:
                self.renderer.disp.ShowImage(image, 0, 0)

            return (image, draw)

        image, draw = draw_pause_screen()
        sleep(0.1)
        self.hw_inputs.block_for_all_buttons_release()

        while True:
            # this if statement is for the unlock sequence to exit the game menu
            if able_to_unlock and not unlocked and self.hw_inputs.check_for_low(key=HardwareButtonsConstants.KEY1):
                button_presses = 0
                released = True
                while self.hw_inputs.check_for_low(key=HardwareButtonsConstants.KEY1):
                    if not self.hw_inputs.check_for_low(key=HardwareButtonsConstants.KEY_PRESS):
                        released = True

                    if released and self.hw_inputs.check_for_low(key=HardwareButtonsConstants.KEY_PRESS):
                        button_presses += 1
                        print("Button Presses: ", button_presses)
                        released = False

                    if self.hw_inputs.check_for_low(keys=[
                        HardwareButtonsConstants.KEY_UP,
                        HardwareButtonsConstants.KEY_DOWN,
                        HardwareButtonsConstants.KEY_LEFT,
                        HardwareButtonsConstants.KEY_RIGHT,
                        HardwareButtonsConstants.KEY2,
                        HardwareButtonsConstants.KEY3
                    ]):
                        button_presses = 0

                    # if not unlocked and button_presses == 21:
                    if not unlocked and button_presses == 21:
                        Controller.get_instance().is_unlocked = True
                        unlocked = True
                        print("Unlocking...")

                        # draw.rectangle((0, 0, 240, 240), outline=GUIConstants.BITCOIN_ORANGE, width=2)
                        draw.rectangle((0, 0, 240, 240), outline=BITCOIN_ORANGE, width=2)

                        with self.renderer.lock:
                            self.renderer.disp.ShowImage(image, 0, 0)
                        
                        sleep(0.1)
                        image, draw = draw_pause_screen() # redraw the pause screen once user let's go of KEY1


            if self.hw_inputs.check_for_low(key=HardwareButtonsConstants.KEY2):
                self.hw_inputs.block_for_all_buttons_release()
                return False # continue playing

            if self.hw_inputs.check_for_low(key=HardwareButtonsConstants.KEY3):
                self.hw_inputs.block_for_all_buttons_release()
                return True # exit to menu


    def results_screen(self, won_the_game: bool = None) -> bool:
        FONT_SIZE = 50
        HEIGHT = 15
        GAP = 4
        LEFT = 10
        # bg_color = GUIConstants.DARK_GREEN if won_the_game is True else GUIConstants.DEEP_GREY
        bg_color = DARK_GREEN if won_the_game is True else DEEP_GREY

        image = Image.new("RGB", (240, 240), bg_color)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("./src/seedsigner/resources/fonts/Inconsolata-SemiBold.ttf", 34)
        large_font = ImageFont.truetype("./src/seedsigner/resources/fonts/Inconsolata-SemiBold.ttf", FONT_SIZE)
        # icon_font = ImageFont.truetype("./src/seedsigner/resources/fonts/Font_Awesome_6_Free-Solid-900.otf", 30)

        if won_the_game is None:
            draw.text((LEFT, HEIGHT), "GAME OVER", font=large_font, fill=BRIGHT_PINK)
        else:
            if won_the_game:
                # TODO - try to make the results screen flash the edges of the screen
                # self.threads.append(WarningEdgesThread(args=(self,)))

                LEFT = 24
                draw.text((LEFT, HEIGHT), "YOU WON!", font=large_font, fill=BRIGHT_GOLD)
                draw.rectangle((LEFT-GAP, HEIGHT-GAP, 222, HEIGHT+FONT_SIZE), outline=BRIGHT_PINK, width=2)
            else:
                draw.text((LEFT, HEIGHT), "YOU LOST!", font=large_font, fill=LIGHT_RED)
                draw.rectangle((LEFT-GAP, HEIGHT-GAP, 235, HEIGHT+FONT_SIZE), outline=BRIGHT_GOLD, width=3)

        draw.text((68, 115), "NEW GAME >", font=font, fill=GREEN_1)
        draw.text((136, 180), "QUIT >", font=font, fill=GREEN_2)

        with self.renderer.lock:
            self.renderer.disp.ShowImage(image, 0, 0)

        sleep(0.1)
        self.hw_inputs.block_for_all_buttons_release()
        while True:
            if self.hw_inputs.check_for_low(key=HardwareButtonsConstants.KEY2):
                self.hw_inputs.block_for_all_buttons_release()
                return True # new game

            if self.hw_inputs.check_for_low(key=HardwareButtonsConstants.KEY3):
                self.hw_inputs.block_for_all_buttons_release()
                return False # exit to menu
