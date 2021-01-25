class TeamColours:
    DEFAULT = '\033[0m'
    ARSENAL = '\033[41;1m' # bright red background
    ''' teams with arsenal colours:
    Alfreton, Barnsley, Bristol City, Charlton Athetic, Cheltenham Town, Crawley Town, Crewe Alexandria, Fleetwood Town, Middlesborough, Morecambe, Rotertham United, Salford City, Sheffield United, Swindon Town, '''
    ALDERSHOT = '\033[1;34;41m' # blue text, bright red back  YORK CITY
    ASTONVILLA = '\033[1;34;45m' # claret back and blue text
    '''Burnley, West Ham, Scunthorpe United'''
    BARNET = '\033[48;2;255;165;0m' # orange
    '''Blackpool, Hull, Wolves, Luton Towm'''
    BIRMINGHAM = '\033[44m' # blue back
    '''Blackburn, Bolton, Brighton, Bury, Bristol, Carlisle, Chesterfield, Everton, Hartelpool, Huddersfield, Ipswich, Leicster City, Macclesfield, Oldham, Peterborough, Preston, QPR, Reading, Sheff Wednesday, Southend, Tranmere, West Brom, Wigan'''
    BOURNEMOUTH = '\033[1;30;41;1m' # black and red
    '''Kingtonian, Grimsby, Exeter, '''
    BRADFORD = '\033[33m' # yellow
    '''Burton, Cambridge, Gloucester, Harrogate, Norwich, Oxford,  Watford,  '''
    CHELSEA = '\033[34m' # blue
    '''AFC Wimbledon, Colchester United, Gillingham '''
    FORESTGREEN = '\033[92m' # bright green text
    FULHAM  = '\033[7m' # reversed
    '''Derby County, Millwall, Port Vale '''
    LEEDS = '\033[47;1m' # bright white back
    LIVERPOOL = '\033[41m' # red back
    '''teams with liverpool colours:
    Accrington, Brentford, Nottingham Forest'''
    MANCITY = '\033[46;1m' # light blue back
    NORTH = '\033[45;1m'
    OXFORD = '\033[33;46;1m' # yellow text, blue back
    '''Convey Island, Shrewsbury, Mansfield'''
    SOUTHAMPTON = '\033[1;31;1;47;1m' # bright red text, bright white back'''
    '''teams with liverpool colours:
    Brentord, Doncaster Rovers, Lincoln City, Stevenage, Stoke, Sunderland'''
    YORK = '\033[34;1m\033[41;m' # bright blue text, red back

