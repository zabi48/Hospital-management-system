MENU_ACTIONS = {
    "vp": "view_patients",
    "ap": "add_patient",
    "ad": "add_diagnosis",
    "dp": "delete_patient",
    "cu": "create_user",
    "vs": "view_staff",
    "up": "view_unattended_patients",
    "md": "mark_for_discharge",
    "disp": "discharge_patient",
    "logout": "logout"
}

PERMISSIONS = {
    "admin": {
        "view_patients",
        "delete_patient",
        "create_user",
        "view_staff",
        "logout"
    },
    "doctor": {
        "view_patients",
        "add_diagnosis",
        "view_unattended_patients",
        "mark_for_discharge",
        "logout"
    },
    "receptionist": {
        "view_patients",
        "add_patient",
        "discharge_patient",
        "logout"
    }
}


def load_users():
    users = []

    with open("users.csv", "r") as file:
        for line in file:
            line = line.strip()
            username, pin, role = line.split(",")
            
            user = {
                "username": username,
                "pin": pin,
                "role": role
            }

            users.append(user)

    return users

def load_patients():
    patients = []

    with open("patients.csv", "r") as file:
        for line in file:
            line = line.strip()
            patient_id, name, age, gender, diagnosis, doctor, prescription, status, marked_for_discharge, discharged = line.split(",")
            patient = {
                "patient_id": patient_id,
                "name": name,
                "age": age,
                "gender": gender,
                "diagnosis": diagnosis,
                "doctor": doctor,
                "prescription": prescription,
                "status": status,
                "marked_for_discharge": marked_for_discharge,
                "discharged": discharged
            }

            patients.append(patient)

    return patients

def login(users):
    username = input("Enter username: ")
    pin = input("Enter PIN: ")

    for user in users:
        if user["username"] == username and user["pin"] == pin:
            print(f"Logged in as: {user['username']} ({user['role']})")
            print(f"Welcome, {username}!")
            return user

    return None

def show_menu(role):
    for choice, action in MENU_ACTIONS.items():
        if action in PERMISSIONS[role]:
            print(f"[{choice}] --> {action.replace('_', ' ').title()}")

def is_allowed(role, choices):
    for choice, action in MENU_ACTIONS.items():
        if choices == choice:
            action_name = action
        allowed_actions = PERMISSIONS.get(role, set())

    if action_name in allowed_actions:
        return True
    else:
        return False

def get_user_choice():
    choice = input("Enter your choice: ")
    if choice not in MENU_ACTIONS:
        print("Invalid choice. Please try again.")
        return None
    return choice

def get_next_patient_id():
    with open("last_id.txt", "r") as f:
        last_id = int(f.read().strip())

    new_id = last_id + 1

    with open("last_id.txt", "w") as f:
        f.write(str(new_id))

    return new_id

def save_patients(patients):
    with open("patients.csv", "w") as f:
        for p in patients:
            line = f"{p['patient_id']},{p['name']},{p['age']},{p['gender']},{p['diagnosis']},{p['doctor']},{p['prescription']},{p['status']},{p['marked_for_discharge']},{p['discharged']}\n"
            f.write(line)

def save_users(users):
    with open("users.csv", "w") as f:
        for u in users:
            line = f"{u['username']},{u['pin']},{u['role']}\n"
            f.write(line)

def view_patient(patients):
    print("Patient List:")
    print(f"{'ID':<6}{'Name':<12}{'Age':<11}{'Gender':<12}{'diagnosis':<16}{'Doctor':<12}")
    print("-" * 70)
    for p in patients:
        print(
        f"{p['patient_id']:<6}"
        f"{p['name']:<12}"
        f"{p['age']:<11}"
        f"{p['gender']:<12}"
        f"{p['diagnosis']:<16}"
        f"{p['doctor']:<12}"
    )

def add_patient(patients):
    patient_id = str(get_next_patient_id())
    name = input("Enter patient name: ")
    age = input("Enter patient age: ")
    gender = input("Enter patient gender: ")
    diagnosis = "diagnosis"
    doctor = "doctor" 
    prescription = "prescription"
    status = "admitted"
    mark_for_discharge = "False"
    discharged = "False"

    new_patient = {
        "patient_id": patient_id,
        "name": name,
        "age": age,
        "gender": gender,
        "diagnosis": diagnosis,
        "doctor": doctor,
        "prescription": prescription,
        "status": status,
        "marked_for_discharge": mark_for_discharge,
        "discharged": discharged
    }

    patients.append(new_patient)
    save_patients(patients)

