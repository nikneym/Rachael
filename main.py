#python randrange
from random import randrange

#discord api call
import discord
from discord.ext import commands
from discord import Spotify

#sox ve google speech api call
import sox
from google_speech import Speech

#beautiful soup ve req call
import re
import requests
from bs4 import BeautifulSoup 

#kitapyurdu scrapper
#steam scrapper
from kitapyurdu import kitapyurdu_query
from steam import steam_query

token = "INSERT_YOURS_HERE!"

bot = commands.Bot(
	command_prefix = ">",
	intents = discord.Intents.all()
)

@bot.event
async def on_ready():
	await bot.change_presence(status = discord.Status.idle)
	print("Rachael hizmetinizde!")
pass

@bot.event
async def on_message(message):
	if "dog" in message.content:
		await message.author.send("**bu dili bi ömer konuşur bilader**")
	pass

	await bot.process_commands(message)
pass

@bot.command(name = "help_screen")
async def help_screen(ctx):
	await ctx.send(f"""
**>np** yazarak dinlemekte olduğun parçayı bizimle paylaşabilirsin.

**>say** yazıp mesajını eklediğinde, ben de mesajını tekrarlarım.
*#Örnek: >say Nabersin bakalım?*

**>join** yazarak beni bulunduğun kanala çağırabilirsin.
**>quit** yazdığında yanından ayrılırım...

**>tell** yazıp istediğin cümleyi eklediğinde, onu senin için okuyabilirim!
*#Örnek: >tell Merhaba Dünya!*

**>book** yazıp istediğin kitap, yazar ya da yayıncıyı eklediğinde, kitapyurdu üzerinden istediğin kitabı arayabilirim!
*Örnek: >book Frank Herbert*

**>steam** yazarak şu an steam'de en çok satan oyunlara ulaşabilirsin!

Şimdilik bu kadar!
*nikneym tarafından geliştirilmiştir.*""")
pass

@bot.command(name = "np")
async def get_spotify_song(ctx):
	user = ctx.author
	#user.name.lower()

	sentences = [
		f"{user.name} öyle güzel parçalar dinliyor ki... haydi sen de!",
		f"{user.name} bu nasıl bir müzik zevkidir??",
		f"müzik paylaştıkça güzeldir, en azından {user.name} öyle düşünüyor.",
		f"haydi {user.name} ile birlikte söyle!",
		f"müzik gurmeliği denince akla {user.name} gelir...",
		f"hitleri her zaman {user.name} belirler!",
		f"{user.name} bu şarkıyı mı dinliyon aq",
		f"bi serdar gapılar değil, ama idare eder..."
	]

	for act in user.activities:
		if isinstance(act, Spotify):
			await bot.get_channel(787661130293837854).send(sentences[randrange(len(sentences))] + "\n https://open.spotify.com/track/" + act.track_id)
		pass
	pass
pass

@bot.command(name = "join")
async def join_voice_channel(ctx):
	channel = ctx.author.voice.channel
	await channel.connect()
pass

@bot.command(name = "quit")
async def quit_voice_channel(ctx):
	await ctx.voice_client.disconnect()
pass

@bot.command(name = "tell")
async def speak_voice_channel(ctx, *, arg):
	voice_channel = ctx.voice_client

	speech = Speech(arg, "tr")
	save_speech = speech.save("deneme.mp3")
	#speech.play()
	
	voice_channel.play(discord.FFmpegPCMAudio("deneme.mp3"), after=lambda e: print('done', e))
pass

@bot.command(name = "say")
async def say_something(ctx, *, arg):
	words = ["halil", "alil", "ha-lil", "hlil", "halo", "h-a-l-i-l"]

	for word in words:
		if word in arg:
			await ctx.send("kimse ona adıyla hitap edemez ulen")

			return
		pass
	pass

	await ctx.send(arg)
pass

@bot.command(name = "book")
async def kitapyurdu_scrapper(ctx, *, arg):
	for product_item in kitapyurdu_query(arg):
		#get name
		product_name = product_item.find("div", class_ = "name").get_text()

		#get price
		price_div = product_item.find("div", class_ = "price").get_text()
		temp = re.findall(r'\d+', price_div)
		kitapyurdu_price = list(map(int, temp))
		price = None
		try:
			price = kitapyurdu_price[2]
		except IndexError:
			price = kitapyurdu_price[0]
		pass

		#get publisher
		publisher_div  = product_item.find("div", class_ = "publisher")
		publisher_name = publisher_div.find("a").get_text().upper()

		#get image
		image_link = product_item.find("a", class_ = "pr-img-link")
		image = image_link.find("img")

		#urllib.request.urlretrieve(image["src"], product_name + ".jpg")

		embed = discord.Embed(title = product_name, color = 0xe67e22)
		embed.add_field(name = "Yayıncı", value = publisher_name)
		embed.add_field(name = "Fiyat", value = "₺" + str(price))
		embed.set_thumbnail(url = image["src"])
		await ctx.send(embed = embed)
	pass
pass

@bot.command(name = "steam")
async def steam_scrapper(ctx):
	query = "https://store.steampowered.com/specials#tab=TopSellers"

	for item in steam_query(query):
		item_name  = item.find("div", class_ = "tab_item_name").get_text()
		item_img   = item.find("img", class_ = "tab_item_cap_img")["src"]
		item_price = item.find("div", class_ = "discount_final_price").get_text()
		item_tag   = item.find("div", class_ = "tab_item_top_tags").get_text()

		embed = discord.Embed(title = item_name, color = 0xe67e22)
		embed.add_field(name = "Etiketler", value = item_tag)
		embed.add_field(name = "Fiyat", value = item_price)
		embed.set_thumbnail(url = item_img)

		await ctx.send(embed = embed)
	pass
pass

bot.run(token)