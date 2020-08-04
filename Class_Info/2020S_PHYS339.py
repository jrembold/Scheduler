import datetime as dt

start_date = dt.date(2020, 1, 21)
end_date = dt.date(2020, 5, 4)
classdays = [0,2,4] #MWF
vac_dates = {
    # dt.date(2020, 1, 24): 'MLK Celebration',
    dt.date(2020, 3, 23): "Spring Break",
    dt.date(2020, 3, 25): "Spring Break",
    dt.date(2020, 3, 27): "Spring Break",
    dt.date(2020, 4, 22): "SSRD",
}
extra_dates = [dt.date(2020, 5, 12)]

topics = [
    {"ch": 1, "description": "Newton's Laws of Motion", "duration": 2},
    {"ch": 2, "description": "Projectiles and Charged Particles", "duration": 2},
    {"ch": 3, "description": "Momentum and Angular Momentum", "duration": 2},
    {"ch": 4, "description": "Energy", "duration": 3},
    {"ch": 5, "description": "Oscillations", "duration": 2},
    {"ch": 6, "description": "Calculus of Variations", "duration": 1},
    {"ch": 7, "description": "Lagranges Equations", "duration": 4},
    {"ch": 8, "description": "Two-Body Central Force Problems", "duration": 2},
    {"ch": 9, "description": "Mechanics in Noninertial Frames", "duration": 2},
    {"ch": 10, "description": "Rotational Motion of Rigid Bodies", "duration": 4},
    {"ch": 11, "description": "Coupled Oscillators", "duration": 4},
    {"ch": "", "description": "Final Project Readings", "duration": 1},
]

#Using as compdays
tests = [
        {"description": "CompDay 1: Intro", "date":dt.date(2020,1,27)},
        {"description": "CompDay 2: Projectile Motion", "date":dt.date(2020,2,3)},
        {"description": "CompDay 3: Rockets", "date":dt.date(2020,2,10)},
        {"description": "CompDay 4: Sympy and Energy", "date":dt.date(2020,2,17)},
        {"description": "CompDay 5: 2D Oscillators", "date":dt.date(2020,2,24)},
        {"description": "CompDay 6: Fourier Series", "date":dt.date(2020,3,2)},
        {"description": "CompDay 7: Lagrangians with Sympy", "date":dt.date(2020,3,9)},
        {"description": "CompDay 8: Binary Star Orbits", "date":dt.date(2020,3,18)},
        {"description": "CompDay 9: Hohmann Tranfers", "date":dt.date(2020,3,30)},
        {"description": "CompDay 10: Coriolis Merry-Go-Round", "date":dt.date(2020,4,6)},
        {"description": "CompDay 11: Inertial Tensors", "date":dt.date(2020,4,13)},
        {"description": "CompDay 12: Visualizing Oscillation Modes", "date":dt.date(2020,4,27)},
        {"description": "Final", "date": dt.date(2020,5,12)},
]

hw = [
        {"description": "HW1", "date": dt.date(2020, 1, 27)},
        {"description": "CompDay 1", "date": dt.date(2020, 1, 29)},
        {"description": "HW2", "date": dt.date(2020, 2, 3)},
        {"description": "CompDay 2", "date": dt.date(2020, 2, 5)},
        {"description": "HW3", "date": dt.date(2020, 2, 10)},
        {"description": "CompDay 3", "date": dt.date(2020, 2, 12)},
        {"description": "HW4", "date": dt.date(2020, 2, 17)},
        {"description": "CompDay 4", "date": dt.date(2020, 2, 19)},
        {"description": "HW5", "date": dt.date(2020, 2, 24)},
        {"description": "CompDay 5", "date": dt.date(2020, 2, 26)},
        {"description": "HW6", "date": dt.date(2020, 3, 2)},
        {"description": "CompDay 6", "date": dt.date(2020, 3, 4)},
        {"description": "CompDay 7", "date": dt.date(2020, 3, 11)},
        {"description": "HW7", "date": dt.date(2020, 3, 16)},
        {"description": "CompDay 8", "date": dt.date(2020, 4, 1)},
        {"description": "HW8", "date": dt.date(2020, 3, 30)},
        {"description": "CompDay 9", "date": dt.date(2020, 4, 1)},
        {"description": "HW9", "date": dt.date(2020, 4, 6)},
        {"description": "CompDay 10", "date": dt.date(2020, 4, 8)},
        {"description": "CompDay 11", "date": dt.date(2020, 4, 15)},
        {"description": "HW10", "date": dt.date(2020, 4, 20)},
        {"description": "CompDay 12", "date": dt.date(2020, 4, 29)},
        {"description": "HW11", "date": dt.date(2020, 4, 29)},
        # descriptions
        {"description": "Midterm", "date": dt.date(2020, 3, 20)},
        {"description": "Final", "date": dt.date(2020, 5, 12)},
]

columns = ["Week", "Date", "Chapter", "Description", "Due"]
