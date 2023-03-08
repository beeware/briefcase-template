"""
{{ cookiecutter.description|escape_toml }}
"""
{% if cookiecutter.gui_framework == 'Toga' -%}
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class {{ cookiecutter.class_name }}(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box()

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return {{ cookiecutter.class_name }}()
{% elif cookiecutter.gui_framework in ('PySide2', 'PySide6') -%}
import sys

try:
    from importlib import metadata as importlib_metadata
except ImportError:
    # Backwards compatibility - importlib.metadata was added in Python 3.8
    import importlib_metadata

from {{ cookiecutter.gui_framework }} import QtWidgets


class {{ cookiecutter.class_name }}(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('{{ cookiecutter.app_name }}')
        self.show()


def main():
    # Linux desktop environments use app's .desktop file to integrate the app
    # to their application menus. The .desktop file of this app will include
    # StartupWMClass key, set to app's formal name, which helps associate
    # app's windows to its menu item.
    #
    # For association to work any windows of the app must have WMCLASS
    # property set to match the value set in app's desktop file. For PySide2
    # this is set with setApplicationName().

    # Find the name of the module that was used to start the app
    app_module = sys.modules['__main__'].__package__
    # Retrieve the app's metadata
    metadata = importlib_metadata.metadata(app_module)

    QtWidgets.QApplication.setApplicationName(metadata['Formal-Name'])

    app = QtWidgets.QApplication(sys.argv)
    main_window = {{ cookiecutter.class_name }}()
    {%- if cookiecutter.gui_framework == 'PySide2' %}
    sys.exit(app.exec_())
    {%- else %}
    sys.exit(app.exec())
    {%- endif %}
{%- elif cookiecutter.gui_framework == 'PursuedPyBear' %}
import os
import sys

try:
    from importlib import metadata as importlib_metadata
except ImportError:
    # Backwards compatibility - importlib.metadata was added in Python 3.8
    import importlib_metadata

import ppb


class {{ cookiecutter.class_name }}(ppb.Scene):
    def __init__(self, **props):
        super().__init__(**props)

        self.add(ppb.Sprite(
            image=ppb.Image('{{ cookiecutter.module_name }}/resources/{{ cookiecutter.app_name }}.png'),
        ))


def main():
    # Linux desktop environments use app's .desktop file to integrate the app
    # to their application menus. The .desktop file of this app will include
    # StartupWMClass key, set to app's formal name, which helps associate
    # app's windows to its menu item.
    #
    # For association to work any windows of the app must have WMCLASS
    # property set to match the value set in app's desktop file. For PPB this
    # is set using environment variable.

    # Find the name of the module that was used to start the app
    app_module = sys.modules['__main__'].__package__
    # Retrieve the app's metadata
    metadata = importlib_metadata.metadata(app_module)

    os.environ['SDL_VIDEO_X11_WMCLASS'] = metadata['Formal-Name']

    ppb.run(
        starting_scene={{ cookiecutter.class_name }},
        title=metadata['Formal-Name'],
    )
{%- elif cookiecutter.gui_framework == 'Pygame' %}
import pygame
import sys

try:
    from importlib import metadata as importlib_metadata
except ImportError:
    # Backwards compatibility - importlib.metadata was added in Python 3.8
    import importlib_metadata


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
FPS = 60


def main():
    # Find the name of the module that was used to start the app
    app_module = sys.modules["__main__"].__package__
    # Retrieve the app's metadata
    metadata = importlib_metadata.metadata(app_module)

    pygame.init()
    pygame.display.set_caption(metadata["Formal-Name"])

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        screen.fill(WHITE)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()
{% else -%}
def main():
    # This should start and launch your app!
    pass
{% endif -%}
