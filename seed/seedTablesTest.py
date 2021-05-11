# Create database and tables, add initial data
import sqlite3

con = sqlite3.connect('../instance/databaseTest.db')

cur = con.cursor()


def seedTablesTest():
    # You can comment a table if you want to keep the data
    con.execute("DROP TABLE IF EXISTS users")
    con.execute("DROP TABLE IF EXISTS weather")
    con.execute("DROP TABLE IF EXISTS energy_consumption")
    con.execute("DROP TABLE IF EXISTS energy_production")
    con.execute("DROP TABLE IF EXISTS prediction_data")

    createTables()

    con.commit()

    con.close()

    print("Finished seedTablesTest.py")


def createTables():
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                (sign_up_date    TEXT        NOT NULL, 
                username             TEXT        NOT NULL, 
                password         TEXT        NOT NULL, 
                isAdmin          INTEGER)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS weather
                (date        TEXT     NOT NULL,
                temperature  REAL     NOT NULL, 
                cloud        INTEGER  NOT NULL, 
                wind         REAL     NOT NULL, 
                pressure     INTEGER  NOT NULL)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS prediction_data
                (predicted_on    TEXT    NOT NULL,
                predicted_date   REAL    NOT NULL,
                prediction      TEXT    NOT NULL)''')

    # (tables from the old database)
    cur.execute('''CREATE TABLE IF NOT EXISTS grid (
        [No] INTEGER            PRIMARY KEY AUTOINCREMENT,
        Time [UNSIGNED BIG INT],
        V1   REAL,
        V2   REAL,
        V3   REAL,
        I1   REAL,
        I2   REAL,
        I3   REAL,
        P1   REAL,
        P2   REAL,
        P3   REAL,
        Q1   REAL,
        Q2   REAL,
        Q3   REAL,
        S1   REAL,
        S2   REAL,
        S3   REAL,
        PF1  REAL,
        PF2  REAL,
        PF3  REAL,
        F    REAL
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS energy_production  (
        [No] INTEGER,
        Time [UNSIGNED BIG INT],
        V1   REAL,
        V2   REAL,
        V3   REAL,
        I1   REAL,
        I2   REAL,
        I3   REAL,
        P1   REAL,
        P2   REAL,
        P3   REAL,
        Q1   REAL,
        Q2   REAL,
        Q3   REAL,
        S1   REAL,
        S2   REAL,
        S3   REAL,
        PF1  REAL,
        PF2  REAL,
        PF3  REAL,
        F    REAL
    )''')


# Automatically run seedTables if run (not imported)
if __name__ == '__main__':
    seedTablesTest()
