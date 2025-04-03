from datetime import datetime, timedelta
from flask import Flask, render_template

app = Flask(__name__)

MOTIVATIONAL_PHRASES = [
    "Every day is a new opportunity to grow and succeed.",
    "Your hard work today will pay off tomorrow.",
    "Stay focused, stay determined, and keep moving forward.",
    "Success is the sum of small efforts repeated daily.",
    "The only way to do great work is to love what you do.",
    "Your future is created by what you do today.",
    "Dream big, work hard, stay focused, and surround yourself with good people.",
    "The journey of a thousand miles begins with a single step.",
    "Success is not final, failure is not fatal: it is the courage to continue that counts.",
    "Believe you can and you're halfway there.",
    "The harder you work for something, the greater you'll feel when you achieve it.",
    "Don't watch the clock; do what it does. Keep going.",
    "Success is walking from failure to failure with no loss of enthusiasm.",
    "The only limit to our realization of tomorrow is our doubts of today.",
    "You are never too old to set another goal or to dream a new dream.",
    "The secret of getting ahead is getting started.",
    "It does not matter how slowly you go as long as you do not stop.",
    "The future belongs to those who believe in the beauty of their dreams.",
    "Success is not the key to happiness. Happiness is the key to success.",
    "The only way to achieve the impossible is to believe it is possible.",
    "Your time is limited, don't waste it living someone else's life.",
    "The best way to predict the future is to create it.",
    "Don't let yesterday take up too much of today.",
    "The only person you are destined to become is the person you decide to be.",
    "Success is not about the destination, it's about the journey.",
    "The difference between ordinary and extraordinary is that little extra.",
    "You don't have to be great to start, but you have to start to be great.",
    "The only limit to the height of your achievements is the reach of your dreams.",
    "Success is not in what you have, but who you are.",
    "The best revenge is massive success."
]

def get_current_day():
    """
    Returns the current day of the week and full date
    """
    now = datetime.now()
    return f"{now.strftime('%A')}, {now.strftime('%B %d')}"

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

def get_daily_motivation():
    """
    Returns a motivational phrase based on the current date
    """
    today = datetime.now()
    # Use the day of the month to select a phrase (0-29)
    phrase_index = (today.day - 1) % len(MOTIVATIONAL_PHRASES)
    return MOTIVATIONAL_PHRASES[phrase_index]

@app.route('/')
def index():
    current_day = get_current_day()
    today = get_today_date()
    days_since_august = days_since_august_first()
    business_days_remaining = business_days_until_july_31_2026()
    remaining_debt, amount_paid, percentage_paid, daily_payment = calculate_remaining_bcg_debt()
    daily_motivation = get_daily_motivation()
    
    return render_template('index.html',
                         current_day=current_day,
                         today=today,
                         days_since_august=days_since_august,
                         business_days_remaining=business_days_remaining,
                         daily_payment=f"{daily_payment:,.2f}",
                         amount_paid=f"{amount_paid:,.2f}",
                         percentage_paid=f"{percentage_paid:.1f}",
                         remaining_debt=f"{remaining_debt:,.2f}",
                         daily_motivation=daily_motivation)

if __name__ == "__main__":
    app.run(debug=True)
