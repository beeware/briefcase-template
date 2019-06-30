from {{ cookiecutter.app_name }}.app import main

if __name__ == '__main__':
{%- if cookiecutter.gui_framework == 'Toga' %}
    main().main_loop()
{%- if cookiecutter.gui_framework == 'PySide2' %}
    main()
{%- else %}
    main()
{%- endif %}
