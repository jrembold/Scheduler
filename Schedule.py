import datetime as dt
import argparse
import yaml
from rich import print
from rich.table import Table
from typing import TypedDict

# Type hinting classes or aliases
Date = dt.datetime


class Event(TypedDict):
    description: str
    date: Date


class TopicType(TypedDict):
    ch: str
    description: str
    duration: int


# Main code


class Calendar:
    """
    Creates a new calendar object, in which a schedule is stored.
    """

    def __init__(self, start: Date, end: Date, classdays: list[int]) -> None:
        """
        Initializes a list of Days corresponding to class days.
        """
        date = start
        self.days = []  # type: list[Day]
        self.classdays = classdays  # for later reference
        while date <= end:
            if date.weekday() in classdays:
                if date.weekday() == classdays[0]:
                    self.days.append(Day(date, new_week=True))
                else:
                    self.days.append(Day(date))
            date += dt.timedelta(1)

    def __repr__(self) -> str:
        """
        Prints out a nice ascii summary of the schedule.
        """
        output = ""
        # Sort since days may have been added out of order
        self.days.sort(key=lambda day: day.date)
        weeks_included = []  # type: list[int]
        for day in self.days:
            if day.weeknum not in weeks_included:
                output += "-" * 23 + "\n"
                weeks_included.append(day.weeknum)
            output += str(day) + "\n"
        return output

    def print_rich_table(self) -> None:
        tab = Table(title="Schedule")
        tab.add_column("Week", justify="center")
        tab.add_column("Weekday")
        tab.add_column("Date")
        tab.add_column("Topics")
        tab.add_column("Due")
        self.days.sort(key=lambda day: day.date)
        for day in self.days:
            # Extract information from topic(s)
            if len(day.topic):
                if len(day.topic) > 1:
                    desc = "\n".join(
                        [f"{top}: {day.topic[top].description}" for top in day.topic]
                    )
                else:
                    desc = "\n".join(
                        [f"{day.topic[top].description}" for top in day.topic]
                    )
                is_important = any([day.topic[top].is_important for top in day.topic])
            else:
                desc = day.description
                is_important = False
            # Set coloring
            color = "default"
            if is_important:
                color = "bold red"
            elif day.weeknum % 2:
                color = "green"
            # Add the actual data to the row
            tab.add_row(
                f"[{color}]{day.semester_week if day.new_week else ''}",
                f"[{color}]{day.weekday}",
                f"[{color}]{str(day.date)}",
                f"[{color}]{desc if desc else ''}",
                f"[{color}]{','.join([e for e in day.events])}",
            )

        print(tab)

    def add_extra_days(self, date_list: list[Date]) -> None:
        """
        Adds extra dates to the schedule. Frequently non-lecture
        days as they should have already been added initially.
        """
        self.days.extend([Day(d) for d in date_list])
        self.mark_new_weeks()

    def mark_new_weeks(self) -> None:
        possible_weeks = set(day.weeknum for day in self.days)
        for day in self.days:
            if day.weeknum in possible_weeks:
                day.new_week = True
                possible_weeks.discard(day.weeknum)

    def assign_holidays(self, vacation_dict: dict[Date, str]) -> None:
        """
        Sets specified days already in calendar to vacation days.
        """
        for day in self.days:
            if day.date in vacation_dict.keys():
                day.day_off(vacation_dict[day.date])

    def assign_fixed(self, fixed_list: list[Event], is_important: bool = False) -> None:
        """
        Assigns activities which come on determined dates (like tests) to the
        correct date on the calendar.
        """
        for activity in fixed_list:
            idx = [day.date for day in self.days].index(activity["date"])
            self.days[idx].assign_topic(
                Topic(**activity, duration=1, important=is_important),
                topic_name="fixed",
            )

    def assign_topics(self, topic_list: list[TopicType], topic_name: str) -> None:
        """
        Goes through the list of topics and assigns the correct number of
        available days to each topic in sequential order.
        """
        __days = self.days.copy()
        __topics = topic_list.copy()
        for t in __topics:
            used = 0
            while used < t["duration"]:
                # for _ in range(t["duration"]):
                thisday = __days.pop(0)
                while (
                    not thisday.hasclass
                    or thisday.topic.get(topic_name) is not None
                    or thisday.topic.get("fixed")
                ):
                    thisday = __days.pop(0)
                idx = self.days.index(thisday)
                self.days[idx].assign_topic(Topic(**t), topic_name)
                used += 1

    def assign_events(self, event_list: list[Event]) -> None:
        """
        Adds extra events to the calendar. These are not generally lecture
        days, but instead things like homework deadlines, labs, or
        announcements.
        """
        for event in event_list:
            dates = [day.date for day in self.days]
            if event["date"] not in dates:
                self.days.append(Day(event["date"]))
                dates = [day.date for day in self.days]
            idx = dates.index(event["date"])
            self.days[idx].assign_event(event["description"])

    def reassign_new_weeks(self) -> None:
        """ Goes back through dates and reassigns new week tags as necessary. """
        encountered_weeks = []
        self.days.sort(key=lambda day: day.date) # get dates in chrono order
        for day in self.days:
            if day.semester_week not in encountered_weeks:
                day.new_week = True
                encountered_weeks.append(day.semester_week)
            else:
                day.new_week = False

    def generate_html(self, columns: list[str]) -> None:
        """Outputs an html table to the screen. This can then be piped to saved
        however one might desire.

        This method feels cludgy and could almost certainly be greatly improved.
        """

        def format_Week(day: Day, topic_num: int = 0) -> str:
            if topic_num == 0 and day.new_week:
                return r"<td rowspan='{}'>{}</td>".format(
                    week_num_topics, day.semester_week
                )
            return ""

        def format_Date(day: Day, topic_num: int = 0) -> str:
            if len(day.topic) <= 1:
                return r"<td>{}</td>".format(day.date.strftime("%b %d"))
            elif topic_num == 0:
                return r"<td rowspan='{}'>{}</td>".format(
                    len(day.topic) if day.topic else 1, day.date.strftime("%b %d")
                )
            return ""

        def format_Chapter(day: Day, topic_num: int = 0) -> str:
            if len(day.topic) > 0:
                topics = sorted([top for top in day.topic])
                chap = day.topic[topics[topic_num]].chapter
                if chap and len(day.topic) > 1:
                    return r"<td>{}: Ch {}</td>".format(topics[topic_num], chap)
                elif chap:
                    return r"<td>Ch {}</td>".format(chap)

            return r"<td></td>"

        def format_Description(day: Day, topic_num: int = 0) -> str:
            if len(day.topic) > 0:
                topics = sorted([top for top in day.topic])
                topic = day.topic[topics[topic_num]]
            else:
                topic = None

            if not day.hasclass:
                return r"<td bgcolor=#005146>{}</td>".format(
                    topic.description if topic else day.description
                )
            if topic and topic.is_important:
                return r"<td bgcolor=#A20C00>{}</td>".format(
                    topic.description if topic else day.description
                )
            if topic:
                return r"<td>{}</td>".format(topic.description)
            return r"<td></td>"

        def format_Event(day: Day, topic_num: int = 0) -> str:
            if topic_num == 0:
                return r"<td>{}</td>".format(", ".join(day.events))
            return "<td></td>"

        def format_row(day: Day, topic_num: int = 0) -> str:
            func_lookup = {
                "Week": format_Week,
                "Date": format_Date,
                "Chapter": format_Chapter,
                "Description": format_Description,
                "Due": format_Event,
                "Lab": format_Event,
            }
            row = "<tr>"
            for column in columns:
                row += "\n"
                row += func_lookup[column](day, topic_num)
            row += "\n</tr>\n"
            return row

        def print_day(day: Day) -> str:
            output = ""
            if len(day.topic) > 0:
                for i in range(len(day.topic)):
                    row = format_row(day, topic_num=i)
                    output += row
            else:
                row = format_row(day)
                output += row
            return output

        def print_header() -> None:
            print("<tr>")
            for c in columns:
                print(r"<th>{}</th>".format(c))
            print("</tr>")

        self.days.sort(key=lambda day: day.date)
        print("+++")
        print('title = "Semester\'s Schedule"')
        print("date =", dt.datetime.now().strftime("%Y-%m-%d"))
        print("+++")
        print("<br>")
        print("<center>")
        print("<table id='schedule'>")
        print_header()
        for i, day in enumerate(self.days):
            curr_week = day.semester_week
            week_num_topics = sum(
                [
                    len(day.topic) if day.topic else 1
                    for day in self.days
                    if day.semester_week == curr_week
                ]
            )
            if day.new_week and i != 0:
                print("</tbody>")
            if day.new_week:
                print("<tbody>")
            print(print_day(day))
        print("</tbody>")
        print("</table>")
        print("</center>")

    def generate_latex(self, columns: list[str]) -> None:
        def format_Week(day: Day, topic_num: int = 0) -> str:
            week_str = ""
            if topic_num == 0:
                if day.new_week:
                    week_str = r"\multirow{{{}}}{{*}}{{{}}}".format(
                        week_num_topics, day.semester_week
                    )
            return week_str

        def format_Date(day: Day, topic_num: int = 0) -> str:
            output = ""
            if topic_num == 0:
                output = r"\multirow{{{}}}{{*}}{{{}}}".format(
                    len(day.topic) if day.topic else 1, day.date.strftime("%a, %b %d")
                )
                # output = day.date.strftime("%a, %b %d")
            return output

        def format_Chapter(day: Day, topic_num: int = 0) -> str:
            output = ""
            if len(day.topic) > 0:
                topics = sorted([top for top in day.topic])
                chap = day.topic[topics[topic_num]].chapter
                if chap and len(day.topic) > 1:
                    output = r"{}: Ch {}".format(topics[topic_num], chap)
                elif chap:
                    output = r"Ch {}".format(chap)
            return output

        def format_Description(day: Day, topic_num: int = 0) -> str:
            if len(day.topic) > 0:
                topics = sorted([top for top in day.topic])
                topic = day.topic[topics[topic_num]]
            else:
                topic = None
            if not day.hasclass:
                return r"\emph{{{}}}".format(
                    topic.description if topic else day.description
                )
            if topic and topic.is_important:
                return r"\textbf{{{}}}".format(
                    topic.description if topic else day.description
                )
            if topic:
                return topic.description
            return ""

        def format_Event(day: Day, topic_num: int = 0) -> str:
            output = ""
            if topic_num == 0:
                output = ", ".join(day.events)
            return output

        def format_row(day: Day, topic_num: int = 0) -> str:
            func_lookup = {
                "Week": format_Week,
                "Date": format_Date,
                "Chapter": format_Chapter,
                "Description": format_Description,
                "Due": format_Event,
                "Lab": format_Event,
            }
            row = r""
            for column in columns:
                row += func_lookup[column](day, topic_num)
                if column != columns[-1]:
                    row += r" & "
            row += r" \\"
            return row

        def make_header() -> str:
            row = r""
            for c in columns:
                row += c
                if c != columns[-1]:
                    row += " & "
            row += r" \\"
            return row

        def format_day(day: Day) -> str:
            output = r""
            if len(day.topic) > 0:
                for i in range(len(day.topic)):
                    row = format_row(day, topic_num=i)
                    row += "\n"
                    output += row
            else:
                row = format_row(day)
                row += "\n"
                output += row

            return output.strip()

        self.days.sort(key=lambda day: day.date)
        print(r"\documentclass[varwidth]{standalone}")
        print(r"\usepackage{booktabs,multirow,longtable}")
        print(r"\begin{document}")
        print(r"\begin{longtable}{ccccc}")
        print(r"\toprule")
        print(make_header())
        print(r"\midrule")
        print(r"\endhead")
        for i, day in enumerate(self.days):
            curr_week = day.semester_week
            week_num_topics = sum(
                [
                    len(day.topic) if day.topic else 1
                    for day in self.days
                    if day.semester_week == curr_week
                ]
            )
            if day.new_week and i != 0:
                print(r"\midrule")
            print(format_day(day))
        print(r"\bottomrule")
        print(r"\end{longtable}")
        print(r"\end{document}")

    def generate_json(self) -> list:
        class_weeks = []
        week_count = 0
        weeks = []
        days = []
        self.days.sort(key=lambda day: day.date)
        for day in self.days:
            new_week = False
            if day.weeknum not in class_weeks:
                class_weeks.append(day.weeknum)
                new_week = True
                week_count += 1
            if new_week:
                if len(days) > 0:
                    weeks.append(days)
                days = []
            topic = day.topic
            if len(topic) < 1:
                chapter = ""
                description = day.description
                important = False
                js_day = {
                    "date": str(day.date),
                    "topic": None,
                    "chapter": chapter,
                    "description": description,
                    "important": important,
                    "events": day.events,
                }
                days.append(js_day)
            else:
                for top in topic:
                    chapter = topic[top].chapter
                    description = topic[top].description
                    important = topic[top].is_important
                    js_day = {
                        "date": str(day.date),
                        "topic": top,
                        "chapter": chapter,
                        "description": description,
                        "important": important,
                        "events": day.events,
                    }
                    days.append(js_day)
        # Add last remaining week
        weeks.append(days)
        print(weeks)
        return weeks


