DEBUG = False

from dataclasses import dataclass

from seedsigner.views.view import View, Destination, BackStackView, NotYetImplementedView, RET_CODE__BACK_BUTTON
from seedsigner.views.tools_views import ButtonListScreen

from modules.apps import BaseAppScreen
from modules.games.fonts import FontAwesomeIcons


@dataclass
class Handler(BaseAppScreen):
    display_name: str = "Always Crashes"
    font_icon: FontAwesomeIcons = FontAwesomeIcons.POOP
    intro_image_filename: str = None # TODO should be Path()???

    def run(self):
         # use skip_current_view=True else we go back to the Handler which will run SimpleMenu again and not bring us back to the AppMenuView
        return Destination( SimpleMenu, skip_current_view=True )




class SimpleMenu(View):
    pass
    # def __init__(self):
    #     super().__init__()

    # def run(self):
    #     """
    #         This satisfies the View interface.
    #         This is the main entry point for the application.
    #     """
    #     SCAN_SEED = ("Add something", "+")
    #     SCAN_DESCRIPTOR = ("Subtract something", "-")
    #     TYPE_12WORD = ("That way", ">")
    #     button_data = []

    #     button_data.append(SCAN_SEED)
    #     button_data.append(SCAN_DESCRIPTOR)
    #     button_data.append(TYPE_12WORD)

    #     selected_menu_num = ButtonListScreen(
    #         title="Dummy app",
    #         button_data=button_data,
    #         is_button_text_centered=False,
    #         is_bottom_list=True,
    #     ).display()

    #     if selected_menu_num == RET_CODE__BACK_BUTTON:
    #         return Destination(BackStackView)

    #     # return Destination(NotYetImplementedView)
    #     return Destination(BackStackView)
