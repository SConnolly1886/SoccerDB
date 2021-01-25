from pathlib import Path
import requests
import datetime

# get current date, needed to determine last season available
now = datetime.datetime.now()

# ascii colours for terminal
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


#----------------Set the beginning url, need to add final path, files


# using free resource for soccer/football stats. stats include gambling info. only keeping bet365 data
starting_url = "http://www.football-data.co.uk/mmz4281/%s/"

#----------------Determine what tier of English soccer/football is wanted



def inputTier(msg):
    while True:
        try:
            L = int(input(msg))
        except ValueError:
            print(f'{TerminalColours.ERROR}**ERROR** Select (1 to 8) only{TerminalColours.ENDC}')
            continue
        except TypeError:
            print(f'{TerminalColours.ERROR}**ERROR** Select (1 to 8) only{TerminalColours.ENDC}')
            continue
        if 1 <= L <= 8:
            return L
        else:
            print(f'{TerminalColours.ERROR}**ERROR** Select (1 to 8) only{TerminalColours.ENDC}')



# prompting for which tier.
tier = inputTier('\nPlease select which tier of English Soccer/Football you would like:\n\n1) Premier League\t(1993/1994 - present)\n2) Championship\t\t(2004/2005 - present)\n3) League One\t\t(2004/2005 - present)\n4) League Two\t\t(2004/2005 - present)\n5) Conference\t\t(2004/2005 - present)\n6) Division One\t\t(1993/1994 - 2003/2004)\n7) Division Two\t\t(1993/1994 - 2003/2004)\n8) Division Three\t(1993/1994 - 2003/2004)\n')


def tierNum(tier):
    if tier == 1:
        name = 'Premier League'
        type = 'E0'
        start = 1993
        end = now.year - 1
    if tier == 2:
        name = 'Championship'
        type = 'E1'
        start = 2004
        end = now.year - 1
    if tier == 3:
        name = 'League One'
        type = 'E2'
        start = 2004
        end = now.year - 1
    if tier == 4:
        name = 'League Two'
        type = 'E3'
        start = 2004
        end = now.year - 1
    if tier == 5:
        name = 'Conference'
        type = 'EC'
        start = 2004
        end = now.year - 1
    if tier == 6:
        name = 'Division One'
        type = 'E1'
        start = 1993
        end = 2003
    if tier == 7:
        name = 'Division Two'
        type = 'E2'
        start = 1993
        end = 2003
    if tier == 8:
        name = 'Division Three'
        type = 'E3'
        start = 1993
        end = 2003
    return name, type, start, end


res = tierNum(tier)

print(f'{TerminalColours.WIN} --{res[0]} selected-- {TerminalColours.ENDC}')

# set the base url based on user input
base_url = f'{starting_url}{res[1]}.csv'

#----------------Determine range of years for seasons


def inputSeason(msg):
    while True:
        try:
            L = int(input(msg))
        except ValueError:
            print(f'{TerminalColours.ERROR}**ERROR** Select from {res[2]} to {res[3]} only{TerminalColours.ENDC}')
            continue
        if res[2] <= L <= res[3]:
            return L
        else:
            print(f'{TerminalColours.ERROR}**ERROR** Select from {res[2]} to {res[3]} only{TerminalColours.ENDC}')


first_season = inputSeason('Please enter a 4 digit starting season: ')
first_year = f'{first_season}/{first_season+1}'
print(f'{TerminalColours.WIN} --{first_year} selected-- {TerminalColours.ENDC}')

last_season = inputSeason('Please enter a 4 digit ending season: ')
last_year = f'{last_season}/{last_season+1}'
print(f'{TerminalColours.WIN} --{last_year} selected-- {TerminalColours.ENDC}')

# in case enters earlier year on second prompt
if last_season <= first_season:
    first_season, last_season = last_season, first_season

# split the data based on the year range. Prior to 02/03 there is no odds data. Half time data is also missing in earlier years.
if first_season < 2002:
    print(f'\n{TerminalColours.WIN} --Attention--{TerminalColours.ENDC}\nYears prior to the 2002/2003 season has different data, and must be stored in a seperate DB\n')

# seasons with last 2 years of season example 2002/2003 season becomes 0203


def epl_season(start):
    end = start + 1
    return str(start)[-2:] + str(end)[-2:]

#----------------Now the years and division has been selected. Iterate and write to files


# set first season to download
season = first_season


# iterate through seasons selected
while season <= last_season:
    season_year = epl_season(season)
    # data is different before 03/04 season, move to different directory
    if season < 2002:
        seasondata_folder = Path('oldfootie')
    else:
        seasondata_folder = Path('footie')
    # using Path, create folders if necessary
    seasondata_folder.mkdir(exist_ok=True)
    # add initial url with selected seasons
    response = requests.get(base_url % season_year, stream=True)
    # check for ok (200) code before attempting to write
    if response.status_code == 200:
        with open(f'{seasondata_folder}/{res[0]} {season_year}.csv', 'wb') as season_file:
            season_file.write(response.text.encode('utf-8'))

    season += 1

# coloured arrow for repeat use
arrows = f'{TerminalColours.OKBLUE}------------->{TerminalColours.ENDC}'

# print tier selected/seasons selected
print(f'\n{TerminalColours.UNDERLINE}Downloaded:{TerminalColours.ENDC}\nSoccer/Football Tier:\n{arrows}{res[0]}\nSeasons:\n{arrows}{first_year} to {last_year}\n')
