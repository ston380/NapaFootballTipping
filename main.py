#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from numpy import random
# import sys
# from kitchen.text.converters import getwriter
# import matplotlib.pyplot as plt
# import matplotlib.ticker as plticker
# from pandas.tools.plotting import table
import matplotlib
import requests
from bs4 import BeautifulSoup
import re

scrape_all = True

wiki_url = 'https://en.wikipedia.org/wiki/2018_FIFA_World_Cup'
warnings_url = None
player_stats_url = None
team_standings_url = None
goals_allowed_url = None


# coupons file
submissionsfile = "fifa_2018_napa.csv"

team_status = ("Open", "Eliminated", "Group Runner-up", "Group Winner", "Semifinals", "Final")

submissions_df = pd.read_csv(submissionsfile)

wiki_get = requests.get(wiki_url)
soup = BeautifulSoup(wiki_get.content, "html.parser")


class Competition:
    def __init__(self, data):
        self.name = [] # make this the scraped data
        self.teams
        self.groups


    def name(self):
        return com

    def teams(self):
        pass

    def groups(self):
        pass

    def results(self):
        pass



class Team:
    def __init__(self):
        self.name




def get_groups(datafile=None):
    groups = []
    if not datafile:
        for link in soup.find_all('a'):
            ref = link.get('href')
            # print ref
            try:
                if len(ref) == 8 and str(ref)[:-2] == '#Group':
                    groups.append(str(ref)[1:].replace('_', ' '))
            except TypeError:
                pass
    else:
        groups = pd.read_csv(datafile)
    return groups


def get_schedule(groups=get_groups()):
    teams = {}
    matches = {}
    full_text = "2018 FIFA World Cup "

    for g in groups:
        match_no = None
        group_teams = []
        try:
            tags = soup.find_all('a', {'title': full_text + g})
            tags = tags[1:-2]
            for t in tags:
                # print t.text
                link = str(t.get('href'))
                hash_pos = link.find('#')
                vs_pos = link.find('_vs_')
                home_team = link[hash_pos + 1:vs_pos].replace('_', ' ')
                away_team = link[vs_pos + 4:].replace('_', ' ')
                match_no = int(t.text[-2:].strip())
                group_teams.extend([home_team, away_team])
                matches[match_no] = {'home': home_team,
                                     'away': away_team,
                                     'home_goals': None,
                                     'away_goals': None,
                                     'group': g[-1:]}
        except (UnicodeError or TypeError):
            pass
        group_teams = set(group_teams)
        teams[g] = group_teams

    group_stage_matches = max(matches.keys())
    # print "Total of {} group stage matches".format(group_stage_matches)

    try:
        tags = soup.find_all('a', {'title': full_text + 'knockout stage'})
        tags = tags[1:-1]

        for t in tags:
            match_no = None
            stage = None
            link = str(t.get('href'))
            hash_pos = link.find('#')
            vs_pos = link.find('_vs_')

            home_team = str(link[hash_pos + 1:vs_pos].replace('_', ' '))
            away_team = str(link[vs_pos + 4:].replace('_', ' '))

            if home_team.find('Winners Group') == 0:
                home_team = home_team[-1:] + '1'
                away_team = away_team[-1:] + '2'
                stage = 'R16'
            elif home_team.find('Winners Match') == 0:
                home_team = 'W' + home_team[-2:]
                away_team = 'W' + away_team[-2:]
                stage = 'QF'
            elif vs_pos < 0:
                words = t.parent.parent.text.split()
                home_team = 'L' + words[2]
                away_team = 'L' + words[-1]
                stage = '3P'
            else:
                pass

            match_no = int(t.text[-2:].strip())

            if match_no > group_stage_matches + 12 and not stage:
                stage = 'SF'

            matches[match_no] = {'home': home_team,
                                 'away': away_team,
                                 'group': stage}

            if max(list(matches.keys())) == 63:
                matches[64] = {'home': matches[63]['home'].replace('L', 'W'),
                               'away': matches[63]['away'].replace('L', 'W'),
                               'group': '1F'}

    except (UnicodeError or TypeError):
        # print t
        pass

    return teams, matches


def get_match_results(results=get_schedule()[1]):
    for k in results.keys():
        print
        "Match " + str(k)
        results[k]['home_goals'] = None
        results[k]['away_goals'] = None

        if results[k]['home_goals'] is not None:
            if results[k]['home_goals'] == results[k]['away_goals']:
                results[k][result] = 'X'
            elif results[k]['home_goals'] > results[k]['away_goals']:
                results[k]['result'] = '1'
            else:
                results[k]['result'] = '2'
        else:
            results[k]['result'] = None

    pass
    # return results


def get_coupon_data(df, email='all'):
    if email == 'all':
        user_submission = df
        return user_submission
    else:
        user_submission = df[df.Email == email]
        return user_submission.T


def get_player_goals():
    pass


def get_team_warnings():
    pass


def get_goals_allowed():
    pass


def get_total_goals():
    pass


def update_rankings():
    pass


get_match_results()