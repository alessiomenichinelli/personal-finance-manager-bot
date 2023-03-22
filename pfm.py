import csv

USERS_FILE = "users.txt" # Ogni riga chat_id
BALANCES_FILE = "balances.txt" # Ogni riga chat_id e bilanci
PM_FILE = "payment_methods.txt" # Ogni riga chat_id e metodi di pagamento
CATEGORIES_FILE = "categories.txt" # Ogni riga chat_id e categorie
EXPENSES_CSV_FILE = "expenses.csv"

# !!! UTENTI

# Legge TUTTI gli utenti e ritorna users
# users: lista di interi
def get_users():
    file = open(USERS_FILE, "r")
    users = file.readlines()
    file.close()
    users = [int(elem.rstrip()) for elem in users]
    return users

# Aggiunge l'utente in tutti i file di gestione
def add_user(chat_id):
    file = open(USERS_FILE, "a")
    file.write(str(chat_id)+"\n")
    file.close
    file = open(BALANCES_FILE, "a")
    file.write(str(chat_id)+"\n")
    file.close
    file = open(PM_FILE, "a")
    file.write(str(chat_id)+"\n")
    file.close
    file = open(CATEGORIES_FILE, "a")
    file.write(str(chat_id)+"\n")
    file.close

# !!! BILANCI

# Legge TUTTI i bilanci e ritorna balances_dict
# balances_dict: dizionario di liste nella forma chat_id: [balance1, balance2, ...]
def read_balances():
    balances_dict = {}
    file = open(BALANCES_FILE, "r")
    balances = file.readlines()
    file.close()
    for el in balances:
        el = el.rstrip()
        el = el.split()
        balances_dict[int(el[0])]=[]
        for i in range(1,len(el)):
            balances_dict[int(el[0])].append(el[i])
    return balances_dict

# Riscrive i bilanci nel file
def load_balances(balances_dict):
    file = open(BALANCES_FILE, "w")
    for key in balances_dict:
        string = str(key)
        for el in balances_dict[key]:
            string += " "
            string += str(el)
        file.write(string+"\n")
    file.close()

# Legge i bilanci di chat_id e ritorna balances
# balances: lista di bilanci
def get_balances(chat_id):
    balances = []
    file = open(BALANCES_FILE, "r")
    methods = file.readlines()
    file.close()
    for el in methods:
        el = el.rstrip()
        el = el.split()
        if int(el[0]) == chat_id:
            for i in range(1,len(el)):
                balances.append(el[i])
    return balances

# Aggiunge un bilancio a chat_id
def add_balances(chat_id, balance):
    users = get_users()
    balances_dict = read_balances()
    if chat_id in users:
        balances_dict[chat_id].append(balance)
    load_balances(balances_dict)

def calculate_balances(chat_id):
    balances = {}
    balances_names = get_balances(chat_id)

    for name in balances_names:
        balances[name] = 0

    expenses = get_expenses(chat_id)
    for exp in expenses:
        for name in balances_names:
            if(name == exp[1]):
                balances[name] -= float(exp[3])

    return balances


# !!! PAYMENT METHODS

# Legge TUTTI i metodi e ritorna pm_dict
# pm_dict: dizionario di liste nella forma chat_id: [method1, method2, ...]
def read_pm():
    pm_dict = {}
    file = open(PM_FILE, "r")
    methods = file.readlines()
    file.close()
    for el in methods:
        el = el.rstrip()
        el = el.split()
        pm_dict[int(el[0])]=[]
        for i in range(1,len(el)):
            pm_dict[int(el[0])].append(el[i])
    return pm_dict

# Riscrive i matodi nel file
def load_pm(pm_dict):
    file = open(PM_FILE, "w")
    for key in pm_dict:
        string = str(key)
        for el in pm_dict[key]:
            string += " "
            string += str(el)
        file.write(string+"\n")
    file.close()

