# Report superpy

## Problem 1

1st problem I ran into while creating sell function is that it did not filter out already sold products and expired products.
After already creating an if statement to check if product is in stock, I further used this logic to also filter out sold products by grabbing list of `bought_id's` from sold.csv and using this list to ignore products if id's match when itterating over the `bought_list`.

```
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

```

I followed this up by moving expired items to sold with a sell price of 0 to help keep track of profits with expired items calculated in.

## Problem 2

When creating the report function I managed to get a product count to increase whenever a duplicate `product_name` would be detected, but did not account for the fact that products could have registered different expiration dates and buy in prices so for this I opted in to redefine the `['Buy Price']` and ` ['Expiration date']` keys in the `iventory_list` when increasing count.

```
    elif any(d['Product Name'] == row['product_name'] for d in inventory_list):
        for i in range(len(inventory_list)):
            if row['product_name'] in inventory_list[i].values():
                inventory_list[i]['Count'] += 1
                inventory_list[i]['Buy Price'] = inventory_list[i]['Buy Price'] + ", " + (row['buy_price'])
                inventory_list[i]['Expiration date'] = inventory_list[i]['Expiration date'] + ", " + (row['expiration_date'])
                continue
```

## Problem 3

When receiving date arguments for the report functions the arguments `--today` `--yesterday` and `--now` are not formatted as date strings.
To solve this issue I created the `get_report_inventory` `get_report_revenue` `get_report_profit` to check the strings and call functions to change it to the corrosponding date string accordingly.

_example below for report inventory_

```
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
```

To further add to this with `get_report_revenue` and `get_report_profit` I added an extra variable to pass down to function call so the function can print out the revenue and profit calculations with the variable names in.

```
    if date == "Today" or date == "Now":
        get_date()
        today_now = current_date
        revenue_report(today_now, date)
```

```
    if date_name == 'Now':
        console.print(f"Revenue right now: {revenue}", style=report_style)
    elif date_name == 'Today' or date_name == 'Yesterday':
        console.print(f"{date_name}'s revenue: {revenue}", style=report_style)
    else:
        console.print(f"Revenue from {date_name}: {revenue}", style=report_style)
```
