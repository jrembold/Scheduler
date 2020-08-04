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
extra_dates = [dt.date(2019,12,13)]

topics = [
        {'ch': 1,       'desc': 'Science and the Universe',             'duration': 1},
        {'ch': 2,       'desc': 'Observing the Sky',            'duration': 3},
        {'ch': 3,       'desc': 'Orbits and Gravity',          'duration': 2},
        {'ch': 4,       'desc': 'Earth and Sky',                'duration': 2},
        {'ch': 5,       'desc': 'Radiation and Spectra',   'duration': 3},
        {'ch': 6,       'desc': 'Astronomical Instruments',                  'duration': 1},
        {'ch': 7,      'desc': 'Intro to the Solar System',        'duration': 1},
        {'ch': 8,      'desc': 'Earth as a Planet',            'duration': 1},
        {'ch': 9,      'desc': 'Cratered Worlds',                 'duration': 1},
        {'ch': 11,      'desc': 'The Giant Planets',                 'duration': 1},
        {'ch': 12,      'desc': 'Rings, Moons, and Pluto',                 'duration': 1},
        {'ch': 13,      'desc': 'Comets and Asteroids',                 'duration': 2},
        {'ch': 14,      'desc': 'Origin of the Solar System',                 'duration': 1},
        {'ch': 15,      'desc': 'A Garden Variety Star',                 'duration': 2},
        {'ch': 16,      'desc': 'A Nuclear Powerhouse',                 'duration': 1},
        {'ch': 17,      'desc': 'Analyzing Starlight',                 'duration': 1},
        {'ch': 18,      'desc': 'A Celestial Census',                 'duration': 1},
        {'ch': 20,      'desc': 'Celestial Distances',                 'duration': 1},
        {'ch': 21,      'desc': 'Birth of Stars',                 'duration': 1},
        {'ch': 22,      'desc': 'Adolescence to Old Age',                 'duration': 1},
        {'ch': 23,      'desc': 'Death of Stars',                 'duration': 1},
        {'ch': 24,      'desc': 'Black Holes and Curved Spacetime',                 'duration': 1},
        {'ch': 25,      'desc': 'The Milky Way Galaxy',                 'duration': 2},
        {'ch': 26,      'desc': 'Galaxies',                 'duration': 2},
        {'ch': 29,      'desc': 'The Big Bang',                 'duration': 2},
        {'ch': 30,      'desc': 'Life in the Universe',                 'duration': 1},
]

tests = [
        {'name': 'Exam 1 (Ch 1-6)', 'date': dt.date(2019,9,27)},
        {'name': 'Exam 2 (Ch 7-14)', 'date': dt.date(2019,10,25)},
        {'name': 'Exam 3 (Ch 15-24)', 'date': dt.date(2019,11,15)},
        {'name': 'Final', 'date': dt.date(2019,12,13)},
]

hw = [
]

columns = ['Week', 'Date', 'Chapter', 'Description']
