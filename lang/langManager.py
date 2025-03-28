
import importlib, os, json, discord

from collections import defaultdict

class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'

from utils import *
from economy import *
from config import *
from functions import checkData

class langManager():
    def __init__(self):
        super().__init__()

        self.langDirectory = 'lang/'
        self.availableLanguages = []
        self.languagesNames = []

        for lang in os.listdir(self.langDirectory):

            if not lang.endswith('.json'):
                continue

            with open(self.langDirectory + lang, 'r', encoding='utf-8') as file:
                data = json.load(file)


            self.languagesNames.append(data['languageName'])
            self.availableLanguages.append(lang.replace('.json', ''))


    def getLangStrings(self, guildID):
        for lang in os.listdir(self.langDirectory):

            if not lang.endswith('.json'):
                continue

            if getServerLang(guildID) in lang:
                with open(self.langDirectory + lang, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                    return data

    def getString(self, stringName='langChange', member: discord.member.Member = None, guildID = None, extra1 = None, extra2 = None, extra3 = None):
        strings = self.getLangStrings(guildID)

        if strings == None:
            with open(self.langDirectory + 'en.json', 'r', encoding='utf-8') as file:
                strings = json.load(file)

        if not stringName in strings:
            return 'String was not found.'

        string = strings[stringName]

        if member != None:

            if '{memberName}' in string:
                string = string.format_map(SafeDict(memberName = member.display_name))


            if '{memberBalance}' in string:
                string = string.format_map(SafeDict(memberBalance = getUserMoney(member)))


        if guildID != None:

            if '{coinSymbol}' in string:
                string = string.format_map(SafeDict(coinSymbol=getCoinSymbol(guildID)))


            if '{coinName}' in string:
                string = string.format_map(SafeDict(coinName=getCoinName(guildID)))


        if extra1 != None:

            if '{extra1}' in string:
                string = string.format_map(SafeDict(extra1=extra1))

        if extra2 != None:

            if '{extra2}' in string:
                string = string.format_map(SafeDict(extra2=extra2))

        if extra3 != None:

            if '{extra3}' in string:
                string = string.format_map(SafeDict(extra3=extra3))

        return string

langMan = langManager()