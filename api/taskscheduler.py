from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .models import Task  # your Task model

from .models import Task, Reminder

def send_due_date_reminders():
    now = timezone.now().date()
    reminder_day = now + timezone.timedelta(days=1)
    
    tasks = Task.objects.filter(due_date=reminder_day, is_completed=False)

    for task in tasks:
        Reminder.objects.create(
            user=task.user,
            task=task,
            message=f"Task '{task.title}' is due tomorrow!"
        )
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_due_date_reminders, "interval", hours=24)
    scheduler.start()

def stop_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.shutdown()
    scheduler = None
    print("Scheduler stopped.")