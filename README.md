# SoccerDB
Soccer Database that stores statistics from English FA 1993-present
# footiescraper.py
Downloads Seasons of Soccer/Football based on user input. The program renames files based on division and season (example file E0 is converted to 'Premier League 0304') and adds them to one of 2 folders. 'Footie' and oldfootie'. 
# footeparser.py and # oldfootieparser.py 
Both files parse the data. SQLAlchemy is used. The data is split depemnding on the season and assigned to the appropriate database. In the years before the 2002/2003 season no statistics for gambling odds were saved so that data is stored in a different database with less info. (matchData.db has all seasons from 2002/2003-present, OldmatchData.db has seasons from 1993/1994-2001/2002).
# footiesql.py
Program the executes queries for both databases. Made possible by using two sessions (SQLAlchemy). Results are displauyed using ascii escape colours (when defined)
# teamcolours.py  
containts the ascii escape colours for all of the teams in the english FA. (Premier League, Championship, League One, League Two, Conference, Divsion One, Division Two and Division Three)
