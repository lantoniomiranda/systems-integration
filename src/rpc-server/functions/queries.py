from database import database


def get_top_10_players_with_highest_pts_avg():
    try:

        query = '''
            SELECT player_ref,
                AVG(CAST(pts AS FLOAT)) as avg_pts
            FROM (
                SELECT  unnest(xpath('//Player/@id', xml_converter::xml_converter))::text AS player_ref,
                        unnest(xpath('//Player/Stats/Points/text()', xml_converter::xml_converter))::text AS pts
                FROM imported_documents
                WHERE deleted_on IS NULL
            ) as player_stats
            GROUP BY player_ref
            ORDER BY avg_pts DESC 
            LIMIT 10;
        '''

        results = database.execute_query(query)
        if results:
            top_players = [{'player_ref': row[0], 'avg_pts': row[1]} for row in results]
            return top_players
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        database.close_connection()


def get_highest_scoring_season_by_player(player_name):
    try:
        query = '''
            SELECT season, points
            FROM (
                SELECT
                    unnest(xpath('//Player[@name=$1]/season/text()', xml))::text AS season,
                    unnest(xpath('//Player[@name=$1]/Stats/pts/text()', xml))::text AS points
                FROM imported_documents
            ) AS player_seasons
            ORDER BY points::float DESC
            LIMIT 1;
        '''

        results = database.query(query, (player_name,))
        return results

    except Exception as e:
        return f"An error occurred: {e}"



def get_top_5_players_with_most_triple_double_seasons():
    try:
        query = '''
            WITH PlayerStats AS (
                SELECT
                    unnest(xpath('//Player/@id', xml_converter))::text AS player_id,
                    unnest(xpath('//Player/Seasons/Season/@name', xml_converter))::text AS season,
                    unnest(xpath('//Player/Seasons/Season/Stats/Points/text()', xml_converter))::int AS points,
                    unnest(xpath('//Player/Seasons/Season/Stats/Rebounds/text()', xml_converter))::int AS rebounds,
                    unnest(xpath('//Player/Seasons/Season/Stats/Assists/text()', xml_converter))::int AS assists
                FROM
                    imported_documents
                WHERE
                    deleted_on IS NULL
            ),
            TripleDoubles AS (
                SELECT
                    player_id,
                    season,
                    (points >= 10 AND rebounds >= 10 AND assists >= 10) AS is_triple_double
                FROM
                    PlayerStats
            ),
            TripleDoubleSeasons AS (
                SELECT
                    player_id,
                    COUNT(season) AS triple_double_seasons
                FROM
                    TripleDoubles
                WHERE
                    is_triple_double
                GROUP BY
                    player_id
            )
            SELECT
                player_id,
                triple_double_seasons
            FROM
                TripleDoubleSeasons
            ORDER BY
                triple_double_seasons DESC
            LIMIT 5;
        '''
        results = database.execute_query(query)
        if results:
            return [{'player_id': row[0], 'triple_double_seasons': row[1]} for row in results]
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        database.close_connection()


def get_most_improved_player():
    try:
        query = '''
            WITH SeasonStats AS (
                SELECT
                    player_ref,
                    season,
                    CAST(pts AS FLOAT) as points
                FROM (
                    SELECT
                        unnest(xpath('//Player/@id', xml_converter))::text AS player_ref,
                        unnest(xpath('//Player/Seasons/Season/@name', xml_converter))::text AS season,
                        unnest(xpath('//Player/Seasons/Season/Stats/Points/text()', xml_converter))::text AS pts
                    FROM imported_documents
                    WHERE deleted_on IS NULL
                ) as stats
            ),
            SeasonImprovement AS (
                SELECT
                    player_ref,
                    LAG(points) OVER (PARTITION BY player_ref ORDER BY season) as previous_points,
                    points
                FROM SeasonStats
            )
            SELECT
                player_ref,
                (points - previous_points) as improvement
            FROM SeasonImprovement
            ORDER BY improvement DESC
            LIMIT 1;
        '''
        results = database.execute_query(query)
        if results:
            return {'player_ref': results[0][0], 'improvement': results[0][1]}
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        database.close_connection()


# PER = Player Efficiency Rating
def get_top_10_players_by_per():
    try:
        query = '''
            WITH PlayerStats AS (
                SELECT
                    player_ref,
                    season,
                    CAST(pts AS FLOAT) as points,
                    CAST(reb AS FLOAT) as rebounds,
                    CAST(ast AS FLOAT) as assists,
                FROM (
                    SELECT
                        unnest(xpath('//Player/@id', xml_converter))::text AS player_ref,
                        unnest(xpath('//Player/Seasons/Season/@name', xml_converter))::text AS season,
                        unnest(xpath('//Player/Seasons/Season/Stats/Points/text()', xml_converter))::text AS pts,
                        unnest(xpath('//Player/Seasons/Season/Stats/Rebounds/text()', xml_converter))::text AS reb,
                        unnest(xpath('//Player/Seasons/Season/Stats/Assists/text()', xml_converter))::text AS ast
                    FROM imported_documents
                    WHERE deleted_on IS NULL
                ) as stats
            ),
            PlayerPER AS (
                SELECT
                    player_ref,
                    AVG(points + rebounds + assists /* - turnovers + ... */) as avg_per
                FROM PlayerStats
                GROUP BY player_ref
            )
            SELECT
                player_ref,
                avg_per
            FROM PlayerPER
            ORDER BY avg_per DESC
            LIMIT 10;
        '''
        results = database.execute_query(query)
        if results:
            return [{'player_ref': row[0], 'avg_per': row[1]} for row in results]
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        database.close_connection()


def get_best_colleges_for_nba_talent():
    try:
        query = '''
            WITH CollegePerformance AS (
                SELECT
                    college,
                    COUNT(player_name) AS num_players,
                    AVG(CAST(pts AS FLOAT)) as avg_points,
                    AVG(CAST(reb AS FLOAT)) as avg_rebounds,
                    AVG(CAST(ast AS FLOAT)) as avg_assists
                FROM (
                    SELECT
                        unnest(xpath('//Player/College/text()', xml_converter))::text AS college,
                        unnest(xpath('//Player/@name', xml_converter))::text AS player_name,
                        unnest(xpath('//Player/Seasons/Season/Stats/Points/text()', xml_converter))::text AS pts,
                        unnest(xpath('//Player/Seasons/Season/Stats/Rebounds/text()', xml_converter))::text AS reb,
                        unnest(xpath('//Player/Seasons/Season/Stats/Assists/text()', xml_converter))::text AS ast
                    FROM imported_documents
                    WHERE deleted_on IS NULL
                ) as player_stats
                GROUP BY college
            )
            SELECT
                college,
                num_players,
                avg_points,
                avg_rebounds,
                avg_assists
                -- Include other average stats in the SELECT if needed
            FROM CollegePerformance
            ORDER BY num_players DESC, avg_points DESC
            LIMIT 10;
        '''
        results = database.execute_query(query)
        if results:
            return [{
                'college': row[0],
                'num_players': row[1],
                'avg_points': row[2],
                'avg_rebounds': row[3],
                'avg_assists': row[4],
            } for row in results]
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        database.close_connection()