def get_unattended_patients(patients):
    unattended = []
    for p in patients:
        if p["doctor"] == "pending" and p["diagnosis"] == "pending":
            unattended.append(p)
    print("Unattended Patients:")
    for patient in unattended:
        print(f"Patient ID: {patient['patient_id']}")
        print(f"Name: {patient['name']}")
        print(f"Age: {patient['age']}")
        print(f"Gender: {patient['gender']}")
        print(f"diagnosis: {patient['diagnosis']}")
        print(f"Doctor: {patient['doctor']}")
        print()
    return unattended    

def logout():
    print("Logging out...")
    
def add_diagnosis(patients):
    patient_id = input("Enter patient ID to add diagnosis: ")
    for p in patients:
        if p["patient_id"] == patient_id:
            print(f"Current diagnosis: {p['diagnosis']}")
            diagnosis = input("Enter new diagnosis: ")
            p["diagnosis"] = diagnosis
            p["doctor"] = current_user["username"]
            save_patients(patients)
            print("Diagnosis updated.")
            return

def delete_patient(patients):
    patient_id = input("Enter patient ID to delete: ")
    for p in patients:
        if p["patient_id"] == patient_id:
            confirm = input(f"Are you sure you want to delete patient {p['name']}? (y/n): ")
            if confirm.lower() != 'y':
                print("Deletion cancelled.")
                return
            
            patients.remove(p)
            save_patients(patients)
            print("Patient deleted.")
            return
            
    print("Patient not found.")

def create_user(users):
    username = input("Enter new username: ")
    pin = input("Enter new PIN: ")
    role = input("Enter role (doctor/receptionist): ")

    if role == "admin":
        print("Creating an admin is not allowed")
        return
    
    confirm = input(f"Are you sure you want to create an {role} user? (y/n): ")
    if confirm.lower() != 'y':
        print("User creation cancelled.")
        return    
        
    new_user = {
        "username": username,
        "pin": pin,
        "role": role
    }

    users.append(new_user)

    save_users(users)

    print("User created successfully.")

def view_staff(users):
    print("Staff Members:")
    print(f"{'Username':<15}{'Role':<15}")
    print("-" * 30)
    for u in users:
        print(f"{u['username']:<15}"
              f"{u['role']:<15}")

def delete_user(users):
    username = input("Enter username to delete: ")
    for u in users:
        if u["username"] == username:
            if u["role"] == "admin":
                print("Cannot delete admin user.")
                return
            confirm = input(f"Are you sure you want to delete user {username}? (y/n): ")
            if confirm.lower() != 'y':
                print("Deletion cancelled.")
                return
            
            users.remove(u)
            save_users(users)
            print("User deleted.")
            return
            
    print("User not found.")

def mark_for_discharge(patients):
    patient_id = input("Enter patient ID to mark for discharge: ")
    for p in patients:
        if p["patient_id"] == patient_id:
            p["ready_for_discharge"] = "True"
            save_patients(patients)
            print("Patient marked for discharge.")
            return
    print("Patient not found.")

def discharge_patient(patients):
    patient_id = input("Enter patient ID to discharge: ")
    for patient in patients:
        if patient["patient_id"] == patient_id:
            if patient["marked_for_discharge"] != "True":
                print("Patient is not marked for discharge.")
                return
            patient["discharged"] = "True"
            patient["status"] = "discharged"
            save_patients(patients)
            print("Patient discharged.")
            return
    print("Patient not found.")

print("="*75)
print(" HOSPITAL MANAGEMENT SYSTEM ".center(50))
print("="*75)

users = load_users()
patients = load_patients()
current_user = login(users)
if current_user is None:
    print("Login failed. Exiting program.")
    exit()

role = current_user["role"]

show_menu(role)

while True:
    choice = get_user_choice()
    if (choice == None):
        continue
    elif not is_allowed(role, choice):
        print("You do not have permission to perform this action.")
        continue
    elif choice == 'vp':
        view_patient(patients)
    elif choice == 'ap':
        add_patient(patients)
    elif choice == 'ad':
        add_diagnosis(patients)
    elif choice == 'dp':
        delete_patient(patients)
    elif choice == 'cu':
        create_user(users)
    elif choice == 'vs':
        view_staff(users)
    elif choice == 'up':
       get_unattended_patients(patients)
    elif choice == 'md':
        mark_for_discharge(patients)
    elif choice == 'disp':
        discharge_patient(patients)
    elif choice == 'logout':
        logout()
        break
    else:
        print("Invalid choice. Please try again.")

print("Exiting program. Goodbye!")