import mysql.connector
from hashlib import sha256

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Prateek@2006",
    database="FITNESSAPP" # DATABASE PEHLE HEE CREATE KAR LENA
)

cursor = db.cursor()

def create_tables():
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(64), height FLOAT, weight FLOAT, age INT, activity_level INT, goal VARCHAR(50))")
    cursor.execute("CREATE TABLE IF NOT EXISTS daily_stats (user_id INT, calories_consumed INT, calories_burnt INT, water_consumed INT, FOREIGN KEY(user_id) REFERENCES users(id))")
    db.commit()

#user registration
def register_user():
    username = input("Enter your username: ")
    password = sha256(input("Enter your password: ").encode()).hexdigest()

    # check if the user already exists
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        print("Account already exists. Please log in.")
        return None

    height = float(input("Enter your height in meters: "))
    weight = float(input("Enter your weight in kg: "))
    age = int(input("Enter your age: "))
    activity_level = int(input("Enter your activity level (1: No Activity, 2: Barely Active, 3: Pretty Active, 4: Fitness Freak): "))
    goal = input("Enter your goal (Gain Mass, Gain Muscle, Lose Weight, Stay in shape): ")

    # confirm details
    print("Details Entered:")
    print(f"Username: {username}")
    print(f"Height: {height} m, Weight: {weight} kg, Age: {age}, Activity Level: {activity_level}, Goal: {goal}")

    confirm = input("Do you want to save these details? (y/n): ")

    if confirm.lower() == 'y':
        cursor.execute("INSERT INTO users (username, password, height, weight, age, activity_level, goal) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (username, password, height, weight, age, activity_level, goal))
        db.commit()
        return cursor.lastrowid  # Return the user ID
    else:
        print("Details not saved.")
        return None

# user login
def login_user(username, password):
    username = input("Enter your username: ")
    password = sha256(input("Enter your password: ").encode()).hexdigest()

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    if user:
        return user
    else:
        print("Incorrect details. Please try again.")
        return None

# display user details
def display_user_details(user_id):
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    if user:
        print("\nUser Details:")
        print(f"Name: {user[1]}")
        print(f"Height: {user[3]} m")
        print(f"Weight: {user[4]} kg")
        
        # BMI
        bmi = user[4] / (user[3] ** 2)
        print(f"BMI: {bmi:.2f}")

        current_level = calculate_current_level(user[5], user[4], user[3])
        desired_weight = calculate_desired_weight(user[4], user[3], user[7])

        print(f"Current Level: {current_level}")
        print(f"Desired Weight: {desired_weight} kg")
    else:
        print("User not found.")
# activity level ka kuch jugaad
def calculate_current_level(activity_level, weight, height):
    pass
    #return f"Level {activity_level}"

# desired weight ka jugaad
def calculate_desired_weight(weight, height, goal):
    pass

# LOGIN PAGE IS OVER HERE

# ISKE AAGE HOMESCREEN HAI###

# edit user details
def edit_user_details(user_id):
    print("Edit User Details:")
    print("1. Edit Name\n2. Edit Weight\n3. Edit Height\n4. Edit Age\n5. Edit Password\n6. Edit Goal")

    choice = input("Enter your choice: ")

    if choice == "1":
        new_name = input("Enter new name: ")
        cursor.execute("UPDATE users SET username = %s WHERE id = %s", (new_name, user_id))
    elif choice == "2":
        new_weight = float(input("Enter new weight in kg: "))
        cursor.execute("UPDATE users SET weight = %s WHERE id = %s", (new_weight, user_id))
    elif choice == "3":
        new_height = float(input("Enter new height in meters: "))
        cursor.execute("UPDATE users SET height = %s WHERE id = %s", (new_height, user_id))
    elif choice == "4":
        new_age = int(input("Enter new age: "))
        cursor.execute("UPDATE users SET age = %s WHERE id = %s", (new_age, user_id))
    elif choice == "5":
        new_password = sha256(input("Enter new password: ").encode()).hexdigest()
        cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_password, user_id))
    elif choice == "6":
        new_goal = input("Enter new goal: ")
        cursor.execute("UPDATE users SET goal = %s WHERE id = %s", (new_goal, user_id))
    else:
        print("Invalid choice. No changes made.")

    db.commit()
    print("User details updated successfully.")

# add more water
def add_water(user_id):
    pass

# add calories eaten
def add_calories(user_id):
    pass

# start workout
def start_workout(user_id):
    pass

def main():
    create_tables()
    user = None

    choice = input("1. Login\n2. Sign Up\nEnter your choice: ")

    if choice == "1":
        username = input("Enter your username: ")
        password = sha256(input("Enter your password: ").encode()).hexdigest()
        user = login_user(username, password)

    elif choice == "2":
        user_id = register_user()
        if user_id:
            user = display_user_details(user_id)

    while user:
        print("\nHome Screen:")
        display_user_details(user[1])  # Pass username for displaying details
        print("1. Edit User Details\n2. Add More Glass of Water\n3. Add Calories Eaten\n4. Start Workout\n5. Exit")

        option = input("Enter your choice: ")

        if option == "1":
            edit_user_details(user[0])  # Pass user_id for editing
        elif option == "2":
            add_water(user[0])  # Pass user_id for adding water
        elif option == "3":
            add_calories(user[0])  # Pass user_id for adding calories
        elif option == "4":
            start_workout(user[0])  # Pass user_id for starting workout
        elif option == "5":
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
