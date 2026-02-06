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
    "Vegetables": {"value": 40, "emoji": "🥕"}
}

# CORRECT BASE MATURATION TIMES (in seconds at 1x) from ARK data
# Formula: actual_time = base_time / mature_multiplier
DINO_DATA = {
    "Achatina": {"base_maturation": 124416, "food_drain": 0.000062, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/f/f7/Achatina.png/300px-Achatina.png", "category": "herbivore"},
    "Allosaurus": {"base_maturation": 166666, "food_drain": 0.000124, "food_type": ["Raw Meat", "Cooked Meat", "Raw Prime Meat"], "image": "https://ark.wiki.gg/images/thumb/c/c4/Allosaurus.png/300px-Allosaurus.png", "category": "carnivore"},
    "Andrewsarchus": {"base_maturation": 200000, "food_drain": 0.000124, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/5/50/Andrewsarchus.png/300px-Andrewsarchus.png", "category": "omnivore"},
    "Ankylosaurus": {"base_maturation": 119904, "food_drain": 0.000124, "food_type": ["Vegetables", "Mejoberries", "Berries"], "image": "https://ark.wiki.gg/images/thumb/9/98/Ankylosaurus.png/300px-Ankylosaurus.png", "category": "herbivore"},
    "Araneo": {"base_maturation": 91998, "food_drain": 0.000083, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/c/c0/Araneo.png/300px-Araneo.png", "category": "carnivore"},
    "Argentavis": {"base_maturation": 119904, "food_drain": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/1/1e/Argentavis.png/300px-Argentavis.png", "category": "carnivore"},
    "Baryonyx": {"base_maturation": 119904, "food_drain": 0.000103, "food_type": ["Raw Meat", "Raw Fish Meat", "Cooked Fish Meat"], "image": "https://ark.wiki.gg/images/thumb/e/e8/Baryonyx.png/300px-Baryonyx.png", "category": "carnivore"},
    "Basilisk": {"base_maturation": 240020, "food_drain": 0.000144, "food_type": ["Raw Meat", "Raw Prime Meat"], "image": "https://ark.wiki.gg/images/thumb/6/6d/Basilisk.png/300px-Basilisk.png", "category": "carnivore"},
    "Basilosaurus": {"base_maturation": 166666, "food_drain": 0.000144, "food_type": ["Raw Meat", "Raw Prime Meat"], "image": "https://ark.wiki.gg/images/thumb/b/b3/Basilosaurus.png/300px-Basilosaurus.png", "category": "carnivore"},
    "Beelzebufo": {"base_maturation": 91998, "food_drain": 0.000083, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/7/71/Beelzebufo.png/300px-Beelzebufo.png", "category": "carnivore"},
    "Brontosaurus": {"base_maturation": 238356, "food_drain": 0.000165, "food_type": ["Vegetables", "Mejoberries", "Berries"], "image": "https://ark.wiki.gg/images/thumb/d/d4/Brontosaurus.png/300px-Brontosaurus.png", "category": "herbivore"},
    "Carbonemys": {"base_maturation": 119904, "food_drain": 0.000103, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/6/65/Carbonemys.png/300px-Carbonemys.png", "category": "herbivore"},
    "Carnotaurus": {"base_maturation": 119904, "food_drain": 0.000124, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/d/d5/Carnotaurus.png/300px-Carnotaurus.png", "category": "carnivore"},
    "Castoroides": {"base_maturation": 142560, "food_drain": 0.000103, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/8/88/Castoroides.png/300px-Castoroides.png", "category": "herbivore"},
    "Ceratosaurus": {"base_maturation": 166666, "food_drain": 0.000124, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/8/8e/Ceratosaurus.png/300px-Ceratosaurus.png", "category": "carnivore"},
    "Daeodon": {"base_maturation": 238356, "food_drain": 0.000144, "food_type": ["Raw Meat", "Cooked Meat", "Vegetables"], "image": "https://ark.wiki.gg/images/thumb/0/08/Daeodon.png/300px-Daeodon.png", "category": "omnivore"},
    "Deinonychus": {"base_maturation": 142560, "food_drain": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/d/d3/Deinonychus.png/300px-Deinonychus.png", "category": "carnivore"},
    "Dimetrodon": {"base_maturation": 119904, "food_drain": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/e/e5/Dimetrodon.png/300px-Dimetrodon.png", "category": "carnivore"},
    "Dimorphodon": {"base_maturation": 73728, "food_drain": 0.000062, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/d/dd/Dimorphodon.png/300px-Dimorphodon.png", "category": "carnivore"},
    "Diplocaulus": {"base_maturation": 91998, "food_drain": 0.000083, "food_type": ["Raw Meat", "Raw Fish Meat"], "image": "https://ark.wiki.gg/images/thumb/9/94/Diplocaulus.png/300px-Diplocaulus.png", "category": "carnivore"},
    "Diplodocus": {"base_maturation": 238356, "food_drain": 0.000144, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/0/05/Diplodocus.png/300px-Diplodocus.png", "category": "herbivore"},
    "Dire Bear": {"base_maturation": 166666, "food_drain": 0.000124, "food_type": ["Raw Meat", "Cooked Meat", "Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/0/04/Direbear.png/300px-Direbear.png", "category": "omnivore"},
    "Dire Wolf": {"base_maturation": 119904, "food_drain": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/3/3c/Direwolf.png/300px-Direwolf.png", "category": "carnivore"},
    "Doedicurus": {"base_maturation": 142560, "food_drain": 0.000124, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/9/9e/Doedicurus.png/300px-Doedicurus.png", "category": "herbivore"},
    "Dodo": {"base_maturation": 57024, "food_drain": 0.000062, "food_type": ["Vegetables", "Mejoberries", "Berries"], "image": "https://ark.wiki.gg/images/thumb/d/d5/Dodo.png/300px-Dodo.png", "category": "herbivore"},
    "Dreadnoughtus": {"base_maturation": 360000, "food_drain": 0.000185, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/4/48/Dreadnoughtus.png/300px-Dreadnoughtus.png", "category": "herbivore"},
    "Dunkleosteus": {"base_maturation": 142560, "food_drain": 0.000124, "food_type": ["Raw Meat"], "image": "https://ark.wiki.gg/images/thumb/a/a9/Dunkleosteus.png/300px-Dunkleosteus.png", "category": "carnivore"},
    "Equus": {"base_maturation": 119904, "food_drain": 0.000083, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/f/f2/Equus.png/300px-Equus.png", "category": "herbivore"},
    "Fasolasuchus": {"base_maturation": 258000, "food_drain": 0.000165, "food_type": ["Raw Meat", "Raw Prime Meat"], "image": "https://ark.wiki.gg/images/thumb/a/a9/Fasolasuchus.png/300px-Fasolasuchus.png", "category": "carnivore"},
    "Fenrir": {"base_maturation": 240020, "food_drain": 0.000165, "food_type": ["Raw Meat", "Raw Prime Meat"], "image": "https://ark.wiki.gg/images/thumb/7/74/Fenrir.png/300px-Fenrir.png", "category": "carnivore"},
    "Gallimimus": {"base_maturation": 119904, "food_drain": 0.000083, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/5/5f/Gallimimus.png/300px-Gallimimus.png", "category": "herbivore"},
    "Giganotosaurus": {"base_maturation": 359990, "food_drain": 0.000165, "food_type": ["Raw Meat", "Cooked Meat", "Raw Prime Meat"], "image": "https://ark.wiki.gg/images/thumb/1/1e/Giganotosaurus.png/300px-Giganotosaurus.png", "category": "carnivore"},
    "Gigantopithecus": {"base_maturation": 142560, "food_drain": 0.000103, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/0/0a/Gigantopithecus.png/300px-Gigantopithecus.png", "category": "herbivore"},
    "Griffin": {"base_maturation": 238356, "food_drain": 0.000103, "food_type": ["Raw Meat", "Cooked Meat", "Raw Prime Meat"], "image": "https://ark.wiki.gg/images/thumb/3/3f/Griffin.png/300px-Griffin.png", "category": "carnivore"},
    "Hyaenodon": {"base_maturation": 119904, "food_drain": 0.000083, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/e/e3/Hyaenodon.png/300px-Hyaenodon.png", "category": "carnivore"},
    "Ichthyornis": {"base_maturation": 73728, "food_drain": 0.000062, "food_type": ["Raw Meat", "Raw Fish Meat"], "image": "https://ark.wiki.gg/images/thumb/d/dc/Ichthyornis.png/300px-Ichthyornis.png", "category": "carnivore"},
    "Ichthyosaurus": {"base_maturation": 73728, "food_drain": 0.000083, "food_type": ["Raw Meat", "Raw Fish Meat"], "image": "https://ark.wiki.gg/images/thumb/8/87/Ichthyosaurus.png/300px-Ichthyosaurus.png", "category": "carnivore"},
    "Iguanodon": {"base_maturation": 119904, "food_drain": 0.000103, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/3/3c/Iguanodon.png/300px-Iguanodon.png", "category": "herbivore"},
    "Jerboa": {"base_maturation": 57024, "food_drain": 0.000042, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/a/a7/Jerboa.png/300px-Jerboa.png", "category": "herbivore"},
    "Kaprosuchus": {"base_maturation": 119904, "food_drain": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/8/8f/Kaprosuchus.png/300px-Kaprosuchus.png", "category": "carnivore"},
    "Karkinos": {"base_maturation": 240020, "food_drain": 0.000144, "food_type": ["Raw Meat", "Raw Prime Meat"], "image": "https://ark.wiki.gg/images/thumb/6/62/Karkinos.png/300px-Karkinos.png", "category": "carnivore"},
    "Kentrosaurus": {"base_maturation": 142560, "food_drain": 0.000103, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/a/ae/Kentrosaurus.png/300px-Kentrosaurus.png", "category": "herbivore"},
    "Lymantria": {"base_maturation": 73728, "food_drain": 0.000062, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/d/df/Lymantria.png/300px-Lymantria.png", "category": "herbivore"},
    "Lystrosaurus": {"base_maturation": 57024, "food_drain": 0.000062, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/e/e3/Lystrosaurus.png/300px-Lystrosaurus.png", "category": "herbivore"},
    "Mammoth": {"base_maturation": 190350, "food_drain": 0.000144, "food_type": ["Vegetables", "Mejoberries", "Berries"], "image": "https://ark.wiki.gg/images/thumb/2/29/Mammoth.png/300px-Mammoth.png", "category": "herbivore"},
    "Managarmr": {"base_maturation": 238356, "food_drain": 0.000124, "food_type": ["Raw Meat", "Cooked Meat", "Raw Prime Meat"], "image": "https://ark.wiki.gg/images/thumb/e/e0/Managarmr.png/300px-Managarmr.png", "category": "carnivore"},
    "Manta": {"base_maturation": 119904, "food_drain": 0.000083, "food_type": ["Raw Meat", "Raw Fish Meat"], "image": "https://ark.wiki.gg/images/thumb/5/54/Manta.png/300px-Manta.png", "category": "carnivore"},
    "Mantis": {"base_maturation": 166666, "food_drain": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/d/d6/Mantis.png/300px-Mantis.png", "category": "carnivore"},
    "Megalania": {"base_maturation": 142560, "food_drain": 0.000124, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/5/54/Megalania.png/300px-Megalania.png", "category": "carnivore"},
    "Megaloceros": {"base_maturation": 119904, "food_drain": 0.000083, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/c/c8/Megaloceros.png/300px-Megaloceros.png", "category": "herbivore"},
    "Megalodon": {"base_maturation": 142560, "food_drain": 0.000124, "food_type": ["Raw Meat", "Raw Fish Meat", "Cooked Fish Meat"], "image": "https://ark.wiki.gg/images/thumb/3/35/Megalodon.png/300px-Megalodon.png", "category": "carnivore"},
    "Megalosaurus": {"base_maturation": 166666, "food_drain": 0.000124, "food_type": ["Raw Meat", "Cooked Meat", "Raw Prime Meat"], "image": "https://ark.wiki.gg/images/thumb/5/57/Megalosaurus.png/300px-Megalosaurus.png", "category": "carnivore"},
    "Megatherium": {"base_maturation": 166666, "food_drain": 0.000124, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/f/f4/Megatherium.png/300px-Megatherium.png", "category": "herbivore"},
    "Mesopithecus": {"base_maturation": 57024, "food_drain": 0.000062, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/7/70/Mesopithecus.png/300px-Mesopithecus.png", "category": "herbivore"},
    "Microraptor": {"base_maturation": 73728, "food_drain": 0.000062, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/1/14/Microraptor.png/300px-Microraptor.png", "category": "carnivore"},
    "Morellatops": {"base_maturation": 119904, "food_drain": 0.000103, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/a/ae/Morellatops.png/300px-Morellatops.png", "category": "herbivore"},
    "Moschops": {"base_maturation": 73728, "food_drain": 0.000083, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/a/a0/Moschops.png/300px-Moschops.png", "category": "herbivore"},
    "Mosasaurus": {"base_maturation": 238356, "food_drain": 0.000165, "food_type": ["Raw Meat", "Raw Prime Meat"], "image": "https://ark.wiki.gg/images/thumb/5/53/Mosasaurus.png/300px-Mosasaurus.png", "category": "carnivore"},
    "Ovis": {"base_maturation": 57024, "food_drain": 0.000062, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/3/3c/Ovis.png/300px-Ovis.png", "category": "herbivore"},
    "Pachyrhinosaurus": {"base_maturation": 142560, "food_drain": 0.000103, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/a/ad/Pachyrhinosaurus.png/300px-Pachyrhinosaurus.png", "category": "herbivore"},
    "Pachy": {"base_maturation": 73728, "food_drain": 0.000083, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/9/91/Pachy.png/300px-Pachy.png", "category": "herbivore"},
    "Parasaur": {"base_maturation": 73728, "food_drain": 0.000083, "food_type": ["Vegetables", "Mejoberries", "Berries"], "image": "https://ark.wiki.gg/images/thumb/8/84/Parasaur.png/300px-Parasaur.png", "category": "herbivore"},
    "Pelagornis": {"base_maturation": 73728, "food_drain": 0.000083, "food_type": ["Raw Meat", "Raw Fish Meat"], "image": "https://ark.wiki.gg/images/thumb/c/c9/Pelagornis.png/300px-Pelagornis.png", "category": "carnivore"},
    "Phiomia": {"base_maturation": 119904, "food_drain": 0.000103, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/c/c2/Phiomia.png/300px-Phiomia.png", "category": "herbivore"},
    "Plesiosaur": {"base_maturation": 238356, "food_drain": 0.000144, "food_type": ["Raw Meat", "Raw Prime Meat"], "image": "https://ark.wiki.gg/images/thumb/e/e4/Plesiosaur.png/300px-Plesiosaur.png", "category": "carnivore"},
    "Procoptodon": {"base_maturation": 142560, "food_drain": 0.000103, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/5/51/Procoptodon.png/300px-Procoptodon.png", "category": "herbivore"},
    "Pteranodon": {"base_maturation": 73728, "food_drain": 0.000083, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/6/6f/Pteranodon.png/300px-Pteranodon.png", "category": "carnivore"},
    "Pulmonoscorpius": {"base_maturation": 119904, "food_drain": 0.000083, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/8/89/Pulmonoscorpius.png/300px-Pulmonoscorpius.png", "category": "carnivore"},
    "Purlovia": {"base_maturation": 119904, "food_drain": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/e/ec/Purlovia.png/300px-Purlovia.png", "category": "carnivore"},
    "Pyromane": {"base_maturation": 190350, "food_drain": 0.000124, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/d/dc/Pyromane.png/300px-Pyromane.png", "category": "carnivore"},
    "Quetzal": {"base_maturation": 258000, "food_drain": 0.000124, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/0/0b/Quetzal.png/300px-Quetzal.png", "category": "carnivore"},
    "Raptor": {"base_maturation": 119904, "food_drain": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/9/9f/Raptor.png/300px-Raptor.png", "category": "carnivore"},
    "Ravager": {"base_maturation": 142560, "food_drain": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/1/1f/Ravager.png/300px-Ravager.png", "category": "carnivore"},
    "Reaper": {"base_maturation": 240020, "food_drain": 0.000165, "food_type": ["Raw Meat"], "image": "https://ark.wiki.gg/images/thumb/5/57/Reaper.png/300px-Reaper.png", "category": "carnivore"},
    "Rex": {"base_maturation": 238356, "food_drain": 0.000124, "food_type": ["Raw Meat", "Cooked Meat", "Raw Prime Meat"], "image": "https://ark.wiki.gg/images/thumb/c/c3/Rex.png/300px-Rex.png", "category": "carnivore"},
    "Rock Drake": {"base_maturation": 240020, "food_drain": 0.000124, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/8/82/Rock_Drake.png/300px-Rock_Drake.png", "category": "carnivore"},
    "Roll Rat": {"base_maturation": 142560, "food_drain": 0.000103, "food_type": ["Vegetables", "Berries"], "image": "https://ark.wiki.gg/images/thumb/c/c2/Roll_Rat.png/300px-Roll_Rat.png", "category": "herbivore"},
    "Sabertooth": {"base_maturation": 119904, "food_drain": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/5/5f/Sabertooth.png/300px-Sabertooth.png", "category": "carnivore"},
    "Sarco": {"base_maturation": 142560, "food_drain": 0.000124, "food_type": ["Raw Meat", "Raw Fish Meat"], "image": "https://ark.wiki.gg/images/thumb/0/0f/Sarco.png/300px-Sarco.png", "category": "carnivore"},
    "Shastasaurus": {"base_maturation": 238356, "food_drain": 0.000144, "food_type": ["Raw Meat", "Raw Fish Meat"], "image": "https://ark.wiki.gg/images/thumb/2/2b/Shastasaurus.png/300px-Shastasaurus.png", "category": "carnivore"},
    "Snow Owl": {"base_maturation": 190350, "food_drain": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/c/c7/Snow_Owl.png/300px-Snow_Owl.png", "category": "carnivore"},
    "Spino": {"base_maturation": 238356, "food_drain": 0.000124, "food_type": ["Raw Meat", "Cooked Meat", "Raw Fish Meat"], "image": "https://ark.wiki.gg/images/thumb/7/7e/Spino.png/300px-Spino.png", "category": "carnivore"},
    "Stegosaurus": {"base_maturation": 142560, "food_drain": 0.000124, "food_type": ["Vegetables", "Mejoberries", "Berries"], "image": "https://ark.wiki.gg/images/thumb/8/80/Stegosaurus.png/300px-Stegosaurus.png", "category": "herbivore"},
    "Tapejara": {"base_maturation": 119904, "food_drain": 0.000083, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/7/72/Tapejara.png/300px-Tapejara.png", "category": "carnivore"},
    "Terror Bird": {"base_maturation": 119904, "food_drain": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/3/3f/Terror_Bird.png/300px-Terror_Bird.png", "category": "carnivore"},
    "Therizinosaurus": {"base_maturation": 238356, "food_drain": 0.000144, "food_type": ["Vegetables", "Mejoberries"], "image": "https://ark.wiki.gg/images/thumb/5/56/Therizinosaurus.png/300px-Therizinosaurus.png", "category": "herbivore"},
    "Thorny Dragon": {"base_maturation": 119904, "food_drain": 0.000083, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/4/4e/Thorny_Dragon.png/300px-Thorny_Dragon.png", "category": "carnivore"},
    "Thylacoleo": {"base_maturation": 119904, "food_drain": 0.000124, "food_type": ["Raw Meat", "Cooked Meat", "Raw Prime Meat"], "image": "https://ark.wiki.gg/images/thumb/0/00/Thylacoleo.png/300px-Thylacoleo.png", "category": "carnivore"},
    "Triceratops": {"base_maturation": 142560, "food_drain": 0.000124, "food_type": ["Vegetables", "Mejoberries", "Berries"], "image": "https://ark.wiki.gg/images/thumb/9/9f/Triceratops.png/300px-Triceratops.png", "category": "herbivore"},
    "Troodon": {"base_maturation": 73728, "food_drain": 0.000083, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/4/4e/Troodon.png/300px-Troodon.png", "category": "carnivore"},
    "Tusoteuthis": {"base_maturation": 190350, "food_drain": 0.000144, "food_type": ["Raw Meat", "Raw Prime Meat"], "image": "https://ark.wiki.gg/images/thumb/8/82/Tusoteuthis.png/300px-Tusoteuthis.png", "category": "carnivore"},
    "Velonasaur": {"base_maturation": 166666, "food_drain": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/5/59/Velonasaur.png/300px-Velonasaur.png", "category": "carnivore"},
    "Vulture": {"base_maturation": 73728, "food_drain": 0.000062, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/5/5d/Vulture.png/300px-Vulture.png", "category": "carnivore"},
    "Woolly Rhino": {"base_maturation": 166666, "food_drain": 0.000144, "food_type": ["Vegetables", "Mejoberries", "Berries"], "image": "https://ark.wiki.gg/images/thumb/f/f1/Woolly_Rhino.png/300px-Woolly_Rhino.png", "category": "herbivore"},
    "Wyvern": {"base_maturation": 240020, "food_drain": 0.000165, "food_type": ["Raw Meat"], "image": "https://ark.wiki.gg/images/thumb/4/4f/Wyvern.png/300px-Wyvern.png", "category": "carnivore"},
    "Yi Ling": {"base_maturation": 73728, "food_drain": 0.000062, "food_type": ["Raw Meat", "Cooked Meat"], "image": "https://ark.wiki.gg/images/thumb/e/e5/Yi_Ling.png/300px-Yi_Ling.png", "category": "carnivore"},
    "Yutyrannus": {"base_maturation": 238356, "food_drain": 0.000124, "food_type": ["Raw Meat", "Cooked Meat", "Raw Prime Meat"], "image": "https://ark.wiki.gg/images/thumb/d/d6/Yutyrannus.png/300px-Yutyrannus.png", "category": "carnivore"}
}

def is_evo_weekend():
    now_utc = datetime.utcnow()
    now_et = now_utc + timedelta(hours=-5)
    weekday, hour = now_et.weekday(), now_et.hour
    return (weekday == 4 and hour >= 17) or weekday in [5, 6] or (weekday == 0 and hour < 21)

def get_multipliers():
    if is_evo_weekend():
        return {"mature": 4, "cuddle_interval": 0.6, "imprint_amount": 4, "event_name": "🎉 EVO Weekend"}
    return {"mature": 2, "cuddle_interval": 1.0, "imprint_amount": 1, "event_name": "📅 Weekday"}

def calculate_breeding(dino_name, weight, food_type):
    if dino_name not in DINO_DATA:
        return None
    dino = DINO_DATA[dino_name]
    mults = get_multipliers()
    food_val = FOOD_TYPES[food_type]["value"]
    
    # CORRECT FORMULA matching Crumplecorn
    total_maturation_time = dino["base_maturation"] / mults["mature"]
    time_to_juvenile = total_maturation_time * 0.1
    time_to_adult = total_maturation_time
    
    # Food calculations (food consumed per second * time * weight / food value)
    baby_food = (dino["food_drain"] * time_to_juvenile * weight) / food_val
    juv_food = (dino["food_drain"] * (time_to_adult - time_to_juvenile) * weight) / food_val
    
    # Cuddle calculations
    cuddle_interval = 28800 * mults["cuddle_interval"]
    cuddle_count = int(time_to_adult / cuddle_interval)
    
    return {
        "dino_name": dino_name, "weight": weight, "food_type": food_type,
        "food_emoji": FOOD_TYPES[food_type]["emoji"], "multipliers": mults,
        "time_to_juvenile": time_to_juvenile, "time_to_adult": time_to_adult,
        "baby_food": baby_food, "juv_food": juv_food, "total_food": baby_food + juv_food,
        "cuddle_interval": cuddle_interval, "cuddle_count": cuddle_count,
        "image": dino.get("image", "")
    }

def format_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"

class FoodSelect(Select):
    def __init__(self, dino, weight):
        self.dino, self.weight = dino, weight
        foods = DINO_DATA[dino]["food_type"]
        opts = [discord.SelectOption(label=f, emoji=FOOD_TYPES[f]["emoji"], description=f"Value: {FOOD_TYPES[f]['value']}") for f in foods]
        super().__init__(placeholder="Select food type...", options=opts)
    
    async def callback(self, i):
        stats = calculate_breeding(self.dino, self.weight, self.values[0])
        if not stats:
            return await i.response.send_message("Error!", ephemeral=True)
        
        e = discord.Embed(
            title=f"🦖 {stats['dino_name']} - Breeding Calculator",
            description=f"**Weight:** {stats['weight']} | **Food Type:** {stats['food_emoji']} {stats['food_type']}",
            color=discord.Color.blue()
        )
        
        if stats['image']:
            e.set_image(url=stats['image'])
        
        e.add_field(
            name="📅 Server Settings",
            value=f"**Event:** {stats['multipliers']['event_name']}\n**Mature Speed:** {stats['multipliers']['mature']}x",
            inline=True
        )
        
        e.add_field(
            name="⏱️ Maturation Times",
            value=f"**Time to Juvenile:** {format_time(stats['time_to_juvenile'])}\n**Time to Adult:** {format_time(stats['time_to_adult'])}",
            inline=True
        )
        
        e.add_field(
            name=f"{stats['food_emoji']} Food Required",
            value=f"**To Juvenile:** {int(stats['baby_food'])}\n**To Adult:** {int(stats['juv_food'])}\n**TOTAL:** {int(stats['total_food'])}",
            inline=True
        )
        
        e.add_field(
            name="💕 Imprinting",
            value=f"**Cuddles:** {stats['cuddle_count']}\n**Interval:** {format_time(stats['cuddle_interval'])}\n**Per Cuddle:** +{100//stats['cuddle_count'] if stats['cuddle_count'] > 0 else 0}%",
            inline=False
        )
        
        e.set_footer(text="ARK: Survival Ascended | Small Tribes | Crumplecorn-accurate")
        
        await i.response.send_message(embed=e)

class WeightModal(discord.ui.Modal, title="Baby Weight"):
    def __init__(self, dino):
        super().__init__()
        self.dino = dino
        self.w = discord.ui.TextInput(label="Baby Weight", placeholder="e.g. 100", max_length=10)
        self.add_item(self.w)
    
    async def on_submit(self, i):
        try:
            weight = float(self.w.value)
            if weight <= 0:
                raise ValueError()
            v = View()
            v.add_item(FoodSelect(self.dino, weight))
            await i.response.send_message(f"🦖 **{self.dino}** | Weight: **{weight}**\nSelect food:", view=v, ephemeral=True)
        except:
            await i.response.send_message("❌ Invalid weight!", ephemeral=True)

async def dino_autocomplete(i: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    dinos = sorted(DINO_DATA.keys())
    return [app_commands.Choice(name=d, value=d) for d in dinos if current.lower() in d.lower()][:25]

@tree.command(name="breeding", description="Calculate breeding stats with autocomplete search")
@app_commands.autocomplete(dino=dino_autocomplete)
@app_commands.describe(dino="Type to search for a creature")
async def breeding(i: discord.Interaction, dino: str):
    if dino not in DINO_DATA:
        return await i.response.send_message(f"❌ '{dino}' not found! Use `/dinos` to see all.", ephemeral=True)
    await i.response.send_modal(WeightModal(dino))

@tree.command(name="dinos", description="List all creatures")
async def dinos(i: discord.Interaction):
    carns = sorted([n for n,d in DINO_DATA.items() if d["category"]=="carnivore"])
    herbs = sorted([n for n,d in DINO_DATA.items() if d["category"]=="herbivore"])
    omnis = sorted([n for n,d in DINO_DATA.items() if d["category"]=="omnivore"])
    e = discord.Embed(title="📋 All Breedable Creatures", description=f"**Total: {len(DINO_DATA)} creatures**\n\n*Type `/breeding <name>` with autocomplete!*", color=discord.Color.green())
    if carns:
        e.add_field(name=f"🥩 Carnivores ({len(carns)})", value=", ".join(carns[:25]) + (" ..." if len(carns) > 25 else ""), inline=False)
    if herbs:
        e.add_field(name=f"🥕 Herbivores ({len(herbs)})", value=", ".join(herbs[:25]) + (" ..." if len(herbs) > 25 else ""), inline=False)
    if omnis:
        e.add_field(name=f"🍖 Omnivores ({len(omnis)})", value=", ".join(omnis), inline=False)
    await i.response.send_message(embed=e)

@tree.command(name="event", description="Show current event status")
async def event(i: discord.Interaction):
    m = get_multipliers()
    e = discord.Embed(title=m['event_name'], description="**Small Tribes Rates**", color=discord.Color.green() if is_evo_weekend() else discord.Color.blue())
    e.add_field(name="⚙️ Multipliers", value=f"**Hatch:** 2x/4x\n**Mature:** {m['mature']}x\n**Cuddle:** {m['cuddle_interval']}x\n**Imprint:** {m['imprint_amount']}x", inline=False)
    if is_evo_weekend():
        e.add_field(name="🎉 EVO Active!", value="Friday 17:00 - Monday 21:00 ET\n**Rates:** 4x breeding!", inline=False)
    else:
        e.add_field(name="📅 Weekday", value="EVO starts: Friday 17:00 ET (23:00 CET)", inline=False)
    await i.response.send_message(embed=e)

@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot online: {client.user}")
    print(f"📊 {len(DINO_DATA)} creatures | CORRECT CALCULATIONS")
    print(f"🔍 Autocomplete search enabled")

if __name__ == "__main__":
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        try:
            with open("config.json") as f:
                token = json.load(f).get("bot_token")
        except:
            print("❌ No token!")
            exit(1)
    print("🚀 Starting ARK Breeding Bot (Crumplecorn-accurate)...")
    client.run(token)
