import datetime as dt

start_date = dt.date(2020, 1, 21)
end_date = dt.date(2020, 5, 4)
vac_dates = {
    # dt.date(2020, 1, 24): 'MLK Celebration',
    dt.date(2020, 3, 23): "Spring Break",
    dt.date(2020, 3, 25): "Spring Break",
    dt.date(2020, 3, 27): "Spring Break",
    dt.date(2020, 4, 22): "SSRD",
}
extra_dates = [dt.date(2020, 5, 9)]

topics = [
    {"ch": "", "desc": "Intro and Review", "duration": 1},
    {"ch": 13, "desc": "The Electric Field", "duration": 3},
    {"ch": 14, "desc": "Electric Fields and Matter", "duration": 3},
    {"ch": 15, "desc": "Electric Field and Distributed Charges", "duration": 4},
    {"ch": 16, "desc": "Electric Potential", "duration": 4},
    {"ch": 17, "desc": "Magnetic Field", "duration": 3},
    {"ch": 18, "desc": "Electric Field and Circuits", "duration": 3},
    {"ch": 19, "desc": "Circuit Elements", "duration": 3},
    {"ch": 20, "desc": "Magnetic Force", "duration": 3},
    {"ch": 21, "desc": "Patterns in Fields in Space", "duration": 3},
    {"ch": 22, "desc": "Faraday's Law", "duration": 1},
    {"ch": 23, "desc": "Electromagnetic Radiation", "duration": 3},
    {"ch": "S3", "desc": "Waves", "duration": 3},
    {"ch": "", "desc": "Review Day", "duration": 1},
]

tests = [
    {"name": "Test 1 (Ch 13--15)", "date": dt.date(2020, 2, 21)},
    {"name": "Test 2 (Ch 16--19)", "date": dt.date(2020, 3, 20)},
    {"name": "Test 3 (Ch 20--23)", "date": dt.date(2020, 4, 24)},
    {"name": "Final", "date": dt.date(2020, 5, 9)},
]

# Treat as Lab
hw = [
    {"name": "Glowscript Review", "due": dt.date(2020, 1, 29)},
    {"name": "Electric Field and Forces", "due": dt.date(2020, 2, 5)},
    {"name": "Electric Dipole Field", "due": dt.date(2020, 2, 12)},
    {"name": "Distributed Charges", "due": dt.date(2020, 2, 19)},
    {"name": "Potential Difference", "due": dt.date(2020, 2, 26)},
    {"name": "Magnetic Field", "due": dt.date(2020, 3, 4)},
    {"name": "Magnetic Dipoles and Energy in Circuits", "due": dt.date(2020, 3, 11)},
    {"name": "DC Circuits", "due": dt.date(2020, 3, 18)},
    {"name": "Gap Week", "due": dt.date(2020, 4, 1)},
    {"name": "Magnetic Force", "due": dt.date(2020, 4, 8)},
    {"name": "Faraday's Law", "due": dt.date(2020, 4, 15)},
    {"name": "Lenses", "due": dt.date(2020, 4, 22)},
    {"name": "Interference", "due": dt.date(2020, 4, 29)},
]

columns = ["Week", "Date", "Chapter", "Description", "Lab"]
