from prettytable import PrettyTable
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from teamcolours import team_colour_dict

# ansii escape colours. '\033' for escape. coloroma is easy to use as well
class TerminalColours:
    HEADER = '\033[95m'  # light magenta
    OKBLUE = '\033[94m'  # light blue
    WIN = '\033[92m'   # light green
    DRAW = '\033[93m'  # light yellow
    LOSS = '\033[91m'  # light red
    ENDC = '\033[0m'  # reset
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'

# engine = create_engine('sqlite:///:memory:', echo=True)
# echo causing hangs in atom


def runsql(sql, colourize=None):
    # create 2 engines, one for each database. you can query both dbs this way
    engine1 = create_engine('sqlite:///matchData.db', echo=False)
    engine2 = create_engine('sqlite:///OldmatchData.sqlite', echo=False)
    # sqlalchemy sessionmaker
    SessionOne = sessionmaker(bind=engine1)
    SessionTwo = sessionmaker(bind=engine2)
    session1 = SessionOne()
    session2 = SessionTwo()
    rs = session1.execute(sql)
    # rs = session2.execute(sql)
    col_names = [cn for cn in rs.keys()]
    results = rs.fetchall()
    # if query returns no results, try other database
    if not results:
        rs = session2.execute(sql)
        results = rs.fetchall()
    x = PrettyTable(col_names)
    # left align rows
    x.align = 'l'

    for r in results:
        row = list(r)
        if colourize is not None:
            for c in colourize:
                try:
                    column_name = c['column']
                    colour_map = c['colour_map']
                    column_colour = colour_map[row[col_names.index(column_name)]]
                    row[col_names.index(column_name)] = column_colour + row[col_names.index(column_name)] + TerminalColours.ENDC
                except ValueError:
                    pass
        x.add_row(row)

    print(x)
    return results


#----------------Dictionaries for ascii colours in sql queries

win_lose_draw_dict = {
        'W': TerminalColours.WIN + TerminalColours.BOLD,
        'L': TerminalColours.LOSS + TerminalColours.BOLD,
        'D': TerminalColours.DRAW + TerminalColours.BOLD
        }

home_away_draw_dict = {
        'H': TerminalColours.WIN + TerminalColours.BOLD,
        'A': TerminalColours.LOSS + TerminalColours.BOLD,
        'D': TerminalColours.DRAW + TerminalColours.BOLD
        }

division_dict = {
        'Premier League': TerminalColours.OKBLUE + TerminalColours.BOLD,
        'Championship': TerminalColours.LOSS + TerminalColours.BOLD,
        'League One': TerminalColours.DRAW + TerminalColours.BOLD,
        'League Two': TerminalColours.HEADER + TerminalColours.BOLD,
        'Conference': TerminalColours.WIN + TerminalColours.BOLD,
        'Division One': TerminalColours.UNDERLINE + TerminalColours.LOSS,
        'Division Two': TerminalColours.UNDERLINE + TerminalColours.DRAW,
        'Division Three': TerminalColours.UNDERLINE + TerminalColours.HEADER,
        }


#----------------SQL Queries

# teams from 2013/2014 season. show team colours with names
print(f"{TerminalColours.HEADER + TerminalColours.BOLD}\nTeams from 2013/2014 Season (All Leagues)\n{TerminalColours.ENDC}")
runsql("select t.name name from teams t join games g on g.home_id = t.id or g.away_id=t.id where g.season='2013/2014' group by name;",
        colourize=[
        {'column': 'name',
        'colour_map': team_colour_dict}])

# search for points total 2018/2019 week 24
print(f"{TerminalColours.HEADER + TerminalColours.BOLD}\nTeam Points Total after 2018/2019 Season Week 24\n{TerminalColours.ENDC}")
runsql("select g.div Division, g.season Season, p.week Week,  ht.name Team, p.points Points from performances p join games g on p.game_id = g.id join teams ht on ht.id = p.team_id where g.season='2018/2019' and p.week=24 order by case g.div when 'Premier League' then 0 when 'Championship' then 1 when 'League One' then 2 when 'League Two' then 3 when 'Conference' then 4 end, p.points desc;",
        colourize=[
        {'column': 'Division',
        'colour_map': division_dict},
        {'column': 'Team',
        'colour_map': team_colour_dict}
        ])

