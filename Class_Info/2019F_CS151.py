import datetime as dt

start_date = dt.date(2019, 8, 26)
end_date = dt.date(2019, 12, 6)
vac_dates = {
        dt.date(2019, 9, 2): 'Labor Day',
        dt.date(2019, 10, 18): 'Midsemester Day',
        dt.date(2019, 11, 25): 'Thanksgiving',
        dt.date(2019, 11, 27): 'Thanksgiving',
        dt.date(2019, 11, 29): 'Thanksgiving',
}
extra_dates = [dt.date(2019,12,10)]

topics = [
        {'ch': 1,       'desc': 'Introduction',             'duration': 1},
        {'ch': 2,       'desc': 'Coding Basics',            'duration': 5},
        {'ch': 3,       'desc': 'Simple Programs',          'duration': 5},
        {'ch': 4,       'desc': 'Functions',                'duration': 6},
        {'ch': 5,       'desc': 'Lists and Dictionaries',   'duration': 5},
        {'ch': 8,       'desc': 'Classes',                  'duration': 7},
        {'ch': 10,      'desc': 'Common Algorithms',        'duration': 5},
        {'ch': 11,      'desc': 'Visualization',            'duration': 2},
        {'ch': '',      'desc': 'Projects',                 'duration': 3},
]

tests = [
        {'name': 'Midterm', 'date': dt.date(2019,10,25)},
        {'name': 'Final', 'date': dt.date(2019,12,10)},
]

hw = [
        {'name':'HW 1', "due": dt.date(2019,9,4)},
        {'name':'HW 2', "due": dt.date(2019,9,11)},
        {'name':'HW 3', "due": dt.date(2019,9,18)},
        {'name':'HW 4', "due": dt.date(2019,9,25)},
        {'name':'HW 5', "due": dt.date(2019,10,2)},
        {'name':'HW 6', "due": dt.date(2019,10,9)},
        {'name':'HW 7', "due": dt.date(2019,10,16)},
        {'name':'HW 8', "due": dt.date(2019,10,30)},
        {'name':'HW 9', "due": dt.date(2019,11,6)},
        {'name':'HW 10', "due": dt.date(2019,11,13)},
]

columns = ['Week', 'Date', 'Chapter', 'Description', 'Due']
