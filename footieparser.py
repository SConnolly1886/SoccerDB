from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float
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


# create 4 tables. games with generic information, teams, referees and performances valid from 2003/2004 season to present

home_result_dict = {'H': 'W', 'D': 'D', 'A': 'L'}
away_result_dict = {'A': 'W', 'D': 'D', 'H': 'L'}
points_dict = {'W': 3, 'D': 1, 'L': 0, 'NA': 0}

'''
Initially going to require input to select which SQLAlchemy dialect. SQLite works best with the data. So a choice in dialects is not given. If comfortable with other dialects. Make manual changes (sqlalchemy imports, new engine etc)
'''

# echoing seems to hang atom
engine = create_engine('sqlite:///matchData.db', echo=False)

# drop existing tables/data, write anew
connection = engine.raw_connection()
cursor = connection.cursor()
command = "DROP TABLE IF EXISTS games; DROP TABLE IF EXISTS performances; DROP TABLE IF EXISTS teams; DROP TABLE IF EXISTS referees;"
cursor.executescript(command)
connection.commit()
cursor.close()


'''callable returns a new base class from which all mapped classes should inherit.
When the class definition is completed, a new Table and mapper() will have been generated.'''
Base = declarative_base()

''' sqlalchemy is great with python and classes (ORM)
first class will make games table. has basic stats including odds for the game. then performances, referees and teams.
Using classes in python and converting them to sql tables.
I considered having 2 engines similar to footiesql.py and create both matchdata and OldmatchData in one program but for simplicity a python file for each database (matchData, OldmatchData)'''


class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    season = Column(Integer)
    div = Column(String)
    date = Column(Date)
    home_id = Column(Integer, ForeignKey('performances.id'))
    away_id = Column(Integer, ForeignKey('performances.id'))
    referee_id = Column(Integer, ForeignKey('referees.id'))
    ft_result = Column(String)
    ft_score = Column(String)
    ht_result = Column(String)
    ht_score = Column(String)
    home_odds = Column(Float)
    draw_odds = Column(Float)
    away_odds = Column(Float)
    odds_predicted = Column(String)

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
    odds_predicted = Column(String)
    venue = Column(String)
    shots = Column(Integer)
    shots_ot = Column(Integer)
    fouls = Column(Integer)
    corners = Column(Integer)
    yellows = Column(Integer)
    reds = Column(Integer)
    week = Column(Integer)
    points = Column(Integer)
    gd = Column(Integer)


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Referee(Base):
    __tablename__ = "referees"
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

# same applies for referees, add new refs as they come


def process_ref(name, session):
    ref = session.query(Referee.id).filter(Referee.name == name).one_or_none()
    if ref is not None:
        return ref[0]
    else:
        ref = Referee(**{'name': name})
        session.add(ref)
        session.flush()
        session.refresh(ref)
        return ref.id

# access the metadata where newly defined tables objects are collected


Base.metadata.create_all(engine)

# from sqlalchemy
Session = sessionmaker(bind=engine)
session = Session()

# name of folder containing csv files
seasondata_folder = "footie/"
# Number of Relevant columns, excludes betting odds for multiple companies
data_cols = 27

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

            match_data = {header_keys[h]['key']: row[header_keys[h]['index']] for h in header_keys.keys()}

            home_team_id = process_team(match_data['hometeam_'], session)
            away_team_id = process_team(match_data['awayteam_'], session)
            try:
                referee_id = process_ref(match_data['referee_'], session)
            except KeyError:
                referee_id = 'NA'

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
            # half time score from home perspective
            season_data[home_team_id]['htscore'] = match_data['hthg_'] + '-' + match_data['htag_']

            try:
                ho_ = float(match_data['b365h_'])
                do_ = float(match_data['b365d_'])
                ao_ = float(match_data['b365a_'])
                h_odds = 100.0/(1.0 + ho_/do_ + ho_/ao_)
                d_odds = 100.0/(1.0 + do_/ao_ + do_/ho_)
                a_odds = 100.0/(1.0 + ao_/do_ + ao_/ho_)

                # determine betting odds, predicted outcome of match
                max_odds = max(h_odds, d_odds, a_odds)
                if h_odds == max_odds:
                    odds_predicted = 'H'
                elif d_odds == max_odds:
                    odds_predicted = 'D'
                else:
                    odds_predicted = 'A'
            except KeyError:
                continue

            try:
                match_data['hs_']
            except KeyError:
                match_data['hs_'] = 'NA'
            try:
                match_data['hst_']
            except KeyError:
                match_data['hst_'] = 'NA'
            try:
                match_data['as_']
            except KeyError:
                match_data['as_'] = 'NA'
            try:
                match_data['ast_']
            except KeyError:
                match_data['ast_'] = 'NA'
            try:
                match_data['hf_']
            except KeyError:
                match_data['hf_'] = 'NA'
            try:
                match_data['hc_']
            except KeyError:
                match_data['hc_'] = 'NA'
            try:
                match_data['af_']
            except KeyError:
                match_data['af_'] = 'NA'
            try:
                match_data['ac_']
            except KeyError:
                match_data['ac_'] = 'NA'

            try:
                home_result_dict[match_data['htr_']]
            except KeyError:
                home_result_dict[match_data['htr_']] = 'NA'
            try:
                away_result_dict[match_data['htr_']]
            except KeyError:
                away_result_dict[match_data['htr_']] = 'NA'

            home_p = Performance(**{
                'team_id': home_team_id,
                'ft_goals_for': match_data['fthg_'],
                'ht_goals_for': match_data['hthg_'],
                'shots': match_data['hs_'],
                'shots_ot': match_data['hst_'],
                'fouls': match_data['hf_'],
                'corners': match_data['hc_'],
                'yellows': match_data['hy_'],
                'reds': match_data['hr_'],
                'ft_result': home_result_dict[match_data['ftr_']],
                'odds_predicted': home_result_dict[odds_predicted],
                'ht_result': home_result_dict[match_data['htr_']],
                'venue': 'H',
                'week': season_data[home_team_id]['week'],
                'points': season_data[home_team_id]['points'],
                'gd': season_data[home_team_id]['gd'],
                })

            away_p = Performance(**{
                'team_id': away_team_id,
                'ft_goals_for': match_data['ftag_'],
                'ht_goals_for': match_data['htag_'],
                'shots': match_data['as_'],
                'shots_ot': match_data['ast_'],
                'fouls': match_data['af_'],
                'corners': match_data['ac_'],
                'yellows': match_data['ay_'],
                'reds': match_data['ar_'],
                'ft_result': away_result_dict[match_data['ftr_']],
                'odds_predicted': away_result_dict[odds_predicted],
                'ht_result': away_result_dict[match_data['htr_']],
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

            end_yearchoice = 2000

            season = f'{end_yearchoice+int(division_year[-2:])-1}/{end_yearchoice+int(division_year[-2:])}'

            game = Game(**{
                'season': season,
                'date': fix_date,
                'home_id': home_p.team_id,
                'away_id': away_p.team_id,
                'referee_id': referee_id,
                # replace value for division - set as E0 instead of EPL
                'div': division_name,
                'ft_result': match_data['ftr_'],
                'ft_score': season_data[home_team_id]['score'],
                'ht_result': match_data['htr_'],
                'ht_score': season_data[home_team_id]['htscore'],
                'home_odds': match_data['b365h_'],
                'draw_odds': match_data['b365d_'],
                'away_odds': match_data['b365a_'],
                'odds_predicted': odds_predicted,
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
