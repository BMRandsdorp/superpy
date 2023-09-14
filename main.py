# Imports
from argparse import *
import csv
from datetime import date
from functions import *
from rich import print
from rich.console import Console
from rich.style import Style

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
"""
CLI tool commands:
    - buy
    - sell
    - report:
        - inventory
        - revenue
    - set date
    - advance time (x days)
    - delete date
"""
# general console.print styles
console = Console()
warning_style = Style(color="red", bold=True)


# Argparse superpy
parser = ArgumentParser(description="Welcome to superpy, use this to track buying/selling of inventory.")
subparsers = parser.add_subparsers(dest="command")

# Subparsers section
# buy subparser to store new item
buy_parser = subparsers.add_parser("buy", help="Used to register newly bought items to inventory list")
buy_parser.add_argument("product_name", type=str, help="Specify product name, if it contains spaces put in parentheses")
buy_parser.add_argument("price", type=float, help="Specify buy-in price")
buy_parser.add_argument("expiration_date", type=str, help="Register product expiration date format in yyyy-mm-dd")

# sell subparser
sell_parser = subparsers.add_parser("sell", help="Register sales made in the store")
sell_parser.add_argument("product_name", type=str, help="Specify product name as registered in inventory")
sell_parser.add_argument("price", type=float, help="Specifiy sale price")

# report subparser
report_parser = subparsers.add_parser("report", help="Used to report inventory, revenue or profit from a specific day/date, use optional arguments to specify from when")
report_parser.add_argument("report_type", type=str, choices=['inventory', 'revenue', 'profit'], help="Specificy what to report on: inventory, revenue or profit")
report_parser.add_argument("--date", type=str, help="specifiy date/month write out in yyyy-mm-dd or yyyy-mm format")
report_parser.add_argument("--today", type=str, nargs='?', const="today", help="Used to get report for today")
report_parser.add_argument("--yesterday", type=str, nargs='?', const="yesterday", help="Used to get report for yesterday")
report_parser.add_argument("--now", type=str, nargs='?', const="now", help="Used to get report for current moment in time")

# advance time subparser
time_parser = subparsers.add_parser("time", help="Used to change the perceived day/date as right now")
time_parser.add_argument("--advance_time", type=int, help="give number of days you want to advance current date")
time_parser.add_argument("--set_date", type=str, help="Set current date in yyyy-mm-dd format")

# clear date subparser
clear_date_parser = subparsers.add_parser("clear_date", help="Use to clear (changed) date percieved as today")

# Parse arguments

args = parser.parse_args()

if args.command == "buy":
    # console.print(f'bought {args.product_name} for {args.price} which expires on {args.expiration_date}')
    buy_product(args.product_name, args.price, args.expiration_date)

if args.command == "sell":
    # console.print(f"selling {args.product_name} for {args.price}")
    sell_product(args.product_name, args.price)

if args.command == "report":
    # arg_list to check if more than optional arg is used
    arg_list = [args.now is not None, args.today is not None, args.yesterday is not None, args.date is not None]
    if all(i is None for i in [args.now, args.today, args.yesterday, args.date]):
        console.print("Please specifiy day or date for report", style=warning_style)
    elif sum(arg_list) >= 2:
        console.print("Please only use 1 optional argument to specifiy", style=warning_style)
    else:
        if args.now is not None:
            date_arg = "Now"
        if args.today is not None:
            date_arg = "Today"
        if args.yesterday is not None:
            date_arg = "Yesterday"
        if args.date is not None:
            date_arg = args.date
        # check report types
        if args.report_type == "inventory":
            get_report_inventory(date_arg)
        if args.report_type == "revenue":
            get_report_revenue(date_arg)
        if args.report_type == "profit":
            get_report_profit(date_arg)

if args.command == "time":
    if args.advance_time is None and args.set_date is None:
        console.print("ERROR use --advance_time or --set_date arguments to change the time", style=warning_style)
    if args.advance_time is not None and args.set_date is not None:
        console.print("ERROR only use 1 optional arguments to change the date", style=warning_style)
    if args.advance_time is not None and args.set_date is None:
        advance_time(args.advance_time)
    if args.set_date is not None and args.advance_time is None:
        console.print(f'changing date to {args.set_date}')
        change_date(args.set_date)

if args.command == "clear_date":
    clear_date()


def main():
    pass


if __name__ == "__main__":
    main()
