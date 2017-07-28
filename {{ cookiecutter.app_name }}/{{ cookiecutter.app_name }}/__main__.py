from .app import main

if __name__ == '__main__':
{%- if cookiecutter.gui_framework == 'Toga' %}
    main().main_loop()
{%- else %}
    main()
{%- endif %}
