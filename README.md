# SuperPy

This application is used to record buying/selling of products and displaying inventory revenue and profit.

## Buying product

when you want to record buying a product use:

```
python main.py buy <product-name> <price> <expiration-date format yyyy-mm-dd>
```

## Selling product

You can sell product with:

```
python main.py sell <product-name> <sell-price>
```

if product is not in stock an error will be returned

## Report

For report function there's 3 options to choose from: **inventory, revenue and profit**
You need to declare which of these 3 you want a report from and from what day/date.

### Inventory

To get a overview of all items in inventory at a certain date use:

```
python main.py report inventory --today
python main.py report inventory --now
python main.py report inventory --yesterday
python main.py report inventory --date <date formatted in yyyy-mm-dd>
```

Can only get inventory for a specific day.

### Revenue

To know how much revenue was made on a specific date or month use:

```
python main.py report revenue --today
python main.py report revenue --now
python main.py report revenue --yesterday
python main.py report revenue --date <specific date formatted in yyyy-mm-dd>
python main.py report revenue --date <month date formatted in yyyy-mm>
```

### Profit

To know how much profit was made on a specific date or month use:

```
python main.py report profit --now
python main.py report profit --today
python main.py report profit --yesterday
python main.py report profit --date <specific date formatted in yyyy-mm-dd>
python main.py report profit --date <month date formatted in yyyy-mm>
```

## Time

To change the date percieved as today for the program use:

```
python main.py time --advance_time <number of days you want to advance time>
python main.py time --set_date <date you want to change to in yyyy-mm-dd format>
```

## Clearing Stored date

Since date percieved as today is stored in a separate file, you can clear this by using the following command:

```
python main.py clear_date
```

## Help

For all commands a help command is available. Using `--help` or `--h` after command

```
python main.py --help
python main.py <main command> --help
```
