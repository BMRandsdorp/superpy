import csv
from datetime import datetime, date, timedelta
from rich import print
from rich.console import Console
from rich.style import Style
from rich.table import Table

"""
functions:
    - report (read):
        - bought --> iventory
        - sold --> sales report (revenue, profit)
    - (write):
        - bought (buy)
        - sold (sell)
        - report (revenue, profit)
    - store Date:
        - advance time (number of days)
        - change date (yyyy-mm-dd)
    - delete?
    - expired?
"""

# general console.print styles
console = Console()
warning_style = Style(color="red", bold=True)
confirmation_style = Style(color="green", bold=True)
report_style = Style(color="white", bgcolor="green", bold=True)

"""date functions"""
# Set global variable to use in functions
current_date = ""  # (placeholder date formatted yyyy-mm-dd)


# function to store date in txt file
def store_date():
    global current_date
    # write date to txt file
    file = open("./data/date.txt", "w")
    file.write(current_date)
    file.close()


# Function to get todays date once and won't change after user changed date
def todays_date():
    global current_date
    if current_date != "":
        console.print("already accessed todays date once no need to update", style=confirmation_style)
        return
    working_date = date.today()
    current_date = datetime.strftime(working_date, '%Y-%m-%d')
    store_date()
    console.print("defined todays date", style=confirmation_style)


# small QoL function to clear stored date
def clear_date():
    global current_date
    current_date = ""
    console.print("clearing stored date", style=warning_style)
    file = open("./data/date.txt", "w")
    file.write(current_date)


# changes date percieved as today in date.txt
def change_date(date_yyyy_mm_dd):
    global current_date
    # change date to specified date
    date_formatted = datetime.strptime(date_yyyy_mm_dd, '%Y-%m-%d')
    current_date = date_formatted
    store_date()


def advance_time(number_of_days):
    todays_date()
    global current_date
    file = open("./data/date.txt", "r")
    date_str = file.read()
    date1 = datetime.strptime(date_str, '%Y-%m-%d')
    # use timedelta to add number of days to stored date
    date2 = date1 + timedelta(days=number_of_days)
    # store new date to global var and call store_date
    current_date = date2
    store_date()
    console.print(f'advanced date by {number_of_days} days', style=confirmation_style)


def get_date():
    file = open("./data/date.txt", "r")  # read date.txt
    today = file.read()
    if today == "":
        console.print("no date stored getting todays date", style=confirmation_style)
        todays_date()
    else:
        global current_date
        current_date = today
        console.print(f'Using {current_date} as todays date', style=confirmation_style )
        file.close()


"""CSV functions"""


