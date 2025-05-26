# Using django with apis

This project is a complete Django application built with **Django REST Framework** and **Django Ninja**, featuring advanced admin customization using **Django Unfold**, along with a secure JWT token management system including token rotation and revocation to support advanced authentication scenarios.

---

## Project Structure

* The main source code is located inside the `src` folder.
* Project settings are divided into multiple files within `src` for better organization and maintainability.
* The project follows the popular Cookiecutter structure for Django to ensure scalability and clarity.
* The APIs include detailed token management with precise data schemas and comprehensive security logging.

---

## Getting Started

### Prerequisites

* Python (version 3.8 or above)
* `uv` package manager (or you can use `pip` instead)
* Docker (optional, for running services like Redis and PostgreSQL)

### Installation and Running Steps

1. Install the `uv` package manager (if not already installed):

   ```bash
   pip install uv
   ```

2. Initialize the database and create a superuser:

   ```bash
   uv run ./manage makemigrations
   uv run ./manage migrate
   uv run ./manage createsuperuser
   ```

3. Run the development server:

   ```bash
   uv run ./manage runserver
   ```

---

### Running with Docker

You can easily start helper services like Redis and PostgreSQL using Docker Compose:

```bash
docker-compose up -d
```

This runs the services in detached mode, allowing the application to connect to them seamlessly.

---

## Project Components

The project contains two main apps:

* **apis**: Apis Endpoints Samples and models
* **core**: Token management, Profile and auth/permission logic

---


### Models

The project includes several models to handle workouts, exercises, statistics, and their relationships with user profiles Also Token model with profile&user relation.

#### Exercise

Represents a physical exercise entry, linked to a user's profile and workouts.

* **Fields:**

  * `name`: Name of the exercise.
  * `description`: Optional detailed description.
  * `duration`: Duration in minutes (optional).
  * `profile`: Foreign key linking to the `Profile` model, representing the owner of the exercise.
  * `workouts`: Many-to-many relationship to `Workout`, representing the workouts this exercise belongs to.

* **Manager:**

  * Uses a custom `WorkoutManager` for specialized query capabilities.

#### Stat

Tracks statistics related to a user's workout activities.

* **Fields:**

  * `profile`: One-to-one link with the `Profile` model to tie stats to a user.
  * `total_workouts`: Count of workouts performed.
  * `total_exercises`: Count of exercises completed.
  * `evaluation`: An integer representing an evaluation score or progress metric.

* **Manager:**

  * Uses a custom `StatManager` for managing statistics-specific queries and operations.

#### Workout

Represents a workout session, containing multiple exercises and metadata.

* **Fields:**

  * `title`: The workout's title or name.
  * `date`: Date when the workout took place.
  * `notes`: Optional additional notes about the workout.
  * `workout_type`: Categorizes the workout type with predefined choices (e.g., strength, cardio).

* **Manager:**

  * Uses `WorkoutManager` for customized queries.


* **Signals:**

  * Automatically creates a `Profile` upon new user registration.
  * Synchronizes `Profile` data with updates to the user data.

* **Admin Customization:**

  * Using [Django Unfold](https://unfoldadmin.com/docs/) for enhanced data management experience.

* **Views and Pages:**

  * Profile page that displays user info in a card after logging in via API.

---

## Highlights

* Rotation reduces the risk of replay attacks.
* Token validation and blacklists ensure authentication integrity.
* Comprehensive logging of errors and security events to enhance traceability and auditing.
* Data validation using Pydantic and Ninja schemas to guarantee data integrity before processing.
* API architecture designed using `ninja_extra` for full CRUD control with well-organized responsibilities.
* Use of Django signals (`post_save`, `post_delete`, `pre_save`) to update related statistics (e.g., updating `Stat` records on exercise creation/deletion).
* Use of `transaction.atomic()` to guarantee data consistency.
* Query optimization using `select_related` and `prefetch_related`.
* Data schemas supporting partial updates (PATCH) and custom filtering.
* Advanced security settings and permissions control.
---
* Implements a complete JWT token system supporting:

  * Token issuance on authentication.
  * Token rotation with automatic checking of refresh tokens.
  * Endpoints for manual token revocation.
  * Display of token trees (access tokens linked to refresh tokens).
  * Token validation with precise exception logging to enhance security.
  * Full integration with Django Ninja and global authentication support.

---

## Contact and Support

* **Email:** [mahmoud.ezzat.moustafa@gmail.com](mailto:mahmoud.ezzat.moustafa@gmail.com)
* **Phone:** +2 (010) 1612-7655

---

## Contribution

Feel free to report issues or submit pull requests. Your contributions help continuously improve the project!