class Day:
    """
    Represents a single day in a calendar.
    """

    semester_start_week = 0

    def __init__(self, date: Date, new_week: bool = False):
        self.date = date
        self.hasclass = True
        self.holiday = False
        self.weekday = date.strftime("%A")
        self.weeknum = int(date.strftime("%U"))
        if Day.semester_start_week == 0:
            Day.semester_start_week = self.weeknum
        self.semester_week = self.weeknum - self.semester_start_week + 1
        self.topic: dict[str, "Topic"] = {}
        self.description = None
        self.events = []  # type: list[str]
        self.new_week = new_week

    def __repr__(self) -> str:
        """
        Returns a string summary of what occurs or is scheduled for that day.
        """
        if len(self.topic):
            msg = "\n".join(
                [self.topic[topic].description for topic in self.topic.keys()]
            )
        elif self.description:
            msg = self.description
        else:
            msg = ""
        if len(self.events) > 0:
            due = "(" + ", ".join(self.events) + ")"
        else:
            due = ""
        return f"{self.weekday:10s} ({self.date}): {msg:40s} {due}"

    def day_off(self, description: str):
        """Makes a day a holiday!"""
        self.hasclass = False
        self.description = description
        self.holiday = True

    def assign_topic(self, topic: "Topic", topic_name: str):
        """Assigns a topic to a day and updates the topic"""
        self.topic[topic_name] = topic
        topic.set_day(self.date)

    def assign_event(self, event_name: str):
        """Adds an event to a given day"""
        self.events.append(event_name)


