# Film App — Local Setup

Quick instructions to run the project locally, load the sample MovieLens data, and view the API docs.

## Prerequisites
- Python (recommended 3.10+)
- git (optional)

## 1. Create and activate a virtual environment
```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

## 2. Install dependencies
Install from the provided requirements file: [`requirements.txt`](requirements.txt)
```bash
pip install -r requirements.txt
```

## 3. Apply migrations
Run Django migrations (uses the project `manage.py`):
```bash
python manage.py makemigrations
python manage.py migrate
```
Create a superuser which will used in loading data 
```bash
python manage.py createsuperuser
```
## 4. Load sample data
Place your MovieLens CSV files (`movies.csv`, `ratings.csv`, `tags.csv`, `links.csv`) into a folder named `data` at the project root.

Use the provided management command to load data:

```bash
python manage.py load_sample_data
```
CSV source files are in the `data/` folder (e.g. `data/movies.csv`, `data/ratings.csv`, ...).

## 5. Start the dev server
```bash
python manage.py runserver
```

## 6. Open Swagger UI
The Swagger UI is exposed at:
http://127.0.0.1:8000/api/schema/swagger-ui/

This route is configured in [`film_app/urls.py`](film_app/urls.py).

