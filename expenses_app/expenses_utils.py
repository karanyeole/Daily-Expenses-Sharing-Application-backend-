# expenses_app/expenses_utils.py

from decimal import Decimal

def split_equal(total_amount, participants):
    """Split total_amount equally among participants"""
    per_person = total_amount / len(participants)
    return {p: per_person for p in participants}


def split_exact(amounts, participants):
    """Split based on exact amounts provided"""
    if len(amounts) != len(participants):
        raise ValueError("Number of amounts should match the number of participants.")
    return {p: amt for p, amt in zip(participants, amounts)}


def split_percentage(percentages, total_amount, participants):
    """Split based on percentages provided"""
    if sum(percentages) != 100:
        raise ValueError("Percentages must add up to 100.")
    return {p: (percent / 100) * total_amount for p, percent in zip(participants, percentages)}
