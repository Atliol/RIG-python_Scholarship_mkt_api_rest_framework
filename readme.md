# RIG-Python Scholarship Homework

### Setup a Project

### 1. Navigate to project

```bash
cd <foldername>
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Activate virtual environment

| Platform  | Script                      |
| --------- | --------------------------- |
| Windows   | `.venv\Scripts\activate `   |

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create superuser 

```bash
python manage.py createsuperuser
```

### 7. Run development server

```bash
python manage.py runserver
```