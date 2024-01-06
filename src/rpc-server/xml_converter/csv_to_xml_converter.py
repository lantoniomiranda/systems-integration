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
            attrs=["player_name"],
            builder=lambda row: Player(
                name=row["player_name"],
                age=row["age"],
                height=row["player_height"],
                weight=row["player_weight"],
                college=row["college"],
                country=row["country"],
                draft_year=row["draft_year"],
                draft_round=row["draft_round"],
                draft_number=row["draft_number"]
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

        # generate the final xml_converter
        root_el = ET.Element("NBA")

        teams_el = ET.Element("Teams")
        for team in teams.values():
            teams_el.append(team.to_xml())

        countries_el = ET.Element("Countries")
        for country in countries.values():
            countries_el.append(country.to_xml())

        colleges_el = ET.Element("Colleges")
        for college in colleges.values():
            colleges_el.append(college.to_xml())

        seasons_el = ET.Element("Seasons")
        for season in seasons.values():
            seasons_el.append(season.to_xml())

        stats_el = ET.Element("Stats")
        for stat in stats.values():
            stats_el.append(stat.to_xml())

        players_el = ET.Element("Players")
        for player in players.values():
            players_el.append(player.to_xml())

        root_el.append(players_el)
        root_el.append(teams_el)
        root_el.append(countries_el)
        root_el.append(colleges_el)
        root_el.append(stats_el)
        root_el.append(seasons_el)

        return root_el

    def to_xml_str(self):
        xml_str = ET.tostring(self.to_xml(), encoding='utf8', method='xml_converter').decode()
        dom = md.parseString(xml_str)
        pretty_xml_str = dom.toprettyxml()

        # save as file
        file_path = os.path.join(os.path.dirname(__file__), 'allSeasons.xml')
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(pretty_xml_str)
            print("File 'allSeasons.xml' created successfully!")
            return True
        except Exception as e:
            print(f"Failed to create file: {e}")
            return False



