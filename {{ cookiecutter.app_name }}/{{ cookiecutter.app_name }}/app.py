{% set app_class_name = cookiecutter.formal_name.title().replace(' ','').replace('-','').replace('!','').replace('.','').replace(',','') -%}
{% if cookiecutter.gui_framework == 'Toga' %}import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class {{ app_class_name }}(toga.App):
    def startup(self):
        # Create a main window with a name matching the app
        self.main_window = toga.MainWindow(title=self.name)

        # Create a main content box
        main_box = toga.Box()

        # Add the content on the main window
        self.main_window.content = main_box

        # Show the main window
        self.main_window.show()


def main():
    return {{ app_class_name }}('{{ cookiecutter.formal_name }}', '{{ cookiecutter.bundle }}.{{ cookiecutter.app_name }}')
{% else -%}
def main():
    # This should start and launch your app!
    pass
{% endif -%}
