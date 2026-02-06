import discord
from discord import app_commands
from discord.ui import Select, View
import asyncio
from datetime import datetime, timedelta
import json
import os

# Bot Setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ARK Dino Datenbank mit Basis-Stats (Base rates ohne Multiplier)
DINO_DATA = {
    "Rex": {
        "maturation_time": 9.259259 * 3600,  # in Sekunden (Basis ohne Multiplier)
        "food_consumption": 0.000124,  # Food pro Sekunde
        "food_type": "Raw Meat",
        "juvenile_percent": 0.1,  # 10% = Juvenile
        "cuddle_interval": 28800  # 8 Stunden in Sekunden (Basis)
    },
    "Giga": {
        "maturation_time": 13.888888 * 3600,
        "food_consumption": 0.000165,
        "food_type": "Raw Meat",
        "juvenile_percent": 0.1,
        "cuddle_interval": 28800
    },
    "Thylacoleo": {
        "maturation_time": 4.62963 * 3600,
        "food_consumption": 0.000124,
        "food_type": "Raw Meat",
        "juvenile_percent": 0.1,
        "cuddle_interval": 28800
    },
    "Spino": {
        "maturation_time": 9.259259 * 3600,
        "food_consumption": 0.000124,
        "food_type": "Raw Meat / Fish",
        "juvenile_percent": 0.1,
        "cuddle_interval": 28800
    },
    "Argentavis": {
        "maturation_time": 5.555555 * 3600,
        "food_consumption": 0.000103,
        "food_type": "Raw Meat",
        "juvenile_percent": 0.1,
        "cuddle_interval": 28800
    },
    "Ankylosaurus": {
        "maturation_time": 4.62963 * 3600,
        "food_consumption": 0.000124,
        "food_type": "Vegetables",
        "juvenile_percent": 0.1,
        "cuddle_interval": 28800
    },
    "Pteranodon": {
        "maturation_time": 3.703703 * 3600,
        "food_consumption": 0.000083,
        "food_type": "Raw Meat",
        "juvenile_percent": 0.1,
        "cuddle_interval": 28800
    },
    "Raptor": {
        "maturation_time": 4.62963 * 3600,
        "food_consumption": 0.000103,
        "food_type": "Raw Meat",
        "juvenile_percent": 0.1,
        "cuddle_interval": 28800
    },
    "Carno": {
        "maturation_time": 4.62963 * 3600,
        "food_consumption": 0.000124,
        "food_type": "Raw Meat",
        "juvenile_percent": 0.1,
        "cuddle_interval": 28800
    },
    "Brontosaurus": {
        "maturation_time": 9.259259 * 3600,
        "food_consumption": 0.000165,
        "food_type": "Vegetables",
        "juvenile_percent": 0.1,
        "cuddle_interval": 28800
    },
    "Mammoth": {
        "maturation_time": 7.407407 * 3600,
        "food_consumption": 0.000144,
        "food_type": "Vegetables",
        "juvenile_percent": 0.1,
        "cuddle_interval": 28800
    },
    "Dire Wolf": {
        "maturation_time": 4.62963 * 3600,
        "food_consumption": 0.000103,
        "food_type": "Raw Meat",
        "juvenile_percent": 0.1,
        "cuddle_interval": 28800
    },
    "Sabertooth": {
        "maturation_time": 4.62963 * 3600,
        "food_consumption": 0.000103,
        "food_type": "Raw Meat",
        "juvenile_percent": 0.1,
        "cuddle_interval": 28800
    }
}

# Aktive Timer speichern (User -> Timer Liste)
active_timers = {}

