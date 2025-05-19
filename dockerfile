FROM python:3.12-slim-bookworm

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"


# VOLUME [ "/app" ]
# Create and set the working directory

# Copy your application files into the container
# COPY . /app
ADD . /app

WORKDIR /app
# Install Python dependencies
# RUN pip install pipx
# RUN pipx install uv

# RUN pipx ensurepath

# RUN uv run manage.py makemigrations
# RUN uv run manage.py migrate
# RUN uv run manage.py collectstatic --no-input

# CMD ["uv", "run", "manage.py", "runserver"]