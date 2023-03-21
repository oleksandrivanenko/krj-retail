# Import libraries
import pandas as pd
import postcodes_uk
from datetime import datetime

# To get the data about items
df = pd.read_csv('product.csv')

# To keep data
basket = []

# To print colors in terminal
def pr_red(skk): print("\033[91m{}\033[00m" .format(skk))
def pr_green(skk): print("\033[92m{}\033[00m" .format(skk))
def pr_yellow(skk): print("\033[93m{}\033[00m" .format(skk))


# The login() function (If 3 attempts were used, the system is blocked)
def login():
    user_data = pd.read_csv("user.csv")
    attempts = 3
    print("---------- LOGIN ----------")
    while not(attempts == 0):
        username = input("USERNAME: ")
        password = input("PASSWORD: ")
        if username in user_data["username"].unique():
            user_index = (user_data.index[user_data["username"] == username])[0]
            if password == str(user_data.iloc[user_index][1]):
                pr_green("LOGIN IS SUCCESSFUL")
                return True
            else:
              attempts -= 1
        else:
            attempts -= 1
        pr_red("LOGIN IS NOT SUCCESSFUL")
    else:
        return False


# The main function for the main menu
def menu():
    while True:
        print("-------- KRJ RETAIL -------\n"
              "|  1. SELL A PRODUCT      |\n"
              "|  2. ADD AN ITEM         |\n"
              "|  3. EXIT                |\n"
              "---------------------------")

        options = ["1", "2", "3"]
        option = ""
        while not option in options:
            option = input("OPTION: ")
            if not option in options:
                pr_red("THERE IS NO SUCH OPTION | TRY AGAIN")

        if option == "1":
            sell_product()
        elif option == "2":
            add_item()
        else:
            pr_yellow("YOU HAVE EXITED THE PROGRAM")
            break


# The function for the first option
def sell_product():
    global basket

    # To show the list with items
    def show_list():
        product = df.iloc[:, 0]
        price = df.iloc[:, 1]
        print("------ LIST OF ITEMS ------")
        for i in range(len(product)):
            print(product[i], "-", price[i])
        print("---------------------------")


    # To get item and number of items
    def get_item():

        item = ""
        while not (item in df["Item"].unique()) and not (item == "Done"):
            item = input("TYPE ITEM OR TYPE 'DONE' TO CHECK OUT: ").capitalize()

            if item == "Done":
                return False
            else:

                if not (item in df["Item"].unique()):
                    pr_red("THERE IS NO SUCH PRODUCT | TRY AGAIN")
                else:
                    item_row = df.loc[df["Item"] == item]
                    price = item_row["Price"].values[0]


        while True:
            try:
                num_item = int(input("NUMBER: "))
                if num_item < 1 or num_item > 1000:
                    raise ValueError("TYPE NUMBER BETWEEN 1 AND 1000 | TRY AGAIN")
                break
            except ValueError:
                pr_red("TYPE NUMBER BETWEEN 1 AND 1000 | TRY AGAIN")


        basket.append([item, price, num_item])

        pr_green("ADDED ITEM")
        print("BASKET: " + ', '.join(('{} ({})'.format(i[0], i[2]) for i in basket)))


    # To get customer details for the receipt
    def get_customer_details():
        global customer

        forename = ""
        surname = ""
        address = ""
        postcode = ""
        number = ""

        print("----------DETAILS----------")

        while not (1 < len(forename) < 20) or not (forename.isalpha()):
            forename = input("FORENAME: ").capitalize()
            if not (1 < len(forename) < 20):
                pr_red("MUST CONTAIN BETWEEN 2 AND 20 CHARACTERS | TRY AGAIN")
            elif not (forename.isalpha()):
                pr_red("PLEASE USE ONLY LETTERS | TRY AGAIN")

        while not (1 < len(surname) < 20) or not (surname.isalpha()):
            surname = input("SURNAME: ").capitalize()
            if not (1 < len(surname) < 20):
                pr_red("MUST CONTAIN BETWEEN 2 AND 20 CHARACTERS | TRY AGAIN")
            elif not (surname.isalpha()):
                pr_red("PLEASE USE ONLY LETTERS | TRY AGAIN")

        while not (len(address) > 2):
            address = input("ADDRESS: ")
            if not (len(address) > 5):
                pr_red("MUST CONTAIN MORE THAN 5 CHARACTERS")

        while not (postcodes_uk.validate(postcode)):
            postcode = input("POSTCODE: ").upper()
            if not (postcodes_uk.validate(postcode)):
                pr_red("INVALID POSTCODE | TRY AGAIN")

        while not (len(number) == 11) or not (number.isnumeric()):
            number = input("NUMBER: ")
            if not (len(number) == 11) or not (number.isnumeric()):
                pr_red("MUST CONTAIN 11 DIGITS | TRY AGAIN")

        print("---------------------------")

        customer = [forename, surname, address, postcode, number]

    # To print the receipt
    def receipt():
        print("---------RECEIPT-----------")
        print(f"CUSTOMER: {customer[0]} {customer[1]}")
        print(f"ADDRESS: {customer[2]}")
        print(f"POSTCODE: {customer[3]}")
        print(f"NUMBER: {customer[4]}")
        print("ITEMS BOUGHT:\n" + '\n'.join(
            ('{} {} (TOTAL: £{:.2f})'.format(i[2], i[0], float(i[1]) * i[2]) for i in basket)))
        print(f"TOTAL: £{round(sum((i[1] * int(i[2]) for i in basket)), 2)}")
        print(f"{datetime.now().date()} {datetime.now().strftime('%H:%M:%S')}")
        print("---------------------------")

    # The main algorithm for the first option
    show_list()
    while True:
        if get_item() == False:
            get_customer_details()
            receipt()
            basket = []
            break


# The function to add an item
def add_item():

    print("-------ADD AN ITEM---------")

    item_name = ""

    while not (1 < len(item_name) < 20) or not (item_name.isalpha()):
        item_name = input("ITEM: ").capitalize()
        if not (1 < len(item_name) < 20):
            pr_red("MUST CONTAIN BETWEEN 2 AND 20 CHARACTERS | TRY AGAIN")
        elif not (item_name.isalpha()):
            pr_red("PLEASE USE ONLY LETTERS | TRY AGAIN")

    while True:
        try:
            item_price = float(input("PRICE: "))
            if item_price < 0 or item_price > 1000:
                raise ValueError("TYPE NUMBER BETWEEN 0 AND 1000 | TRY AGAIN")
            break
        except ValueError:
            pr_red("TYPE NUMBER BETWEEN 0 AND 1000 | TRY AGAIN")

    df.loc[len(df)] = [item_name, item_price]
    df.to_csv("product.csv", index=False)
    pr_green("ITEM ADDED TO THE LIST")

    print("---------------------------")


# The main program
if login():
    menu()
else:
    pr_red("---------------------------\n"
          "|       SYSTEM LOCKED     |\n"
          "---------------------------")