# search for results 2010/2011 season, week 14. show games where winner was correctly predicted
print(f"{TerminalColours.HEADER + TerminalColours.BOLD}\nCorrectly Predicted Results 2010/2011 Season Week 14\n{TerminalColours.ENDC}")
runsql("select ht.name Home, at.name Away, g.ft_score Score, g.odds_predicted 'Correctly Predicted Result' from games g join teams ht on\
        g.home_id = ht.id join teams at on g.away_id = at.id join performances p on g.id = p.game_id and g.home_id = p.team_id and g.ft_result = g.odds_predicted where g.season='2010/2011' and p.week=14",
        colourize=[
            {'column': 'Correctly Predicted Result',
            'colour_map': home_away_draw_dict
            }
        ])

# search for results 2003/2004 season, week 38. A great ball through to Viera ensures an Arsenal Invincibles season. Colour for division and result
print(f"{TerminalColours.HEADER + TerminalColours.BOLD}\nResults 03/04 Season Week 38\n{TerminalColours.ENDC}")
runsql("select g.div Division, ht.name Home, at.name Away, g.ft_score Score, g.ft_result Result from games g join teams ht on\
        g.home_id = ht.id join teams at on g.away_id = at.id join performances p on g.id = p.game_id and g.home_id = p.team_id where g.season='2003/2004' and p.week=38 order by case Division when 'Premier League' then 0 when 'Division One' then 1 when 'Division Two' then 2 when 'Division Three' then 3 end;",
        colourize=[
            {'column': 'Result',
            'colour_map': home_away_draw_dict
            },
            {'column': 'Division',
            'colour_map': division_dict}
        ])


# final table for premier league 2003/2004 points. Colour code team names by team colours
print(f"{TerminalColours.HEADER + TerminalColours.BOLD}\nFinal Premier League Standings 03/04 Season\n{TerminalColours.ENDC}")
runsql("select t.name Team, p.points Points from performances p join games g on p.game_id = g.id join teams t on t.id = p.team_id and p.week=38 where g.season='2003/2004' and div='Premier League' order by p.points desc;", colourize=[{'column': 'team', 'colour_map': team_colour_dict}])

# teams relegated from 2019/2020 premier league
print(f"{TerminalColours.HEADER + TerminalColours.BOLD}\nPremier League teams relegated 2019/2020 season\n{TerminalColours.ENDC}")
runsql("select * from (select t.name Team, p.points Points from performances p join games g on p.game_id = g.id join teams t on t.id = p.team_id and p.week=38 where g.season='2019/2020' and div='Premier League' order by p.points limit 3) order by Points desc;")

# search Conference 2011/2012 season, last week (46). show teams and result
print(f"{TerminalColours.HEADER + TerminalColours.BOLD}\nConference Final Week Scores 2011/2012 Season\n{TerminalColours.ENDC}")
runsql("select g.div as Division, g.season as Season, p.week Week, ht.name Home, at.name Away, ft_score Score from games g join teams ht on g.home_id = ht.id join teams at on g.away_id = at.id join performances p on g.id = p.game_id and g.home_id = p.team_id and p.week = 46 where g.div like 'Conference' and g.season='2011/2012';")

# ARSENAL results week to week points total Invincibles season. Colour code Win, Loss, Draw
print(f"{TerminalColours.HEADER + TerminalColours.BOLD}\nArsenal Results by Week 03/04 Season\n{TerminalColours.ENDC}")
runsql("select p.week Week, g.date Date, g.ft_score Score, p.ft_result Result, p.points Points from performances p join games g on g.id = p.game_id join teams t on p.team_id=t.id and t.name = 'Arsenal' where g.season='2003/2004';", colourize=[{'column': 'Result', 'colour_map': win_lose_draw_dict}])

# check Olddata database
# ARSENAL results week to week points total 1994/1995 season. Colour code Win, Loss, Draw
print(f"{TerminalColours.HEADER + TerminalColours.BOLD}\nArsenal Results by Week 94/95 Season\n{TerminalColours.ENDC}")
runsql("select p.week Week, g.date Date, g.ft_score Score, p.ft_result Result, p.points Points from performances p join games g on g.id = p.game_id join teams t on p.team_id=t.id and t.name = 'Arsenal' where g.season='1994/1995';", colourize=[{'column': 'Result', 'colour_map': win_lose_draw_dict}])
