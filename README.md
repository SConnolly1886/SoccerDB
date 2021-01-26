# SoccerDB
Soccer Database that stores statistics from English FA 1993-present
# footiescraper.py
![scraper](https://user-images.githubusercontent.com/62077185/105781790-2ac50500-5f41-11eb-9e37-8b8b26a45374.JPG)
Downloads Seasons of Soccer/Football based on user input. The program renames files based on division and season (example file E0 is converted to 'Premier League 0304') and adds them to one of 2 folders. 'Footie' and oldfootie'. 
![scraper2](https://user-images.githubusercontent.com/62077185/105781823-3c0e1180-5f41-11eb-8992-fa51e9c51ff1.JPG)
# footeparser.py and oldfootieparser.py 
Both files parse the data. SQLAlchemy is used. The data is split depending on the season and assigned to the appropriate database. In the years before the 2002/2003 season no statistics for gambling odds were saved so that data is stored in a different database with less info. (matchData.db has all seasons from 2002/2003-present, OldmatchData.db has seasons from 1993/1994-2001/2002).
![parser](https://user-images.githubusercontent.com/62077185/105781895-5fd15780-5f41-11eb-86a9-618446d9fd34.JPG)
# footiesql.py
Program that executes queries for both databases. Made possible by using two sessions (SQLAlchemy). Results are displayed using ascii escape colours (when defined)
![db1](https://user-images.githubusercontent.com/62077185/105781881-5cd66700-5f41-11eb-8758-266fb1b0f228.jpg)
![db2](https://user-images.githubusercontent.com/62077185/105781885-5e079400-5f41-11eb-9258-944b251f4c1b.JPG)
# teamcolours.py  
Contains the ascii escape colours for all of the teams in the English FA. (Premier League, Championship, League One, League Two, Conference, Divsion One, Division Two and Division Three)

