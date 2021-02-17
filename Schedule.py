import datetime as dt
import argparse
import yaml
import textwrap


class Calendar:
    def __init__(self, start, end, classdays):
        date = start
        self.days = []
        while date <= end:
            if date.weekday() in classdays:
                self.days.append(Day(date))
            date += dt.timedelta(1)

    def __repr__(self):
        output = ""
        weeks_included = []
        self.days.sort(key=lambda day: day.date)
        for day in self.days:
            if day.weeknum not in weeks_included:
                output += "-" * 23 + "\n"
                weeks_included.append(day.weeknum)
            output += str(day) + "\n"
        return output

    def add_extra_days(self, date_list):
        self.days.extend([Day(d) for d in date_list])

    def assign_holidays(self, vacation_dict):
        # Set certain days to holidays
        for day in self.days:
            if day.date in vacation_dict.keys():
                day.day_off(vacation_dict[day.date])

    def assign_fixed(self, fixed_list, is_important=False):
        for activity in fixed_list:
            idx = [day.date for day in self.days].index(activity["date"])
            self.days[idx].assign_topic(
                Topic(**activity, duration=1, important=is_important)
            )

    def assign_topics(self, topic_list):
        __days = self.days.copy()
        __topics = topic_list.copy()
        for t in __topics:
            for _ in range(t["duration"]):
                thisday = __days.pop(0)
                while not thisday.hasclass or thisday.topic is not None:
                    thisday = __days.pop(0)
                idx = self.days.index(thisday)
                self.days[idx].assign_topic(Topic(**t))

    def assign_events(self, event_list):
        for event in event_list:
            dates = [day.date for day in self.days]
            if event["date"] not in dates:
                self.days.append(Day(event["date"]))
                dates = [day.date for day in self.days]
            idx = dates.index(event["date"])
            self.days[idx].assign_event(event["description"])

    def generate_html(self, columns):
        """Outputs an html table to the screen. This can then be piped to saved
        however one might desire.

        This method feels cludgy and could almost certainly be greatly improved.
        """

        def format_Week(day):
            if new_week:
                week_str = r"<td rowspan='4'>{}</td>".format(week_count)
            else:
                week_str = ""
            return week_str

        def format_Date(day):
            return r"<td>{}</td>".format(day.date.strftime("%b %d"))

        def format_Chapter(day):
            if day.topic:
                if day.topic.chapter:
                    return r"<td>Ch {}</td>".format(day.topic.chapter)
            return "<td></td>"

        def format_Description(day):
            if not day.hasclass:
                return r"<td bgcolor=#005146>{}</td>".format(
                    day.topic.description if day.topic else day.description
                )
            if day.topic and day.topic.is_important:
                return r"<td bgcolor=#A20C00>{}</td>".format(
                    day.topic.description if day.topic else day.description
                )
            if day.topic:
                return r"<td>{}</td>".format(day.topic.description)
            return r"<td></td>"

        def format_Event(day):
            if len(day.events) > 0:
                return r"<td>{}</td>".format(", ".join(day.events))
            return "<td></td>"

        def print_day(day):
            func_lookup = {
                "Week": format_Week,
                "Date": format_Date,
                "Chapter": format_Chapter,
                "Description": format_Description,
                "Due": format_Event,
                "Lab": format_Event,
            }
            if new_week:
                if week_count > 0:
                    print("</tbody>")
                print("<tbody>")
            print("<tr>")
            for column in columns:
                if func_lookup[column](day):
                    print(func_lookup[column](day))
            print("</tr>\n")
            # if day.weekday == 'Friday':
            # print("</tbody>\n")

        def print_header():
            print("<tr>")
            for c in columns:
                print(r"<th>{}</th>".format(c))
            print("</tr>")

        self.days.sort(key=lambda day: day.date)
        print("+++")
        print('title = "Semester\'s Schedule"')
        print("date = 2019-08-21")
        print("+++")
        print("<br>")
        print("<center>")
        print("<table id='schedule'>")
        print_header()
        class_weeks = []
        week_count = 0
        for day in self.days:
            new_week = False
            if day.weeknum not in class_weeks:
                class_weeks.append(day.weeknum)
                new_week = True
                week_count += 1
            print_day(day)
        print("</tbody>")
        print("</table>")
        print("</center>")

    def generate_latex(self, columns):
        def format_Week(day):
            if day.weekday == "Monday":
                week_str = r"\multirow{{3}}{{*}}{{{}}}".format(week_count)
            else:
                week_str = ""
            return week_str

        def format_Date(day):
            return day.date.strftime("%b %d")

        def format_Chapter(day):
            if day.topic:
                if day.topic.chapter:
                    return r"Ch {}".format(day.topic.chapter)
            return ""

        def format_Description(day):
            if not day.hasclass:
                return r"\emph{{{}}}".format(
                    day.topic.description if day.topic else day.description
                )
            if day.topic and day.topic.is_important:
                return r"\textbf{{{}}}".format(
                    day.topic.description if day.topic else day.description
                )
            if day.topic:
                return day.topic.description
            return ""

        def format_Event(day):
            if len(day.events) > 0:
                return ", ".join(day.events)
            return ""

        def format_row(day):
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
                row += func_lookup[column](day)
                if column != columns[-1]:
                    row += r" & "
            row += r" \\"
            return row

        def make_header():
            row = r""
            for c in columns:
                row += c
                if c != columns[-1]:
                    row += " & "
            row += r" \\"
            return row

        self.days.sort(key=lambda day: day.date)
        print(r"\documentclass[varwidth]{standalone}")
        print(r"\usepackage{booktabs,multirow,longtable}")
        print(r"\begin{document}")
        print(r"\begin{longtable}{ccccc}")
        print(r"\toprule")
        print(make_header())
        print(r"\midrule")
        print(r"\endhead")
        week_count = 1
        for day in self.days:
            print(format_row(day))
            if day.weekday == "Friday":
                week_count += 1
                print(r"\midrule")
        print(r"\bottomrule")
        print(r"\end{longtable}")
        print(r"\end{document}")


