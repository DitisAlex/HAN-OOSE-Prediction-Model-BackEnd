# Backend Web Interface HANW@TTS Prediction model

Flask API

## Install & Run

There are two options to run this backend: on your local machine using Python virtual environment or inside a Docker container. The latter is easier to use.

### Local

1. Make a Python virtual environment  
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
3. Install this project
   ```bash
   $ pip install -r requirements.txt
   ```
4. Start the application:
   ```
   $ python run.py
   ```
   You can access the backend via http://localhost:5000 or http://0.0.0.0:5000.
5. Initialize database:
    ```
    $ flask init-db
    ```

### Docker

1. Install [Docker](https://docs.docker.com/engine/install/) and [Docker compose](https://docs.docker.com/compose/install/)
2. Start the container by running  
    **Linux/Mac**

   ```bash
   $ docker-compose up
   ```

   > If you want to rebuild the container run the above command with `--build` flag.

   **Windows**

   > **TODO: Add instructions**

3. The backend is automatically started after container is build. You can access it via http://localhost:5000 or http://0.0.0.0:5000.

## Project Layout

This project uses a feature based folder structure. This means that all components (`routes`, `controllers`, `daos`) of each feature are in the same folder.

```bash
/path/to/your/project
├── app/
│   ├── __init__.py
│   ├── core
|   |   ├── __init__.py # __init.py__ lets python know this folder is a package.
|   |   └── db.py
|   ├── auth
|   |   ├── __init__.py
|   |   ├── routes.py
|   |   ├── controller.py
|   |   └── dao.py
|   └── feature...
|       ├── __init__.py
|       ├── routes.py
|       ├── controller.py
|       └── dao.py
├── instance/
|   └── database.db
├── tests/
│   ├── conftest.py
│   ├── data.sql
│   ├── test_factory.py
│   ├── test_db.py
│   └── test_auth.py
├── venv/
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── readme.md
├── requirements.txt
└── run.py
```

- `app/`: Python package containing the appliciation. Similar to the `src/` folder in Java projects.
- `instance/`: a directory containing instance related files like environment secrets and database files.
- `tests/`: a directory containing test modules.
- `venv/`: a Python virtual environment where Flask and other dependencies are installed.
- `run.py`: Entrypoint to the application.
- `requirements.txt`: file containing list Python dependencies for this project.
- `.git` and `.gitignore`: git related files.
- `Dockerfile` and `docker-compose.yml`: docker related files.

## Endpoints

### Energy

#### **Production**

- `/energy/production/fetch`: fetches new energy production data from the Raspberry Pi and inserts it in the local database.

#### **Consumption**

- `/energy/consumption/fetch`: fetches new energy consumption data from the Raspberry Pi and inserts it in the local database.

### **Weather**

- `/weather/fetch` [GET]: inserts new weather data into the database 

#### **Prediction**

- `/prediction?hours=?` [GET]: (dummy data for now) generates predictions, with an amount equal to the `hours` query parameter. Has to to between 1 and 4.

### **Authentication**

> **TODO**

- `/auth/login`:
- `/auth/logout`:


## CLI commands

This application also contains several CLI commands for setup and testing purposes. These command can be executed after the Python virtual environment has been activated or inside the running Docker container.

#### **Initialize database**

When you start this application for the first time a database has to be initialized first. This can be done after starting this application:

```
$ flask init-db
Initialized the database.
```

#### **Manually inserting test data**

```
$ flask insert-test-data
Inserted test data.
```

#### **Show contents of a table**

```
$ flask show-table [table name]
```

**example:**

```
$ flask show-table energy_production
        no        time     V1     V2     V3   I1   I2   I3   P1   P2   P3   Q1   Q2   Q3   S1   S2   S3  PF1  PF2  PF3      F
0        1  1617589961  234.5  234.2  234.5  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  1.0  1.0  50.00
1        2  1617590041  234.3  233.9  234.3  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  1.0  1.0  50.00
2        3  1617590152  234.5  234.1  234.5  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  1.0  1.0  50.00
3        4  1617590248  234.6  234.1  234.5  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  1.0  1.0  50.03
4        5  1617590361  234.5  234.1  234.7  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  1.0  1.0  50.00
...    ...         ...    ...    ...    ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...    ...
6143  6144  1618257422  234.6  233.8  233.7  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  1.0  1.0  50.05
6144  6145  1618257508  234.8  234.1  234.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  1.0  1.0  50.04
6145  6146  1618257564  235.0  234.3  234.3  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  1.0  1.0  50.00
6146  6147  1618257661  232.0  231.2  231.3  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  1.0  1.0  49.93
6147  6148  1618257768  232.0  231.1  231.2  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  1.0  1.0  49.94

[6148 rows x 21 columns]
```

## Unit testing
this project uses two Python packages to perform unit tests: pytest and coverage. To run the test use the following command:
```Bash
$ pytest

==================== test session starts ====================
platform linux -- Python 3.8.5, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /../backend-hanwatts-prediction-model-web-interface, configfile: setup.cfg, testpaths: tests
collected 4 items                                           

tests/test_db.py ..                                   [ 50%]
tests/test_factory.py ..                              [100%]

===================== 4 passed in 1.40s =====================
```
> Run the above command with the `-v` flag to get a list fo eacht test function.

### Measuring code coverage 
To measure the code coverage of the test use the following command instead  just `pytest`:
```Bash
coverage run -m pytest
```

To view the coverage report in the terminal:
```bash
$ coverage report

Name                        Stmts   Miss Branch BrPart  Cover
-------------------------------------------------------------
app/__init__.py                24      0      2      0   100%
app/core/db.py                 58     16      8      1    71%
-------------------------------------------------------------
TOTAL                         247    108     22      1    54%
```

To generate a HTML report of this report run the following command:
```Bash
$ coverage html
```
The report can be found in `htmlcov/index.html`.

<br><br>

# Flask Cheatsheet

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