def buy_product(product_name, price, expiration_date):
    # call todays_date, get_today to get date from sytem/after changing date
    get_date()

    # read/write file, so function can iterate through list + update id
    with open('./data/bought.csv', 'r+', newline='') as bought_file:
        reader = csv.DictReader(bought_file)
        bought_list = list(reader)

        # set new_id to 0 and check if rows exist to change
        new_id = 0
        for row in bought_list:
            if row == bought_list[-1]:
                # print(f'working with {row}')
                new_id = int(row['id']) + 1
                # print(new_id)

        new_item = {
            "id": new_id,
            "product_name": product_name,
            "buy_date": current_date,
            "buy_price": price,
            "expiration_date": expiration_date
            }
        bought_list.append(new_item)

        bought_file.seek(0)
        # write function used to add newly bought item to bought.csv rows data
        writer = csv.DictWriter(bought_file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(bought_list)

        console.print(f"added {new_item} to inventory", style=confirmation_style )
        bought_file.close()


def sell_product(product_name, price):
    get_date()

    # sell function checks if item is in stock (check bought.csv)
    with open('./data/sold.csv', 'r+', newline='') as sold_file:
        sold_reader = csv.DictReader(sold_file)
        sold_list = list(sold_reader)

        new_sale_id = 0
        for row in sold_list:
            if row == sold_list[-1]:
                new_sale_id = int(row['id']) + 1

        # list of sold items id to filter out
        sold_items_id = []
        for row in sold_list:
            sold_items_id.append(row['bought_id'])

    # open/read bought and iterate through rows to see if product is in stock
        with open('./data/bought.csv', 'r+', newline='') as bought_file:
            reader = csv.DictReader(bought_file)
            bought_list = list(reader)

            for row in bought_list:
                if row['product_name'] != product_name:
                    continue
                if row['product_name'] == product_name and row['id'] in sold_items_id:
                    continue
                else:
                    # check if item is expired
                    exp_date = datetime.strptime(row['expiration_date'], '%Y-%m-%d')
                    today = datetime.strptime(current_date, '%Y-%m-%d')
                    delta = exp_date - today
                    if delta.days < 0:
                        # move item to sold with 0 sale price if expired
                        bought_for = row['buy_price']
                        exp_item = {
                            "id": new_sale_id,
                            "bought_id": row['id'],
                            "sell_date": current_date,
                            "sell_price": 0,
                            "buy_price": bought_for
                            }
                        sold_list.append(exp_item)
                        new_sale_id += 1
                        continue
                    else:
                        sale_id = row['id']
                        bought_for = row['buy_price']
                        sale_item = {
                            "id": new_sale_id,
                            "bought_id": sale_id,
                            "sell_date": current_date,
                            "sell_price": price,
                            "buy_price": bought_for
                            }
                        sold_list.append(sale_item)

                        # add items to sold.csv
                        sold_file.seek(0)
                        writer = csv.DictWriter(sold_file, fieldnames=sold_reader.fieldnames)
                        writer.writeheader()
                        writer.writerows(sold_list)
                        sold_file.close()
                        bought_file.close()
                        return
            console.print("ERROR: item unavailable", style=warning_style)
            sold_file.close()
            bought_file.close()


""" report functions"""


def inventory_report(arg_date):
    # get bought id list from sold to filter out sold products from inventory up to given date
    sold_items_id = []
    with open('./data/sold.csv', 'r+', newline='') as sold_file:
        sold_reader = csv.DictReader(sold_file)
        sold_list = list(sold_reader)

        for row in sold_list:
            # filter up to arg_date
            sold_date = datetime.strptime(row['sell_date'], '%Y-%m-%d')
            argument_date = datetime.strptime(arg_date, '%Y-%m-%d')
            delta = argument_date - sold_date
            if delta.days < 0:
                continue
            else:
                sold_items_id.append(row['bought_id'])

    with open('./data/bought.csv', 'r+', newline='') as bought_file:
        reader = csv.DictReader(bought_file)
        bought_list = list(reader)

        inventory_list = []
        for row in bought_list:
            # filter out dates after arg_date
            buyin_date = datetime.strptime(row['buy_date'], '%Y-%m-%d')
            argument_date = datetime.strptime(arg_date, '%Y-%m-%d')
            delta = argument_date - buyin_date
            if delta.days >= 0:
                # filter out expired items
                expiration = datetime.strptime(row['expiration_date'], '%Y-%m-%d')
                expiration_delta = expiration - argument_date
                if expiration_delta.days < 0:
                    # print("expired not adding item to list")
                    continue
                # filter out sold items
                if row['id'] in sold_items_id:
                    # print("already sold product")
                    continue
                else:
                    # add dict if iventory list is empty
                    if inventory_list == [""]:
                        inventory_list = [{
                            'Product Name': row['product_name'],
                            'Count': 1,
                            'Buy Price': row['buy_price'],
                            'Expiration date': row['expiration_date']
                            }]
                        continue
                    # if product is in iventory list add +1 to count and add price and exp date
                    elif any(d['Product Name'] == row['product_name'] for d in inventory_list):
                        for i in range(len(inventory_list)):
                            if row['product_name'] in inventory_list[i].values():
                                inventory_list[i]['Count'] += 1
                                inventory_list[i]['Buy Price'] = inventory_list[i]['Buy Price'] + ", " + (row['buy_price'])
                                inventory_list[i]['Expiration date'] = inventory_list[i]['Expiration date'] + ", " + (row['expiration_date'])
                                continue
                    else:
                        inventory_list.append({
                            'Product Name': row['product_name'],
                            'Count': 1,
                            'Buy Price': row['buy_price'],
                            'Expiration date': row['expiration_date']
                            })

        # convert to table with rich.table
        table = Table(show_header=True, header_style="bold")
        table.add_column("Product Name")
        table.add_column("Count")
        table.add_column("Buy Price(s)")
        table.add_column("Expiration date(s)")

        if inventory_list == []:
            console.print("No inventory to display for given date", style=warning_style)
        else:
            for d in inventory_list:
                table.add_row(
                    d['Product Name'],
                    str(d['Count']),
                    d['Buy Price'],
                    d['Expiration date'],
                    )
        console.print(table)

    bought_file.close()
    sold_file.close()


def revenue_report(arg_date, date_name):
    # open sold.csv to get sale price and add together
    with open('./data/sold.csv', 'r+', newline='') as sold_file:
        sold_reader = csv.DictReader(sold_file)
        sold_list = list(sold_reader)

        revenue = 0.0
        if len(arg_date) == 7:
            for row in sold_list:
                if row['sell_date'].startswith(arg_date):
                    revenue = revenue + float(row['sell_price'])
                    continue
        else:
            for row in sold_list:
                if row['sell_date'] == arg_date:
                    revenue = revenue + float(row['sell_price'])
                    continue

        if date_name == 'Now':
            console.print(f"Revenue right now: {revenue}", style=report_style)
        elif date_name == 'Today' or date_name == 'Yesterday':
            console.print(f"{date_name}'s revenue: {revenue}", style=report_style)
        else:
            console.print(f"Revenue from {date_name}: {revenue}", style=report_style)
    sold_file.close()


def profit_report(arg_date, date_name):
    # open sold.csv to get sale price and add together
    with open('./data/sold.csv', 'r+', newline='') as sold_file:
        sold_reader = csv.DictReader(sold_file)
        sold_list = list(sold_reader)

        profit = 0.0
        if len(arg_date) == 7:
            for row in sold_list:
                if row['sell_date'].startswith(arg_date):
                    sale = float(row['sell_price']) - float(row['buy_price'])
                    profit = profit + sale
                    continue
        else:
            for row in sold_list:
                if row['sell_date'] == arg_date:
                    sale = float(row['sell_price']) - float(row['buy_price'])
                    profit = profit + sale
                    continue

        if date_name == 'Now':
            console.print(f"Profit right now: {profit}", style=report_style)
        elif date_name == 'Today' or date_name == 'Yesterday':
            console.print(f"{date_name}'s profit: {profit}", style=report_style)
        else:
            console.print(f"Profit from {date_name}: {profit}", style=report_style)
    sold_file.close()


"""get functions"""


def get_report_inventory(date):
    global current_date
    # change keywords to date string for function call
    if date == "Today" or date == "Now":
        get_date()
        today_now = current_date
        inventory_report(today_now)
    elif date == "Yesterday":
        get_date()
        today = datetime.strptime(current_date, '%Y-%m-%d')
        delta = today - timedelta(days=1)
        str_delta = datetime.strftime(delta, '%Y-%m-%d')
        inventory_report(str_delta)
    else:
        inventory_report(date)


def get_report_revenue(date):
    global current_date
    # change keywords to date string for function call
    if date == "Today" or date == "Now":
        get_date()
        today_now = current_date
        revenue_report(today_now, date)
    elif date == "Yesterday":
        get_date()
        today = datetime.strptime(current_date, '%Y-%m-%d')
        delta = today - timedelta(days=1)
        str_delta = datetime.strftime(delta, '%Y-%m-%d')
        revenue_report(str_delta, date)
    else:
        if len(date) == 7:
            # change date string to month full name and year
            date_ob = datetime.strptime(date, '%Y-%m')
            month_year = date_ob.strftime('%B %Y')
            revenue_report(date, month_year)
        else:
            # change date string to date - month abbreviated - year
            date_ob = datetime.strptime(date, '%Y-%m-%d')
            date_str = date_ob.strftime('%d %b %Y')
            revenue_report(date, date_str)


def get_report_profit(date):
    global current_date
    # change keywords to date string for function call
    if date == "Today" or date == "Now":
        get_date()
        today_now = current_date
        profit_report(today_now, date)
    elif date == "Yesterday":
        get_date()
        today = datetime.strptime(current_date, '%Y-%m-%d')
        delta = today - timedelta(days=1)
        str_delta = datetime.strftime(delta, '%Y-%m-%d')
        profit_report(str_delta, date)
    else:
        if len(date) == 7:
            # change date string to month full name and year
            date_ob = datetime.strptime(date, '%Y-%m')
            month_year = date_ob.strftime('%B %Y')
            profit_report(date, month_year)
        else:
            # change date string to date - month abbreviated - year
            date_ob = datetime.strptime(date, '%Y-%m-%d')
            date_str = date_ob.strftime('%d %b %Y')
            profit_report(date, date_str)
