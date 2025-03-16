from datetime import datetime
from pytz import timezone

india_tz = timezone('Asia/Kolkata')
current_time_india = datetime.now(india_tz)
def get_current_period(ctime):
    # Define the periods
    periods = [
        "9:05:00 - 10:00:00", "10:00:00 - 10:55:00", "10:55:00 - 11:50:00",
        "11:50:00 - 12:45:00", "12:45:00 - 1:40:00", "1:40:00 - 2:35:00",
        "2:35:00 - 3:30:00", "3:30:00 - 4:25:00"
    ]

    current_time = current_time_india.time()

    for i, period in enumerate(periods, start=1):
        start_time, end_time = period.split(" - ")
        start_time = datetime.strptime(start_time, "%H:%M:%S").time()
        end_time = datetime.strptime(end_time, "%H:%M:%S").time()

        if start_time <= current_time <= end_time:
            return f"Currently in Period {i}"

    return "Not within any period"


# Get the current time in the format HH:MM:SS
current_time = datetime.now().strftime("%H:%M:%S")


# Call the function with the current time
current_period = get_current_period(current_time)
print(current_period)
