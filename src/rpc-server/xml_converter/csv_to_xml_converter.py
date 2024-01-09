import os.path
import xml.dom.minidom as md
import xml.etree.ElementTree as ET

from .csv_reader import CSVReader
from .entities.college import College
from .entities.country import Country
from .entities.player import Player
from .entities.season import Season
from .entities.stats import Stats
from .entities.team import Team


class CSVtoXMLConverter:

    def __init__(self, path):
        self._reader = CSVReader(path)

    def to_xml(self):

        colleges = self._reader.read_entities(
            attrs=["college"],
            builder=lambda row: College(row["college"])
        )

        countries = self._reader.read_entities(
            attrs=["country"],
            builder=lambda row: Country(row["country"])
        )

        # read teams
        teams = self._reader.read_entities(
            attrs=["team_abbreviation"],
            builder=lambda row: Team(row["team_abbreviation"])
        )

        seasons = self._reader.read_entities(
            attrs=["season"],
            builder=lambda row: Season(row["season"])
        )

        players = self._reader.read_entities(
            attrs=["player_name", "season"],
            builder=lambda row: Player(
                name=row["player_name"],
                age=row["age"],
                height=row["player_height"],
                weight=row["player_weight"],
                college=row["college"],
                country=row["country"],
                draft_year=row["draft_year"],
                draft_round=row["draft_round"],
                draft_number=row["draft_number"],
                season=row["season"]
            )
        )

        stats = self._reader.read_entities(
            attrs=["player_name", "team_abbreviation", "season"],
            builder=lambda row: Stats(
                gp=row["gp"],
                pts=row["pts"],
                reb=row["reb"],
                ast=row["ast"],
                net_rating=row["net_rating"],
                oreb_pct=row["oreb_pct"],
                dreb_pct=row["dreb_pct"],
                usg_pct=row["usg_pct"],
                ts_pct=row["ts_pct"],
                ast_pct=row["ast_pct"],
                season=row["season"],
                player=row["player_name"]
            )
        )


        # def after_creating_player(player, row, season):
        #     # add the player to the appropriate team
        #     stats[row["player"]].add_player(player)


        # self._reader.read_entities(
        #     attrs=["full_name"],
        #     builder=lambda row: Player(
        #         name=row["player_name"],
        #         age=row["age"],
        #         country=countries[row["country"]]
        #     ),
        #     # after_create=after_creating_player
        # )

        root_el = ET.Element("NBA")

        # Group players by season
        players_by_season = {}
        for player in players.values():
            season = player._season  # Assuming player has a season attribute
            if season not in players_by_season:
                players_by_season[season] = []
            players_by_season[season].append(player)

        # Now iterate over seasons

        for season_year, season_players in players_by_season.items():
            season_el = ET.SubElement(root_el, "Season")
            season_el.set('season', season_year)

            for player in season_players:
                player_el = ET.Element("Player")
                player_el.set('id', str(player.get_id()))
                player_el.set('college_id', str(player.get_college()))
                player_el.set('country_ref', player.get_country())

                # Create child elements for the player attributes
                ET.SubElement(player_el, "name").text = player._name
                ET.SubElement(player_el, "age").text = str(player._age)
                ET.SubElement(player_el, "height").text = str(player._height)
                ET.SubElement(player_el, "weight").text = str(player._weight)
                ET.SubElement(player_el, "draft_year").text = player._draft_year
                ET.SubElement(player_el, "draft_round").text = player._draft_round
                ET.SubElement(player_el, "draft_number").text = player._draft_number
                ET.SubElement(player_el, "season").text = player._season

                season_el.append(player_el)
                root_el.append(season_el)

        # teams_el = ET.Element("Teams")
        # for team in teams.values():
        #     teams_el.append(team.to_xml())
        #
        # countries_el = ET.Element("Countries")
        # for country in countries.values():
        #     countries_el.append(country.to_xml())
        #
        # colleges_el = ET.Element("Colleges")
        # for college in colleges.values():
        #     colleges_el.append(college.to_xml())
        #
        # seasons_el = ET.Element("Seasons")
        # for season in seasons.values():
        #     seasons_el.append(season.to_xml())
        #
        # stats_el = ET.Element("Stats")
        # for stat in stats.values():
        #     stats_el.append(stat.to_xml())
        #
        # players_el = ET.Element("Players")
        # for player in players.values():
        #     players_el.append(player.to_xml())
        #
        # root_el.append(teams_el)
        # root_el.append(countries_el)
        # root_el.append(colleges_el)
        # root_el.append(stats_el)
        # root_el.append(seasons_el)

        return root_el

    def to_xml_str(self):
        root_el = self.to_xml()  # Get the root element from the to_xml method

        try:
            # Convert the XML element to a string
            xml_str = ET.tostring(root_el, encoding='utf8', method='xml').decode()
            dom = md.parseString(xml_str)
            pretty_xml_str = dom.toprettyxml()

            # Save as a file
            file_path = os.path.join(os.path.dirname(__file__), 'allSeasons.xml')
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(pretty_xml_str)

            print("File 'allSeasons.xml' created successfully!")
            return pretty_xml_str  # Return the XML string instead of True
        except Exception as e:
            print(f"Failed to create file: {e}")
            return "Failed"  # Return None in case of failure



