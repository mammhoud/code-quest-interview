# code-quest-interview
 
this repo defined a simple project using django + django rest framework + django unfold
`src` dir contains a base settings of the project and separated on files to be more readalbe and organized with the same structure of cookiecutters implementation

``
pip install uv
uv run ./manage makemigrations
uv run ./manage migrate
uv run ./manage runserver
``

## apps:
    - core
    - apis

### core:
    contains a basic urls and base models like `profile, defaultbase`
        `profile` -> model:
            - with one to one relation with `user_auth_model`
            - user, bio, birth_date, created_at, full_name, profile_image, cover_image, language, notes
        `created_user` -> permission Class:
            it was created to be added as permission to check if the user was the same user that created the record to delete or update it correctly
