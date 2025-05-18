# code-quest-interview
 
this repo defined a simple project using django + django rest framework + django unfold
`src` dir contains a base settings of the project and separated on files to be more readalbe and organized with the same structure of cookiecutters implementation


could be running by run shell script `run.sh` after install `uv` package manager or use your package manager like pip with  `requirements.txt`
- `pip install uv`
- `uv run ./manage makemigrations `
- `uv run ./manage migrate `
- `uv run ./manage createsuperuser`
- `uv run ./manage runserver `


- starting docker with `docker-compose up -d` for run the databases "redis/postgres"

## apps:
    - core
    - apis

### core:

    contains a basic urls and base models like `profile, defaultbase`
        - `profile` -> model:
            - with one to one relation with `user_auth_model`
            - user, bio, birth_date, created_at, full_name, profile_image, cover_image, language, notes
        - `created_user` -> permission Class:
            it was created to be added as permission to check if the user was the same user that created the record to delete or update it correctly

        - also it could contains some signals to perform action with some triggers
            - create user profile after creating a user 
            - update the user profile after update the user data related to the profile data
        - a templete folder contain a profile page with a card to be displayed to the user after login on api page
        - admin configuration using unfold `https://unfoldadmin.com/docs/`
        - and one view with the profile data

[![asciicast]([https://drive.google.com/file/d/1U1N0KG5v0uqIyItskfBlW8-yArhdhSPg/view?usp=drive_link]())]
