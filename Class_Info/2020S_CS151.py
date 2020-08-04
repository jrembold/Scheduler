import datetime as dt

start_date = dt.date(2020, 1, 21)
end_date = dt.date(2020, 5, 4)
vac_dates = {
        dt.date(2020, 1, 24): 'MLK Celebration',
        dt.date(2020, 3, 23): 'Spring Break',
        dt.date(2020, 3, 25): 'Spring Break',
        dt.date(2020, 3, 27): 'Spring Break',
        dt.date(2020, 4, 22): 'SSRD',
}
extra_dates = [dt.date(2020,5,8)]

topics = [
        {'ch': 1,       'desc': 'Introduction',             'duration': 1},
        {'ch': 2,       'desc': 'Coding Basics',            'duration': 4},
        {'ch': '',       'desc': 'Intro to Arcade',            'duration': 1},
        {'ch': 3,       'desc': 'Simple Programs',          'duration': 5},
        {'ch': 4,       'desc': 'Functions',                'duration': 6},
        {'ch': 5,       'desc': 'Lists and Dictionaries',   'duration': 5},
        {'ch': '',       'desc': 'String Formatting',   'duration': 1},
        {'ch': 8,       'desc': 'Classes',                  'duration': 6},
        # {'ch': 10,      'desc': 'Common Algorithms',        'duration': 5},
        {'ch': 11,      'desc': 'Visualization',            'duration': 2},
        {'ch': '',      'desc': 'Animation and Game Control',   'duration': 2},
        {'ch': '',      'desc': 'Organizing Group Programming',   'duration': 1},
        {'ch': '',      'desc': 'Digital Dodgeball',   'duration': 1},
        {'ch': '',      'desc': 'Projects',                 'duration': 3},
        {'ch': '',      'desc': 'Presentations',                 'duration': 1},
]

tests = [
        {'name': 'Midterm', 'date': dt.date(2020,3,20)},
        {'name': 'Final', 'date': dt.date(2020,5,8)},
]

hw = [
        {'name':'HW 1', "due": dt.date(2020,1,31)},
        {'name':'HW 2', "due": dt.date(2020,2,7)},
        {'name':'HW 3', "due": dt.date(2020,2,14)},
        {'name':'HW 4', "due": dt.date(2020,2,21)},
        {'name':'HW 5', "due": dt.date(2020,2,28)},
        {'name':'HW 6', "due": dt.date(2020,3,6)},
        {'name':'HW 7', "due": dt.date(2020,3,13)},
        {'name':'HW 8', "due": dt.date(2020,4,3)},
        {'name':'HW 9', "due": dt.date(2020,4,10)},
        {'name':'HW 10', "due": dt.date(2020,4,17)},
]

columns = ['Week', 'Date', 'Chapter', 'Description', 'Due']
