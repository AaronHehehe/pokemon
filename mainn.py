import discord
from discord.ext import commands
from config import token
from logic import Pokemon

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# 🐣 Create Pokémon
@bot.command()
async def go(ctx):
    author = ctx.author.name

    if author not in Pokemon.pokemons:
        pokemon = Pokemon(author)
        await ctx.send(await pokemon.info())

        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed()
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
    else:
        await ctx.send("❗ Kamu sudah punya Pokémon!")

# ℹ️ Pokémon info
@bot.command()
async def pokemon(ctx):
    author = ctx.author.name

    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        await ctx.send(await pokemon.info())
    else:
        await ctx.send("❗ Kamu belum punya Pokémon. Gunakan `!go`")

# 🍖 Feed Pokémon
@bot.command()
async def feed(ctx):
    author = ctx.author.name

    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        exp, level_up = pokemon.feed()

        msg = f"🍖 Pokémon diberi makan! +{exp} EXP"
        if level_up:
            msg += f"\n🎉 Pokémon naik ke level {pokemon.level}!"

        await ctx.send(msg)
    else:
        await ctx.send("❗ Kamu belum punya Pokémon. Gunakan `!go`")

# 🖼️ Show Pokémon Image
@bot.command()
async def img(ctx):
    author = ctx.author.name

    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        image_url = await pokemon.show_img()

        if image_url:
            embed = discord.Embed()
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Gagal memuat gambar Pokémon.")
    else:
        await ctx.send("❗ Kamu belum punya Pokémon. Gunakan `!go`")

@bot.command()
async def info(ctx):
        # 2. Periksa apakah pengguna punya Pokémon
        if ctx.author.name in Pokemon.pokemons:
            # 3. Ambil Pokémon dari dictionary
            pok = Pokemon.pokemons[ctx.author.name]

            # 4. Kirim info Pokémon ke chat
            pokemon_info = await pok.info()
            await ctx.send(pokemon_info)
        else:
            # Jika pengguna belum punya Pokémon
            await ctx.send("Kamu belum punya Pokémon. Gunakan perintah lain untuk mendapatkannya!")


# Run bot
bot.run(token)