team_colour_dict = {
        'AFC Telford United': TeamColours.FULHAM,
        'AFC Wimbledon': TeamColours.CHELSEA,
        'Accrington': TeamColours.LIVERPOOL,
        'Aldershot': TeamColours.ALDERSHOT,
        'Alfreton Town': TeamColours.ARSENAL,
        'Altrincham': TeamColours.SOUTHAMPTON,
        'Arsenal': TeamColours.ARSENAL,
        'Aston Villa': TeamColours.ASTONVILLA,
        'Barnet': TeamColours.BARNET,
        'Barnsley': TeamColours.ARSENAL,
        'Barrow': TeamColours.BIRMINGHAM,
        'Bath City': TeamColours.FULHAM,
        'Birmingham': TeamColours.BIRMINGHAM,
        'Blackburn': TeamColours.BIRMINGHAM,
        'Blackpool': TeamColours.BARNET,
        'Bolton': TeamColours.BIRMINGHAM,
        'Boreham Wood': TeamColours.FULHAM,
        'Boston': TeamColours.BRADFORD,
        'Bournemouth': TeamColours.BOURNEMOUTH,
        'Bradford': TeamColours.BRADFORD,
        'Braintree Town': TeamColours.BARNET,
        'Brentford': TeamColours.LIVERPOOL,
        'Brighton': TeamColours.BIRMINGHAM,
        'Bristol City': TeamColours.ARSENAL,
        'Bristol Rvs': TeamColours.BIRMINGHAM,
        'Bromley': TeamColours.LEEDS,
        'Burnley': TeamColours.ASTONVILLA,
        'Burton': TeamColours.BRADFORD,
        'Bury': TeamColours.BIRMINGHAM,
        'Cambridge': TeamColours.BRADFORD,
        'Cardiff': TeamColours.MANCITY,
        'Canvey Island': TeamColours.OXFORD,
        'Carlisle': TeamColours.BIRMINGHAM,
        'Charlton': TeamColours.ARSENAL,
        'Chelsea': TeamColours.CHELSEA,
        'Cheltenham': TeamColours.ARSENAL,
        'Chester': TeamColours.BIRMINGHAM,
        'Chesterfield': TeamColours.BIRMINGHAM,
        'Chorley': TeamColours.FULHAM,
        'Colchester': TeamColours.CHELSEA,
        'Coventry': TeamColours.MANCITY,
        'Crawley Town': TeamColours.ARSENAL,
        'Crewe': TeamColours.ARSENAL,
        'Crystal Palace': TeamColours.ALDERSHOT,
        'Dag and Red': TeamColours.ALDERSHOT,
        'Darlington': TeamColours.FULHAM,
        'Dartford': TeamColours.FULHAM,
        'Derby': TeamColours.FULHAM,
        'Doncaster': TeamColours.SOUTHAMPTON,
        'Dover Athletic': TeamColours.FULHAM,
        'Droylsden': TeamColours.SOUTHAMPTON,
        'Eastbourne Borough': TeamColours.SOUTHAMPTON,
        'Eastleigh': TeamColours.BIRMINGHAM,
        'Ebbsfleet': TeamColours.ARSENAL,
        'Everton': TeamColours.BIRMINGHAM,
        'Exeter': TeamColours.BOURNEMOUTH,
        'Farsley': TeamColours.FORESTGREEN,
        'Fleetwood Town': TeamColours.ARSENAL,
        'Forest Green': TeamColours.FORESTGREEN,
        'Fulham': TeamColours.FULHAM,
        'Fylde': TeamColours.YORK,
        'Gateshead': TeamColours.FULHAM,
        'Gillingham': TeamColours.CHELSEA,
        'Gravesend': TeamColours.ARSENAL,
        'Grays': TeamColours.MANCITY,
        'Grimsby': TeamColours.BOURNEMOUTH,
        'Guiseley': TeamColours.OXFORD,
        'Halifax': TeamColours.BIRMINGHAM,
        'Harrogate': TeamColours.BRADFORD,
        'Hartlepool': TeamColours.BIRMINGHAM,
        'Havant & Waterlooville': TeamColours.OXFORD,
        'Hayes & Yeading': TeamColours.MANCITY,
        'Hereford': TeamColours.FULHAM,
        'Histon': TeamColours.BOURNEMOUTH,
        'Huddersfield': TeamColours.BIRMINGHAM,
        'Hull': TeamColours.BARNET,
        'Hyde United': TeamColours.LIVERPOOL,
        'Ipswich': TeamColours.BIRMINGHAM,
        'Kettering Town': TeamColours.BOURNEMOUTH,
        'Kidderminster': TeamColours.SOUTHAMPTON,
        'Kings Lynn Town': TeamColours.OXFORD,
        'Leeds': TeamColours.LEEDS,
        'Leicester': TeamColours.BIRMINGHAM,
        'Lewes': TeamColours.BOURNEMOUTH,
        'Leyton Orient': TeamColours.LIVERPOOL,
        'Lincoln': TeamColours.SOUTHAMPTON,
        'Liverpool': TeamColours.LIVERPOOL,
        'Luton': TeamColours.BARNET,
        'Macclesfield': TeamColours.BIRMINGHAM,
        'Maidenhead': TeamColours.FULHAM,
        'Maidstone': TeamColours.BARNET,
        'Man City': TeamColours.MANCITY,
        'Man United': TeamColours.BOURNEMOUTH,
        'Mansfield': TeamColours.BARNET,
        'Middlesbrough': TeamColours.LIVERPOOL,
        'Millwall': TeamColours.FULHAM,
        'Milton Keynes Dons': TeamColours.BRADFORD,
        'Morecambe': TeamColours.SOUTHAMPTON,
        'Newcastle': TeamColours.FULHAM,
        'Newport County': TeamColours.BARNET,
        'North Ferriby': TeamColours.FORESTGREEN,
        'Northampton': TeamColours.NORTH,
        'Northwich': TeamColours.FORESTGREEN,
        'Norwich': TeamColours.BRADFORD,
        "Nott'm Forest": TeamColours.ARSENAL,
        'Notts County': TeamColours.FULHAM,
        'Nuneaton Town': TeamColours.BIRMINGHAM,
        'Oldham': TeamColours.BIRMINGHAM,
        'Oxford': TeamColours.OXFORD,
        'Peterboro': TeamColours.CHELSEA,
        'Plymouth': TeamColours.FORESTGREEN,
        'Port Vale': TeamColours.FULHAM,
        'Portsmouth': TeamColours.BIRMINGHAM,
        'Preston': TeamColours.BIRMINGHAM,
        'QPR': TeamColours.BIRMINGHAM,
        'Reading': TeamColours.BIRMINGHAM,
        'Rochdale': TeamColours.YORK,
        'Rotherham': TeamColours.SOUTHAMPTON,
        'Rushden & D': TeamColours.CHELSEA,
        'Salford': TeamColours.SOUTHAMPTON,
        'Salisbury': TeamColours.FULHAM,
        'Scarborough': TeamColours.BARNET,
        'Scunthorpe': TeamColours.ASTONVILLA,
        'Sheffield United': TeamColours.ARSENAL,
        'Sheffield Weds': TeamColours.BIRMINGHAM,
        'Shrewsbury': TeamColours.OXFORD,
        'Solihull': TeamColours.OXFORD,
        'Southampton': TeamColours.SOUTHAMPTON,
        'Southend': TeamColours.BIRMINGHAM,
        'Southport': TeamColours.BARNET,
        'St. Albans': TeamColours.FULHAM,
        'Stafford Rangers': TeamColours.FULHAM,
        'Stevenage': TeamColours.SOUTHAMPTON,
        'Stockport': TeamColours.CHELSEA,
        'Stoke': TeamColours.SOUTHAMPTON,
        'Sunderland': TeamColours.SOUTHAMPTON,
        'Sutton': TeamColours.BRADFORD,
        'Swansea': TeamColours.FULHAM,
        'Swindon': TeamColours.SOUTHAMPTON,
        'Tamworth': TeamColours.BOURNEMOUTH,
        'Telford United': TeamColours.FULHAM,
        'Torquay': TeamColours.BRADFORD,
        'Tottenham': TeamColours.FULHAM,
        'Tranmere': TeamColours.BIRMINGHAM,
        'Walsall': TeamColours.ARSENAL,
        'Watford': TeamColours.BRADFORD,
        'Wealdstone': TeamColours.OXFORD,
        'Welling United': TeamColours.LIVERPOOL,
        'West Brom': TeamColours.BIRMINGHAM,
        'West Ham': TeamColours.ASTONVILLA,
        'Weymouth': TeamColours.MANCITY,
        'Wigan': TeamColours.BIRMINGHAM,
        'Wimbledon': TeamColours.CHELSEA,
        'Woking': TeamColours.ARSENAL,
        'Wolves': TeamColours.BRADFORD,
        'Wrexham': TeamColours.ARSENAL,
        'Wycombe': TeamColours.MANCITY,
        'Yeovil': TeamColours.FORESTGREEN,
        'York': TeamColours.ALDERSHOT,
}