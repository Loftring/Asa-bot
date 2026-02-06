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

DINO_DATA = {
    "Rex": {"maturation_time": 33333, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Cooked Meat", "Raw Prime Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/c/c3/Rex.png/256px-Rex.png", "category": "carnivore"},
    "Giganotosaurus": {"maturation_time": 50000, "food_consumption": 0.000165, "food_type": ["Raw Meat", "Cooked Meat", "Raw Prime Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/1/1e/Giganotosaurus.png/256px-Giganotosaurus.png", "category": "carnivore"},
    "Spino": {"maturation_time": 33333, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Cooked Meat", "Raw Fish Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/7/7e/Spino.png/256px-Spino.png", "category": "carnivore"},
    "Thylacoleo": {"maturation_time": 16667, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Cooked Meat", "Raw Prime Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/0/00/Thylacoleo.png/256px-Thylacoleo.png", "category": "carnivore"},
    "Argentavis": {"maturation_time": 20000, "food_consumption": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/1/1e/Argentavis.png/256px-Argentavis.png", "category": "carnivore"},
    "Pteranodon": {"maturation_time": 13333, "food_consumption": 0.000083, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/6/6f/Pteranodon.png/256px-Pteranodon.png", "category": "carnivore"},
    "Raptor": {"maturation_time": 16667, "food_consumption": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/9/9f/Raptor.png/256px-Raptor.png", "category": "carnivore"},
    "Carnotaurus": {"maturation_time": 16667, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/d/d5/Carnotaurus.png/256px-Carnotaurus.png", "category": "carnivore"},
    "Allosaurus": {"maturation_time": 20000, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Cooked Meat", "Raw Prime Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/c/c4/Allosaurus.png/256px-Allosaurus.png", "category": "carnivore"},
    "Baryonyx": {"maturation_time": 16667, "food_consumption": 0.000103, "food_type": ["Raw Meat", "Raw Fish Meat", "Cooked Fish Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/e/e8/Baryonyx.png/256px-Baryonyx.png", "category": "carnivore"},
    "Ankylosaurus": {"maturation_time": 16667, "food_consumption": 0.000124, "food_type": ["Vegetables", "Mejoberries", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/9/98/Ankylosaurus.png/256px-Ankylosaurus.png", "category": "herbivore"},
    "Stegosaurus": {"maturation_time": 20000, "food_consumption": 0.000124, "food_type": ["Vegetables", "Mejoberries", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/8/80/Stegosaurus.png/256px-Stegosaurus.png", "category": "herbivore"},
    "Brontosaurus": {"maturation_time": 33333, "food_consumption": 0.000165, "food_type": ["Vegetables", "Mejoberries", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/d/d4/Brontosaurus.png/256px-Brontosaurus.png", "category": "herbivore"},
    "Triceratops": {"maturation_time": 20000, "food_consumption": 0.000124, "food_type": ["Vegetables", "Mejoberries", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/9/9f/Triceratops.png/256px-Triceratops.png", "category": "herbivore"},
    "Mammoth": {"maturation_time": 26667, "food_consumption": 0.000144, "food_type": ["Vegetables", "Mejoberries", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/2/29/Mammoth.png/256px-Mammoth.png", "category": "herbivore"},
    "Dire Wolf": {"maturation_time": 16667, "food_consumption": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/3/3c/Direwolf.png/256px-Direwolf.png", "category": "carnivore"},
    "Sabertooth": {"maturation_time": 16667, "food_consumption": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/5/5f/Sabertooth.png/256px-Sabertooth.png", "category": "carnivore"},
    "Dire Bear": {"maturation_time": 23333, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Cooked Meat", "Vegetables", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/0/04/Direbear.png/256px-Direbear.png", "category": "omnivore"},
    "Therizinosaurus": {"maturation_time": 33333, "food_consumption": 0.000144, "food_type": ["Vegetables", "Mejoberries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/5/56/Therizinosaurus.png/256px-Therizinosaurus.png", "category": "herbivore"},
    "Yutyrannus": {"maturation_time": 33333, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Cooked Meat", "Raw Prime Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/d/d6/Yutyrannus.png/256px-Yutyrannus.png", "category": "carnivore"},
    "Megalosaurus": {"maturation_time": 23333, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Cooked Meat", "Raw Prime Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/5/57/Megalosaurus.png/256px-Megalosaurus.png", "category": "carnivore"},
    "Griffin": {"maturation_time": 33333, "food_consumption": 0.000103, "food_type": ["Raw Meat", "Cooked Meat", "Raw Prime Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/3/3f/Griffin.png/256px-Griffin.png", "category": "carnivore"},
    "Managarmr": {"maturation_time": 33333, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Cooked Meat", "Raw Prime Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/e/e0/Managarmr.png/256px-Managarmr.png", "category": "carnivore"},
    "Snow Owl": {"maturation_time": 26667, "food_consumption": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/c/c7/Snow_Owl.png/256px-Snow_Owl.png", "category": "carnivore"},
    "Woolly Rhino": {"maturation_time": 23333, "food_consumption": 0.000144, "food_type": ["Vegetables", "Mejoberries", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/f/f1/Woolly_Rhino.png/256px-Woolly_Rhino.png", "category": "herbivore"},
    "Daeodon": {"maturation_time": 33333, "food_consumption": 0.000144, "food_type": ["Raw Meat", "Cooked Meat", "Vegetables"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/0/08/Daeodon.png/256px-Daeodon.png", "category": "omnivore"},
    "Mantis": {"maturation_time": 23333, "food_consumption": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/d/d6/Mantis.png/256px-Mantis.png", "category": "carnivore"},
    "Parasaur": {"maturation_time": 13333, "food_consumption": 0.000083, "food_type": ["Vegetables", "Mejoberries", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/8/84/Parasaur.png/256px-Parasaur.png", "category": "herbivore"},
    "Dodo": {"maturation_time": 10000, "food_consumption": 0.000062, "food_type": ["Vegetables", "Mejoberries", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/d/d5/Dodo.png/256px-Dodo.png", "category": "herbivore"},
    "Megalodon": {"maturation_time": 20000, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Raw Fish Meat", "Cooked Fish Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/3/35/Megalodon.png/256px-Megalodon.png", "category": "carnivore"},
    "Basilosaurus": {"maturation_time": 26667, "food_consumption": 0.000144, "food_type": ["Raw Meat", "Raw Prime Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/b/b3/Basilosaurus.png/256px-Basilosaurus.png", "category": "carnivore"},
    "Mosasaurus": {"maturation_time": 33333, "food_consumption": 0.000165, "food_type": ["Raw Meat", "Raw Prime Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/5/53/Mosasaurus.png/256px-Mosasaurus.png", "category": "carnivore"},
    "Tusoteuthis": {"maturation_time": 26667, "food_consumption": 0.000144, "food_type": ["Raw Meat", "Raw Prime Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/8/82/Tusoteuthis.png/256px-Tusoteuthis.png", "category": "carnivore"},
    "Dunkleosteus": {"maturation_time": 20000, "food_consumption": 0.000124, "food_type": ["Raw Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/a/a9/Dunkleosteus.png/256px-Dunkleosteus.png", "category": "carnivore"},
    "Wyvern": {"maturation_time": 33333, "food_consumption": 0.000165, "food_type": ["Raw Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/4/4f/Wyvern.png/256px-Wyvern.png", "category": "carnivore"},
    "Rock Drake": {"maturation_time": 33333, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/8/82/Rock_Drake.png/256px-Rock_Drake.png", "category": "carnivore"},
    "Reaper": {"maturation_time": 33333, "food_consumption": 0.000165, "food_type": ["Raw Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/5/57/Reaper.png/256px-Reaper.png", "category": "carnivore"},
    "Voidwyrm": {"maturation_time": 33333, "food_consumption": 0.000165, "food_type": ["Raw Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/3/33/Voidwyrm.png/256px-Voidwyrm.png", "category": "carnivore"},
    "Deinonychus": {"maturation_time": 20000, "food_consumption": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/d/d3/Deinonychus.png/256px-Deinonychus.png", "category": "carnivore"},
    "Equus": {"maturation_time": 16667, "food_consumption": 0.000083, "food_type": ["Vegetables", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/f/f2/Equus.png/256px-Equus.png", "category": "herbivore"},
    "Megalania": {"maturation_time": 20000, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/5/54/Megalania.png/256px-Megalania.png", "category": "carnivore"},
    "Kaprosuchus": {"maturation_time": 16667, "food_consumption": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/8/8f/Kaprosuchus.png/256px-Kaprosuchus.png", "category": "carnivore"},
    "Purlovia": {"maturation_time": 16667, "food_consumption": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/e/ec/Purlovia.png/256px-Purlovia.png", "category": "carnivore"},
    "Beelzebufo": {"maturation_time": 16667, "food_consumption": 0.000083, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/7/71/Beelzebufo.png/256px-Beelzebufo.png", "category": "carnivore"},
    "Tapejara": {"maturation_time": 16667, "food_consumption": 0.000083, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/7/72/Tapejara.png/256px-Tapejara.png", "category": "carnivore"},
    "Pelagornis": {"maturation_time": 13333, "food_consumption": 0.000083, "food_type": ["Raw Meat", "Raw Fish Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/c/c9/Pelagornis.png/256px-Pelagornis.png", "category": "carnivore"},
    "Quetzal": {"maturation_time": 36000, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/0/0b/Quetzal.png/256px-Quetzal.png", "category": "carnivore"},
    "Procoptodon": {"maturation_time": 20000, "food_consumption": 0.000103, "food_type": ["Vegetables", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/5/51/Procoptodon.png/256px-Procoptodon.png", "category": "herbivore"},
    "Dimetrodon": {"maturation_time": 16667, "food_consumption": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/e/e5/Dimetrodon.png/256px-Dimetrodon.png", "category": "carnivore"},
    "Ovis": {"maturation_time": 10000, "food_consumption": 0.000062, "food_type": ["Vegetables", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/3/3c/Ovis.png/256px-Ovis.png", "category": "herbivore"},
    "Moschops": {"maturation_time": 13333, "food_consumption": 0.000083, "food_type": ["Vegetables", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/a/a0/Moschops.png/256px-Moschops.png", "category": "herbivore"}
}

active_timers = {}

def is_evo_weekend():
    now_utc = datetime.utcnow()
    now_et = now_utc + timedelta(hours=-5)
    weekday, hour = now_et.weekday(), now_et.hour
    return (weekday == 4 and hour >= 17) or weekday in [5, 6] or (weekday == 0 and hour < 21)

def get_multipliers():
    if is_evo_weekend():
        return {"mature": 4, "cuddle_interval": 0.6, "imprint_amount": 4, "event_name": "EVO Weekend"}
    return {"mature": 2, "cuddle_interval": 1.0, "imprint_amount": 1, "event_name": "Weekday"}

def calculate_breeding(dino_name, weight, food_type):
    if dino_name not in DINO_DATA:
        return None
    dino = DINO_DATA[dino_name]
    mults = get_multipliers()
    food_val = FOOD_TYPES[food_type]["value"]
    mat_time = dino["maturation_time"] / mults["mature"]
    juv_time = mat_time * dino["juvenile_percent"]
    baby_food = (dino["food_consumption"] * juv_time * weight) / food_val
    juv_food = (dino["food_consumption"] * (mat_time - juv_time) * weight) / food_val
    cuddle_int = dino["cuddle_interval"] * mults["cuddle_interval"]
    return {
        "dino_name": dino_name, "weight": weight, "food_type": food_type,
        "food_emoji": FOOD_TYPES[food_type]["emoji"], "multipliers": mults,
        "time_to_juvenile": juv_time, "time_to_adult": mat_time,
        "baby_food": baby_food, "juv_food": juv_food, "total_food": baby_food + juv_food,
        "cuddle_interval": cuddle_int, "cuddle_count": int(mat_time / cuddle_int),
        "image": dino.get("image", "")
    }

def format_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    if h > 24:
        return f"{h//24}d {h%24}h {m}m"
    return f"{h}h {m}m" if h > 0 else f"{m}m"

class DinoSelect(Select):
    def __init__(self):
        opts = [discord.SelectOption(label=n, emoji="🦖", description=DINO_DATA[n]["category"].title()) for n in sorted(DINO_DATA.keys())]
        super().__init__(placeholder="Choose dinosaur...", options=opts[:25])
    async def callback(self, i):
        await i.response.send_modal(WeightModal(self.values[0]))

class FoodSelect(Select):
    def __init__(self, dino, weight):
        self.dino, self.weight = dino, weight
        foods = DINO_DATA[dino]["food_type"]
        opts = [discord.SelectOption(label=f, emoji=FOOD_TYPES[f]["emoji"], description=f"Value: {FOOD_TYPES[f]['value']}") for f in foods]
        super().__init__(placeholder="Select food...", options=opts)
    async def callback(self, i):
        stats = calculate_breeding(self.dino, self.weight, self.values[0])
        if not stats:
            return await i.response.send_message("Error!", ephemeral=True)
        e = discord.Embed(title=f"🦖 {stats['dino_name']} Calculator", description=f"Weight: {stats['weight']} | Food: {stats['food_emoji']} {stats['food_type']}", color=discord.Color.blue())
        if stats['image']:
            e.set_thumbnail(url=stats['image'])
        e.add_field(name="📅 Event", value=f"{stats['multipliers']['event_name']}\nMature: {stats['multipliers']['mature']}x", inline=False)
        e.add_field(name="⏱️ Times", value=f"Juvenile: {format_time(stats['time_to_juvenile'])}\nAdult: {format_time(stats['time_to_adult'])}", inline=True)
        e.add_field(name=f"{stats['food_emoji']} Food", value=f"Baby: {int(stats['baby_food'])}\nJuvenile: {int(stats['juv_food'])}\nTotal: {int(stats['total_food'])}", inline=True)
        e.add_field(name="💕 Imprint", value=f"Cuddles: {stats['cuddle_count']}\nInterval: {format_time(stats['cuddle_interval'])}", inline=False)
        e.set_footer(text="ARK: Survival Ascended | Small Tribes")
        await i.response.send_message(embed=e)

class WeightModal(discord.ui.Modal, title="Dino Weight"):
    def __init__(self, dino):
        super().__init__()
        self.dino = dino
        self.w = discord.ui.TextInput(label="Baby Weight", placeholder="e.g. 400", max_length=10)
        self.add_item(self.w)
    async def on_submit(self, i):
        try:
            weight = float(self.w.value)
            if weight <= 0:
                raise ValueError()
            v = View()
            v.add_item(FoodSelect(self.dino, weight))
            await i.response.send_message(f"🦖 {self.dino} | Weight: {weight}\nSelect food:", view=v, ephemeral=True)
        except:
            await i.response.send_message("Invalid weight!", ephemeral=True)

@tree.command(name="breeding", description="Calculate breeding stats")
async def breeding(i: discord.Interaction):
    e = discord.Embed(title="🦖 ARK Breeding Calculator", description="Select a dinosaur from the menu!", color=discord.Color.blue())
    m = get_multipliers()
    e.add_field(name="📅 Current Event", value=f"{m['event_name']}\nMature: {m['mature']}x | Cuddle: {m['cuddle_interval']}x", inline=False)
    e.set_footer(text="ARK: Survival Ascended | Small Tribes")
    v = View()
    v.add_item(DinoSelect())
    await i.response.send_message(embed=e, view=v)

@tree.command(name="dinos", description="List all creatures")
async def dinos(i: discord.Interaction):
    carns = [n for n,d in DINO_DATA.items() if d["category"]=="carnivore"]
    herbs = [n for n,d in DINO_DATA.items() if d["category"]=="herbivore"]
    omnis = [n for n,d in DINO_DATA.items() if d["category"]=="omnivore"]
    e = discord.Embed(title="📋 Available Creatures", description=f"Total: {len(DINO_DATA)} creatures", color=discord.Color.green())
    if carns:
        e.add_field(name=f"🥩 Carnivores ({len(carns)})", value=", ".join(carns[:20]) + ("..." if len(carns) > 20 else ""), inline=False)
    if herbs:
        e.add_field(name=f"🥕 Herbivores ({len(herbs)})", value=", ".join(herbs[:20]) + ("..." if len(herbs) > 20 else ""), inline=False)
    if omnis:
        e.add_field(name=f"🍖 Omnivores ({len(omnis)})", value=", ".join(omnis), inline=False)
    e.set_footer(text="Use /breeding to calculate!")
    await i.response.send_message(embed=e)

@tree.command(name="event", description="Show event status")
async def event(i: discord.Interaction):
    m = get_multipliers()
    e = discord.Embed(title=m['event_name'], description="Small Tribes Rates", color=discord.Color.green() if is_evo_weekend() else discord.Color.blue())
    e.add_field(name="⚙️ Multipliers", value=f"Hatch: 2x/4x\nMature: {m['mature']}x\nCuddle: {m['cuddle_interval']}x\nImprint: {m['imprint_amount']}x", inline=False)
    if is_evo_weekend():
        e.add_field(name="🎉 EVO Active!", value="Friday 17:00 - Monday 21:00 ET\nDouble rates!", inline=False)
    else:
        e.add_field(name="📅 Weekday", value="EVO starts Friday 17:00 ET (23:00 CET)", inline=False)
    await i.response.send_message(embed=e)

@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot online: {client.user}")
    print(f"📊 {len(DINO_DATA)} creatures available")
    print(f"🎮 Active in {len(client.guilds)} servers")

if __name__ == "__main__":
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        try:
            with open("config.json") as f:
                token = json.load(f).get("bot_token")
        except:
            print("❌ No token found!")
            exit(1)
    if not token:
        print("❌ Token not set!")
        exit(1)
    print("🚀 Starting bot...")
    client.run(token)
