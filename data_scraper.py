# Import libraries
import requests
import pandas as pd

def fetch_skater_data():
    """Uses the NHL API to request skater stats and characteristics.

    Through structured API calls this returns a DataFrame with
    skater information for each current team for the '08/'09' through
    '18/'19 seasons. Goalie information is excluded as the stat categories
    differ greatly from skaters.

    This API returns data only on currently active players; meaning any
    that retired in any year between the start and end seasons specified
    are excluded. As a result data will be skewed towards recent seasons.

    Parameters
    ----------

    Returns
    ------
    df : DataFrame
        A Pandas Dataframe with scraped information on each skater for every
        team & year specified.
    """

    # Teams names and ID's
    team_dict = {
    '1': 'New Jersey Devils', '2': 'New York Islanders', '3': 'New York Rangers',
    '4': 'Philadelphia Flyers', '5': 'Pittsburgh Penguins', '6': 'Boston Bruins',
    '7': 'Buffalo Sabres', '8': 'Montréal Canadiens', '9': 'Ottawa Senators',
    '10': 'Toronto Maple Leafs', '12': 'Carolina Hurricanes', '13': 'Florida Panthers',
    '14': 'Tampa Bay Lightning', '15': 'Washington Capitals', '16': 'Chicago Blackhawks',
    '17': 'Detroit Red Wings', '18': 'Nashville Predators', '19': 'St. Louis Blues',
    '20': 'Calgary Flames', '21': 'Colorado Avalanche', '22': 'Edmonton Oilers',
    '23': 'Vancouver Canucks', '24': 'Anaheim Ducks', '25': 'Dallas Stars',
    '26': 'Los Angeles Kings', '28': 'San Jose Sharks', '29': 'Columbus Blue Jackets',
    '30': 'Minnesota Wild', '52': 'Winnipeg Jets', '53': 'Arizona Coyotes',
    '54': 'Vegas Golden Knights'
    }

    # Seasons to scrape (excludes lockout & half years)
    seasons = [
    '20082009', '20092010', '20102011', '20112012',
    '20132014', '20142015', '20152016', '20162017',
    '20172018', '20182019'
    ]

    # Initialise list to hold data
    li = []

    for season in seasons:
        print(f'Retrieving {season[:4]}-{season[4:]} season data...')

        for team in team_dict.keys():

            # Request roster info for season
            roster = requests.get(f'https://statsapi.web.nhl.com/api/v1/teams/{team}/roster')

            # Using roster, get player info
            for player in roster.json()['roster']:
                player_id = player['person']['id']
                full_name = player['person']['fullName']
                position_code = player['position']['code']
                position_type = player['position']['type']
                number = player['jerseyNumber']

                # Only work with skaters (not goalies)
                if position_code != 'G':

                    # Get player characteristics
                    character = requests.get(f'https://statsapi.web.nhl.com/api/v1/people/{player_id}')
                    character = character.json()['people'][0]
                    age = character['currentAge']
                    birth_date = character['birthDate']
                    nationality = character['nationality']
                    alternate_capt = character['alternateCaptain']
                    captain = character['captain']
                    rookie = character['rookie']
                    shoots = character['shootsCatches']
                    weight = character['weight']
                    height = character['height']

                    try:
                    # Get skater season stats (if stats exist)
                    # Only currently active players are returned through API
                        stats = requests.get(f'https://statsapi.web.nhl.com/api/v1/people/{player_id}/stats?stats=statsSingleSeason&season={season}')
                        stats = stats.json()['stats'][0]['splits'][0]['stat']
                        toi = stats['timeOnIce']
                        pptoi = stats['powerPlayTimeOnIce']
                        shtoi = stats['shortHandedTimeOnIce']
                        etoi = stats['evenTimeOnIce']
                        assists = stats['assists']
                        goals = stats['goals']
                        pim = stats['pim']
                        shots = stats['shots']
                        games = stats['games']
                        hits = stats['hits']
                        shotpct = stats['shotPct']
                        blocked = stats['blocked']
                        plusminus = stats['plusMinus']
                        shifts = stats['shifts']
                        points = stats['points']

                        # Append data to list
                        li.append([season, team_dict[team], full_name, birth_date,
                                   age, nationality, height, weight, number, rookie,
                                   position_code, position_type, captain, alternate_capt, shoots,
                                   toi, pptoi, shtoi, etoi, assists, goals, pim, shots, shotpct,
                                   games, hits, blocked, plusminus, shifts, points])

                    except IndexError:
                        pass

                # Dont scrape goalies
                else:
                    continue

        print(f'{season[:4]}-{season[4:]} season data scraped. Total rows: {len(li)}')
        print('-'*10)

    # Create Dataframe with data
    df = pd.DataFrame(li, columns=['season', 'team', 'name', 'birthday',
                                   'age', 'nationality', 'height', 'weight', 'number', 'rookie',
                                   'position_code', 'position_type', 'captain', 'alternate_capt', 'handedness',
                                   'toi', 'pp_toi', 'sh_toi', 'ev_toi', 'assists', 'goals', 'pim', 'shots',
                                   'shot_perc', 'games', 'hits', 'blocked', 'plusminus', 'shifts', 'points'])
    return df


