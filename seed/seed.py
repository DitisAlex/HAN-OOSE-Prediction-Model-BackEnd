# Create database and tables, add initial data
import sqlite3

con = sqlite3.connect('../instance/database.db')

cur = con.cursor()


def seed():
    # You can comment a table if you want to keep the data
    con.execute("DROP TABLE IF EXISTS users")
    con.execute("DROP TABLE IF EXISTS weather")
    con.execute("DROP TABLE IF EXISTS energy_consumption")
    con.execute("DROP TABLE IF EXISTS energy_production")
    con.execute("DROP TABLE IF EXISTS prediction_data")

    createTables()

    # You can comment a table if you don't
    # want to add data into it
    insertUsers()
    insertWeather()
    insertEnergyConsumption()
    insertEnergyProduction()
    insertPredictions()

    con.commit()

    con.close()

    print("Finished seed.py")


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
    cur.execute('''CREATE TABLE IF NOT EXISTS energy_consumption  (
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


def insertUsers():
    cur.execute(
        "INSERT INTO users VALUES (datetime('now'), 'rowan','password',1)")


def insertWeather():
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-20 09:45:14', 10.38, 36, 4.73, 1023)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-20 10:45:14', 9.62, 32, 4.16, 1023)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-20 11:45:14', 8.31, 27, 3.45, 1023)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-20 12:45:14', 6.68, 22, 3.05, 1024)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-20 13:45:14', 4.92, 17, 2.7, 1024)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-20 14:45:14', 3.32, 12, 2.45, 1024)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-20 15:45:14', 3.3, 13, 2.22, 1023)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-20 16:45:14', 3.87, 57, 2.37, 1023)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-20 17:45:14', 4.76, 74, 2.29, 1023)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-20 18:45:14', 5.17, 83, 2.4, 1022)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-20 19:45:14', 5.34, 87, 2.16, 1022)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-20 20:45:14', 5.5, 90, 1.95, 1023)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-20 21:45:14', 5.91, 91, 2.16, 1023)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-20 22:45:14', 6.73, 100, 1.95, 1023)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-20 23:45:14', 8.15, 100, 1.79, 1023)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-21 0:45:14', 9.94, 100, 1.88, 1023)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-21 1:45:14', 12.36, 98, 2.2, 1022)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-21 2:45:14', 12.69, 96, 2.53, 1022)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-21 3:45:14', 12.69, 96, 2.53, 1022)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-21 4:45:14', 12.42, 97, 2.96, 1022)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-21 5:45:14', 13.59, 82, 2.87, 1022)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-21 6:45:14', 13.64, 89, 3.26, 1021)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-21 7:45:14', 13.71, 82, 3.55, 1021)")
    cur.execute(
        "INSERT INTO weather VALUES ('2021-04-21 8:45:14', 13.46, 73, 4.08, 1021)")


def insertEnergyConsumption():
    cur.execute(
        '''INSERT INTO energy_consumption   VALUES (1, 1617589961, 234.5, 234.2, 234.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_consumption   VALUES (2, 1617590041, 234.3, 233.9, 234.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_consumption   VALUES (3, 1617590152, 234.5, 234.1, 234.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_consumption   VALUES (4, 1617590248, 234.6, 234.1, 234.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.03)''')
    cur.execute(
        '''INSERT INTO energy_consumption   VALUES (5, 1617590361, 234.5, 234.1, 234.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_consumption   VALUES (6, 1617590512, 234.7, 234.2, 234.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_consumption   VALUES (7, 1617590625, 234.5, 234.1, 234.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_consumption   VALUES (8, 1617590739, 234.7, 234.2, 234.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_consumption   VALUES (9, 1617590788, 234.5, 234.2, 234.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_consumption   VALUES (10, 1617590917, 234.2, 234.0, 234.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_consumption   VALUES (11, 1617591008, 234.1, 233.8, 234.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.03)''')
    cur.execute(
        '''INSERT INTO energy_consumption   VALUES (12, 1617591103, 234.3, 233.9, 234.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_consumption   VALUES (13, 1617591250, 234.3, 233.9, 234.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_consumption   VALUES (14, 1617591587, 234.8, 234.5, 234.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_consumption   VALUES (15, 1617591682, 234.6, 234.2, 234.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_consumption   VALUES (16, 1617591766, 234.2, 234.2, 234.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_consumption   VALUES (17, 1617591908, 234.2, 233.8, 234.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_consumption   VALUES (18, 1617592126, 234.0, 233.7, 234.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_consumption   VALUES (19, 1617592251, 233.9, 233.6, 234.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_consumption   VALUES (20, 1617592536, 234.0, 233.7, 234.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')


def insertEnergyProduction():
    cur.execute(
        '''INSERT INTO energy_production   VALUES (1, 1617589961, 234.5, 234.2, 234.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_production   VALUES (2, 1617590041, 234.3, 233.9, 234.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_production   VALUES (3, 1617590152, 234.5, 234.1, 234.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_production   VALUES (4, 1617590248, 234.6, 234.1, 234.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.03)''')
    cur.execute(
        '''INSERT INTO energy_production   VALUES (5, 1617590361, 234.5, 234.1, 234.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_production   VALUES (6, 1617590512, 234.7, 234.2, 234.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_production   VALUES (7, 1617590625, 234.5, 234.1, 234.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_production   VALUES (8, 1617590739, 234.7, 234.2, 234.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_production   VALUES (9, 1617590788, 234.5, 234.2, 234.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_production   VALUES (10, 1617590917, 234.2, 234.0, 234.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_production   VALUES (11, 1617591008, 234.1, 233.8, 234.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.03)''')
    cur.execute(
        '''INSERT INTO energy_production   VALUES (12, 1617591103, 234.3, 233.9, 234.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_production   VALUES (13, 1617591250, 234.3, 233.9, 234.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_production   VALUES (14, 1617591587, 234.8, 234.5, 234.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_production   VALUES (15, 1617591682, 234.6, 234.2, 234.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_production   VALUES (16, 1617591766, 234.2, 234.2, 234.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_production   VALUES (17, 1617591908, 234.2, 233.8, 234.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_production   VALUES (18, 1617592126, 234.0, 233.7, 234.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_production   VALUES (19, 1617592251, 233.9, 233.6, 234.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')
    cur.execute(
        '''INSERT INTO energy_production   VALUES (20, 1617592536, 234.0, 233.7, 234.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0)''')


def insertPredictions():
    cur.execute(
        '''INSERT INTO prediction_data VALUES ('2021-04-23 9:00:00', '2021-04-21 8:45:14', 2.9)'''
    )
    cur.execute(
        '''INSERT INTO prediction_data VALUES ('2021-04-23 9:00:00', '2021-04-21 9:45:14', 23.2)'''
    )


# Automatically run seed if run (not imported)
if __name__ == '__main__':
    seed()
