from datetime import datetime, timedelta
from flask import Flask, render_template

app = Flask(__name__)

def get_today_date():
    """
    Returns today's date in YYYY-MM-DD format
    """
    return datetime.now().strftime('%Y-%m-%d')

def days_since_august_first():
    """
    Calculates the number of days that have passed since August 1, 2024
    Returns the number of days as an integer
    """
    august_first = datetime(2024, 8, 1)
    today = datetime.now()
    days_passed = (today - august_first).days
    return days_passed

def business_days_until_july_31_2026():
    """
    Calculates the number of business days (excluding weekends)
    remaining until July 31, 2026
    Returns the number of business days as an integer
    """
    july_31_2026 = datetime(2026, 7, 31)
    today = datetime.now()
    
    # Count business days
    business_days = 0
    current_date = today
    
    while current_date <= july_31_2026:
        # Skip weekends (5 is Saturday, 6 is Sunday)
        if current_date.weekday() < 5:
            business_days += 1
        current_date += timedelta(days=1)
    
    return business_days

def calculate_remaining_bcg_debt():
    """
    Calculates the remaining debt to BCG based on proportional daily payments
    over a 24-month period (August 1, 2024 to July 31, 2026)
    Returns the remaining amount in USD
    """
    total_debt = 220000  # USD
    start_date = datetime(2024, 8, 1)
    end_date = datetime(2026, 7, 31)
    today = datetime.now()
    
    # Calculate total business days in the period
    total_business_days = 0
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Skip weekends
            total_business_days += 1
        current_date += timedelta(days=1)
    
    # Calculate business days passed
    business_days_passed = 0
    current_date = start_date
    while current_date <= today:
        if current_date.weekday() < 5:  # Skip weekends
            business_days_passed += 1
        current_date += timedelta(days=1)
    
    # Calculate daily payment rate
    daily_payment = total_debt / total_business_days
    
    # Calculate remaining debt
    remaining_business_days = total_business_days - business_days_passed
    remaining_debt = daily_payment * remaining_business_days
    
    # Calculate amount paid
    amount_paid = daily_payment * business_days_passed
    
    # Calculate percentage paid
    percentage_paid = (amount_paid / total_debt) * 100
    
    return round(remaining_debt, 2), round(amount_paid, 2), round(percentage_paid, 2), round(daily_payment, 2)

@app.route('/')
def index():
    today = get_today_date()
    days_since_august = days_since_august_first()
    business_days_remaining = business_days_until_july_31_2026()
    remaining_debt, amount_paid, percentage_paid, daily_payment = calculate_remaining_bcg_debt()
    
    return render_template('index.html',
                         today=today,
                         days_since_august=days_since_august,
                         business_days_remaining=business_days_remaining,
                         daily_payment=f"{daily_payment:,.2f}",
                         amount_paid=f"{amount_paid:,.2f}",
                         percentage_paid=f"{percentage_paid:.1f}",
                         remaining_debt=f"{remaining_debt:,.2f}")

if __name__ == "__main__":
    app.run(debug=True)
