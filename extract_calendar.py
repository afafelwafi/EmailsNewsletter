import json
from nylas import APIClient
import pandas as pd
import datetime

f = open("config.json")
nylas_config = json.load(f)

nylas = APIClient(
    nylas_config["CLIENT_ID"],
    nylas_config["CLIENT_SECRET"],
    nylas_config["ACCESS_TOKEN"],
)
calendars = nylas.calendars.all()
CALENDER_ID = [
    calendar["id"] for calendar in calendars if "Calendrier" in calendar["name"]
][0]


def generate_fake_events(start_hour: int, end_hour: int, fake_email: str) -> None:
    today = datetime.date.today()
    # Today’s date at 12:00:00 am
    START_TIME = int(
        datetime.datetime(
            today.year, today.month, today.day, start_hour, 0, 0
        ).strftime("%s")
    )
    # Today’s date at 11:59:59 pm
    END_TIME = int(
        datetime.datetime(today.year, today.month, today.day, end_hour, 0, 0).strftime(
            "%s"
        )
    )
    # Create event draft
    event = nylas.events.create()
    # Define event elements
    event.title = "Work meeting"
    event.location = "Casablanca, Morocco"
    event.when = {"start_time": START_TIME, "end_time": END_TIME}
    event.participants = [{"name": "Blag", "email": fake_email}]
    event.calendar_id = CALENDER_ID
    # We would like to notify participants
    event.save(notify_participants=True)
    if event.id:
        print("Event created successfully")
    else:
        print("There was an error creating the event")


def extract_weekly_events() -> pd.DataFrame:
    # Get today’s date
    all_events = []
    today = datetime.date.today()
    next_week = datetime.date.today() + datetime.timedelta(days=7)
    # Today’s date at 12:00:00 am
    AFTER = int(
        datetime.datetime(today.year, today.month, today.day, 0, 0, 0).strftime("%s")
    )
    # End of week's date at 11:59:59 pm
    BEFORE = int(
        datetime.datetime(
            next_week.year, next_week.month, today.day, 23, 59, 59
        ).strftime("%s")
    )
    # Access and print all events information
    events = nylas.events.where(
        calendar_id=CALENDER_ID, starts_after=AFTER, ends_before=BEFORE
    )
    for event in events:
        # This is a event with an start and end date
        if "start_time" in event.when:
            all_events.append(
                {
                    "Title": event.title,
                    "Start": datetime.datetime.fromtimestamp(
                        event.when["start_time"]
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                    "End": datetime.datetime.fromtimestamp(
                        event.when["end_time"]
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                    "Participants": event.participants,
                }
            )

        # This an all-day event
        else:
            all_events.append(
                {
                    "Title": event.title,
                    "Start": event.when["date"],
                    "End": event.when["date"],
                    "Participants": event.participants,
                }
            )
    return pd.DataFrame(all_events)



if __name__ == "__main__":
    # Read your inbox and display the results
    events = extract_weekly_events()
    events.to_csv("events_corpus.csv")