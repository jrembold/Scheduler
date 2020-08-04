import datetime as dt
import argparse
import importlib


def gen_lecture_dates(start_date, end_date, vac_dates, extra_dates):
    date = start_date
    mwf = [0, 2, 4]
    lecture_dates = []

    while date <= end_date:
        if date.weekday() in mwf:
            if date in vac_dates.keys():
                lecture_dates.append(Day(date, False, topic=Topic(vac_dates[date], 1)))
            else:
                lecture_dates.append(Day(date, True))
        date += dt.timedelta(1)
    lecture_dates.extend([Day(d, True) for d in extra_dates])
    return lecture_dates


def assign_class_topics(topics_list, days_list):
    # Be sure to run after test dates are assigned
    days_disposable = days_list.copy()
    topics_disposable = topics_list.copy()
    for t in topics_disposable:
        for d in range(t.duration):
            _day = days_disposable.pop(0)
            while not _day.haslecture or _day.topic is not None:
                _day = days_disposable.pop(0)
            t.days.append(_day)
            _day.topic = t


def assign_hw(hw_list, days_list):
    for hw in hw_list:
        idx = [d.date for d in days_list].index(hw["due"])
        days_list[idx].homework = hw["name"]


def assign_tests(test_list, days_list):
    for test in test_list:
        idx = [d.date for d in days_list].index(test["date"])
        days_list[idx].topic = Topic(desc=test["name"], duration=1, is_test=True)


def generate_latex(days_list):
    def format_Week(day):
        if day.weekday == "Monday":
            week_str = r"\multirow{{3}}{{*}}{{{}}}".format(week_count)
        else:
            week_str = ""
        return week_str

    def format_Date(day):
        return day.date.strftime("%b %d")

    def format_Chapter(day):
        if day.topic.chapter:
            return r"Ch {}".format(day.topic.chapter)
        return ""

    def format_Description(day):
        if not day.haslecture:
            return r"\emph{{{}}}".format(day.topic.description)
        if day.topic.is_test:
            return r"\textbf{{{}}}".format(day.topic.description)
        return day.topic.description

    def format_Due(day):
        if day.homework:
            return day.homework
        return ""

    def format_row(day):
        func_lookup = {
            "Week": format_Week,
            "Date": format_Date,
            "Chapter": format_Chapter,
            "Description": format_Description,
            "Due": format_Due,
            "Lab": format_Due,
        }
        row = r""
        for column in theclass.columns:
            row += func_lookup[column](day)
            if column != theclass.columns[-1]:
                row += r" & "
        row += r" \\"
        return row

    def make_header():
        row = r""
        for c in theclass.columns:
            row += c
            if c != theclass.columns[-1]:
                row += " & "
        row += r" \\"
        return row

    print(r"\documentclass{standalone}")
    print(r"\usepackage{booktabs,multirow}")
    print(r"\begin{document}")
    print(r"\begin{tabular}{ccccc}")
    print(r"\toprule")
    print(make_header())
    print(r"\midrule")
    week_count = 1
    for day in days_list:
        print(format_row(day))
        if day.weekday == "Friday":
            week_count += 1
            print(r"\midrule")
    print(r"\bottomrule")
    print(r"\end{tabular}")
    print(r"\end{document}")

def generate_html(days_list):
    def format_Week(day):
        if new_week:
            week_str = r"<td rowspan='3'>{}</td>".format(week_count)
        else:
            week_str = ""
        return week_str

    def format_Date(day):
        return r"<td>{}</td>".format(day.date.strftime("%b %d"))

    def format_Chapter(day):
        if day.topic.chapter:
            return r"<td>Ch {}</td>".format(day.topic.chapter)
        return "<td></td>"

    def format_Description(day):
        if not day.haslecture:
            return r"<td bgcolor=#005146>{}</td>".format(day.topic.description)
        if day.topic.is_test:
            return r"<td bgcolor=#A20C00>{}</td>".format(day.topic.description)
        return r"<td>{}</td>".format(day.topic.description)

    def format_Due(day):
        if day.homework:
            return r"<td>{}</td>".format(day.homework)
        return "<td></td>"

    def print_day(day):
        func_lookup = {
            "Week": format_Week,
            "Date": format_Date,
            "Chapter": format_Chapter,
            "Description": format_Description,
            "Due": format_Due,
            "Lab": format_Due,
        }
        if new_week:
            print("<tbody>")
        print("<tr>")
        for column in theclass.columns:
            if func_lookup[column](day):
                print(func_lookup[column](day))
        print("</tr>\n")
        if day.weekday == 'Friday':
            print("</tbody>\n")

    def print_header():
        print("<tr>")
        for c in theclass.columns:
            print(r"<th>{}</th>".format(c))
        print("</tr>")
    print('+++')
    print("title = \"Semester's Schedule\"")
    print("date = 2019-08-21")
    print("+++")
    print("<br>")
    print("<center>")
    print("<table id='schedule'>")
    print_header()
    class_weeks = []
    week_count = 0
    for day in days:
        new_week = False
        if day.weeknum not in class_weeks:
            class_weeks.append(day.weeknum)
            new_week =True
            week_count += 1
        print_day(day)
    print("</table>")
    print("</center>")







class Day:
    lecture_count = 0
    def __init__(self, date, haslecture=True, topic=None):
        self.date = date
        self.haslecture = haslecture
        if self.haslecture:
            Day.lecture_count += 1
            self.lecture_number = Day.lecture_count
        self.weekday = date.strftime("%A")
        self.weeknum = int(date.strftime("%W"))
        self.topic = topic
        self.homework = None

    def __str__(self):
        if self.weekday == "Monday":
            pre = "------\n"
        else:
            pre = ""
        if self.haslecture:
            return (
                pre
                + f"There is a lecture ({self.lecture_number}) on {self.topic} on {self.weekday}, {str(self.date)}."
            )
        else:
            return (
                pre
                + f"There is NOT a lecture on {self.weekday}, {str(self.date)}. It is {self.topic.description}."
            )


class Topic:
    def __init__(self, desc, duration: int, date=None, ch=None, is_test=False):
        self.chapter = ch
        self.description = desc
        self.duration = duration
        self.is_test = is_test
        if date:
            self.days = [date]
        else:
            self.days = []

    def __str__(self):
        return f"Ch {self.chapter}: {self.description}"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("thisclass", help="Config file with class information", type=str)
    ap.add_argument(
        "--latex", action="store_true", help="Flag to specify latex output to stdout"
    )

    ap.add_argument(
        "--html", action="store_true", help="Flag to specify latex output to stdout"
    )
    args = ap.parse_args()

    # Import in config file as module
    theclass = importlib.import_module(args.thisclass[:-3])

    # List of day classes
    days = gen_lecture_dates(
        theclass.start_date, theclass.end_date, theclass.vac_dates, theclass.extra_dates
    )

    # List of topic classes
    tps = [Topic(**i) for i in theclass.topics]

    # Assign topics to days
    if hasattr(theclass, 'tests'):
        assign_tests(theclass.tests, days)
    if hasattr(theclass, 'topics'):
        assign_class_topics(tps, days)
    if hasattr(theclass, 'hw'):
        assign_hw(theclass.hw, days)

    if args.latex:
        generate_latex(days)
    elif args.html:
        generate_html(days)
    else:
        print(*days, sep="\n")
