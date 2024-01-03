#!/usr/bin/env python3
"""
This module generates invoices for a given date range.
"""

import argparse
import hashlib
import os
import subprocess

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from dateutil.rrule import WEEKLY, rrule

def generate_invoices(name, task, details, amount, recipient, first, last, template):
    """
    Generate invoices for a given date range.

    Args:
        name (str): The object of the invoice.
        task (str): The task title of the invoice.
        details (str): The details of the mission.
        amount (str): The amount of the invoice.
        recipient (str): The recipient of the invoice.
        first (str): The first date of the invoice.
        last (str): The last date of the invoice.
        template (str): The Quarto document to serve as template for the invoice.
    """

    start_date = parse(first)
    end_date = parse(last)
    month_counter = 1
    previous_month = start_date.month
    for issued_date in rrule(WEEKLY, dtstart=start_date, until=end_date, interval=2):
        if issued_date.month != previous_month:
            month_counter = 1
        invoice_number = f"{issued_date.strftime('2024%m')}-{month_counter:03d}"
        hash_object = hashlib.sha256(invoice_number.encode())
        hex_dig = hash_object.hexdigest()
        due_date = issued_date + relativedelta(day=31, months=1)

        month_counter += 1
        previous_month = issued_date.month

        filename = f"input/{invoice_number}.yml"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"title: {name} {start_date.year}\n")
            invoice_start_date = (issued_date - relativedelta(weeks=2)).strftime('%Y/%m/%d')
            invoice_end_date = (issued_date - relativedelta(days=1)).strftime('%Y/%m/%d')
            file.write(f"description: {invoice_start_date} -- {invoice_end_date}\n")
            file.write("invoice:\n")
            file.write(f"  task: {task}\n")
            file.write(f"  details: {details}\n")
            file.write(f"  number: {invoice_number}\n")
            file.write(f"  issued: {issued_date.strftime('%Y-%m-%d')}\n")
            file.write(f"  due: {due_date.strftime('%Y-%m-%d')}\n")
            file.write(f"  reference: {hex_dig[:9]}\n")
            file.write(f"  amount: {amount}\n")

    for file in os.listdir('input'):
        invoice, _ = os.path.splitext(file)

        subprocess.run([
            'quarto', 'render', f'{template}',
            '--metadata-file', f'input/{invoice}.yml',
            '--output', f'INVOICE-N{invoice}-{recipient}.pdf'
        ], check=True)

        os.rename(
            f'INVOICE-N{invoice}-{recipient}.pdf',
            f'output/INVOICE-N{invoice}-{recipient}.pdf'
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", help="The object of the invoice")
    parser.add_argument("--task", help="The task title of the invoice")
    parser.add_argument("--details", help="The details of the mission")
    parser.add_argument("--amount", help="The amount of the invoice")
    parser.add_argument("--recipient", help="The recipient of the invoice")
    parser.add_argument("--first", help="The first date of the invoice")
    parser.add_argument("--last", help="The last date of the invoice")
    parser.add_argument("--template", help="The Quarto document to serve as template for the invoice")
    args = parser.parse_args()

    generate_invoices(
        name=args.name,
        task=args.task,
        details=args.details,
        amount=args.amount,
        recipient=args.recipient,
        first=args.first,
        last=args.last,
        template=args.template
    )
