# Minimal Django HTMX Run Tracker

This is a simple run tracking app I built to practice Django and HTMX.

## Features

- Track your runs with distance, time, and date
- Paginated running history
- chart.js graph with monthly distance ran

## Technologies Used

- Django: Web framework for building the backend
- HTMX: For dynamic, AJAX-style interactions without writing JavaScript
- SQLite: Built-in database for storing run data
- uv: Fast Python package installer and resolver

## Prerequisites

- Python 3.8+
- uv

## Installing uv

Before proceeding with the installation, you need to install `uv`. Follow these steps:

1. Install `uv` using `pip`:
   ```pip install uv```

   Or, if you prefer to use `pipx` for isolated installations:
   ```pipx install uv```

2. Verify the installation:
   ```uv --version```

For more detailed installation instructions, visit the [official uv documentation](https://github.com/astral-sh/uv).

## Installation

1. Clone the repository:
   ```git clone https://github.com/DarioRubenScanferlato/minimal-django-htmx-run-tracker.git```
   ```cd minimal-django-htmx-run-tracker```

2. Install the required Python packages:
   ```uv sync```

3. Apply migrations:
   ```python manage.py migrate```

4. (optional) Load initial data fixture:
   ```python manage.py loaddata runs.json```

## Running the Application

1. Start the Django development server:
   ```python manage.py runserver```

2. Open your browser and navigate to `http://localhost:8000`.
