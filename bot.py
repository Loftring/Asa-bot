import discord
from discord import app_commands
from discord.ui import Select, View
import asyncio
from datetime import datetime, timedelta
import json
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# FOOD VALUES (Crumplecorn exact)
FOOD_TYPES = {
    "Raw Meat": {"value": 50, "emoji": "🥩"},
    "Cooked Meat": {"value": 25, "emoji": "🍖"},
    "Raw Prime Meat": {"value": 50, "emoji": "🥩"},
    "Cooked Prime Meat": {"value": 50, "emoji": "🍖"},
    "Raw Fish Meat": {"value": 25, "emoji": "🐟"},
    "Cooked Fish Meat": {"value": 12.5, "emoji": "🐠"},
    "Raw Mutton": {"value": 50, "emoji": "🥩"},
    "Mejoberries": {"value": 30, "emoji": "🫐"},
    "Berries": {"value": 20, "emoji": "🍇"},
    "Vegetables": {"value": 40, "emoji": "🥕"},
    "Spoiled Meat": {"value": 50, "emoji": "💀"}
}

# ALL 146 DINOS - CRUMPLECORN EXACT DATA
DINO_DATA = {
    "Allosaurus": {"base_mat": 166666.7, "food_drain": 0.740800, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/a/allosaurus.png/300px-Allosaurus.png", "cat": "carnivore"},
    "Amargasaurus": {"base_mat": 333333.3, "food_drain": 1.262400, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/a/amargasaurus.png/300px-Amargasaurus.png", "cat": "herbivore"},
    "Andrewsarchus": {"base_mat": 208333.3, "food_drain": 1.262400, "foods": ['Raw Meat', 'Cooked Meat', 'Mejoberries', 'Berries'], "img": "https://ark.wiki.gg/images/thumb/a/andrewsarchus.png/300px-Andrewsarchus.png", "cat": "omnivore"},
    "Anglerfish": {"base_mat": 133333.3, "food_drain": 0.740800, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/a/anglerfish.png/300px-Anglerfish.png", "cat": "carnivore"},
    "Ankylosaurus": {"base_mat": 175438.6, "food_drain": 1.262400, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/a/ankylosaurus.png/300px-Ankylosaurus.png", "cat": "herbivore"},
    "Araneo": {"base_mat": 90090.1, "food_drain": 0.694400, "foods": ['Spoiled Meat', 'Raw Meat'], "img": "https://ark.wiki.gg/images/thumb/a/araneo.png/300px-Araneo.png", "cat": "omnivore"},
    "Archaeopteryx": {"base_mat": 55555.6, "food_drain": 0.520800, "foods": ['Raw Meat', 'Cooked Meat'], "img": "https://ark.wiki.gg/images/thumb/a/archaeopteryx.png/300px-Archaeopteryx.png", "cat": "omnivore"},
    "Archelon": {"base_mat": 666666.7, "food_drain": 3.086400, "foods": ['Vegetables', 'Berries'], "img": "https://ark.wiki.gg/images/thumb/a/archelon.png/300px-Archelon.png", "cat": "omnivore"},
    "Argentavis": {"base_mat": 196078.4, "food_drain": 0.740800, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/a/argentavis.png/300px-Argentavis.png", "cat": "carnivore"},
    "Armadoggo": {"base_mat": 196078.4, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/a/armadoggo.png/300px-Armadoggo.png", "cat": "carnivore"},
    "Arthropluera": {"base_mat": 185185.2, "food_drain": 0.617200, "foods": ['Spoiled Meat', 'Raw Meat'], "img": "https://ark.wiki.gg/images/thumb/a/arthropluera.png/300px-Arthropluera.png", "cat": "omnivore"},
    "Astrodelphis": {"base_mat": 196078.4, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/a/astrodelphis.png/300px-Astrodelphis.png", "cat": "carnivore"},
    "Aureliax": {"base_mat": 333333.3, "food_drain": 4.000000, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/a/aureliax.png/300px-Aureliax.png", "cat": "carnivore"},
    "Baryonyx": {"base_mat": 166666.7, "food_drain": 0.617200, "foods": ['Raw Fish Meat', 'Cooked Fish Meat'], "img": "https://ark.wiki.gg/images/thumb/b/baryonyx.png/300px-Baryonyx.png", "cat": "carnivore"},
    "Basilisk": {"base_mat": 666666.7, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/b/basilisk.png/300px-Basilisk.png", "cat": "carnivore"},
    "Basilosaurus": {"base_mat": 416666.7, "food_drain": 1.171600, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/b/basilosaurus.png/300px-Basilosaurus.png", "cat": "carnivore"},
    "Beelzebufo": {"base_mat": 133333.3, "food_drain": 0.771600, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/b/beelzebufo.png/300px-Beelzebufo.png", "cat": "carnivore"},
    "Bison": {"base_mat": 151515.2, "food_drain": 1.422400, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/b/bison.png/300px-Bison.png", "cat": "herbivore"},
    "Bloodstalker": {"base_mat": 196078.4, "food_drain": 0.617200, "foods": ['Raw Meat'], "img": "https://ark.wiki.gg/images/thumb/b/bloodstalker.png/300px-Bloodstalker.png", "cat": "omnivore"},
    "Brontosaurus": {"base_mat": 333333.3, "food_drain": 3.086400, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/b/brontosaurus.png/300px-Brontosaurus.png", "cat": "herbivore"},
    "Bulbdog": {"base_mat": 175438.6, "food_drain": 0.347200, "foods": ['Raw Meat', 'Cooked Meat', 'Mejoberries', 'Berries'], "img": "https://ark.wiki.gg/images/thumb/b/bulbdog.png/300px-Bulbdog.png", "cat": "omnivore"},
    "Carbonemys": {"base_mat": 83333.3, "food_drain": 1.262400, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/c/carbonemys.png/300px-Carbonemys.png", "cat": "herbivore"},
    "Carcharodontosaurus": {"base_mat": 878348.7, "food_drain": 0.925600, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/c/carcharodontosaurus.png/300px-Carcharodontosaurus.png", "cat": "carnivore"},
    "Carnotaurus": {"base_mat": 166666.7, "food_drain": 0.740800, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/c/carnotaurus.png/300px-Carnotaurus.png", "cat": "carnivore"},
    "Castoroides": {"base_mat": 222222.2, "food_drain": 0.925600, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/c/castoroides.png/300px-Castoroides.png", "cat": "herbivore"},
    "Cat": {"base_mat": 111111.1, "food_drain": 0.320000, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/c/cat.png/300px-Cat.png", "cat": "carnivore"},
    "Ceratosaurus": {"base_mat": 476190.5, "food_drain": 0.925600, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/c/ceratosaurus.png/300px-Ceratosaurus.png", "cat": "carnivore"},
    "Chalicotherium": {"base_mat": 296296.3, "food_drain": 1.262400, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/c/chalicotherium.png/300px-Chalicotherium.png", "cat": "herbivore"},
    "Compsognathus": {"base_mat": 75757.6, "food_drain": 0.347200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/c/compsognathus.png/300px-Compsognathus.png", "cat": "carnivore"},
    "Cosmo": {"base_mat": 333333.3, "food_drain": 0.347200, "foods": ['Raw Meat', 'Cooked Meat'], "img": "https://ark.wiki.gg/images/thumb/c/cosmo.png/300px-Cosmo.png", "cat": "omnivore"},
    "Crystal Wyvern": {"base_mat": 333333.3, "food_drain": 0.006660, "foods": ['Raw Meat'], "img": "https://ark.wiki.gg/images/thumb/c/crystal_Wyvern.png/300px-Crystal_Wyvern.png", "cat": "omnivore"},
    "Daeodon": {"base_mat": 175438.6, "food_drain": 0.640000, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/d/daeodon.png/300px-Daeodon.png", "cat": "carnivore"},
    "Deinonychus": {"base_mat": 133333.3, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/d/deinonychus.png/300px-Deinonychus.png", "cat": "carnivore"},
    "Deinosuchus": {"base_mat": 333333.3, "food_drain": 4.000000, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/d/deinosuchus.png/300px-Deinosuchus.png", "cat": "carnivore"},
    "Deinotherium": {"base_mat": 666666.7, "food_drain": 0.925600, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/d/deinotherium.png/300px-Deinotherium.png", "cat": "herbivore"},
    "Desmodus": {"base_mat": 256410.3, "food_drain": 0.617200, "foods": ['Raw Meat'], "img": "https://ark.wiki.gg/images/thumb/d/desmodus.png/300px-Desmodus.png", "cat": "omnivore"},
    "Dilophosaurus": {"base_mat": 75757.6, "food_drain": 0.347200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/d/dilophosaurus.png/300px-Dilophosaurus.png", "cat": "carnivore"},
    "Dimetrodon": {"base_mat": 166666.7, "food_drain": 0.694400, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/d/dimetrodon.png/300px-Dimetrodon.png", "cat": "carnivore"},
    "Dimorphodon": {"base_mat": 90090.1, "food_drain": 0.520800, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/d/dimorphodon.png/300px-Dimorphodon.png", "cat": "carnivore"},
    "Dinopithecus": {"base_mat": 333333.3, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/d/dinopithecus.png/300px-Dinopithecus.png", "cat": "carnivore"},
    "Diplocaulus": {"base_mat": 133333.3, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/d/diplocaulus.png/300px-Diplocaulus.png", "cat": "carnivore"},
    "Diplodocus": {"base_mat": 333333.3, "food_drain": 3.086400, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/d/diplodocus.png/300px-Diplodocus.png", "cat": "herbivore"},
    "Direbear": {"base_mat": 166666.7, "food_drain": 1.262400, "foods": ['Raw Meat', 'Cooked Meat', 'Mejoberries', 'Berries'], "img": "https://ark.wiki.gg/images/thumb/d/direbear.png/300px-Direbear.png", "cat": "omnivore"},
    "Direwolf": {"base_mat": 175438.6, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/d/direwolf.png/300px-Direwolf.png", "cat": "carnivore"},
    "Dodo": {"base_mat": 55555.6, "food_drain": 0.347200, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/d/dodo.png/300px-Dodo.png", "cat": "herbivore"},
    "Doedicurus": {"base_mat": 208333.3, "food_drain": 1.262400, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/d/doedicurus.png/300px-Doedicurus.png", "cat": "herbivore"},
    "Drakeling": {"base_mat": 90090.1, "food_drain": 0.520800, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/d/drakeling.png/300px-Drakeling.png", "cat": "carnivore"},
    "Dreadmare": {"base_mat": 416666.7, "food_drain": 0.771600, "foods": ['Spoiled Meat', 'Raw Meat'], "img": "https://ark.wiki.gg/images/thumb/d/dreadmare.png/300px-Dreadmare.png", "cat": "omnivore"},
    "Dreadnoughtus": {"base_mat": 666666.7, "food_drain": 4.000000, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/d/dreadnoughtus.png/300px-Dreadnoughtus.png", "cat": "herbivore"},
    "Dunkleosteus": {"base_mat": 296296.3, "food_drain": 0.740800, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/d/dunkleosteus.png/300px-Dunkleosteus.png", "cat": "carnivore"},
    "Electrophorus": {"base_mat": 166666.7, "food_drain": 1.171600, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/e/electrophorus.png/300px-Electrophorus.png", "cat": "carnivore"},
    "Equus": {"base_mat": 166666.7, "food_drain": 0.771600, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/e/equus.png/300px-Equus.png", "cat": "herbivore"},
    "Fasolasuchus": {"base_mat": 666666.7, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/f/fasolasuchus.png/300px-Fasolasuchus.png", "cat": "carnivore"},
    "Featherlight": {"base_mat": 175438.6, "food_drain": 0.347200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/f/featherlight.png/300px-Featherlight.png", "cat": "carnivore"},
    "Ferox": {"base_mat": 333333.3, "food_drain": 0.347200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/f/ferox.png/300px-Ferox.png", "cat": "carnivore"},
    "Fjordhawk": {"base_mat": 166666.7, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Mejoberries', 'Berries'], "img": "https://ark.wiki.gg/images/thumb/f/fjordhawk.png/300px-Fjordhawk.png", "cat": "omnivore"},
    "Gacha": {"base_mat": 416666.7, "food_drain": 4.000000, "foods": ['Raw Meat', 'Cooked Meat', 'Mejoberries', 'Berries'], "img": "https://ark.wiki.gg/images/thumb/g/gacha.png/300px-Gacha.png", "cat": "omnivore"},
    "Gallimimus": {"base_mat": 95238.1, "food_drain": 0.771600, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/g/gallimimus.png/300px-Gallimimus.png", "cat": "herbivore"},
    "Gasbag": {"base_mat": 166666.7, "food_drain": 0.826400, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/g/gasbag.png/300px-Gasbag.png", "cat": "herbivore"},
    "Giganotosaurus": {"base_mat": 878348.7, "food_drain": 0.925600, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/g/giganotosaurus.png/300px-Giganotosaurus.png", "cat": "carnivore"},
    "Gigantopithecus": {"base_mat": 277777.8, "food_drain": 1.662400, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/g/gigantopithecus.png/300px-Gigantopithecus.png", "cat": "herbivore"},
    "Gigantoraptor": {"base_mat": 166666.7, "food_drain": 0.925600, "foods": ['Raw Meat', 'Cooked Meat', 'Mejoberries', 'Berries'], "img": "https://ark.wiki.gg/images/thumb/g/gigantoraptor.png/300px-Gigantoraptor.png", "cat": "omnivore"},
    "Glowtail": {"base_mat": 175438.6, "food_drain": 0.347200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/g/glowtail.png/300px-Glowtail.png", "cat": "carnivore"},
    "Hesperornis": {"base_mat": 101010.1, "food_drain": 0.555600, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/h/hesperornis.png/300px-Hesperornis.png", "cat": "carnivore"},
    "Hyaenodon": {"base_mat": 166666.7, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/h/hyaenodon.png/300px-Hyaenodon.png", "cat": "carnivore"},
    "Ichthyornis": {"base_mat": 133333.3, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/i/ichthyornis.png/300px-Ichthyornis.png", "cat": "carnivore"},
    "Ichthyosaurus": {"base_mat": 208333.3, "food_drain": 0.771600, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/i/ichthyosaurus.png/300px-Ichthyosaurus.png", "cat": "carnivore"},
    "Iguanodon": {"base_mat": 166666.7, "food_drain": 0.771600, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/i/iguanodon.png/300px-Iguanodon.png", "cat": "herbivore"},
    "Jerboa": {"base_mat": 75757.6, "food_drain": 0.347200, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/j/jerboa.png/300px-Jerboa.png", "cat": "herbivore"},
    "Kairuku": {"base_mat": 101010.1, "food_drain": 0.555600, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/k/kairuku.png/300px-Kairuku.png", "cat": "carnivore"},
    "Kaprosuchus": {"base_mat": 133333.3, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/k/kaprosuchus.png/300px-Kaprosuchus.png", "cat": "carnivore"},
    "Karkinos": {"base_mat": 416666.7, "food_drain": 1.262400, "foods": ['Spoiled Meat', 'Raw Meat'], "img": "https://ark.wiki.gg/images/thumb/k/karkinos.png/300px-Karkinos.png", "cat": "omnivore"},
    "Kentrosaurus": {"base_mat": 185185.2, "food_drain": 2.136400, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/k/kentrosaurus.png/300px-Kentrosaurus.png", "cat": "herbivore"},
    "Lymantria": {"base_mat": 111111.1, "food_drain": 0.740800, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/l/lymantria.png/300px-Lymantria.png", "cat": "herbivore"},
    "Lystrosaurus": {"base_mat": 55555.6, "food_drain": 0.347200, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/l/lystrosaurus.png/300px-Lystrosaurus.png", "cat": "herbivore"},
    "Maewing": {"base_mat": 166666.7, "food_drain": 4.000000, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/m/maewing.png/300px-Maewing.png", "cat": "carnivore"},
    "Magmasaur": {"base_mat": 666666.7, "food_drain": 0.154000, "foods": ['Raw Meat'], "img": "https://ark.wiki.gg/images/thumb/m/magmasaur.png/300px-Magmasaur.png", "cat": "omnivore"},
    "Malwyn": {"base_mat": 175438.6, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/m/malwyn.png/300px-Malwyn.png", "cat": "carnivore"},
    "Mammoth": {"base_mat": 296296.3, "food_drain": 1.653200, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/m/mammoth.png/300px-Mammoth.png", "cat": "herbivore"},
    "Managarmr": {"base_mat": 333333.3, "food_drain": 0.740800, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/m/managarmr.png/300px-Managarmr.png", "cat": "carnivore"},
    "Manta": {"base_mat": 133333.3, "food_drain": 0.771600, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/m/manta.png/300px-Manta.png", "cat": "carnivore"},
    "Mantis": {"base_mat": 196078.4, "food_drain": 0.925600, "foods": ['Spoiled Meat', 'Raw Meat'], "img": "https://ark.wiki.gg/images/thumb/m/mantis.png/300px-Mantis.png", "cat": "omnivore"},
    "Megachelon": {"base_mat": 333333.3, "food_drain": 4.000000, "foods": ['Raw Meat', 'Cooked Meat', 'Mejoberries', 'Berries'], "img": "https://ark.wiki.gg/images/thumb/m/megachelon.png/300px-Megachelon.png", "cat": "omnivore"},
    "Megalania": {"base_mat": 133333.3, "food_drain": 0.694400, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/m/megalania.png/300px-Megalania.png", "cat": "carnivore"},
    "Megaloceros": {"base_mat": 256410.3, "food_drain": 0.617200, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/m/megaloceros.png/300px-Megaloceros.png", "cat": "herbivore"},
    "Megalodon": {"base_mat": 333333.3, "food_drain": 0.740800, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/m/megalodon.png/300px-Megalodon.png", "cat": "carnivore"},
    "Megalosaurus": {"base_mat": 333333.3, "food_drain": 0.740800, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/m/megalosaurus.png/300px-Megalosaurus.png", "cat": "carnivore"},
    "Megatherium": {"base_mat": 333333.3, "food_drain": 1.262400, "foods": ['Raw Meat', 'Cooked Meat', 'Mejoberries', 'Berries'], "img": "https://ark.wiki.gg/images/thumb/m/megatherium.png/300px-Megatherium.png", "cat": "omnivore"},
    "Mesopithecus": {"base_mat": 111111.1, "food_drain": 0.347200, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/m/mesopithecus.png/300px-Mesopithecus.png", "cat": "herbivore"},
    "Microraptor": {"base_mat": 196078.4, "food_drain": 0.347200, "foods": ['Raw Meat', 'Cooked Meat'], "img": "https://ark.wiki.gg/images/thumb/m/microraptor.png/300px-Microraptor.png", "cat": "omnivore"},
    "Morellatops": {"base_mat": 111111.1, "food_drain": 2.136400, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/m/morellatops.png/300px-Morellatops.png", "cat": "herbivore"},
    "Mosasaurus": {"base_mat": 666666.7, "food_drain": 2.000000, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/m/mosasaurus.png/300px-Mosasaurus.png", "cat": "carnivore"},
    "Moschops": {"base_mat": 175438.6, "food_drain": 0.694400, "foods": ['Raw Meat', 'Cooked Meat', 'Mejoberries', 'Berries'], "img": "https://ark.wiki.gg/images/thumb/m/moschops.png/300px-Moschops.png", "cat": "omnivore"},
    "Onyc": {"base_mat": 101010.1, "food_drain": 1.157200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/o/onyc.png/300px-Onyc.png", "cat": "carnivore"},
    "Ossidon": {"base_mat": 333333.3, "food_drain": 0.925600, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/o/ossidon.png/300px-Ossidon.png", "cat": "carnivore"},
    "Otter": {"base_mat": 75757.6, "food_drain": 0.925600, "foods": ['Raw Fish Meat', 'Cooked Fish Meat'], "img": "https://ark.wiki.gg/images/thumb/o/otter.png/300px-Otter.png", "cat": "carnivore"},
    "Oviraptor": {"base_mat": 75757.6, "food_drain": 0.520800, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/o/oviraptor.png/300px-Oviraptor.png", "cat": "carnivore"},
    "Ovis": {"base_mat": 175438.6, "food_drain": 1.262400, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/o/ovis.png/300px-Ovis.png", "cat": "herbivore"},
    "Pachycephalosaurus": {"base_mat": 95238.1, "food_drain": 0.617200, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/p/pachycephalosaurus.png/300px-Pachycephalosaurus.png", "cat": "herbivore"},
    "Pachyrhinosaurus": {"base_mat": 166666.7, "food_drain": 1.262400, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/p/pachyrhinosaurus.png/300px-Pachyrhinosaurus.png", "cat": "herbivore"},
    "Paraceratherium": {"base_mat": 333333.3, "food_drain": 1.400000, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/p/paraceratherium.png/300px-Paraceratherium.png", "cat": "herbivore"},
    "Parasaurolophus": {"base_mat": 95238.1, "food_drain": 0.771600, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/p/parasaurolophus.png/300px-Parasaurolophus.png", "cat": "herbivore"},
    "Pegomastax": {"base_mat": 111111.1, "food_drain": 0.347200, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/p/pegomastax.png/300px-Pegomastax.png", "cat": "herbivore"},
    "Pelagornis": {"base_mat": 133333.3, "food_drain": 0.617200, "foods": ['Raw Fish Meat', 'Cooked Fish Meat'], "img": "https://ark.wiki.gg/images/thumb/p/pelagornis.png/300px-Pelagornis.png", "cat": "carnivore"},
    "Phiomia": {"base_mat": 175438.6, "food_drain": 1.262400, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/p/phiomia.png/300px-Phiomia.png", "cat": "herbivore"},
    "Plesiosaurus": {"base_mat": 416666.7, "food_drain": 1.543200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/p/plesiosaurus.png/300px-Plesiosaurus.png", "cat": "carnivore"},
    "Procoptodon": {"base_mat": 166666.7, "food_drain": 0.771600, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/p/procoptodon.png/300px-Procoptodon.png", "cat": "herbivore"},
    "Pteranodon": {"base_mat": 133333.3, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/p/pteranodon.png/300px-Pteranodon.png", "cat": "carnivore"},
    "Pulmonoscorpius": {"base_mat": 133333.3, "food_drain": 0.771600, "foods": ['Spoiled Meat', 'Raw Meat'], "img": "https://ark.wiki.gg/images/thumb/p/pulmonoscorpius.png/300px-Pulmonoscorpius.png", "cat": "omnivore"},
    "Purlovia": {"base_mat": 175438.6, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/p/purlovia.png/300px-Purlovia.png", "cat": "carnivore"},
    "Pyromane": {"base_mat": 175438.6, "food_drain": 0.462800, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/p/pyromane.png/300px-Pyromane.png", "cat": "carnivore"},
    "Quetzalcoatlus": {"base_mat": 476190.5, "food_drain": 1.400000, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/q/quetzalcoatlus.png/300px-Quetzalcoatlus.png", "cat": "carnivore"},
    "Raptor": {"base_mat": 133333.3, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/r/raptor.png/300px-Raptor.png", "cat": "carnivore"},
    "Ravager": {"base_mat": 175438.6, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/r/ravager.png/300px-Ravager.png", "cat": "carnivore"},
    "Reaper": {"base_mat": 277777.8, "food_drain": 0.925600, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/r/reaper.png/300px-Reaper.png", "cat": "carnivore"},
    "Rex": {"base_mat": 333333.3, "food_drain": 0.925600, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/r/rex.png/300px-Rex.png", "cat": "carnivore"},
    "Rock Drake": {"base_mat": 333333.3, "food_drain": 0.074000, "foods": ['Raw Meat'], "img": "https://ark.wiki.gg/images/thumb/r/rock_Drake.png/300px-Rock_Drake.png", "cat": "omnivore"},
    "Roll Rat": {"base_mat": 208333.3, "food_drain": 1.262400, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/r/roll_Rat.png/300px-Roll_Rat.png", "cat": "herbivore"},
    "Sabertooth": {"base_mat": 175438.6, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/s/sabertooth.png/300px-Sabertooth.png", "cat": "carnivore"},
    "Sarcosuchus": {"base_mat": 166666.7, "food_drain": 0.631200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/s/sarcosuchus.png/300px-Sarcosuchus.png", "cat": "carnivore"},
    "Shadowmane": {"base_mat": 175438.6, "food_drain": 0.462800, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/s/shadowmane.png/300px-Shadowmane.png", "cat": "carnivore"},
    "Shastasaurus": {"base_mat": 666666.7, "food_drain": 2.000000, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/s/shastasaurus.png/300px-Shastasaurus.png", "cat": "carnivore"},
    "Shinehorn": {"base_mat": 175438.6, "food_drain": 0.347200, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/s/shinehorn.png/300px-Shinehorn.png", "cat": "herbivore"},
    "Sinomacrops": {"base_mat": 55555.6, "food_drain": 0.520800, "foods": ['Raw Meat', 'Cooked Meat'], "img": "https://ark.wiki.gg/images/thumb/s/sinomacrops.png/300px-Sinomacrops.png", "cat": "omnivore"},
    "Snow Owl": {"base_mat": 196078.4, "food_drain": 4.000000, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/s/snow_Owl.png/300px-Snow_Owl.png", "cat": "carnivore"},
    "Solwyn": {"base_mat": 175438.6, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/s/solwyn.png/300px-Solwyn.png", "cat": "carnivore"},
    "Spinosaurus": {"base_mat": 256410.3, "food_drain": 0.826400, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/s/spinosaurus.png/300px-Spinosaurus.png", "cat": "carnivore"},
    "Stegosaurus": {"base_mat": 185185.2, "food_drain": 2.136400, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/s/stegosaurus.png/300px-Stegosaurus.png", "cat": "herbivore"},
    "Tapejara": {"base_mat": 196078.4, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/t/tapejara.png/300px-Tapejara.png", "cat": "carnivore"},
    "Terror Bird": {"base_mat": 166666.7, "food_drain": 0.631200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/t/terror_Bird.png/300px-Terror_Bird.png", "cat": "carnivore"},
    "Therizinosaurus": {"base_mat": 416666.7, "food_drain": 0.925600, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/t/therizinosaurus.png/300px-Therizinosaurus.png", "cat": "herbivore"},
    "Thorny Dragon": {"base_mat": 175438.6, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/t/thorny_Dragon.png/300px-Thorny_Dragon.png", "cat": "carnivore"},
    "Thylacoleo": {"base_mat": 175438.6, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/t/thylacoleo.png/300px-Thylacoleo.png", "cat": "carnivore"},
    "Triceratops": {"base_mat": 166666.7, "food_drain": 1.262400, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/t/triceratops.png/300px-Triceratops.png", "cat": "herbivore"},
    "Troodon": {"base_mat": 75757.6, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/t/troodon.png/300px-Troodon.png", "cat": "carnivore"},
    "Tropeognathus": {"base_mat": 196078.4, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/t/tropeognathus.png/300px-Tropeognathus.png", "cat": "carnivore"},
    "Tusoteuthis": {"base_mat": 666666.7, "food_drain": 2.000000, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/t/tusoteuthis.png/300px-Tusoteuthis.png", "cat": "carnivore"},
    "Veilwyn": {"base_mat": 166666.7, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/v/veilwyn.png/300px-Veilwyn.png", "cat": "carnivore"},
    "Velonasaur": {"base_mat": 166666.7, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/v/velonasaur.png/300px-Velonasaur.png", "cat": "carnivore"},
    "Voidwyrm": {"base_mat": 333333.3, "food_drain": 0.001665, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/v/voidwyrm.png/300px-Voidwyrm.png", "cat": "carnivore"},
    "Vulture": {"base_mat": 90090.1, "food_drain": 0.520800, "foods": ['Spoiled Meat', 'Raw Meat'], "img": "https://ark.wiki.gg/images/thumb/v/vulture.png/300px-Vulture.png", "cat": "omnivore"},
    "Woolly Rhino": {"base_mat": 208333.3, "food_drain": 1.262400, "foods": ['Mejoberries', 'Berries', 'Vegetables'], "img": "https://ark.wiki.gg/images/thumb/w/woolly_Rhino.png/300px-Woolly_Rhino.png", "cat": "herbivore"},
    "Wyvern": {"base_mat": 333333.3, "food_drain": 0.166500, "foods": ['Raw Meat'], "img": "https://ark.wiki.gg/images/thumb/w/wyvern.png/300px-Wyvern.png", "cat": "omnivore"},
    "Xiphactinus": {"base_mat": 333333.3, "food_drain": 0.631200, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/x/xiphactinus.png/300px-Xiphactinus.png", "cat": "carnivore"},
    "Yi Ling": {"base_mat": 166666.7, "food_drain": 0.617200, "foods": ['Raw Meat', 'Cooked Meat', 'Mejoberries', 'Berries'], "img": "https://ark.wiki.gg/images/thumb/y/yi_Ling.png/300px-Yi_Ling.png", "cat": "omnivore"},
    "Yutyrannus": {"base_mat": 666666.7, "food_drain": 0.925600, "foods": ['Raw Meat', 'Cooked Meat', 'Raw Prime Meat'], "img": "https://ark.wiki.gg/images/thumb/y/yutyrannus.png/300px-Yutyrannus.png", "cat": "carnivore"},
}

def is_evo():
    now_utc = datetime.utcnow()
    now_et = now_utc + timedelta(hours=-5)
    wd, h = now_et.weekday(), now_et.hour
    return (wd == 4 and h >= 17) or wd in [5, 6] or (wd == 0 and h < 21)

def get_mults():
    if is_evo():
        return {"mat": 4, "cuddle": 0.6, "imp": 4, "name": "🎉 EVO Weekend"}
    return {"mat": 2, "cuddle": 1.0, "imp": 1, "name": "📅 Weekday"}

def calc_breed(dino, weight, food):
    if dino not in DINO_DATA:
        return None
    d = DINO_DATA[dino]
    m = get_mults()
    fv = FOOD_TYPES.get(food, FOOD_TYPES["Raw Meat"])["value"]
    
    # CRUMPLECORN FORMULA: maturation_time = base_maturation / mature_multiplier
    total_mat = d["base_mat"] / m["mat"]
    juv_time = total_mat * 0.1
    adult_time = total_mat
    
    # Food = (food_drain * time * weight) / food_value
    baby_food = (d["food_drain"] * juv_time * weight) / fv
    juv_food = (d["food_drain"] * (adult_time - juv_time) * weight) / fv
    
    # Cuddles (8 hour base, modified by cuddle multiplier)
    cuddle_int = 28800 * m["cuddle"]
    cuddles = max(1, int(adult_time / cuddle_int))
    
    return {
        "dino": dino, "weight": weight, "food": food,
        "emoji": FOOD_TYPES.get(food, FOOD_TYPES["Raw Meat"])["emoji"], 
        "mults": m, "juv_time": juv_time, "adult_time": adult_time,
        "baby_food": baby_food, "juv_food": juv_food,
        "total_food": baby_food + juv_food,
        "cuddle_int": cuddle_int, "cuddles": cuddles,
        "img": d.get("img", ""), "cat": d.get("cat", "")
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

def prog_bar(pct, length=10):
    filled = int(length * pct)
    bar = "▰" * filled + "▱" * (length - filled)
    return f"{bar} {int(pct*100)}%"

class FoodSelect(Select):
    def __init__(self, dino, weight):
        self.dino, self.weight = dino, weight
        foods = DINO_DATA[dino]["foods"]
        opts = [discord.SelectOption(label=f, emoji=FOOD_TYPES.get(f, FOOD_TYPES["Raw Meat"])["emoji"]) for f in foods[:25]]
        super().__init__(placeholder="🍖 Select food type...", options=opts)
    
    async def callback(self, i):
        s = calc_breed(self.dino, self.weight, self.values[0])
        if not s:
            return await i.response.send_message("❌ Error!", ephemeral=True)
        
        # COLOR BY CATEGORY
        colors = {
            'carnivore': discord.Color.from_rgb(231, 76, 60),
            'herbivore': discord.Color.from_rgb(46, 204, 113),
            'omnivore': discord.Color.from_rgb(241, 196, 15)
        }
        color = colors.get(s['cat'], discord.Color.blue())
        
        e = discord.Embed(color=color, timestamp=datetime.utcnow())
        e.set_author(name=f"🦖 {s['dino']} - Breeding Calculator", icon_url="https://i.imgur.com/QN0l8VH.png")
        
        if s['img']:
            e.set_thumbnail(url=s['img'])
        
        # SERVER INFO BOX
        e.add_field(
            name="⚙️ Server Settings",
            value=f"```yaml\n{s['mults']['name']}\nMature: {s['mults']['mat']}x\nCuddle: {s['mults']['cuddle']}x```",
            inline=True
        )
        
        # BABY INFO BOX
        e.add_field(
            name="👶 Baby Stats",
            value=f"```\nWeight: {s['weight']}\nFood: {s['emoji']} {s['food']}```",
            inline=True
        )
        
        # MATURATION PROGRESS BAR
        e.add_field(
            name="📊 Growth Phases",
            value=f"```\nBaby  ▰▱▱▱▱▱▱▱▱▱ 10%\nAdult ▰▰▰▰▰▰▰▰▰▰ 100%```",
            inline=False
        )
        
        # TIMELINE
        e.add_field(
            name="⏱️ Maturation Timeline",
            value=f"```diff\n+ Juvenile: {fmt_time(s['juv_time'])}\n+ Adult:    {fmt_time(s['adult_time'])}```",
            inline=True
        )
        
        # FOOD REQUIREMENTS
        e.add_field(
            name=f"{s['emoji']} Food Required",
            value=f"```\nBaby:  {int(s['baby_food']):>6,}\nJuv:   {int(s['juv_food']):>6,}\n{'─' * 14}\nTotal: {int(s['total_food']):>6,}```",
            inline=True
        )
        
        # IMPRINTING
        imp_per = min(100, int(100 / s['cuddles']))
        e.add_field(
            name="💕 Imprinting",
            value=f"```fix\nCuddles: {s['cuddles']}\nInterval: {fmt_time(s['cuddle_int'])}\nPer Cuddle: +{imp_per}%```",
            inline=True
        )
        
        e.set_footer(text="ARK: Survival Ascended • Small Tribes • Powered by Crumplecorn Data", icon_url="https://i.imgur.com/QN0l8VH.png")
        
        await i.response.send_message(embed=e)

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
            await i.response.send_message("❌ Invalid weight! Please enter a number.", ephemeral=True)

async def dino_auto(i: discord.Interaction, cur: str):
    dinos = sorted(DINO_DATA.keys())
    matches = [d for d in dinos if cur.lower() in d.lower()]
    return [app_commands.Choice(name=d, value=d) for d in matches[:25]]

@tree.command(name="breeding", description="🦖 Calculate breeding stats with autocomplete search")
@app_commands.autocomplete(dino=dino_auto)
@app_commands.describe(dino="Type to search for a creature")
async def breeding(i: discord.Interaction, dino: str):
    if dino not in DINO_DATA:
        return await i.response.send_message(f"❌ **{dino}** not found! Use `/dinos` to see all creatures.", ephemeral=True)
    await i.response.send_modal(WeightModal(dino))

@tree.command(name="dinos", description="📋 List all available creatures")
async def dinos(i: discord.Interaction):
    carns = sorted([n for n, d in DINO_DATA.items() if d["cat"] == "carnivore"])
    herbs = sorted([n for n, d in DINO_DATA.items() if d["cat"] == "herbivore"])
    omnis = sorted([n for n, d in DINO_DATA.items() if d["cat"] == "omnivore"])
    
    e = discord.Embed(title="📋 All Breedable Creatures", description=f"**Total: {len(DINO_DATA)} creatures**\n\n*Use `/breeding <name>` with autocomplete!*", color=discord.Color.blue())
    
    if carns:
        carns_display = ", ".join(carns[:30]) + (f"... +{len(carns)-30} more" if len(carns) > 30 else "")
        e.add_field(name=f"🥩 Carnivores ({len(carns)})", value=carns_display, inline=False)
    
    if herbs:
        herbs_display = ", ".join(herbs[:30]) + (f"... +{len(herbs)-30} more" if len(herbs) > 30 else "")
        e.add_field(name=f"🥕 Herbivores ({len(herbs)})", value=herbs_display, inline=False)
    
    if omnis:
        e.add_field(name=f"🍖 Omnivores ({len(omnis)})", value=", ".join(omnis), inline=False)
    
    e.set_footer(text="Crumplecorn-accurate calculations")
    await i.response.send_message(embed=e)

@tree.command(name="event", description="📅 Show current event status")
async def event(i: discord.Interaction):
    m = get_mults()
    e = discord.Embed(
        title=m['name'], 
        description="**ARK Small Tribes Rates**", 
        color=discord.Color.green() if is_evo() else discord.Color.blue()
    )
    
    e.add_field(
        name="⚙️ Current Multipliers",
        value=f"```yaml\nHatch:  2x / 4x\nMature: {m['mat']}x\nCuddle: {m['cuddle']}x\nImprint: {m['imp']}x```",
        inline=False
    )
    
    if is_evo():
        e.add_field(
            name="🎉 EVO Weekend Active!",
            value="**Schedule:** Friday 17:00 ET - Monday 21:00 ET\n**Bonuses:** 4x breeding rates!",
            inline=False
        )
    else:
        e.add_field(
            name="📅 Weekday Rates",
            value="**Next EVO:** Friday 17:00 ET (23:00 CET)\n**Current:** 2x standard rates",
            inline=False
        )
    
    e.set_footer(text="Eastern Time (ET) = UTC-5")
    await i.response.send_message(embed=e)

@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot Online: {client.user}")
    print(f"📊 {len(DINO_DATA)} creatures loaded")
    print(f"🔍 Autocomplete enabled")
    print(f"🎯 Crumplecorn-accurate calculations")

if __name__ == "__main__":
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        try:
            with open("config.json") as f:
                token = json.load(f).get("bot_token")
        except:
            print("❌ No token!")
            exit(1)
    print("🚀 Starting ARK Breeding Bot (Crumplecorn Edition)...")
    client.run(token)
