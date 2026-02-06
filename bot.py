import discord
from discord import app_commands  
from discord.ui import Select, View, Button
import asyncio
from datetime import datetime, timedelta
import json
import os

# Bot Setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Food Types with values
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

# DINO_DATA with 34 creatures - abbreviated for file size
DINO_DATA = {
    "Rex": {"maturation_time": 9.259259*3600, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Cooked Meat", "Raw Prime Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/c/c3/Rex.png/256px-Rex.png", "category": "carnivore"},
    "Giganotosaurus": {"maturation_time": 13.888888*3600, "food_consumption": 0.000165, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/1/1e/Giganotosaurus.png/256px-Giganotosaurus.png", "category": "carnivore"},
    "Spino": {"maturation_time": 9.259259*3600, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Raw Fish Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/7/7e/Spino.png/256px-Spino.png", "category": "carnivore"},
    "Thylacoleo": {"maturation_time": 4.62963*3600, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/0/00/Thylacoleo.png/256px-Thylacoleo.png", "category": "carnivore"},
    "Argentavis": {"maturation_time": 5.555555*3600, "food_consumption": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/1/1e/Argentavis.png/256px-Argentavis.png", "category": "carnivore"},
    "Pteranodon": {"maturation_time": 3.703703*3600, "food_consumption": 0.000083, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/6/6f/Pteranodon.png/256px-Pteranodon.png", "category": "carnivore"},
    "Raptor": {"maturation_time": 4.62963*3600, "food_consumption": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/9/9f/Raptor.png/256px-Raptor.png", "category": "carnivore"},
    "Carnotaurus": {"maturation_time": 4.62963*3600, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/d/d5/Carnotaurus.png/256px-Carnotaurus.png", "category": "carnivore"},
    "Allosaurus": {"maturation_time": 5.555555*3600, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/c/c4/Allosaurus.png/256px-Allosaurus.png", "category": "carnivore"},
    "Baryonyx": {"maturation_time": 4.62963*3600, "food_consumption": 0.000103, "food_type": ["Raw Meat", "Raw Fish Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/e/e8/Baryonyx.png/256px-Baryonyx.png", "category": "carnivore"},
    "Ankylosaurus": {"maturation_time": 4.62963*3600, "food_consumption": 0.000124, "food_type": ["Vegetables", "Mejoberries", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/9/98/Ankylosaurus.png/256px-Ankylosaurus.png", "category": "herbivore"},
    "Stegosaurus": {"maturation_time": 5.555555*3600, "food_consumption": 0.000124, "food_type": ["Vegetables", "Mejoberries", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/8/80/Stegosaurus.png/256px-Stegosaurus.png", "category": "herbivore"},
    "Brontosaurus": {"maturation_time": 9.259259*3600, "food_consumption": 0.000165, "food_type": ["Vegetables", "Mejoberries", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/d/d4/Brontosaurus.png/256px-Brontosaurus.png", "category": "herbivore"},
    "Triceratops": {"maturation_time": 5.555555*3600, "food_consumption": 0.000124, "food_type": ["Vegetables", "Mejoberries", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/9/9f/Triceratops.png/256px-Triceratops.png", "category": "herbivore"},
    "Mammoth": {"maturation_time": 7.407407*3600, "food_consumption": 0.000144, "food_type": ["Vegetables", "Mejoberries", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/2/29/Mammoth.png/256px-Mammoth.png", "category": "herbivore"},
    "Dire Wolf": {"maturation_time": 4.62963*3600, "food_consumption": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/3/3c/Direwolf.png/256px-Direwolf.png", "category": "carnivore"},
    "Sabertooth": {"maturation_time": 4.62963*3600, "food_consumption": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/5/5f/Sabertooth.png/256px-Sabertooth.png", "category": "carnivore"},
    "Dire Bear": {"maturation_time": 6.481481*3600, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Vegetables", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/0/04/Direbear.png/256px-Direbear.png", "category": "omnivore"},
    "Therizinosaurus": {"maturation_time": 9.259259*3600, "food_consumption": 0.000144, "food_type": ["Vegetables", "Mejoberries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/5/56/Therizinosaurus.png/256px-Therizinosaurus.png", "category": "herbivore"},
    "Yutyrannus": {"maturation_time": 9.259259*3600, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/d/d6/Yutyrannus.png/256px-Yutyrannus.png", "category": "carnivore"},
    "Megalosaurus": {"maturation_time": 6.481481*3600, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/5/57/Megalosaurus.png/256px-Megalosaurus.png", "category": "carnivore"},
    "Griffin": {"maturation_time": 9.259259*3600, "food_consumption": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/3/3f/Griffin.png/256px-Griffin.png", "category": "carnivore"},
    "Managarmr": {"maturation_time": 9.259259*3600, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/e/e0/Managarmr.png/256px-Managarmr.png", "category": "carnivore"},
    "Snow Owl": {"maturation_time": 7.407407*3600, "food_consumption": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/c/c7/Snow_Owl.png/256px-Snow_Owl.png", "category": "carnivore"},
    "Woolly Rhino": {"maturation_time": 6.481481*3600, "food_consumption": 0.000144, "food_type": ["Vegetables", "Mejoberries", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/f/f1/Woolly_Rhino.png/256px-Woolly_Rhino.png", "category": "herbivore"},
    "Daeodon": {"maturation_time": 9.259259*3600, "food_consumption": 0.000144, "food_type": ["Raw Meat", "Vegetables"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/0/08/Daeodon.png/256px-Daeodon.png", "category": "omnivore"},
    "Mantis": {"maturation_time": 6.481481*3600, "food_consumption": 0.000103, "food_type": ["Raw Meat", "Cooked Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/d/d6/Mantis.png/256px-Mantis.png", "category": "carnivore"},
    "Parasaur": {"maturation_time": 3.703703*3600, "food_consumption": 0.000083, "food_type": ["Vegetables", "Mejoberries", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/8/84/Parasaur.png/256px-Parasaur.png", "category": "herbivore"},
    "Dodo": {"maturation_time": 2.777777*3600, "food_consumption": 0.000062, "food_type": ["Vegetables", "Mejoberries", "Berries"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/d/d5/Dodo.png/256px-Dodo.png", "category": "herbivore"},
    "Megalodon": {"maturation_time": 5.555555*3600, "food_consumption": 0.000124, "food_type": ["Raw Meat", "Raw Fish Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/3/35/Megalodon.png/256px-Megalodon.png", "category": "carnivore"},
    "Basilosaurus": {"maturation_time": 7.407407*3600, "food_consumption": 0.000144, "food_type": ["Raw Meat", "Raw Prime Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/b/b3/Basilosaurus.png/256px-Basilosaurus.png", "category": "carnivore"},
    "Mosasaurus": {"maturation_time": 9.259259*3600, "food_consumption": 0.000165, "food_type": ["Raw Meat", "Raw Prime Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/5/53/Mosasaurus.png/256px-Mosasaurus.png", "category": "carnivore"},
    "Tusoteuthis": {"maturation_time": 7.407407*3600, "food_consumption": 0.000144, "food_type": ["Raw Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/8/82/Tusoteuthis.png/256px-Tusoteuthis.png", "category": "carnivore"},
    "Dunkleosteus": {"maturation_time": 5.555555*3600, "food_consumption": 0.000124, "food_type": ["Raw Meat"], "juvenile_percent": 0.1, "cuddle_interval": 28800, "image": "https://ark.wiki.gg/images/thumb/a/a9/Dunkleosteus.png/256px-Dunkleosteus.png", "category": "carnivore"}
}

active_timers = {}

def is_evo_weekend():
    now_utc = datetime.utcnow()
    et_offset = timedelta(hours=-5)
    now_et = now_utc + et_offset
    weekday, hour = now_et.weekday(), now_et.hour
    if weekday == 4 and hour >= 17: return True
    if weekday in [5,6]: return True
    if weekday == 0 and hour < 21: return True
    return False

def get_multipliers():
    if is_evo_weekend():
        return {"hatch":4, "mature":4, "cuddle_interval":0.6, "imprint_amount":4, "event_name":"🎉 EVO Weekend"}
    return {"hatch":2, "mature":2, "cuddle_interval":1.0, "imprint_amount":1, "event_name":"📅 Weekday"}

def calculate_breeding(dino_name, weight, food_type):
    if dino_name not in DINO_DATA: return None
    dino, multipliers = DINO_DATA[dino_name], get_multipliers()
    food_value = FOOD_TYPES[food_type]["value"]
    actual_maturation = dino["maturation_time"] / multipliers["mature"]
    time_to_juvenile = actual_maturation * dino["juvenile_percent"]
    time_to_adult = actual_maturation
    baby_food_count = (dino["food_consumption"] * time_to_juvenile * weight) / food_value
    juvenile_food_count = (dino["food_consumption"] * (time_to_adult - time_to_juvenile) * weight) / food_value
    cuddle_interval = dino["cuddle_interval"] * multipliers["cuddle_interval"]
    return {
        "dino_name": dino_name, "weight": weight, "food_type": food_type,
        "food_emoji": FOOD_TYPES[food_type]["emoji"], "multipliers": multipliers,
        "time_to_juvenile": time_to_juvenile, "time_to_adult": time_to_adult,
        "baby_food_count": baby_food_count, "juvenile_food_count": juvenile_food_count,
        "total_food_count": baby_food_count + juvenile_food_count,
        "cuddle_interval": cuddle_interval, "cuddle_count": int(time_to_adult/cuddle_interval),
        "image": dino.get("image", "")
    }

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 24:
        days = hours // 24
        hours = hours % 24
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m {secs}s"

class DinoSelect(Select):
    def __init__(self):
        options = [discord.SelectOption(label=name, emoji="🦖", description=DINO_DATA[name]["category"].capitalize()) for name in sorted(DINO_DATA.keys())]
        super().__init__(placeholder="Choose a dinosaur...", min_values=1, max_values=1, options=options[:25])
    async def callback(self, interaction): await interaction.response.send_modal(WeightModal(self.values[0]))

class FoodSelect(Select):
    def __init__(self, dino_name, weight):
        self.dino_name, self.weight = dino_name, weight
        available_foods = DINO_DATA[dino_name]["food_type"]
        options = [discord.SelectOption(label=food, emoji=FOOD_TYPES[food]["emoji"], description=f"Food Value: {FOOD_TYPES[food]['value']}") for food in available_foods]
        super().__init__(placeholder="Select food type...", min_values=1, max_values=1, options=options)
    async def callback(self, interaction):
        food_type = self.values[0]
        stats = calculate_breeding(self.dino_name, self.weight, food_type)
        if not stats: 
            await interaction.response.send_message("❌ Error calculating stats!", ephemeral=True)
            return
        embed = discord.Embed(title=f"🦖 {stats['dino_name']} Breeding Calculator", description=f"**Weight:** {stats['weight']} | **Food:** {stats['food_emoji']} {stats['food_type']}", color=discord.Color.blue())
        if stats['image']: embed.set_thumbnail(url=stats['image'])
        embed.add_field(name="📅 Current Event", value=f"**{stats['multipliers']['event_name']}**
Mature: {stats['multipliers']['mature']}x | Cuddle: {stats['multipliers']['cuddle_interval']}x", inline=False)
        embed.add_field(name="⏱️ Maturation Times", value=f"**Juvenile:** {format_time(stats['time_to_juvenile'])}
**Adult:** {format_time(stats['time_to_adult'])}", inline=True)
        embed.add_field(name=f"{stats['food_emoji']} Food Required", value=f"**Baby:** {int(stats['baby_food_count'])}
**Juvenile:** {int(stats['juvenile_food_count'])}
**Total:** {int(stats['total_food_count'])}", inline=True)
        embed.add_field(name="💕 Imprinting", value=f"**Cuddles:** {stats['cuddle_count']}
**Interval:** {format_time(stats['cuddle_interval'])}", inline=False)
        embed.set_footer(text="ARK: Survival Ascended | Small Tribes")
        view = View()
        timer_button = Button(label="🔔 Start Timer", style=discord.ButtonStyle.green)
        async def timer_callback(btn_interaction):
            await btn_interaction.response.send_message(f"✅ Timer started for **{stats['dino_name']}**!", ephemeral=True)
            user_id = btn_interaction.user.id
            if user_id not in active_timers: active_timers[user_id] = []
            active_timers[user_id].append({'stats': stats, 'start_time': datetime.now()})
            asyncio.create_task(juvenile_timer(btn_interaction, stats))
            asyncio.create_task(adult_timer(btn_interaction, stats))
            asyncio.create_task(imprint_timer(btn_interaction, stats, btn_interaction.user))
        timer_button.callback = timer_callback
        view.add_item(timer_button)
        await interaction.response.send_message(embed=embed, view=view)

class WeightModal(discord.ui.Modal, title="Dino Details"):
    def __init__(self, dino_name):
        super().__init__()
        self.dino_name = dino_name
        self.weight_input = discord.ui.TextInput(label="Baby Dino Weight", placeholder="e.g. 400", required=True, max_length=10)
        self.add_item(self.weight_input)
    async def on_submit(self, interaction):
        try:
            weight = float(self.weight_input.value)
            if weight <= 0: raise ValueError("Weight must be positive")
            view = View()
            view.add_item(FoodSelect(self.dino_name, weight))
            await interaction.response.send_message(f"🦖 **{self.dino_name}** | Weight: **{weight}**
Select food:", view=view, ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Invalid weight!", ephemeral=True)

async def juvenile_timer(interaction, stats):
    await asyncio.sleep(stats['time_to_juvenile'])
    embed = discord.Embed(title="🎯 Juvenile Stage!", description=f"**{stats['dino_name']}** reached Juvenile!", color=discord.Color.gold())
    embed.add_field(name="⏱️ Until Adult", value=format_time(stats['time_to_adult'] - stats['time_to_juvenile']))
    await interaction.channel.send(content=interaction.user.mention, embed=embed)

async def adult_timer(interaction, stats):
    await asyncio.sleep(stats['time_to_adult'])
    embed = discord.Embed(title="🎉 Fully Grown!", description=f"**{stats['dino_name']}** is mature!", color=discord.Color.purple())
    embed.add_field(name="📊 Stats", value=f"**Food Used:** {int(stats['total_food_count'])}
**Time:** {format_time(stats['time_to_adult'])}")
    await interaction.channel.send(content=interaction.user.mention, embed=embed)

async def imprint_timer(interaction, stats, user):
    cuddle_count, max_cuddles = 0, stats['cuddle_count']
    while cuddle_count < max_cuddles:
        await asyncio.sleep(stats['cuddle_interval'])
        cuddle_count += 1
        current_imprint = cuddle_count * stats['multipliers']['imprint_amount']
        try:
            embed = discord.Embed(title="💕 Imprint Time!" if current_imprint < 100 else "💯 100% Imprint!", description=f"**{stats['dino_name']}** wants cuddles!" if current_imprint < 100 else "Fully imprinted!", color=discord.Color.pink() if current_imprint < 100 else discord.Color.green())
            if current_imprint < 100:
                embed.add_field(name="Progress", value=f"**Cuddle #{cuddle_count}/{max_cuddles}**
**Imprint:** {min(current_imprint,100)}%")
            await user.send(embed=embed)
        except discord.Forbidden:
            await interaction.channel.send(content=f"{user.mention} - Imprint time!", embed=embed)

class DinoSelectView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(DinoSelect())

@tree.command(name="breeding", description="Calculate breeding stats")
async def breeding(interaction: discord.Interaction):
    embed = discord.Embed(title="🦖 ARK Breeding Calculator", description="Select a dinosaur!", color=discord.Color.blue())
    multipliers = get_multipliers()
    embed.add_field(name="📅 Event", value=f"**{multipliers['event_name']}**
Mature: {multipliers['mature']}x | Cuddle: {multipliers['cuddle_interval']}x", inline=False)
    embed.set_footer(text="ARK: Survival Ascended | Small Tribes")
    await interaction.response.send_message(embed=embed, view=DinoSelectView())

@tree.command(name="dinos", description="List all dinosaurs")
async def dinos(interaction: discord.Interaction):
    carnivores = [n for n,d in DINO_DATA.items() if d["category"]=="carnivore"]
    herbivores = [n for n,d in DINO_DATA.items() if d["category"]=="herbivore"]
    omnivores = [n for n,d in DINO_DATA.items() if d["category"]=="omnivore"]
    embed = discord.Embed(title="📋 Available Dinosaurs", description=f"**Total:** {len(DINO_DATA)}", color=discord.Color.green())
    if carnivores: embed.add_field(name="🥩 Carnivores", value=", ".join(carnivores[:15]), inline=False)
    if herbivores: embed.add_field(name="🥕 Herbivores", value=", ".join(herbivores[:15]), inline=False)
    if omnivores: embed.add_field(name="🍖 Omnivores", value=", ".join(omnivores), inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name="event", description="Show event status")
async def event(interaction: discord.Interaction):
    multipliers = get_multipliers()
    embed = discord.Embed(title=f"{multipliers['event_name']}", description="Small Tribes Rates", color=discord.Color.green() if is_evo_weekend() else discord.Color.blue())
    embed.add_field(name="⚙️ Multipliers", value=f"**Hatch:** {multipliers['hatch']}x
**Mature:** {multipliers['mature']}x
**Cuddle:** {multipliers['cuddle_interval']}x
**Imprint:** {multipliers['imprint_amount']}x", inline=False)
    if is_evo_weekend():
        embed.add_field(name="🎉 EVO Active!", value="Friday 17:00 - Monday 21:00 ET", inline=False)
    else:
        embed.add_field(name="📅 Weekday", value="EVO starts Friday 17:00 ET", inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name="mytimers", description="Show your timers")
async def mytimers(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id not in active_timers or not active_timers[user_id]:
        await interaction.response.send_message("❌ No active timers!", ephemeral=True)
        return
    embed = discord.Embed(title="⏰ Active Timers", description=f"**{len(active_timers[user_id])}** timers", color=discord.Color.blue())
    for i, timer in enumerate(active_timers[user_id], 1):
        stats, start_time = timer['stats'], timer['start_time']
        elapsed = (datetime.now() - start_time).total_seconds()
        remaining_adult = max(0, stats['time_to_adult'] - elapsed)
        status = "🟢 Running" if remaining_adult > 0 else "✅ Complete"
        time_left = f"Adult in: {format_time(remaining_adult)}" if remaining_adult > 0 else "Fully grown!"
        embed.add_field(name=f"#{i} - {stats['dino_name']} ({status})", value=f"**Weight:** {stats['weight']}
**{time_left}**", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot online as {client.user}")
    print(f"📊 {len(DINO_DATA)} dinos available")

if __name__ == "__main__":
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        try:
            with open("config.json") as f:
                token = json.load(f).get("bot_token")
        except FileNotFoundError:
            print("❌ No token found!")
            exit(1)
    if not token or token == "DEIN_BOT_TOKEN_HIER":
        print("❌ Bot token not set!")
        exit(1)
    print("🚀 Starting bot...")
    client.run(token)
