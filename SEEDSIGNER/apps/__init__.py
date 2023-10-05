from seedsigner.views.view import View, NotYetImplementedView
from seedsigner.views.module_views import ModuleExecutionHandlerView

class BaseAppScreen(ModuleExecutionHandlerView, View):
    def __init__(self):
        self.title = ""
        self.show_back_button = False
        self.framerate = 30
        self.instructions_text = None

    def run(self):
        raise NotYetImplementedView("run() not implemented in application")
