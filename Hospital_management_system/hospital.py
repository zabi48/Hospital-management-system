MENU_ACTIONS = {
    "ap": "add_patient",
    "ad": "add_diagnosis",
    "dp": "delete_patient",
    "as": "add_staff",
    "vs": "view_staff",
    "md": "mark_for_discharge",
    "disp": "discharge_patient",
    "dels": "delete_staff",
    "vpr": "view_patient_record",
    "cp": "change_pin",
    "logout": "logout"
}

PERMISSIONS = {
    "admin": {
        "add_staff",
        "view_staff",
        "delete_staff",
        "view_patient_record",
        "delete_patient",
        "change_pin",
        "logout"
    },
    "doctor": {
        "view_patient_record",
        "add_diagnosis",
        "mark_for_discharge",
        "change_pin",
        "logout"
    },
    "receptionist": {
        "view_patient_record",
        "add_patient",
        "discharge_patient",
        "change_pin",
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
                "username": username.lower(),
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
            patient_id, name, age, gender, diagnosis, doctor, marked_for_discharge, status = line.split(",")
            patient = {
                "patient_id": patient_id,
                "name": name.lower(),
                "age": age,
                "gender": gender.lower(),
                "diagnosis": diagnosis.lower(),
                "doctor": doctor.lower(),
                "marked_for_discharge": marked_for_discharge,
                "status": status.lower()
            }

            patients.append(patient)

    return patients

def login(users):
    username = input("Enter username: ").lower()
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

def apply_filters(patients):
    filtered_list = []
    print("Filter Options:")
    print("[1] View All Patients")
    print("[2] View Admitted Patients")
    print("[3] View Discharged Patients")
    print("[4] View unattended Patients")
    print("[5] View Patients by doctor")
    print("[6] View Patients by diagnosis")
    print("[7] View Patients ready for discharge")
    print("[8] View male patients only")
    print("[9] View female patients only")
    print("[10] View patients by age group")
    filter_choice = input("Select a filter option (1-10): ")
    if filter_choice == '1':
        print("Showing all patients.")
        filtered_list = patients
    elif filter_choice == '2':
        print("Showing admitted patients only.")
        filtered_list = [p for p in patients if p['status'] == 'admitted']
    elif filter_choice == '3':
        print("Showing discharged patients only.")
        filtered_list = [p for p in patients if p['status'] == 'discharged']
    elif filter_choice == '4':
        print("Showing unattended patients only.")
        filtered_list = [p for p in patients if p['doctor'] == 'doctor' and p['diagnosis'] == 'diagnosis']
    elif filter_choice == '5':
        doctor_name = input("Enter doctor's name: ")
        print(f"Showing patients assigned to Dr. {doctor_name}.")
        filtered_list = [p for p in patients if p['doctor'] == doctor_name]
    elif filter_choice == '6':
        diagnosis_name = input("Enter diagnosis: ")
        print(f"Showing patients with diagnosis: {diagnosis_name}.")
        filtered_list = [p for p in patients if p['diagnosis'] == diagnosis_name]
    elif filter_choice == '7':
        print("Showing patients ready for discharge.")
        filtered_list = [p for p in patients if p['marked_for_discharge'] == 'True']
    elif filter_choice == '8':
        print("Showing male patients only.")
        filtered_list = [p for p in patients if p['gender'] == 'm']
    elif filter_choice == '9':
        print("Showing female patients only.")
        filtered_list = [p for p in patients if p['gender'] == 'f']
    elif filter_choice == '10':
        age_group = input("Enter age group (e.g., 20-30): ")
        age_min, age_max = map(int, age_group.split('-'))
        print(f"Showing patients aged between {age_min} and {age_max}.")
        filtered_list = [p for p in patients if age_min <= int(p['age']) <= age_max]
    else:
        print("Invalid filter choice. Showing all patients by default.")
        filtered_list = patients
    return filtered_list

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
    choice = input("Enter your choice: ").lower()
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
            line = f"{p['patient_id']},{p['name']},{p['age']},{p['gender']},{p['diagnosis']},{p['doctor']},{p['marked_for_discharge']},{p['status']}\n"
            f.write(line)

def save_users(users):
    with open("users.csv", "w") as f:
        for u in users:
            line = f"{u['username']},{u['pin']},{u['role']}\n"
            f.write(line)

def view_patient_record(patients):
    if not patients:
        print("No patients found with the applied filters.")
        return
    print("Patient List:")
    print(f"{'ID':<6}{'Name':<12}{'Age':<11}{'Gender':<12}{'diagnosis':<16}{'Doctor':<12}{'Marked for Discharge':<25}{'Status':<12}")
    print("-" * 115)
    for p in patients:
            print(
            f"{p['patient_id']:<6}"
            f"{p['name']:<12}"
            f"{p['age']:<11}"
            f"{p['gender']:<12}"
            f"{p['diagnosis']:<16}"
            f"{p['doctor']:<12}"
            f"{p['marked_for_discharge']:<25}"
            f"{p['status']:<12}"
        )
            
def add_patient(patients):
    patient_id = str(get_next_patient_id())
    name = input("Enter patient name: ").lower()
    age = input("Enter patient age: ")
    gender = input("Enter patient gender: ").lower()
    diagnosis = input("Enter patient diagnosis: ").lower()
    doctor = input("Enter patient doctor: ").lower()
    status = "admitted"
    mark_for_discharge = "False"

    new_patient = {
        "patient_id": patient_id,
        "name": name,
        "age": age,
        "gender": gender,
        "diagnosis": diagnosis,
        "doctor": doctor,
        "marked_for_discharge": mark_for_discharge,
        "status": status        
    }

    patients.append(new_patient)
    save_patients(patients)

def logout():
    print("Logging out...")
    
def add_diagnosis(patients):
    patient_id = input("Enter patient ID to add diagnosis: ")
    for p in patients:
        if p["patient_id"] == patient_id:
            print(f"Current diagnosis: {p['diagnosis']}")
            diagnosis = input("Enter new diagnosis: ").lower()
            p["diagnosis"] = diagnosis
            p["doctor"] = current_user["username"]
            save_patients(patients)
            print("Diagnosis updated.")
            return

def delete_patient(patients):
    patient_id = input("Enter patient ID to delete: ")
    for p in patients:
        if p["patient_id"] == patient_id:
            confirm = input(f"Are you sure you want to delete patient {p['name']}? (y/n): ").lower()
            if confirm.lower() != 'y':
                print("Deletion cancelled.")
                return
            
            patients.remove(p)
            save_patients(patients)
            print("Patient deleted.")
            return
            
    print("Patient not found.")

def create_user(users):
    username = input("Enter new username: ").lower()
    pin = input("Enter new PIN: ")
    role = input("Enter role (doctor/receptionist): ").lower()

    if role == "admin":
        print("Creating an admin is not allowed")
        return
    
    confirm = input(f"Are you sure you want to create an {role} user? (y/n): ").lower()
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
    print("-" * 35)
    for u in users:
        print(f"{u['username']:<15}"
              f"{u['role']:<15}")

def delete_user(users):
    username = input("Enter username to delete: ").lower()
    for u in users:
        if u["username"] == username:
            if u["role"] == "admin":
                print("Cannot delete admin user.")
                return
            confirm = input(f"Are you sure you want to delete user {username}? (y/n): ").lower()
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

def delete_user(users):
    username = input("Enter username to delete: ").lower()
    for u in users:
        if u["username"] == username:
            if u["role"] == "admin":
                print("Cannot delete admin user.")
                return
            confirm = input(f"Are you sure you want to delete user {username}? (y/n): ").lower()
            if confirm.lower() != 'y':
                print("Deletion cancelled.")
                return
            
            users.remove(u)
            save_users(users)
            print("User deleted.")
            return
            
    print("User not found.")

def change_pin(current_user, users):
    new_pin = input("Enter new PIN: ")
    confirm_pin = input("Confirm new PIN: ")
    if new_pin != confirm_pin:
        print("PINs do not match. PIN change failed.")
        return
    for u in users:
        if u["username"] == current_user["username"]:
            u["pin"] = new_pin
            save_users(users)
            print("PIN changed successfully.")
            return

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
    elif choice == 'vpr':
        filter = apply_filters(patients)
        view_patient_record(filter)
    elif choice == 'ap':
        add_patient(patients)
    elif choice == 'ad':
        add_diagnosis(patients)
    elif choice == 'dp':
        delete_patient(patients)
    elif choice == 'as':
        create_user(users)
    elif choice == 'vs':
        view_staff(users)
    elif choice == 'md':
        mark_for_discharge(patients)
    elif choice == 'dels':
        delete_user(users)
    elif choice == 'disp':
        discharge_patient(patients)
    elif choice == 'cp':
        change_pin(current_user, users)
    elif choice == 'logout':
        logout()
        break
    else:
        print("Invalid choice. Please try again.")

print("Exiting program. Goodbye!")

