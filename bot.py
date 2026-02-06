import discord
from discord import app_commands
from discord.ui import Select, View, Button
import asyncio
from datetime import datetime, timedelta
import json
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ALL FOOD TYPES (Crumplecorn exact)
FOOD_TYPES = {
    "Raw Meat": {"value": 50, "emoji": "🥩"},
    "Cooked Meat": {"value": 25, "emoji": "🍖"},
    "Raw Fish Meat": {"value": 25, "emoji": "🐟"},
    "Cooked Fish Meat": {"value": 12.5, "emoji": "🐠"},
    "Raw Meat (Carrion)": {"value": 15, "emoji": "🩸"},
    "Raw Fish Meat (Carrion)": {"value": 7.5, "emoji": "🐟"},
    "Mejoberry": {"value": 30, "emoji": "🫐"},
    "Berry": {"value": 20, "emoji": "🍇"},
    "Vegetables": {"value": 40, "emoji": "🥕"},
    "Spoiled Meat": {"value": 50, "emoji": "💀"},
    "Rare Flower": {"value": 60, "emoji": "🌺"},
    "Chitin": {"value": 50, "emoji": "🦗"},
    "Wyvern Milk": {"value": 1200, "emoji": "🥛"},
    "Primal Crystal": {"value": 350, "emoji": "💎"},
    "Ambergris": {"value": 500, "emoji": "🟡"},
    "Sulfur": {"value": 50, "emoji": "🟨"},
    "Nameless Venom": {"value": 400, "emoji": "🧪"},
    "Blood Pack": {"value": 200, "emoji": "🩸"},
    "Bio Toxin": {"value": 50, "emoji": "☠️"},
    "Berry (Archelon)": {"value": 15, "emoji": "🍇"},
    "Vegetables (Archelon)": {"value": 60, "emoji": "🥕"}
}

