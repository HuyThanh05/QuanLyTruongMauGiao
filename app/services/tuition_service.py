from app.models.Models import TuitionFee, PaymentStatusEnum
from datetime import datetime


def total_revenue():
    paid_tuitions = TuitionFee.query.filter(
        TuitionFee.status == PaymentStatusEnum.Paid
    ).all()
    total_revenue = 0
    for tuition in paid_tuitions:
        total_revenue += tuition.total
    return total_revenue


def monthly_revenue(month, year=None):
    collected = monthly_collected_amounts(month, year)
    uncollected = monthly_uncollected_amounts(month, year)
    return collected + uncollected


def monthly_collected_amounts(month, year=None):
    if year is None:
        year = datetime.now().year
    paid_tuitions = TuitionFee.query.filter(
        TuitionFee.month == month,
        TuitionFee.year == year,
        TuitionFee.status == PaymentStatusEnum.Paid
    ).all()
    collected_amounts = 0
    for tuition in paid_tuitions:
        collected_amounts += tuition.total
    return collected_amounts


def monthly_uncollected_amounts(month, year=None):
    if year is None:
        year = datetime.now().year
    unpaid_tuitions = TuitionFee.query.filter(
        TuitionFee.month == month,
        TuitionFee.year == year,
        TuitionFee.status == PaymentStatusEnum.Unpaid).all()
    uncollected_amounts = 0
    for tuition in unpaid_tuitions:
        uncollected_amounts += tuition.total
    return uncollected_amounts