# Legge i metodi di chat_id e ritorna methods
# methods: lista di metodi
def get_pm(chat_id):
    methods = []
    file = open(PM_FILE, "r")
    row = file.readlines()
    file.close()
    for el in row:
        el = el.rstrip()
        el = el.split()
        if int(el[0]) == chat_id:
            for i in range(1,len(el)):
                methods.append(el[i])
    return methods

# Aggiunge un metodo a chat_id
def add_pm(chat_id, method):
    users = get_users()
    pm_dict = read_pm()
    if chat_id in users:
        pm_dict[chat_id].append(method)
    load_pm(pm_dict)


def calculate_pm(chat_id):
    pm = {}
    pm_names = get_pm(chat_id)

    for name in pm_names:
        pm[name] = 0

    expenses = get_expenses(chat_id)
    for exp in expenses:
        for name in pm_names:
            if(name == exp[2]):
                pm[name] -= float(exp[3])

    return pm

# !!! CATEGORIE

# Legge TUTTI le categorie e ritorna categoties_dict
# categoties_dict: dizionario di liste nella forma chat_id: [cat1, cat2, ...]
def read_categories():
    categoties_dict = {}
    file = open(CATEGORIES_FILE, "r")
    categories = file.readlines()
    file.close()
    for el in categories:
        el = el.rstrip()
        el = el.split()
        categoties_dict[int(el[0])]=[]
        for i in range(1,len(el)):
            categoties_dict[int(el[0])].append(el[i])
    return categoties_dict

# Riscrive le categorie nel file
def load_categories(categoties_dict):
    file = open(CATEGORIES_FILE, "w")
    for key in categoties_dict:
        string = str(key)
        for el in categoties_dict[key]:
            string += " "
            string += str(el)
        file.write(string+"\n")
    file.close()

# Legge le categorie di chat_id e ritorna categories
# categories: lista di categorie
def get_categories(chat_id):
    categories = []
    file = open(CATEGORIES_FILE, "r")
    categories = file.readlines()
    file.close()
    for el in categories:
        el = el.rstrip()
        el = el.split()
        if int(el[0]) == chat_id:
            for i in range(1,len(el)):
                categories.append(el[i])
    return categories

# Aggiunge una categoria a chat_id
def add_categories(chat_id, category):
    users = get_users()
    categoties_dict = read_categories()
    if chat_id in users:
        categoties_dict[chat_id].append(category)
    load_categories(categoties_dict)

# !!! SPESE

def read_expenses():
    csv_file = open(EXPENSES_CSV_FILE, mode='r')
    reader = csv.reader(csv_file)
    expenses = []
    for row in reader:
        expenses.append(row)
    csv_file.close()
    return expenses

def load_expenses(expenses):
    csv_file = open(EXPENSES_CSV_FILE, mode='w', newline='')
    writer = csv.writer(csv_file)
    writer.writerows(expenses)
    csv_file.close()

def get_expenses(chat_id):
    csv_file = open(EXPENSES_CSV_FILE, mode='r')
    reader = csv.reader(csv_file)
    expenses = []
    for row in reader:
        if int(row[0]) == chat_id:
            expenses.append(row)
    csv_file.close()
    return expenses

def add_expense(expense):
    csv_file = open(EXPENSES_CSV_FILE, mode='a', newline='')
    writer = csv.writer(csv_file)
    writer.writerow(expense)
    csv_file.close()

def remove_expense(expense):
    i = 0
    expenses = read_expenses()
    for row in expenses:
        if(expense == row):
            expenses.pop(i)
            load_expenses(expenses)
            return True
        i +=1
    return False

def add_capital_letter(string):
    string = string[0].upper() + string[1:]
    return string

def is_date(string):
    try:
        dd = int(string[0:1])
        mm = int(string[3:4])
    except:
        return False
    
    if 1 <= dd <= 31:
        return False
    
    if 1 <= mm <= 12:
        return False
    
    return True