DINO_DATA = {
    "Allosaurus": {
        "basefoodrate": 0.001852,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 166666.66666666666,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Allosaurus.png/228px-Allosaurus.png"
    },
    "Amargasaurus": {
        "basefoodrate": 0.003156,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 333333.3333333333,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Amargasaurus.png/228px-Amargasaurus.png"
    },
    "Andrewsarchus": {
        "basefoodrate": 0.003156,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 208333.3333333333,
        "type": "Omnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat', 'Mejoberry', 'Berry'],
        "img": "https://ark.wiki.gg/images/thumb/Andrewsarchus.png/228px-Andrewsarchus.png"
    },
    "Anglerfish": {
        "basefoodrate": 0.001852,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 133333.33333333334,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Anglerfish.png/228px-Anglerfish.png"
    },
    "Ankylosaurus": {
        "basefoodrate": 0.003156,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 175438.5964912281,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Ankylosaurus.png/228px-Ankylosaurus.png"
    },
    "Araneo": {
        "basefoodrate": 0.001736,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 90090.09009009009,
        "type": "Carrion",
        "foods": ['Spoiled Meat', 'Raw Meat (Carrion)', 'Raw Fish Meat (Carrion)'],
        "img": "https://ark.wiki.gg/images/thumb/Araneo.png/228px-Araneo.png"
    },
    "Archaeopteryx": {
        "basefoodrate": 0.001302,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 55555.555555555555,
        "type": "Archaeopteryx",
        "foods": ['Chitin'],
        "img": "https://ark.wiki.gg/images/thumb/Archaeopteryx.png/228px-Archaeopteryx.png"
    },
    "Archelon": {
        "basefoodrate": 0.007716,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 666666.6666666666,
        "type": "Archelon",
        "foods": ['Vegetables (Archelon)', 'Bio Toxin', 'Berry (Archelon)'],
        "img": "https://ark.wiki.gg/images/thumb/Archelon.png/228px-Archelon.png"
    },
    "Argentavis": {
        "basefoodrate": 0.001852,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 196078.431372549,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Argentavis.png/228px-Argentavis.png"
    },
    "Armadoggo": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 196078.431372549,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Armadoggo.png/228px-Armadoggo.png"
    },
    "Arthropluera": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 185185.1851851852,
        "type": "Carrion",
        "foods": ['Spoiled Meat', 'Raw Meat (Carrion)', 'Raw Fish Meat (Carrion)'],
        "img": "https://ark.wiki.gg/images/thumb/Arthropluera.png/228px-Arthropluera.png"
    },
    "Astrodelphis": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 196078.431372549,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Astrodelphis.png/228px-Astrodelphis.png"
    },
    "Aureliax": {
        "basefoodrate": 0.01,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 333333.3333333333,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Aureliax.png/228px-Aureliax.png"
    },
    "Baryonyx": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 166666.66666666666,
        "type": "Piscivore",
        "foods": ['Raw Fish Meat', 'Cooked Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Baryonyx.png/228px-Baryonyx.png"
    },
    "Basilisk": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 666666.6666666666,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Basilisk.png/228px-Basilisk.png"
    },
    "Basilosaurus": {
        "basefoodrate": 0.002929,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 416666.6666666666,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Basilosaurus.png/228px-Basilosaurus.png"
    },
    "Beelzebufo": {
        "basefoodrate": 0.001929,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 133333.33333333334,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Beelzebufo.png/228px-Beelzebufo.png"
    },
    "Bison": {
        "basefoodrate": 0.003556,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 151515.15151515152,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Bison.png/228px-Bison.png"
    },
    "Bloodstalker": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 196078.431372549,
        "type": "BloodStalker",
        "foods": ['Blood Pack', 'Raw Meat (Carrion)', 'Raw Fish Meat (Carrion)'],
        "img": "https://ark.wiki.gg/images/thumb/Bloodstalker.png/228px-Bloodstalker.png"
    },
    "Brontosaurus": {
        "basefoodrate": 0.007716,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 333333.3333333333,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Brontosaurus.png/228px-Brontosaurus.png"
    },
    "Bulbdog": {
        "basefoodrate": 0.000868,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 175438.5964912281,
        "type": "Omnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat', 'Mejoberry', 'Berry'],
        "img": "https://ark.wiki.gg/images/thumb/Bulbdog.png/228px-Bulbdog.png"
    },
    "Carbonemys": {
        "basefoodrate": 0.003156,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 83333.33333333333,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Carbonemys.png/228px-Carbonemys.png"
    },
    "Carcharodontosaurus": {
        "basefoodrate": 0.002314,
        "babyfoodrate": 35.0,
        "extrababyfoodrate": 20.0,
        "base_mat": 878348.704435661,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Carcharodontosaurus.png/228px-Carcharodontosaurus.png"
    },
    "Carnotaurus": {
        "basefoodrate": 0.001852,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 166666.66666666666,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Carnotaurus.png/228px-Carnotaurus.png"
    },
    "Castoroides": {
        "basefoodrate": 0.002314,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 222222.22222222222,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Castoroides.png/228px-Castoroides.png"
    },
    "Cat": {
        "basefoodrate": 0.0008,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 111111.11111111111,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Cat.png/228px-Cat.png"
    },
    "Ceratosaurus": {
        "basefoodrate": 0.002314,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 476190.4761904762,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Ceratosaurus.png/228px-Ceratosaurus.png"
    },
    "Chalicotherium": {
        "basefoodrate": 0.003156,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 296296.2962962963,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Chalicotherium.png/228px-Chalicotherium.png"
    },
    "Compsognathus": {
        "basefoodrate": 0.000868,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 75757.57575757576,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Compsognathus.png/228px-Compsognathus.png"
    },
    "Cosmo": {
        "basefoodrate": 0.000868,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 333333.3333333333,
        "type": "CrystalWyvern",
        "foods": ['Primal Crystal'],
        "img": "https://ark.wiki.gg/images/thumb/Cosmo.png/228px-Cosmo.png"
    },
    "Daeodon": {
        "basefoodrate": 0.01,
        "babyfoodrate": 5.0,
        "extrababyfoodrate": 8.0,
        "base_mat": 175438.5964912281,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Daeodon.png/228px-Daeodon.png"
    },
    "Deinonychus": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 133333.33333333334,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Deinonychus.png/228px-Deinonychus.png"
    },
    "Deinosuchus": {
        "basefoodrate": 0.01,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 333333.3333333333,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Deinosuchus.png/228px-Deinosuchus.png"
    },
    "Deinotherium": {
        "basefoodrate": 0.002314,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 666666.6666666666,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Deinotherium.png/228px-Deinotherium.png"
    },
    "Desmodus": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 256410.2564102564,
        "type": "BloodStalker",
        "foods": ['Blood Pack', 'Raw Meat (Carrion)', 'Raw Fish Meat (Carrion)'],
        "img": "https://ark.wiki.gg/images/thumb/Desmodus.png/228px-Desmodus.png"
    },
    "Dilophosaurus": {
        "basefoodrate": 0.000868,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 75757.57575757576,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Dilophosaurus.png/228px-Dilophosaurus.png"
    },
    "Dimetrodon": {
        "basefoodrate": 0.001736,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 166666.66666666666,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Dimetrodon.png/228px-Dimetrodon.png"
    },
    "Dimorphodon": {
        "basefoodrate": 0.001302,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 90090.09009009009,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Dimorphodon.png/228px-Dimorphodon.png"
    },
    "Dinopithecus": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 333333.3333333333,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Dinopithecus.png/228px-Dinopithecus.png"
    },
    "Diplocaulus": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 133333.33333333334,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Diplocaulus.png/228px-Diplocaulus.png"
    },
    "Diplodocus": {
        "basefoodrate": 0.007716,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 333333.3333333333,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Diplodocus.png/228px-Diplodocus.png"
    },
    "Direbear": {
        "basefoodrate": 0.003156,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 166666.66666666666,
        "type": "Omnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat', 'Mejoberry', 'Berry'],
        "img": "https://ark.wiki.gg/images/thumb/Direbear.png/228px-Direbear.png"
    },
    "Direwolf": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 175438.5964912281,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Direwolf.png/228px-Direwolf.png"
    },
    "Dodo": {
        "basefoodrate": 0.000868,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 55555.555555555555,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Dodo.png/228px-Dodo.png"
    },
    "Doedicurus": {
        "basefoodrate": 0.003156,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 208333.3333333333,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Doedicurus.png/228px-Doedicurus.png"
    },
    "Drakeling": {
        "basefoodrate": 0.001302,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 90090.09009009009,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Drakeling.png/228px-Drakeling.png"
    },
    "Dreadmare": {
        "basefoodrate": 0.001929,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 416666.6666666666,
        "type": "Carrion",
        "foods": ['Spoiled Meat', 'Raw Meat (Carrion)', 'Raw Fish Meat (Carrion)'],
        "img": "https://ark.wiki.gg/images/thumb/Dreadmare.png/228px-Dreadmare.png"
    },
    "Dreadnoughtus": {
        "basefoodrate": 0.01,
        "babyfoodrate": 50.0,
        "extrababyfoodrate": 20.0,
        "base_mat": 666666.6666666666,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Dreadnoughtus.png/228px-Dreadnoughtus.png"
    },
    "Dunkleosteus": {
        "basefoodrate": 0.001852,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 296296.2962962963,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Dunkleosteus.png/228px-Dunkleosteus.png"
    },
    "Electrophorus": {
        "basefoodrate": 0.002929,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 166666.66666666666,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Electrophorus.png/228px-Electrophorus.png"
    },
    "Equus": {
        "basefoodrate": 0.001929,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 166666.66666666666,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Equus.png/228px-Equus.png"
    },
    "Fasolasuchus": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 666666.6666666666,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Fasolasuchus.png/228px-Fasolasuchus.png"
    },
    "Featherlight": {
        "basefoodrate": 0.000868,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 175438.5964912281,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Featherlight.png/228px-Featherlight.png"
    },
    "Ferox": {
        "basefoodrate": 0.000868,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 333333.3333333333,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Ferox.png/228px-Ferox.png"
    },
    "Fjordhawk": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 166666.66666666666,
        "type": "Omnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat', 'Mejoberry', 'Berry'],
        "img": "https://ark.wiki.gg/images/thumb/Fjordhawk.png/228px-Fjordhawk.png"
    },
    "Gacha": {
        "basefoodrate": 0.01,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 416666.6666666666,
        "type": "Omnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat', 'Mejoberry', 'Berry'],
        "img": "https://ark.wiki.gg/images/thumb/Gacha.png/228px-Gacha.png"
    },
    "Gallimimus": {
        "basefoodrate": 0.001929,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 95238.09523809522,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Gallimimus.png/228px-Gallimimus.png"
    },
    "Gasbag": {
        "basefoodrate": 0.002066,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 166666.66666666666,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Gasbag.png/228px-Gasbag.png"
    },
    "Giganotosaurus": {
        "basefoodrate": 0.002314,
        "babyfoodrate": 45.0,
        "extrababyfoodrate": 20.0,
        "base_mat": 878348.704435661,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Giganotosaurus.png/228px-Giganotosaurus.png"
    },
    "Gigantopithecus": {
        "basefoodrate": 0.004156,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 277777.7777777778,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Gigantopithecus.png/228px-Gigantopithecus.png"
    },
    "Gigantoraptor": {
        "basefoodrate": 0.002314,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 166666.66666666666,
        "type": "Omnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat', 'Mejoberry', 'Berry'],
        "img": "https://ark.wiki.gg/images/thumb/Gigantoraptor.png/228px-Gigantoraptor.png"
    },
    "Glowtail": {
        "basefoodrate": 0.000868,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 175438.5964912281,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Glowtail.png/228px-Glowtail.png"
    },
    "Hesperornis": {
        "basefoodrate": 0.001389,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 101010.101010101,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Hesperornis.png/228px-Hesperornis.png"
    },
    "Hyaenodon": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 166666.66666666666,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Hyaenodon.png/228px-Hyaenodon.png"
    },
    "Ichthyornis": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 133333.33333333334,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Ichthyornis.png/228px-Ichthyornis.png"
    },
    "Ichthyosaurus": {
        "basefoodrate": 0.001929,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 208333.3333333333,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Ichthyosaurus.png/228px-Ichthyosaurus.png"
    },
    "Iguanodon": {
        "basefoodrate": 0.001929,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 166666.66666666666,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Iguanodon.png/228px-Iguanodon.png"
    },
    "Jerboa": {
        "basefoodrate": 0.000868,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 75757.57575757576,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Jerboa.png/228px-Jerboa.png"
    },
    "Kairuku": {
        "basefoodrate": 0.001389,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 101010.101010101,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Kairuku.png/228px-Kairuku.png"
    },
    "Kaprosuchus": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 133333.33333333334,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Kaprosuchus.png/228px-Kaprosuchus.png"
    },
    "Karkinos": {
        "basefoodrate": 0.003156,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 416666.6666666666,
        "type": "Carrion",
        "foods": ['Spoiled Meat', 'Raw Meat (Carrion)', 'Raw Fish Meat (Carrion)'],
        "img": "https://ark.wiki.gg/images/thumb/Karkinos.png/228px-Karkinos.png"
    },
    "Kentrosaurus": {
        "basefoodrate": 0.005341,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 185185.1851851852,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Kentrosaurus.png/228px-Kentrosaurus.png"
    },
    "Lymantria": {
        "basefoodrate": 0.001852,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 111111.11111111111,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Lymantria.png/228px-Lymantria.png"
    },
    "Lystrosaurus": {
        "basefoodrate": 0.000868,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 55555.555555555555,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Lystrosaurus.png/228px-Lystrosaurus.png"
    },
    "Maewing": {
        "basefoodrate": 0.01,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 166666.66666666666,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Maewing.png/228px-Maewing.png"
    },
    "Magmasaur": {
        "basefoodrate": 0.000385,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 666666.6666666666,
        "type": "Magmasaur",
        "foods": ['Ambergris', 'Sulfur'],
        "img": "https://ark.wiki.gg/images/thumb/Magmasaur.png/228px-Magmasaur.png"
    },
    "Malwyn": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 175438.5964912281,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Malwyn.png/228px-Malwyn.png"
    },
    "Mammoth": {
        "basefoodrate": 0.004133,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 296296.2962962963,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Mammoth.png/228px-Mammoth.png"
    },
    "Managarmr": {
        "basefoodrate": 0.001852,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 333333.3333333333,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Managarmr.png/228px-Managarmr.png"
    },
    "Manta": {
        "basefoodrate": 0.001929,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 133333.33333333334,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Manta.png/228px-Manta.png"
    },
    "Mantis": {
        "basefoodrate": 0.002314,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 196078.431372549,
        "type": "Carrion",
        "foods": ['Spoiled Meat', 'Raw Meat (Carrion)', 'Raw Fish Meat (Carrion)'],
        "img": "https://ark.wiki.gg/images/thumb/Mantis.png/228px-Mantis.png"
    },
    "Megachelon": {
        "basefoodrate": 0.01,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 333333.3333333333,
        "type": "Omnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat', 'Mejoberry', 'Berry'],
        "img": "https://ark.wiki.gg/images/thumb/Megachelon.png/228px-Megachelon.png"
    },
    "Megalania": {
        "basefoodrate": 0.001736,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 133333.33333333334,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Megalania.png/228px-Megalania.png"
    },
    "Megaloceros": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 256410.2564102564,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Megaloceros.png/228px-Megaloceros.png"
    },
    "Megalodon": {
        "basefoodrate": 0.001852,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 333333.3333333333,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Megalodon.png/228px-Megalodon.png"
    },
    "Megalosaurus": {
        "basefoodrate": 0.001852,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 333333.3333333333,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Megalosaurus.png/228px-Megalosaurus.png"
    },
    "Megatherium": {
        "basefoodrate": 0.003156,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 333333.3333333333,
        "type": "Omnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat', 'Mejoberry', 'Berry'],
        "img": "https://ark.wiki.gg/images/thumb/Megatherium.png/228px-Megatherium.png"
    },
    "Mesopithecus": {
        "basefoodrate": 0.000868,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 111111.11111111111,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Mesopithecus.png/228px-Mesopithecus.png"
    },
    "Microraptor": {
        "basefoodrate": 0.000868,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 196078.431372549,
        "type": "Microraptor",
        "foods": ['Raw Meat', 'Cooked Meat', 'Rare Flower'],
        "img": "https://ark.wiki.gg/images/thumb/Microraptor.png/228px-Microraptor.png"
    },
    "Morellatops": {
        "basefoodrate": 0.005341,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 111111.11111111111,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Morellatops.png/228px-Morellatops.png"
    },
    "Mosasaurus": {
        "basefoodrate": 0.005,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 666666.6666666666,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Mosasaurus.png/228px-Mosasaurus.png"
    },
    "Moschops": {
        "basefoodrate": 0.001736,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 175438.5964912281,
        "type": "Omnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat', 'Mejoberry', 'Berry'],
        "img": "https://ark.wiki.gg/images/thumb/Moschops.png/228px-Moschops.png"
    },
    "Onyc": {
        "basefoodrate": 0.002893,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 101010.101010101,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Onyc.png/228px-Onyc.png"
    },
    "Ossidon": {
        "basefoodrate": 0.002314,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 333333.3333333333,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Ossidon.png/228px-Ossidon.png"
    },
    "Otter": {
        "basefoodrate": 0.002314,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 75757.57575757576,
        "type": "Piscivore",
        "foods": ['Raw Fish Meat', 'Cooked Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Otter.png/228px-Otter.png"
    },
    "Oviraptor": {
        "basefoodrate": 0.001302,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 75757.57575757576,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Oviraptor.png/228px-Oviraptor.png"
    },
    "Ovis": {
        "basefoodrate": 0.003156,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 175438.5964912281,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Ovis.png/228px-Ovis.png"
    },
    "Pachycephalosaurus": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 95238.09523809522,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Pachycephalosaurus.png/228px-Pachycephalosaurus.png"
    },
    "Pachyrhinosaurus": {
        "basefoodrate": 0.003156,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 166666.66666666666,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Pachyrhinosaurus.png/228px-Pachyrhinosaurus.png"
    },
    "Paraceratherium": {
        "basefoodrate": 0.0035,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 333333.3333333333,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Paraceratherium.png/228px-Paraceratherium.png"
    },
    "Parasaurolophus": {
        "basefoodrate": 0.001929,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 95238.09523809522,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Parasaurolophus.png/228px-Parasaurolophus.png"
    },
    "Pegomastax": {
        "basefoodrate": 0.000868,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 111111.11111111111,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Pegomastax.png/228px-Pegomastax.png"
    },
    "Pelagornis": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 133333.33333333334,
        "type": "Piscivore",
        "foods": ['Raw Fish Meat', 'Cooked Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Pelagornis.png/228px-Pelagornis.png"
    },
    "Phiomia": {
        "basefoodrate": 0.003156,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 175438.5964912281,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Phiomia.png/228px-Phiomia.png"
    },
    "Plesiosaurus": {
        "basefoodrate": 0.003858,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 416666.6666666666,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Plesiosaurus.png/228px-Plesiosaurus.png"
    },
    "Procoptodon": {
        "basefoodrate": 0.001929,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 166666.66666666666,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Procoptodon.png/228px-Procoptodon.png"
    },
    "Pteranodon": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 133333.33333333334,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Pteranodon.png/228px-Pteranodon.png"
    },
    "Pulmonoscorpius": {
        "basefoodrate": 0.001929,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 133333.33333333334,
        "type": "Carrion",
        "foods": ['Spoiled Meat', 'Raw Meat (Carrion)', 'Raw Fish Meat (Carrion)'],
        "img": "https://ark.wiki.gg/images/thumb/Pulmonoscorpius.png/228px-Pulmonoscorpius.png"
    },
    "Purlovia": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 175438.5964912281,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Purlovia.png/228px-Purlovia.png"
    },
    "Pyromane": {
        "basefoodrate": 0.001157,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 175438.5964912281,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Pyromane.png/228px-Pyromane.png"
    },
    "Quetzalcoatlus": {
        "basefoodrate": 0.0035,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 476190.4761904762,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Quetzalcoatlus.png/228px-Quetzalcoatlus.png"
    },
    "Raptor": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 133333.33333333334,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Raptor.png/228px-Raptor.png"
    },
    "Ravager": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 175438.5964912281,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Ravager.png/228px-Ravager.png"
    },
    "Reaper": {
        "basefoodrate": 0.002314,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 277777.7777777778,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Reaper.png/228px-Reaper.png"
    },
    "Rex": {
        "basefoodrate": 0.002314,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 333333.3333333333,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Rex.png/228px-Rex.png"
    },
    "Sabertooth": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 175438.5964912281,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Sabertooth.png/228px-Sabertooth.png"
    },
    "Sarcosuchus": {
        "basefoodrate": 0.001578,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 166666.66666666666,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Sarcosuchus.png/228px-Sarcosuchus.png"
    },
    "Shadowmane": {
        "basefoodrate": 0.001157,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 175438.5964912281,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Shadowmane.png/228px-Shadowmane.png"
    },
    "Shastasaurus": {
        "basefoodrate": 0.005,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 666666.6666666666,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Shastasaurus.png/228px-Shastasaurus.png"
    },
    "Shinehorn": {
        "basefoodrate": 0.000868,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 175438.5964912281,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Shinehorn.png/228px-Shinehorn.png"
    },
    "Sinomacrops": {
        "basefoodrate": 0.001302,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 55555.555555555555,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Sinomacrops.png/228px-Sinomacrops.png"
    },
    "Solwyn": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 175438.5964912281,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Solwyn.png/228px-Solwyn.png"
    },
    "Spinosaurus": {
        "basefoodrate": 0.002066,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 256410.2564102564,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Spinosaurus.png/228px-Spinosaurus.png"
    },
    "Stegosaurus": {
        "basefoodrate": 0.005341,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 185185.1851851852,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Stegosaurus.png/228px-Stegosaurus.png"
    },
    "Tapejara": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 196078.431372549,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Tapejara.png/228px-Tapejara.png"
    },
    "Therizinosaurus": {
        "basefoodrate": 0.002314,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 416666.6666666666,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Therizinosaurus.png/228px-Therizinosaurus.png"
    },
    "Thylacoleo": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 175438.5964912281,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Thylacoleo.png/228px-Thylacoleo.png"
    },
    "Triceratops": {
        "basefoodrate": 0.003156,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 166666.66666666666,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Triceratops.png/228px-Triceratops.png"
    },
    "Troodon": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 75757.57575757576,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Troodon.png/228px-Troodon.png"
    },
    "Tropeognathus": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 196078.431372549,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Tropeognathus.png/228px-Tropeognathus.png"
    },
    "Tusoteuthis": {
        "basefoodrate": 0.005,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 666666.6666666666,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Tusoteuthis.png/228px-Tusoteuthis.png"
    },
    "Veilwyn": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 166666.66666666666,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Veilwyn.png/228px-Veilwyn.png"
    },
    "Velonasaur": {
        "basefoodrate": 0.001543,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 166666.66666666666,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Velonasaur.png/228px-Velonasaur.png"
    },
    "Voidwyrm": {
        "basefoodrate": 0.000185,
        "babyfoodrate": 13.0,
        "extrababyfoodrate": 3.0,
        "base_mat": 333333.3333333333,
        "type": "Herbivore",
        "foods": ['Mejoberry', 'Berry', 'Vegetables'],
        "img": "https://ark.wiki.gg/images/thumb/Voidwyrm.png/228px-Voidwyrm.png"
    },
    "Vulture": {
        "basefoodrate": 0.001302,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 90090.09009009009,
        "type": "Vulture",
        "foods": ['Spoiled Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Vulture.png/228px-Vulture.png"
    },
    "Wyvern": {
        "basefoodrate": 0.000185,
        "babyfoodrate": 13.0,
        "extrababyfoodrate": 30.0,
        "base_mat": 333333.3333333333,
        "type": "Wyvern",
        "foods": ['Wyvern Milk'],
        "img": "https://ark.wiki.gg/images/thumb/Wyvern.png/228px-Wyvern.png"
    },
    "Xiphactinus": {
        "basefoodrate": 0.001578,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 333333.3333333333,
        "type": "Omnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat', 'Mejoberry', 'Berry'],
        "img": "https://ark.wiki.gg/images/thumb/Xiphactinus.png/228px-Xiphactinus.png"
    },
    "Yutyrannus": {
        "basefoodrate": 0.002314,
        "babyfoodrate": 25.5,
        "extrababyfoodrate": 20.0,
        "base_mat": 666666.6666666666,
        "type": "Carnivore",
        "foods": ['Raw Meat', 'Cooked Meat', 'Raw Fish Meat'],
        "img": "https://ark.wiki.gg/images/thumb/Yutyrannus.png/228px-Yutyrannus.png"
    },
}


