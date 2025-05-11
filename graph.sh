mkdir logs

uv run ./manage.py makemigrations
uv run ./manage.py migrate

uv run ./manage.py graph_models -a --color-code-deletions -g -E -n -X contenttype -o ./.graph-models.png