def is_evo_weekend():
    """Prüft ob gerade EVO Weekend ist (Freitag 17:00 bis Montag 21:00 ET)"""
    # Umrechnung: ET = UTC-5 (Winter) oder UTC-4 (Sommer)
    # Für Einfachheit nehmen wir UTC-5 (EST)
    now_utc = datetime.utcnow()
    et_offset = timedelta(hours=-5)
    now_et = now_utc + et_offset
    
    weekday = now_et.weekday()  # 0=Montag, 4=Freitag, 6=Sonntag
    hour = now_et.hour
    
    # Freitag ab 17 Uhr
    if weekday == 4 and hour >= 17:
        return True
    # Samstag & Sonntag ganztägig
    if weekday in [5, 6]:
        return True
    # Montag bis 21 Uhr
    if weekday == 0 and hour < 21:
        return True
    
    return False

def get_multipliers():
    """Gibt die aktuellen Multiplier zurück basierend auf Wochentag"""
    if is_evo_weekend():
        return {
            "hatch": 4,
            "mature": 4,
            "cuddle_interval": 0.6,
            "imprint_amount": 4,
            "event_name": "🎉 EVO Weekend"
        }
    else:
        return {
            "hatch": 2,
            "mature": 2,
            "cuddle_interval": 1.0,
            "imprint_amount": 1,
            "event_name": "📅 Weekday"
        }

def calculate_breeding(dino_name, weight):
    """Berechnet alle Breeding-Stats für einen Dino"""
    if dino_name not in DINO_DATA:
        return None
    
    dino = DINO_DATA[dino_name]
    multipliers = get_multipliers()
    
    # Maturation Zeit mit Multiplier
    base_maturation = dino["maturation_time"]
    actual_maturation = base_maturation / multipliers["mature"]
    
    # Zeit bis Juvenile (10%)
    time_to_juvenile = actual_maturation * dino["juvenile_percent"]
    
    # Zeit bis Adult (100%)
    time_to_adult = actual_maturation
    
    # Futter-Berechnung
    # Baby phase = 0-10%
    baby_phase_time = time_to_juvenile
    baby_food = (dino["food_consumption"] * baby_phase_time) * weight
    
    # Juvenile phase = 10-100%
    juvenile_phase_time = time_to_adult - time_to_juvenile
    juvenile_food = (dino["food_consumption"] * juvenile_phase_time) * weight
    
    # Cuddle Interval
    cuddle_interval = dino["cuddle_interval"] * multipliers["cuddle_interval"]
    
    return {
        "dino_name": dino_name,
        "weight": weight,
        "food_type": dino["food_type"],
        "multipliers": multipliers,
        "time_to_juvenile": time_to_juvenile,
        "time_to_adult": time_to_adult,
        "baby_food": baby_food,
        "juvenile_food": juvenile_food,
        "total_food": baby_food + juvenile_food,
        "cuddle_interval": cuddle_interval,
        "cuddle_count": int(time_to_adult / cuddle_interval)
    }

