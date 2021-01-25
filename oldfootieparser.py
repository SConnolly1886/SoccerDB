from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
import csv
import os


class TerminalColours:
    HEADER = '\033[95m'   # light magenta
    OKBLUE = '\033[94m'  # light blue
    WIN = '\033[92m'  # light # light green
    DRAW = '\033[93m'  # light yellow
    LOSS = '\033[91m'   # light red
    ERROR = '\033[31m'  # red
    ENDC = '\033[0m'  # reset
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'


# create 3 tables. games with generic information, teams and performances
# valid from 2002/2003 season to present

home_result_dict = {'H': 'W', 'D': 'D', 'A': 'L'}
away_result_dict = {'A': 'W', 'D': 'D', 'H': 'L'}
points_dict = {'W': 3, 'D': 1, 'L': 0}

# echoing seems to hang atom
engine = create_engine('sqlite:///OldmatchData.db', echo=False)

connection = engine.raw_connection()
cursor = connection.cursor()
command = "DROP TABLE IF EXISTS games; DROP TABLE IF EXISTS performances; DROP TABLE IF EXISTS teams;"
cursor.executescript(command)
connection.commit()
cursor.close()


'''callable returns a new base class from which all mapped classes should inherit.
When the class definition is completed, a new Table and mapper() will have been generated.'''
Base = declarative_base()

''' sqlalchemy is great with python and classes
first class will make games table. has basic stats including odds for the game.
Using classes in python and converting them to sql tables.'''


class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    season = Column(Integer)
    div = Column(String)
    date = Column(Date)
    home_id = Column(Integer, ForeignKey('performances.id'))
    away_id = Column(Integer, ForeignKey('performances.id'))
    ft_result = Column(String)
    ft_score = Column(String)
    ht_result = Column(String)
    ht_score = Column(String)

    def __repr__(self):
        return f'<Game(home_id={self.home_id}, away_id={self.away_id})>'


class Performance(Base):
    __tablename__ = "performances"
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    game_id = Column(Integer, ForeignKey('games.id'))
    ft_goals_for = Column(Integer)
    ft_result = Column(String)
    ht_goals_for = Column(Integer)
    ht_result = Column(String)
    venue = Column(String)
    week = Column(Integer)
    points = Column(Integer)
    gd = Column(Integer)


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True)
    name = Column(String)

# every season has new teams, add new teams/id for new seasons


def process_team(name, session):
    team = session.query(Team.id).filter(Team.name == name).one_or_none()
    if team is not None:
        return team[0]
    else:
        team = Team(**{'name': name})
        session.add(team)
        session.flush()
        session.refresh(team)
        return team.id


# access the metadata where newly defined tables objects are collected


Base.metadata.create_all(engine)

# from sqlalchemy
Session = sessionmaker(bind=engine)
session = Session()

# name of folder containing csv files
seasondata_folder = "oldfootie/"
# Number of Relevant columns, this time period has no odds provided
data_cols = 10

print(f'\n{TerminalColours.UNDERLINE}Uploading files to database:{TerminalColours.ENDC}')

arrows = f'{TerminalColours.OKBLUE}------------->{TerminalColours.ENDC}'

