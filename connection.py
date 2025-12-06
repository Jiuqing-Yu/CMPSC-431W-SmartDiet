import pymysql
from meal_calculation import *
from pymysql.cursors import DictCursor
from datetime import date
def food_exist_in_food_table(connection,f_name):
    cursor = connection.cursor()
    sql = "SELECT f_name FROM Food Where f_name = %s;"
    cursor.execute(sql, (f_name,))
    result = cursor.fetchall()
    cursor.close()
    if result:
        return True
    else:
        return False

def food_exist_in_client_avoid_table(connection,userid,f_name):
    cursor = connection.cursor()
    sql = "SELECT f_name FROM Client_Avoids Where f_name = %s AND user_id = %s;"
    cursor.execute(sql, (f_name,userid))
    result = cursor.fetchall()
    cursor.close()
    if result:
        return True
    else:
        return False
def add_food_into_avoid_table(connection,userid,f_name,reason):
    cursor = connection.cursor()
    sql = """
        INSERT INTO Client_Avoids (user_id, f_name,reason)
        VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (userid,f_name,reason))
    cursor.close()
    connection.commit()
def remove_food_into_avoid_table(connection,userid,f_name):
    cursor = connection.cursor()
    sql = """
        DELETE FROM Client_Avoids
        WHERE user_id = %s AND f_name = %s;
    """
    cursor.execute(sql, (userid,f_name))
    cursor.close()
    connection.commit()

def get_food_recommended_number(connection,userid,f_name):
    sql = """
        SELECT COUNT(*) AS recommend_count
        FROM Client_Recommend cr
        JOIN Meal_Food mf 
            ON mf.meal_id IN (cr.breakfast_id, cr.lunch_id, cr.dinner_id)
        WHERE cr.user_id = %s
          AND mf.f_name = %s;
    """
    cursor = connection.cursor()

    cursor.execute(sql, (userid, f_name))
    result = cursor.fetchone()
    cursor.close()
    return result["recommend_count"] if result else 0
def get_food_recommend_dates(connection, user_id, f_name):
    cursor = connection.cursor()
    sql = """
        SELECT DISTINCT cr.rdate
        FROM Client_Recommend cr
        JOIN Meal_Food mf 
          ON mf.meal_id IN (cr.breakfast_id, cr.lunch_id, cr.dinner_id)
        WHERE cr.user_id = %s
          AND mf.f_name = %s
        ORDER BY cr.rdate
    """
    cursor.execute(sql, (user_id, f_name))
    results = cursor.fetchall()
    cursor.close()

    return [row['rdate'] for row in results]
        
def get_client_meal_level(connection,userid):
    cursor = connection.cursor()
    sql = """
        SELECT mh.meal_level
        FROM Meal_Habit mh
        JOIN Client c ON c.meal_habit_id = mh.meal_habit_id
        WHERE c.user_id = %s;
    """
    cursor.execute(sql, (userid,))
    result = cursor.fetchall()
    cursor.close()
    return result[0]['meal_level']



def get_food_nutrient(connection,f_name=None):
    cursor = connection.cursor()
    if f_name:
        sql = """
            SELECT n.f_name,
                   SUM(CASE WHEN n.nutri_type = 'Calcium' THEN n.nutri_value_g ELSE 0 END) AS Calcium,
                   SUM(CASE WHEN n.nutri_type = 'Carbohydrates' THEN n.nutri_value_g ELSE 0 END) AS Carbohydrates,
                   SUM(CASE WHEN n.nutri_type = 'Fat' THEN n.nutri_value_g ELSE 0 END) AS Fat,
                   SUM(CASE WHEN n.nutri_type = 'Fiber' THEN n.nutri_value_g ELSE 0 END) AS Fiber,
                   SUM(CASE WHEN n.nutri_type = 'Iron' THEN n.nutri_value_g ELSE 0 END) AS Iron,
                   SUM(CASE WHEN n.nutri_type = 'Protein' THEN n.nutri_value_g ELSE 0 END) AS Protein,
                   SUM(CASE WHEN n.nutri_type = 'Sugar' THEN n.nutri_value_g ELSE 0 END) AS Sugar,
                   SUM(CASE WHEN n.nutri_type = 'Vitamin A' THEN n.nutri_value_g ELSE 0 END) AS `Vitamin A`,
                   SUM(CASE WHEN n.nutri_type = 'Vitamin C' THEN n.nutri_value_g ELSE 0 END) AS `Vitamin C`
            FROM Nutrition n
            WHERE f_name = %s
            GROUP BY n.f_name;
            """
        cursor.execute(sql,(f_name,))
        result = cursor.fetchall()[0]
    else:
        sql = sql = """
            SELECT n.f_name,
                   SUM(CASE WHEN n.nutri_type = 'Calcium' THEN n.nutri_value_g ELSE 0 END) AS Calcium,
                   SUM(CASE WHEN n.nutri_type = 'Carbohydrates' THEN n.nutri_value_g ELSE 0 END) AS Carbohydrates,
                   SUM(CASE WHEN n.nutri_type = 'Fat' THEN n.nutri_value_g ELSE 0 END) AS Fat,
                   SUM(CASE WHEN n.nutri_type = 'Fiber' THEN n.nutri_value_g ELSE 0 END) AS Fiber,
                   SUM(CASE WHEN n.nutri_type = 'Iron' THEN n.nutri_value_g ELSE 0 END) AS Iron,
                   SUM(CASE WHEN n.nutri_type = 'Protein' THEN n.nutri_value_g ELSE 0 END) AS Protein,
                   SUM(CASE WHEN n.nutri_type = 'Sugar' THEN n.nutri_value_g ELSE 0 END) AS Sugar,
                   SUM(CASE WHEN n.nutri_type = 'Vitamin A' THEN n.nutri_value_g ELSE 0 END) AS `Vitamin A`,
                   SUM(CASE WHEN n.nutri_type = 'Vitamin C' THEN n.nutri_value_g ELSE 0 END) AS `Vitamin C`
            FROM Nutrition n
            GROUP BY n.f_name;
            """
        cursor.execute(sql)
        result = cursor.fetchall()
    cursor.close()
    return result
def get_all_avoided_food(connection,userid):
    cursor = connection.cursor()
    sql = "SELECT f_name FROM Client_Avoids Where user_id = %s;"
    cursor.execute(sql,(userid,))
    result = cursor.fetchall()
    
    food_names = ', '.join(row['f_name'] for row in result)
    cursor.close()
    return food_names
def get_all_food(connection):
    cursor = connection.cursor()
    sql = "SELECT f_name FROM Food;"
    cursor.execute(sql)
    result = cursor.fetchall()
    
    food_names = ', '.join(row['f_name'] for row in result)
    cursor.close()
    return food_names
def get_meal_text(connection,meal_id):
    cursor = connection.cursor()

    cursor.execute("SELECT meal_type FROM Meal WHERE meal_id = %s", (meal_id,))
    meal = cursor.fetchone()
    
    meal_type = meal['meal_type']
    sql = """
    SELECT mf.quantity, f.serve_size, f.serve_size_unit, f.f_name
    FROM Meal_Food mf
    JOIN Food f ON mf.f_name = f.f_name
    WHERE mf.meal_id = %s;
    """
    cursor.execute(sql, (meal_id,))
    foods = cursor.fetchall()
    food_texts = [f"{row['quantity']*row['serve_size']} {row['serve_size_unit']} {row['f_name']}" for row in foods]
    full_text = f"{meal_type}: {', '.join(food_texts)}"
    
    
    return full_text
def get_recommend_meals_text(connection, recommend_id):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT breakfast_id, lunch_id, dinner_id
        FROM Client_Recommend
        WHERE recommend_id = %s
    """, (recommend_id,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        return None 
    meals_text = []
    for meal_name in ['breakfast', 'lunch', 'dinner']:
        meal_id = row[f"{meal_name}_id"]
        if meal_id:
            meal_text = get_meal_text(connection, meal_id)
            meals_text.append(meal_text)
    return "\n".join(meals_text)


        

def test_userid(connection,user_id):
    cursor = connection.cursor()
    sql = "SELECT 1 FROM Client WHERE user_id = %s LIMIT 1;"
    cursor.execute(sql, (user_id,))
    result =cursor.fetchone()
    cursor.close()
    if result:
        return True
    else:
        return False
def user_exist(connection, user_id):
    cursor = connection.cursor()
    sql_check_user = """
        SELECT user_id
        FROM Client
        WHERE user_id = %s
    """
    cursor.execute(sql_check_user, (user_id))
    result =cursor.fetchone()
    cursor.close()
    if result:
        return True
def user_pw_correct(connection,user_id,pw):
    cursor = connection.cursor()
    sql = """
        SELECT user_id
        FROM Client
        WHERE user_id = %s AND pw = %s
    """
    print(pw)
    cursor.execute(sql, (user_id, pw))
    result =cursor.fetchone()
    cursor.close()
    if result:
        return True
    
def insert_client(connection, user_id, pw, gender, age, weight_lbs, height_fts,vegan):
    cursor = connection.cursor()
    sql = """
        Select meal_habit_id
        From Meal_Habit 
        Where meal_level = %s AND vegan = %s
    """
    cursor.execute(sql,(generate_meal_level(gender, age, weight_lbs, height_fts),vegan))
    print((generate_meal_level(gender, age, weight_lbs, height_fts),vegan))
    result = cursor.fetchone()
    if result:
        meal_habit_id = result['meal_habit_id']
    else:
        cursor.close()
        raise ValueError("No matching meal habit found for the given inputs.")
    sql = """
        INSERT INTO Client (user_id, pw, gender, age, weight_lbs, height_fts,meal_habit_id)
        VALUES (%s, %s, %s, %s, %s, %s,%s)
    """
    cursor.execute(sql, (user_id, pw, gender, age, weight_lbs, height_fts,meal_habit_id))
    connection.commit()
    cursor.close()
def client_recommended_today(connection, user_id):
    rdate = date.today()

    cursor = connection.cursor()
    cursor.execute(
        "SELECT 1 FROM client_recommend WHERE user_id = %s AND rdate = %s",
        (user_id,rdate)
    )
    exists = cursor.fetchone() is not None
    cursor.close()
    return exists


def insert_client_recommend_meal(connection,recommend_id , user_id, breakfast_id,lunch_id,dinner_id,rdate):
    """Insert a new recommended meal if it does not already exist."""
    
    

    cursor = connection.cursor()
    sql = """
        INSERT INTO Client_Recommend 
        (recommend_id, user_id, breakfast_id, lunch_id, dinner_id, rdate)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (recommend_id, user_id, breakfast_id, lunch_id, dinner_id, rdate))
    connection.commit()
    cursor.close()
    return recommend_id
def update_recommended_meal(connection,  recommend_id, breakfast_id,lunch_id,dinner_id):
    rdate = date.today()
    
    cursor = connection.cursor()
    sql = """
        UPDATE Client_Recommend
        SET breakfast_id = %s,
            lunch_id = %s,
            dinner_id = %s
        WHERE recommend_id = %s
    """
    cursor.execute(sql, ( breakfast_id, lunch_id, dinner_id,recommend_id))
    connection.commit()
    cursor.close()

def insert_meal(connection, meal_foods,meal_type):
    meal_id = generate_meal_id(meal_foods,meal_type)
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM Meal WHERE meal_id = %s", (meal_id,))
    exists = cursor.fetchone() is not None
    
    if not exists:
        sql = """
            INSERT INTO Meal (meal_id,meal_type)
            VALUES (%s, %s)
        """
        cursor.execute(sql, (meal_id,meal_type))
        for f_name, quantity in meal_foods.items():
            sql = """
                INSERT INTO Meal_Food (meal_id,f_name,quantity)
                VALUES (%s, %s,%s)
            """
            cursor.execute(sql, (meal_id,f_name,quantity))
        connection.commit()
    cursor.close()
    return meal_id

def init_tables():
    with open("localhost_password.txt", "r") as file:
        pw = file.read()
        
    connection = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password=pw,     
        port=3306,
        charset='utf8mb4',
        local_infile=True,
        cursorclass=pymysql.cursors.DictCursor
    )
    

    db_name = "Meal_Recommendation"
    cursor = connection.cursor()
    cursor.execute("SET GLOBAL local_infile = 1;")
    cursor.execute("SHOW DATABASES LIKE %s", (db_name,))
    if cursor.fetchone():
        return
    cursor.execute(f"CREATE DATABASE `{db_name}`")
    cursor.execute(f"USE `{db_name}`")

    cursor.execute("""
    CREATE TABLE Meal_Habit (
        meal_habit_id VARCHAR(20) PRIMARY KEY,
        meal_level VARCHAR(20),
        vegan BOOLEAN
    );
    """)

    cursor.execute("""
    CREATE TABLE Client (
        user_id VARCHAR(20) PRIMARY KEY,
        pw VARCHAR(64),
        gender VARCHAR(20),
        age INT,
        weight_lbs FLOAT, 
        height_fts FLOAT,
        meal_habit_id VARCHAR(20),
        FOREIGN KEY (meal_habit_id) REFERENCES Meal_Habit(meal_habit_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE Food (
        f_name VARCHAR(20) PRIMARY KEY,
        category VARCHAR(20),
        serve_size Float,
        serve_size_unit VARCHAR(20),
        calorie_per_serve INT
    );
    """)

    cursor.execute("""
    CREATE TABLE Nutrition (
        nutri_type VARCHAR(20),
        f_name VARCHAR(20),
        nutri_value_g FLOAT,
        PRIMARY KEY (nutri_type, f_name),
        FOREIGN KEY (f_name) REFERENCES Food(f_name)
    );
    """)

    cursor.execute("""
    CREATE TABLE Client_Avoids (
        user_id VARCHAR(20),
        f_name VARCHAR(20),
        reason VARCHAR(20),
        PRIMARY KEY (user_id, f_name),
        FOREIGN KEY (user_id) REFERENCES Client(user_id),
        FOREIGN KEY (f_name) REFERENCES Food(f_name)
    );
    """)

    cursor.execute("""
    CREATE TABLE Meal (
        meal_id VARCHAR(100) PRIMARY KEY,
        meal_type VARCHAR(20)
    );
    """)

    cursor.execute("""
    CREATE TABLE Meal_Food (
        meal_id VARCHAR(100),
        f_name VARCHAR(50),
        quantity INT,
        PRIMARY KEY (meal_id, f_name),
        FOREIGN KEY (meal_id) REFERENCES Meal(meal_id),
        FOREIGN KEY (f_name) REFERENCES Food(f_name)
    );
    """)

    cursor.execute("""
        CREATE TABLE Client_Recommend (
        recommend_id VARCHAR(150),
        user_id VARCHAR(20),
        breakfast_id VARCHAR(100),
        lunch_id VARCHAR(100),
        dinner_id VARCHAR(100),
        rdate DATE,
        PRIMARY KEY (recommend_id),
        FOREIGN KEY (user_id) REFERENCES Client(user_id),
        FOREIGN KEY (breakfast_id) REFERENCES Meal(meal_id),
        FOREIGN KEY (lunch_id) REFERENCES Meal(meal_id),
        FOREIGN KEY (dinner_id) REFERENCES Meal(meal_id)
    );

    """)

    
    #load csv into Food
    sql = """
    LOAD DATA LOCAL INFILE %s
    INTO TABLE Food
    FIELDS TERMINATED BY ','
    IGNORE 1 ROWS;
    """

    cursor.execute(sql, ('./food.csv',))
    #load csv into Nutrient
    sql = """
    LOAD DATA LOCAL INFILE %s
    INTO TABLE Nutrition
    FIELDS TERMINATED BY ','
    IGNORE 1 ROWS;
    """

    cursor.execute(sql, ('./nutrition.csv',))
    #load csv into Meal Habit
    sql = """
    LOAD DATA LOCAL INFILE %s
    INTO TABLE Meal_Habit
    FIELDS TERMINATED BY ','
    IGNORE 1 ROWS;
    """

    cursor.execute(sql, ('./meal_habit.csv',))
    #index
    cursor.execute("CREATE INDEX idx_nutri_f_name ON Nutrition(f_name);")

    connection.commit()
    cursor.close()
    connection.close()
def get_connection():
    with open("localhost_password.txt", "r") as file:
        pw = file.read()
        
    try:
        connection = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password=pw,     
            port=3306,
            charset='utf8mb4',
            local_infile=True,
            database= "Meal_Recommendation",
            cursorclass=pymysql.cursors.DictCursor
        )
        print("✅ Connected to local database successfully.")
        return connection

    except pymysql.MySQLError as e:
        print(f"❌ Local database connection failed: {e}")
        return None