def format_time(seconds):
    """Formatiert Sekunden zu lesbarer Zeit"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 24:
        days = hours // 24
        hours = hours % 24
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m {secs}s"

class DinoSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=name, emoji="🦖") 
            for name in sorted(DINO_DATA.keys())
        ]
        super().__init__(
            placeholder="Wähle einen Dino aus...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(WeightModal(self.values[0]))

class WeightModal(discord.ui.Modal, title="Dino Details"):
    def __init__(self, dino_name):
        super().__init__()
        self.dino_name = dino_name
        
        self.weight_input = discord.ui.TextInput(
            label="Gewicht des Baby Dinos",
            placeholder="z.B. 400",
            required=True,
            max_length=10
        )
        self.add_item(self.weight_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            weight = float(self.weight_input.value)
            
            # Berechne Stats
            stats = calculate_breeding(self.dino_name, weight)
            
            if not stats:
                await interaction.response.send_message(
                    "❌ Fehler beim Berechnen!", ephemeral=True
                )
                return
            
            # Erstelle Embed
            embed = discord.Embed(
                title=f"🦖 {stats['dino_name']} Breeding Calculator",
                description=f"**Event Status:** {stats['multipliers']['event_name']}\n"
                           f"**Multiplier:** {stats['multipliers']['mature']}x Mature, "
                           f"{stats['multipliers']['hatch']}x Hatch",
                color=discord.Color.green() if is_evo_weekend() else discord.Color.blue()
            )
            
            # Creature Details
            embed.add_field(
                name="📊 Creature Details",
                value=f"**Weight:** {weight}\n"
                      f"**Food Type:** {stats['food_type']}\n"
                      f"**Mature Multiplier:** {stats['multipliers']['mature']}x",
                inline=False
            )
            
            # Maturation
            embed.add_field(
                name="⏱️ Maturation Times",
                value=f"**Time to Juvenile:** {format_time(stats['time_to_juvenile'])}\n"
                      f"**Time to Adult:** {format_time(stats['time_to_adult'])}",
                inline=False
            )
            
            # Food Requirements
            embed.add_field(
                name="🍖 Food Requirements",
                value=f"**Food to Juvenile:** {int(stats['baby_food'])} {stats['food_type']}\n"
                      f"**Food to Adult:** {int(stats['juvenile_food'])} {stats['food_type']}\n"
                      f"**Total Food:** {int(stats['total_food'])} {stats['food_type']}",
                inline=False
            )
            
            # Imprinting
            embed.add_field(
                name="💕 Imprinting",
                value=f"**Cuddle Interval:** {format_time(stats['cuddle_interval'])}\n"
                      f"**Total Cuddles:** ~{stats['cuddle_count']}x\n"
                      f"**Imprint per Cuddle:** {stats['multipliers']['imprint_amount']}%",
                inline=False
            )
            
            embed.set_footer(text="Timer-Erinnerungen aktivieren? Klicke auf 🔔")
            
            # Timer Button
            view = TimerView(stats, interaction.user)
            
            await interaction.response.send_message(embed=embed, view=view)
            
        except ValueError:
            await interaction.response.send_message(
                "❌ Bitte gib eine gültige Zahl ein!", ephemeral=True
            )

class TimerView(View):
    def __init__(self, stats, user):
        super().__init__(timeout=None)
        self.stats = stats
        self.user = user
    
    @discord.ui.button(label="Timer aktivieren", emoji="🔔", style=discord.ButtonStyle.green)
    async def start_timer(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message(
                "❌ Das ist nicht dein Dino!", ephemeral=True
            )
            return
        
        # Speichere Timer
        user_id = interaction.user.id
        if user_id not in active_timers:
            active_timers[user_id] = []
        
        timer_data = {
            "stats": self.stats,
            "start_time": datetime.now(),
            "channel": interaction.channel
        }
        active_timers[user_id].append(timer_data)
        
        # Starte Timer Tasks
        asyncio.create_task(juvenile_timer(interaction, self.stats))
        asyncio.create_task(adult_timer(interaction, self.stats))
        asyncio.create_task(imprint_timer(interaction, self.stats, self.user))
        
        button.disabled = True
        button.label = "Timer läuft..."
        button.style = discord.ButtonStyle.gray
        
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(
            f"✅ Timer aktiviert! Du wirst benachrichtigt:\n"
            f"• In {format_time(self.stats['time_to_juvenile'])} (Juvenile)\n"
            f"• In {format_time(self.stats['time_to_adult'])} (Adult)\n"
            f"• Alle {format_time(self.stats['cuddle_interval'])} (Imprint)",
            ephemeral=True
        )

async def juvenile_timer(interaction, stats):
    """Timer für Juvenile Phase"""
    await asyncio.sleep(stats['time_to_juvenile'])
    
    embed = discord.Embed(
        title="🎯 Dein Dino ist jetzt Juvenile!",
        description=f"**{stats['dino_name']}** hat die Juvenile-Phase erreicht!",
        color=discord.Color.gold()
    )
    embed.add_field(
        name="⏱️ Noch bis Adult",
        value=format_time(stats['time_to_adult'] - stats['time_to_juvenile'])
    )
    
    await interaction.channel.send(
        content=interaction.user.mention,
        embed=embed
    )

async def adult_timer(interaction, stats):
    """Timer für Adult Phase"""
    await asyncio.sleep(stats['time_to_adult'])
    
    embed = discord.Embed(
        title="🎉 Dein Dino ist jetzt Adult!",
        description=f"**{stats['dino_name']}** ist vollständig ausgewachsen!",
        color=discord.Color.purple()
    )
    embed.add_field(
        name="📊 Stats",
        value=f"**Total Food verbraucht:** {int(stats['total_food'])} {stats['food_type']}\n"
              f"**Total Zeit:** {format_time(stats['time_to_adult'])}"
    )
    
    await interaction.channel.send(
        content=interaction.user.mention,
        embed=embed
    )

async def imprint_timer(interaction, stats, user):
    """Timer für Imprint Notifications - NUR für den jeweiligen Spieler sichtbar"""
    cuddle_count = 0
    max_cuddles = stats['cuddle_count']
    
    while cuddle_count < max_cuddles:
        await asyncio.sleep(stats['cuddle_interval'])
        cuddle_count += 1
        
        # Berechne aktuelle Imprint Progress
        current_imprint = cuddle_count * stats['multipliers']['imprint_amount']
        
        try:
            if current_imprint >= 100:
                # 100% Imprint - PRIVATE Nachricht
                embed = discord.Embed(
                    title="💯 100% Imprint erreicht!",
                    description=f"**{stats['dino_name']}** ist jetzt voll geimprintet!",
                    color=discord.Color.green()
                )
                await user.send(embed=embed)
            else:
                # Imprint benötigt - PRIVATE Nachricht
                embed = discord.Embed(
                    title="💕 Imprint Zeit!",
                    description=f"**{stats['dino_name']}** will gekuschelt werden!",
                    color=discord.Color.pink()
                )
                embed.add_field(
                    name="Progress",
                    value=f"**Cuddle #{cuddle_count}/{max_cuddles}**\n"
                          f"**Aktueller Imprint:** {min(current_imprint, 100)}%\n"
                          f"**Nächster Cuddle:** {format_time(stats['cuddle_interval'])}"
                )
                await user.send(embed=embed)
        except discord.Forbidden:
            # Falls User DMs deaktiviert hat, sende in Channel
            await interaction.channel.send(
                content=f"{user.mention} - Imprint Zeit! (Aktiviere DMs für private Benachrichtigungen)",
                embed=embed
            )

class DinoSelectView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(DinoSelect())

@tree.command(name="breeding", description="Berechne Breeding-Stats für deinen Dino")
async def breeding(interaction: discord.Interaction):
    """Hauptcommand für Breeding Calculator"""
    embed = discord.Embed(
        title="🦖 ARK Breeding Calculator",
        description="Wähle einen Dino aus dem Dropdown-Menü!",
        color=discord.Color.blue()
    )
    
    multipliers = get_multipliers()
    embed.add_field(
        name="📅 Aktueller Event Status",
        value=f"**{multipliers['event_name']}**\n"
              f"Hatch: {multipliers['hatch']}x | Mature: {multipliers['mature']}x\n"
              f"Cuddle Interval: {multipliers['cuddle_interval']}x | Imprint: {multipliers['imprint_amount']}x",
        inline=False
    )
    
    view = DinoSelectView()
    await interaction.response.send_message(embed=embed, view=view)

@tree.command(name="dinos", description="Liste aller verfügbaren Dinos")
async def dinos(interaction: discord.Interaction):
    """Zeigt alle verfügbaren Dinos"""
    dino_list = "\n".join([f"🦖 {name}" for name in sorted(DINO_DATA.keys())])
    
    embed = discord.Embed(
        title="📋 Verfügbare Dinos",
        description=dino_list,
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Total: {len(DINO_DATA)} Dinos")
    
    await interaction.response.send_message(embed=embed)

@tree.command(name="event", description="Zeigt den aktuellen Event-Status")
async def event(interaction: discord.Interaction):
    """Zeigt Event-Status und Multiplier"""
    multipliers = get_multipliers()
    
    embed = discord.Embed(
        title=f"{multipliers['event_name']}",
        description="ARK Small Tribes Server Multipliers",
        color=discord.Color.green() if is_evo_weekend() else discord.Color.blue()
    )
    
    embed.add_field(
        name="⚙️ Aktuelle Multipliers",
        value=f"**Egg Hatch Speed:** {multipliers['hatch']}x\n"
              f"**Baby Mature Speed:** {multipliers['mature']}x\n"
              f"**Cuddle Interval:** {multipliers['cuddle_interval']}x\n"
              f"**Imprint Amount:** {multipliers['imprint_amount']}x",
        inline=False
    )
    
    if is_evo_weekend():
        embed.add_field(
            name="🎉 EVO Event läuft!",
            value="Freitag 17:00 - Montag 21:00 ET\n"
                  "Doppelte Breeding-Rates!",
            inline=False
        )
    else:
        embed.add_field(
            name="📅 Weekday Rates",
            value="EVO Weekend startet:\n"
                  "**Freitag 17:00 ET** (23:00 Deutscher Zeit)",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed)

@tree.command(name="mytimers", description="Zeigt deine aktiven Breeding-Timer")
async def mytimers(interaction: discord.Interaction):
    """Zeigt alle aktiven Timer des Users"""
    user_id = interaction.user.id
    
    if user_id not in active_timers or not active_timers[user_id]:
        await interaction.response.send_message(
            "❌ Du hast keine aktiven Timer!\nNutze `/breeding` um einen Timer zu starten.",
            ephemeral=True
        )
        return
    
    embed = discord.Embed(
        title="⏰ Deine aktiven Breeding-Timer",
        description=f"Du hast **{len(active_timers[user_id])}** Timer aktiv",
        color=discord.Color.blue()
    )
    
    for i, timer in enumerate(active_timers[user_id], 1):
        stats = timer['stats']
        start_time = timer['start_time']
        elapsed = (datetime.now() - start_time).total_seconds()
        
        # Berechne verbleibende Zeit
        remaining_juvenile = max(0, stats['time_to_juvenile'] - elapsed)
        remaining_adult = max(0, stats['time_to_adult'] - elapsed)
        
        if remaining_adult > 0:
            status = "🟢 Läuft"
            time_left = f"Adult in: {format_time(remaining_adult)}"
            if remaining_juvenile > 0:
                time_left = f"Juvenile in: {format_time(remaining_juvenile)}"
        else:
            status = "✅ Fertig"
            time_left = "Dino ist Adult!"
        
        embed.add_field(
            name=f"#{i} - {stats['dino_name']} ({status})",
            value=f"**Gewicht:** {stats['weight']}\n"
                  f"**{time_left}**\n"
                  f"**Multiplier:** {stats['multipliers']['mature']}x",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot ist online als {client.user}")
    print(f"📊 {len(DINO_DATA)} Dinos verfügbar")
    print(f"🎮 In {len(client.guilds)} Servern aktiv")

# Bot starten
if __name__ == "__main__":
    # Token aus Umgebungsvariable (Railway) oder config.json lesen
    token = os.getenv("DISCORD_BOT_TOKEN")
    
    if not token:
        # Fallback: Aus config.json lesen (für lokales Testen)
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
                token = config.get("bot_token")
        except FileNotFoundError:
            print("❌ FEHLER: Weder DISCORD_BOT_TOKEN Umgebungsvariable noch config.json gefunden!")
            print("Bitte erstelle eine config.json oder setze die Umgebungsvariable.")
            exit(1)
    
    if not token or token == "DEIN_BOT_TOKEN_HIER":
        print("❌ FEHLER: Bot Token nicht gesetzt!")
        print("Railway: Setze die DISCORD_BOT_TOKEN Umgebungsvariable")
        print("Lokal: Trage den Token in config.json ein")
        exit(1)
    
    print("🚀 Starte Bot...")
    client.run(token)