BASE_MIN_FOOD_RATE = 0.000155
active_timers = {}

def is_evo():
    now_utc = datetime.utcnow()
    now_et = now_utc + timedelta(hours=-5)
    wd, h = now_et.weekday(), now_et.hour
    return (wd == 4 and h >= 13) or wd in [5, 6] or (wd == 0 and h < 21)

def get_mults():
    if is_evo():
        return {"mat": 4, "cuddle": 0.6, "imp": 4, "name": "🎉 EVO Weekend", "consumption": 1.0}
    return {"mat": 2, "cuddle": 1.0, "imp": 1, "name": "Weekday", "consumption": 1.0}

def calc_breed(dino, weight, food):
    if dino not in DINO_DATA:
        return None
    d = DINO_DATA[dino]
    m = get_mults()
    fv = FOOD_TYPES.get(food, FOOD_TYPES["Raw Meat"])["value"]
    
    # CRUMPLECORN EXACT
    total_mat = d["base_mat"] / m["mat"]
    juv_time = total_mat * 0.1
    
    # Food rates (Line 2611-2613)
    max_food_rate = d["basefoodrate"] * d["babyfoodrate"] * d["extrababyfoodrate"] * m["consumption"]
    min_food_rate = BASE_MIN_FOOD_RATE * d["babyfoodrate"] * d["extrababyfoodrate"] * m["consumption"]
    food_rate_decay = (max_food_rate - min_food_rate) / total_mat
    
    # Get food for period (Line 2839-2846)
    def get_food_for_period(start, end):
        end = min(total_mat, max(start, end))
        start_rate = max_food_rate - food_rate_decay * start
        end_rate = max_food_rate - food_rate_decay * end
        time = end - start
        return 0.5 * time * (start_rate - end_rate) + end_rate * time
    
    # Calculate (Line 2658-2665)
    baby_food_points = get_food_for_period(0, juv_time)
    total_food_points = get_food_for_period(0, total_mat)
    
    baby_food_items = baby_food_points / fv
    total_food_items = total_food_points / fv
    
    # Cuddles
    cuddle_int = 28800 * m["cuddle"]
    cuddles = max(1, int(total_mat / cuddle_int))
    
    return {
        "dino": dino, "weight": weight, "food": food,
        "emoji": FOOD_TYPES.get(food, FOOD_TYPES["Raw Meat"])["emoji"], 
        "mults": m, "juv_time": juv_time, "adult_time": total_mat,
        "baby_food": baby_food_items, "total_food": total_food_items,
        "cuddle_int": cuddle_int, "cuddles": cuddles,
        "img": d.get("img", ""), "type": d.get("type", "")
    }

