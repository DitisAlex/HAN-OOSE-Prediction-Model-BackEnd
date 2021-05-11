# Flask REST API Onderzoek

Deze readme zal uitleggen hoe je een REST API ontwikkelt met behulp van [Flask](https://flask.palletsprojects.com). Tevens is dit project een opzet voor het "echte" werk, hierop dient voort gebouwd te worden. Alle informatie uit deze readme is terug te vinden in de officiele Flask documentatie:

- https://flask.palletsprojects.com/en/1.1.x/installation/
- https://flask.palletsprojects.com/en/1.1.x/quickstart/
- https://flask.palletsprojects.com/en/1.1.x/tutorial/

## Installatie

1. Maak een virtuele environment
   ```bash
   $ mkdir myproject
   $ cd myproject
   ```
   **Linux/Mac**
   ```bash
   $ python3 -m venv venv
   ```
   **Windows**
   ```bash
   > py -3 -m venv .venv
   ```
2. Activeer het virtuele environment  
   **Linux/Mac**
   ```bash
   $ . venv/bin/activate
   ```
   **Windows**
   ```bash
   > .venv\scripts\activate
   ```
3. Installeer Flask
   ```bash
   $ pip install Flask
   ```

## Project Layout

In dit project is er besloten om het projectstructuur op basis van features in te delen. Dit betekent dat elke feature zijn eigen map heeft met daarin `routes`, `controllers`, etc.. Het project structuur is als volgt:

```bash
/path/to/your/project
├── flaskr/
│   ├── __init__.py
│   ├── db.py
|   ├── auth
|   |   ├── __init__.py # Maakt van een map een Python Package
|   |   ├── routes.py
|   |   ├── controller.py
|   |   └── model.py?
|   └── feature1
|       ├── __init__.py
|       ├── feature1.routes.py
|       ├── feature1.controller.py
|       └── feature1.model.py?
├── instance/
|   └── database.db
├── tests/
│   ├── conftest.py
│   ├── data.sql
│   ├── test_factory.py
│   ├── test_db.py
│   ├── test_auth.py
│   └── test_blog.py
├── venv/
├── setup.py
├── MANIFEST.in
├── .git
└── .gitignore
```

- `flaskr/`: een Python package waarin de applicatie code staat. Vergelijkbaar met het `src/` map in Java projecten.
- `instance/`: een map waarin configuration secrets en het database bestand staan. Deze map mag **niet** gecommit worden naar git.
- `tests/`: een map waarin alle unittests staan.
- `venv/`: een Python virtual environment waarin Flask en andere dependencies geinstalleerd zijn.
- `setup.py` en `MANIFEST.in`: bestanden die Python nodig heeft om dit project op een machine te installeren, [hier](https://flask.palletsprojects.com/en/1.1.x/tutorial/install/)
- `.git` en `.gitignore`: git versiebeheer bestanden.

  ### **.gitignore**

  ```
  venv/

  *.pyc
  __pycache__/

  instance/

  .pytest_cache/
  .coverage
  htmlcov/

  dist/
  build/
  *.egg-info/
  ```

## Flask starten en stoppen

1. Activeer python virtual environment
2. Start Flask  
   **Linux/Mac**
   ```bash
   $ export FLASK_APP=flaskr
   $ export FLASK_ENV=development
   $ flask run
   ```
   **Windows**
   ```bash
   > set FLASK_APP=flaskr
   > set FLASK_ENV=development
   > flask run
   ```

## Code examples

### routes

#### **Simple route**

```py
@app.route('/test', methods=['GET'])
def test():
    return 'test works!'
```

#### **JSON response**

```py
# Flask automatically returns Dictionaries as JSON objects
@app.route("/me")
def me_api():
    user = get_current_user()
    return {
        "username": user.username,
        "theme": user.theme,
        "image": url_for("user_image", filename=user.image),
    }

# You can also use the builtin methods jsonify() and to_json()
@app.route("/users")
def users_api():
    users = get_all_users()
    return jsonify([user.to_json() for user in users])
```

#### **JSON Request**

```py
@app.route('/books', methods=['POST'])
def make_book():
    requestedBook = request.get_json()

    newBook = {
        'id': len(books),
        'title': requestedBook["title"],
        'author': 'You, the user',
        'first_sentence': 'Testbook',
        'year_published': '2021'
    }

    books.append(newBook)

    return jsonify(newBook)
```

#### **Path parameter**

```py
@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(escape(username))
```

#### **Query parameter**: `?key=value`

```py
param = request.args.get('key', '')
```

### Database

```py
from flaskr import db

db  = db.get_db()
query = "SELECT * FROM PV"

df = pd.read_sql_query(query, db)

print(df)
```

> More examples: https://flask.palletsprojects.com/en/1.1.x/quickstart/