class Topic:
    """
    Represents a topic to be taught.
    """

    def __init__(
        self,
        description: str,
        duration: int,
        date: Date = None,
        ch: str = None,
        important: bool = False,
    ):
        self.chapter = ch
        self.description = description
        self.duration = duration
        self.is_important = important
        if date:
            self.days = [date]
        else:
            self.days = []

    def set_day(self, date: Date) -> None:
        """Set days a topic is assigned to be covered."""
        self.days.append(date)


def read_config(filename: str) -> dict:
    with open(filename, "r") as f:
        config = yaml.full_load(f)
    return config


def main(filename: str) -> tuple[Calendar, dict]:
    """
    Reads in the given configuration file and generates the schedule.
    """
    config = read_config(filename)
    C = Calendar(
        config["calendar_info"]["start_date"],
        config["calendar_info"]["end_date"],
        config["calendar_info"]["class_days"],
    )
    if "extra_dates" in config["calendar_info"]:
        C.add_extra_days(config["calendar_info"]["extra_dates"])
    if "holiday_dates" in config["calendar_info"]:
        C.assign_holidays(config["calendar_info"]["holiday_dates"])
    for key in config:
        if config[key].get("type", None) == "fixed date":
            C.assign_fixed(config[key]["values"], config[key].get("important", False))
    for key in config:
        if config[key].get("type", None) == "topics":
            C.assign_topics(config[key]["values"], key)
    for key in config:
        if config[key].get("type", None) == "event":
            C.assign_events(config[key]["values"])

    C.reassign_new_weeks()

    return C, config


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("class_config", help="Config file with class information", type=str)
    ap.add_argument(
        "--latex", action="store_true", help="Flag to specify latex output to stdout"
    )
    ap.add_argument(
        "--json", action="store_true", help="Flag to specify json output to stdout"
    )

    ap.add_argument(
        "--html", action="store_true", help="Flag to specify latex output to stdout"
    )
    args = ap.parse_args()

    calendar, config = main(args.class_config)

    if args.latex:
        calendar.generate_latex(config["outputs"]["latex"]["columns"])
    elif args.html:
        calendar.generate_html(config["outputs"]["html"]["columns"])
    elif args.json:
        calendar.generate_json()
    else:
        print()
        calendar.print_rich_table()