class Day:
    semester_start_week = 0

    def __init__(self, date):
        self.date = date
        self.hasclass = True
        self.holiday = False
        self.weekday = date.strftime("%A")
        self.weeknum = int(date.strftime("%W"))
        if self.semester_start_week == 0:
            Day.semester_start_week = self.weeknum
        self.semester_week = self.weeknum - self.semester_start_week + 1
        self.topic = None
        self.description = None
        self.events = []

    def __repr__(self):
        if self.topic:
            msg = self.topic.description
        elif self.description:
            msg = self.description
        else:
            msg = ""
        if len(self.events) > 0:
            due = '(' + ', '.join(self.events) + ')'
        else:
            due = ""
        return f"{self.weekday:10s} ({self.date}): {msg:40s} {due}"

    def day_off(self, description):
        """Makes a day a holiday!"""
        self.hasclass = False
        self.description = description
        self.holidary = True

    def assign_topic(self, topic):
        """Assigns a topic to a day and updates the topic"""
        self.topic = topic
        topic.set_day(self.date)

    def assign_event(self, event_name):
        """Adds an event to a given day"""
        self.events.append(event_name)


class Topic:
    def __init__(
        self, description, duration, date=None, ch=None, important=False, **kwargs
    ):
        self.chapter = ch
        self.description = description
        self.duration = duration
        self.is_important = important
        if date:
            self.days = [date]
        else:
            self.days = []

    def set_day(self, date):
        """Set days a topic is assigned to be covered."""
        self.days.append(date)


def read_config(filename: str) -> dict:
    with open(filename, "r") as f:
        config = yaml.full_load(f)
    return config


def main(filename):
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
            C.assign_topics(config[key]["values"])
    for key in config:
        if config[key].get("type", None) == "event":
            C.assign_events(config[key]["values"])
    return C, config


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("class_config", help="Config file with class information", type=str)
    ap.add_argument(
        "--latex", action="store_true", help="Flag to specify latex output to stdout"
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
    else:
        print(calendar)