def fmt_time(s):
    d = int(s // 86400)
    h = int((s % 86400) // 3600)
    m = int((s % 3600) // 60)
    sec = int(s % 60)
    if d > 0:
        return f"{d}d {h:02d}:{m:02d}:{sec:02d}"
    if h > 0:
        return f"{h:02d}:{m:02d}:{sec:02d}"
    return f"{m:02d}:{sec:02d}"

class FoodSelect(Select):
    def __init__(self, dino, weight):
        self.dino, self.weight = dino, weight
        foods = DINO_DATA[dino]["foods"]
        opts = [discord.SelectOption(label=f, emoji=FOOD_TYPES.get(f, {"emoji": "🍖"})["emoji"]) for f in foods[:25]]
        super().__init__(placeholder="🍖 Select food type...", options=opts)
    
    async def callback(self, i):
        s = calc_breed(self.dino, self.weight, self.values[0])
        if not s:
            return await i.response.send_message("❌ Error!", ephemeral=True)
        
        # Color by type
        type_colors = {
            'Carnivore': discord.Color.from_rgb(231, 76, 60),
            'Herbivore': discord.Color.from_rgb(46, 204, 113),
            'Omnivore': discord.Color.from_rgb(241, 196, 15),
            'BloodStalker': discord.Color.from_rgb(139, 0, 0),
            'Wyvern': discord.Color.from_rgb(138, 43, 226),
            'CrystalWyvern': discord.Color.from_rgb(100, 149, 237)
        }
        color = type_colors.get(s['type'], discord.Color.blue())
        
        e = discord.Embed(color=color, timestamp=datetime.utcnow())
        e.set_author(name=f"🦖 {s['dino']} - Breeding Calculator", icon_url="https://i.imgur.com/QN0l8VH.png")
        
        if s['img']:
            e.set_thumbnail(url=s['img'])
        
        e.add_field(
            name="⚙️ Server Settings",
            value=f"```yaml\n{s['mults']['name']}\nMature: {s['mults']['mat']}x\nCuddle: {s['mults']['cuddle']}x```",
            inline=True
        )
        
        e.add_field(
            name="👶 Baby Stats",
            value=f"```\nWeight: {s['weight']}\nFood: {s['emoji']} {s['food']}```",
            inline=True
        )
        
        e.add_field(name="\u200b", value="\u200b", inline=True)
        
        e.add_field(
            name="⏱️ Maturation Timeline",
            value=f"```diff\n+ Time to Juvenile: {fmt_time(s['juv_time'])}\n+ Time to Adult:    {fmt_time(s['adult_time'])}```",
            inline=False
        )
        
        e.add_field(
            name=f"{s['emoji']} Food Required",
            value=f"```\nFood to Juvenile (E): {int(s['baby_food']):,}\nFood to Adult (E):    {int(s['total_food']):,}```",
            inline=False
        )
        
        imp_per = min(100, int(100 / s['cuddles']))
        e.add_field(
            name="💕 Imprinting",
            value=f"```fix\nCuddles: {s['cuddles']}\nInterval: {fmt_time(s['cuddle_int'])}\nPer Cuddle: +{imp_per}%```",
            inline=False
        )
        
        e.set_footer(text="ARK: Survival Ascended • Small Tribes", icon_url="https://i.imgur.com/QN0l8VH.png")
        
        view = View(timeout=None)
        btn = Button(label="⏱️ Start Timer", style=discord.ButtonStyle.primary)
        
        async def start_timer_callback(btn_i):
            timer_id = f"{btn_i.user.id}_{s['dino']}_{int(datetime.utcnow().timestamp())}"
            start_time = datetime.utcnow()
            
            active_timers[timer_id] = {
                "user": btn_i.user.id,
                "dino": s['dino'],
                "start": start_time,
                "adult_time": s['adult_time'],
                "cuddle_int": s['cuddle_int'],
                "cuddles": s['cuddles']
            }
            
            timer_embed = discord.Embed(
                title=f"⏱️ {s['dino']} Timer Started!",
                description=f"**Time to Adult:** {fmt_time(s['adult_time'])}\n**Cuddles:** {s['cuddles']}\n**Ends:** <t:{int((start_time + timedelta(seconds=s['adult_time'])).timestamp())}:R>\n\n✅ You\'ll be pinged for each cuddle and when adult!",
                color=discord.Color.green()
            )
            await btn_i.response.send_message(embed=timer_embed, ephemeral=True)
            
            # Schedule cuddle pings
            asyncio.create_task(schedule_pings(btn_i.user, timer_id, s))
        
        btn.callback = start_timer_callback
        view.add_item(btn)
        
        await i.response.send_message(embed=e, view=view)

class WeightModal(discord.ui.Modal, title="🦖 Baby Weight"):
    def __init__(self, dino):
        super().__init__()
        self.dino = dino
        self.w = discord.ui.TextInput(label="Baby Weight", placeholder="e.g. 100", style=discord.TextStyle.short, max_length=10)
        self.add_item(self.w)
    
    async def on_submit(self, i):
        try:
            weight = float(self.w.value)
            if weight <= 0:
                raise ValueError()
            v = View(timeout=300)
            v.add_item(FoodSelect(self.dino, weight))
            await i.response.send_message(f"🦖 **{self.dino}** • Weight: **{weight}**\nSelect food:", view=v, ephemeral=True)
        except:
            await i.response.send_message("❌ Invalid weight!", ephemeral=True)

async def dino_auto(i: discord.Interaction, cur: str):
    dinos = sorted(DINO_DATA.keys())
    matches = [d for d in dinos if cur.lower() in d.lower()]
    return [app_commands.Choice(name=d, value=d) for d in matches[:25]]

@tree.command(name="breeding")
@app_commands.autocomplete(dino=dino_auto)
async def breeding(i: discord.Interaction, dino: str):
    if dino not in DINO_DATA:
        return await i.response.send_message(f"❌ **{dino}** not found!", ephemeral=True)
    await i.response.send_modal(WeightModal(dino))

@tree.command(name="dinos")
async def dinos(i: discord.Interaction):
    types = {}
    for name, data in DINO_DATA.items():
        t = data["type"]
        if t not in types:
            types[t] = []
        types[t].append(name)
    
    e = discord.Embed(title="📋 All Breedable Creatures", description=f"**Total: {len(DINO_DATA)} creatures**", color=discord.Color.blue())
    
    for dino_type, names in sorted(types.items()):
        display = ", ".join(sorted(names)[:20])
        if len(names) > 20:
            display += f"... +{len(names)-20} more"
        e.add_field(name=f"{dino_type} ({len(names)})", value=display, inline=False)
    
    await i.response.send_message(embed=e)

class DeleteTimerButton(Button):
    def __init__(self, timer_id, dino_name):
        super().__init__(label=f"🗑️ Delete {dino_name}", style=discord.ButtonStyle.danger, custom_id=f"del_{timer_id}")
        self.timer_id = timer_id
    
    async def callback(self, i):
        if self.timer_id in active_timers:
            del active_timers[self.timer_id]
            await i.response.send_message(f"✅ Timer deleted!", ephemeral=True)
        else:
            await i.response.send_message("❌ Timer already finished!", ephemeral=True)

@tree.command(name="timers")
async def timers(i: discord.Interaction):
    user_timers = {k: v for k, v in active_timers.items() if v["user"] == i.user.id}
    if not user_timers:
        return await i.response.send_message("❌ No active timers!", ephemeral=True)
    
    e = discord.Embed(title="⏱️ Your Active Timers", color=discord.Color.blue())
    view = View(timeout=300)
    
    for timer_id, timer in user_timers.items():
        elapsed = (datetime.utcnow() - timer["start"]).total_seconds()
        remaining = max(0, timer["adult_time"] - elapsed)
        progress = min(100, (elapsed / timer["adult_time"]) * 100)
        
        e.add_field(
            name=f"🦖 {timer['dino']}", 
            value=f"Progress: {progress:.1f}%\nRemaining: {fmt_time(remaining)}", 
            inline=True
        )
        
        # Add delete button for each timer
        view.add_item(DeleteTimerButton(timer_id, timer['dino']))
    
    await i.response.send_message(embed=e, view=view, ephemeral=True)

@tree.command(name="event")
async def event(i: discord.Interaction):
    m = get_mults()
    e = discord.Embed(title=m['name'], description="**ARK Small Tribes Rates**", color=discord.Color.green() if is_evo() else discord.Color.blue())
    e.add_field(name="⚙️ Current Multipliers", value=f"```yaml\nMature: {m['mat']}x\nCuddle: {m['cuddle']}x\nImprint: {m['imp']}x```", inline=False)
    await i.response.send_message(embed=e)


# Ping scheduling function
async def schedule_pings(user, timer_id, stats):
    """Schedule pings for cuddles and adult"""
    start_time = active_timers[timer_id]["start"]
    
    # Schedule cuddle pings
    for cuddle_num in range(1, stats['cuddles'] + 1):
        cuddle_time = stats['cuddle_int'] * cuddle_num
        wait_seconds = cuddle_time - (datetime.utcnow() - start_time).total_seconds()
        
        if wait_seconds > 0:
            await asyncio.sleep(wait_seconds)
            
            # Check if timer still active
            if timer_id not in active_timers:
                return
            
            try:
                embed = discord.Embed(
                    title=f"💕 {stats['dino']} needs imprint!",
                    color=discord.Color.from_rgb(255, 105, 180)
                )
                await user.send(embed=embed)
            except:
                pass  # User has DMs disabled
    
    # Schedule adult ping
    adult_wait = stats['adult_time'] - (datetime.utcnow() - start_time).total_seconds()
    if adult_wait > 0:
        await asyncio.sleep(adult_wait)
        
        # Check if timer still active
        if timer_id not in active_timers:
            return
        
        try:
            embed = discord.Embed(
                title=f"🎉 {stats['dino']} is now Adult!",
                description=f"Fully matured! 🦖",
                color=discord.Color.from_rgb(46, 204, 113)
            )
            await user.send(embed=embed)
        except:
            pass  # User has DMs disabled
        
        # Remove from active timers
        if timer_id in active_timers:
            del active_timers[timer_id]

@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot Online: {client.user}")
    print(f"📊 {len(DINO_DATA)} creatures")
    print(f"🍖 {len(FOOD_TYPES)} food types")
    print(f"🎯 100% Crumplecorn-accurate!")

if __name__ == "__main__":
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        try:
            with open("config.json") as f:
                token = json.load(f).get("bot_token")
        except:
            print("❌ No token!")
            exit(1)
    client.run(token)
