# code-quest-interview

This repository contains a simple Django project built with Django REST Framework and Django Unfold for admin customization.

---

## Project Structure

* The main source code is located in the `src` directory.
* The `src` directory contains the base project settings, organized into multiple files for better readability and maintainability.
* The project follows the typical cookiecutter-style structure for Django projects.

---

## Getting Started

### Prerequisites

* Python (recommended version 3.8+)
* `uv` package manager (or you can use `pip`)

### Installation & Running

1. Install the `uv` package manager:

   ```bash
   pip install uv
   ```

2. Run the following commands to set up the database and create a superuser:

   ```bash
   uv run ./manage makemigrations
   uv run ./manage migrate
   uv run ./manage createsuperuser
   ```

3. Start the development server:

   ```bash
   uv run ./manage runserver
   ```

---

### Using Docker

To start the necessary services such as Redis and PostgreSQL databases, you can use Docker Compose:

```bash
docker-compose up -d
```

This will run the required databases in detached mode.

---

## Applications Overview

The project contains two main Django apps:

* **core**
* **apis**

---

### core app

The `core` app handles the fundamental parts of the project, including:

* **Models:**

  * `Profile`:

    * One-to-one relationship with the user authentication model (`User`).
    * Fields include: `user`, `bio`, `birth_date`, `created_at`, `full_name`, `profile_image`, `cover_image`, `language`, and `notes`.
  * `CreatedUser` (Permission Class):

    * Custom permission to ensure that only the user who created a record can update or delete it.

* **Signals:**

  * Automatically creates a `Profile` when a new user is created.
  * Updates the profile when user data changes.

* **Templates:**

  * Contains a profile page template displaying user information in a card format after login via the API.

* **Admin Configuration:**

  * Uses [Django Unfold](https://unfoldadmin.com/docs/) for enhanced admin interface customization.

* **Views:**

  * A view to retrieve and display profile data.

---

## Demo

[Watch demo video](https://drive.google.com/file/d/1U1N0KG5v0uqIyItskfBlW8-yArhdhSPg/view?usp=sharing)

---

## Contact

For any inquiries or support, please reach out to:

* **Email:** [mahmoud.ezzat.moustafa@gmail.com](mailto:mahmoud.ezzat.moustafa@gmail.com)
* **Phone:** +2 (010) 1612-7655

---

If you have any questions or need assistance, feel free to open an issue or contribute to the project.