for csv_file in os.listdir(os.getcwd() + "/" + seasondata_folder):
    print(f'{arrows}{csv_file}')
    with open(seasondata_folder + csv_file, 'r') as f:
        reader = csv.reader(f)
        # skip first row, headers
        header = next(reader)
        header_keys = {h: {'index': idx, 'key': h.lower() + "_"} for idx, h in enumerate(header[:data_cols])}

        # set division, file names using csv files
        file, path = csv_file.split('.')
        division_name = ''.join([i for i in file if not i.isdigit()]).rstrip()
        division_year = ''.join([i for i in file if i.isdigit()])

        season_data = {}

        for row in reader:

            try:
                match_data = {header_keys[h]['key']: row[header_keys[h]['index']] for h in header_keys.keys()}
            except IndexError:
                # some of the earlier seasons have 7 total columns of data
                data_cols = 7

            home_team_id = process_team(match_data['hometeam_'], session)
            away_team_id = process_team(match_data['awayteam_'], session)

            season_data.setdefault(home_team_id, {})
            season_data[home_team_id].setdefault('week', 0)
            season_data[home_team_id].setdefault('points', 0)
            season_data[home_team_id].setdefault('gd', 0)

            season_data.setdefault(away_team_id, {})
            season_data[away_team_id].setdefault('week', 0)
            season_data[away_team_id].setdefault('points', 0)
            season_data[away_team_id].setdefault('gd', 0)
            # count week of season for H/A teams
            season_data[home_team_id]['week'] += 1
            season_data[away_team_id]['week'] += 1
            # points for H/A teams
            season_data[home_team_id]['points'] += points_dict[home_result_dict[match_data['ftr_']]]
            season_data[away_team_id]['points'] += points_dict[away_result_dict[match_data['ftr_']]]
            # goal difference for H/A teams
            season_data[home_team_id]['gd'] += int(match_data['fthg_']) - int(match_data['ftag_'])
            season_data[away_team_id]['gd'] += int(match_data['ftag_']) - int(match_data['fthg_'])
            # full time score from home perspective
            season_data[home_team_id]['score'] = match_data['fthg_'] + '-' + match_data['ftag_']

            # half time results are not always available, fill with NA where needed
            try:
                season_data[home_team_id]['htscore'] = match_data['hthg_'] + '-' + match_data['htag_']
            except KeyError:
                season_data[home_team_id]['htscore'] = 'NA'
            try:
                home_result = home_result_dict[match_data['htr_']]
            except KeyError:
                home_result = 'NA'
            try:
                away_result = away_result_dict[match_data['htr_']]
            except KeyError:
                away_result = 'NA'

            try:
                home_p = Performance(**{
                'team_id': home_team_id,
                'ft_goals_for': match_data['fthg_'],
                'ht_goals_for': match_data['hthg_'],
                'ft_result': home_result_dict[match_data['ftr_']],
                'ht_result': home_result,
                'venue': 'H',
                'week': season_data[home_team_id]['week'],
                'points': season_data[home_team_id]['points'],
                'gd': season_data[home_team_id]['gd'],
                })
            except KeyError:
                home_p = Performance(**{
                'team_id': home_team_id,
                'ft_goals_for': match_data['fthg_'],
                'ht_goals_for': 'NA',
                'ft_result': home_result_dict[match_data['ftr_']],
                'ht_result': 'NA',
                'venue': 'H',
                'week': season_data[home_team_id]['week'],
                'points': season_data[home_team_id]['points'],
                'gd': season_data[home_team_id]['gd'],
                })
            try:
                away_p = Performance(**{
                'team_id': away_team_id,
                'ft_goals_for': match_data['ftag_'],
                'ht_goals_for': match_data['htag_'],
                'ft_result': away_result_dict[match_data['ftr_']],
                'ht_result': away_result,
                'venue': 'A',
                'week': season_data[away_team_id]['week'],
                'points': season_data[away_team_id]['points'],
                'gd': season_data[away_team_id]['gd'],
                })
            except KeyError:
                away_p = Performance(**{
                'team_id': away_team_id,
                'ft_goals_for': match_data['ftag_'],
                'ht_goals_for': 'NA',
                'ft_result': away_result_dict[match_data['ftr_']],
                'ht_result': 'NA',
                'venue': 'A',
                'week': season_data[away_team_id]['week'],
                'points': season_data[away_team_id]['points'],
                'gd': season_data[away_team_id]['gd'],
                })

            session.add(home_p)
            session.add(away_p)
            session.flush()
            session.refresh(home_p)
            session.refresh(away_p)

            # there are 2 digit and 4 digit years in the csv files. try both
            try:
                fix_date = datetime.strptime(row[header_keys['Date']['index']], '%d/%m/%Y')
            except ValueError:
                fix_date = datetime.strptime(row[header_keys['Date']['index']], '%d/%m/%y')

            # 2 different millenia, need to determine if post 2000. Data ends after 02/03 Seasons.
            if division_year[-2:] in ('00', '01', '02'):
                end_yearchoice = 2000
            if division_year[-2:] not in ('00', '01', '02'):
                end_yearchoice = 1900

            # create season using filename split
            season = f'{end_yearchoice+int(division_year[-2:])-1}/{end_yearchoice+int(division_year[-2:])}'

            # need try and accept blocks as some seasons have no halftime stats. Set to NA like other missing fields

            try:
                game = Game(**{
                'season': season,
                'date': fix_date,
                'home_id': home_p.team_id,
                'away_id': away_p.team_id,
                # replace value for division - set as E0 instead of EPL
                'div': division_name,
                'ft_result': match_data['ftr_'],
                'ft_score': season_data[home_team_id]['score'],
                'ht_result': match_data['htr_'],
                'ht_score': season_data[home_team_id]['htscore'],
                })
            except KeyError:
                game = Game(**{
                'season': season,
                'date': fix_date,
                'home_id': home_p.team_id,
                'away_id': away_p.team_id,
                # replace value for division - set as E0 instead of EPL
                'div': division_name,
                'ft_result': match_data['ftr_'],
                'ft_score': season_data[home_team_id]['score'],
                'ht_result': 'NA',
                'ht_score': 'NA',
                })
            # add game to db
            session.add(game)
            # clear buffer
            session.flush()
            # refresh session, easier iteration
            session.refresh(game)

            # set game id to current game for both teams (home,away)
            home_p.game_id = game.id
            away_p.game_id = game.id

            # clear internal buffer before commit
            session.flush()
print(f'{arrows}{TerminalColours.WIN}upload complete!{TerminalColours.ENDC}\n')
session.commit()
cursor.close()
