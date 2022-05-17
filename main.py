import discord
from discord.ext import commands
from discord.ext import tasks
import random

bot = commands.Bot("c.", case_insensitive=True)
prefix = ("c.")

@bot.event
async def on_ready():
    print(f'Bot {bot.user} logado com sucesso!')
    print(f"ID do bot: {bot.user.id}")
    channel = bot.get_channel(579794454244884514)
    await channel.send('OOOOOPPPPPPPAAAAAAAAAAAA FUI INICIADOOOOOOOOOOOOO')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} Você não tem permissões suficientes para utilizar este comando.')
        await ctx.message.delete()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'{ctx.author.mention} Este comando não existe em minha aplicação.')
        await ctx.message.delete()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "prefixo" in message.content.lower():
        await message.channel.send(f'Meu prefixo é **{prefix}**')

    if "ovo" in message.content.lower():
        await message.channel.send('PASSA A MÃO NO OVÃO DO COBRÃO VAI 🖐🥚')

    if "ulto?" in message.content.lower():
        sorteio = random.choice(['Sim', 'Não', 'será?', 'Você que escolhe!'])
        await message.channel.send(sorteio)

    await bot.process_commands(message)


@bot.command(name='ajuda') 
async def send_help(ctx):
    try:
        name = ctx.author.mention
        response = f'Comandos enviados no seu privado. {name}'
        mensagem_priv = (f'**Lista de comandos**\nc.help\n{prefix}sorteio [sorteios disponíveis: lol, valorant]\n{prefix}vavaarmas\nprefixo\nulto?')
        await ctx.send(response)
        await ctx.author.send(mensagem_priv)

    except discord.errors.Forbidden:
        await ctx.send('Não consigo te enviar os comandos na sua DM, habilite receber mensagens de qualquer pessoa do servidor (Opções > Privacidade)')

@bot.command(name='calcular')
async def calculate_expression(ctx, *expression):
    expression = "".join(expression)

    response = eval(expression)
    await ctx.send('A resposta é: ' + str(response))

@bot.command(nome='sorteio')
async def sorteio(ctx, tipo_sorteio):
    if tipo_sorteio == 'lol':
        name = ctx.author.mention

        response = f'{name}, {frase_sorteio()} {sorteio_lol()} {emoji_sorteio()}'
        await ctx.send(response)

    elif tipo_sorteio == 'valorant':
        name = ctx.author.mention

        response = f'{name}, {frase_sorteio()} {sorteio_vava()} {emoji_sorteio()}'
        await ctx.send(response)

    elif tipo_sorteio == 'armas':
        name = ctx.author.mention

        response = f'{name}, você irá jogar de {sorteio_vava_armas()} neste round.'
        await ctx.send(response)

    else:
        await ctx.send(f'Não existe nenhum sorteio de **{tipo_sorteio}.**\nConfira o comando **{prefix}ajuda** para ver os sorteios disponíveis.')

@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=0):
    try:
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'{amount} mensagens foram excluidas desse canal de texto.')
    except:
        await ctx.message.send('Você não tem permissão para utilizar esse comando.')
    
@bot.command(name='ping')
async def ping(ctx):
    await ctx.channel.send(f'Pong! {round(bot.latency * 1000)}ms')


def sorteio_lol(): 
    campeoes = ['Ahri', 'Akali', 'akshan', 'amumu','alistar', 'anivia', 'annie', 'aphelios', 'ashe', 'aurelion sol', 'aatrox', 'azir', 'bardo', 'blitzcrank', 'brand', 'braum', 'caitlyn', 'camille', 'cassiopeia', 'cho gath', 'corki', 'darius', 'diana', 'dr mundo', 'draven', 'ekko', 'elise', 'evelynn', 'ezreal', 'fiddle', 'galio', 'fiora', 'fizz', 'gangplank', 'garen', 'gnar', 'gragas', 'graves', 'gwen', 'hecarim', 'heimerdinger', 'illaoi', 'irelia', 'JANNA', 'jarvan', 'jax', 'jayce', 'jhin', 'jinx', 'kaisa', 'kalista', 'karma', 'karthus', 'kassadin', 'katarina', 'kayle', 'kayn', 'kennen', 'kha zix', 'kindred', 'kled', 'kog maw', 'le blanc', 'lee sin', 'leona', 'lilian', 'lissandra', 'lucian', 'lulu', 'lux', 'malphite', 'malzahar','maokai', 'master yi', 'miss fortune', 'mordekaiser', 'morgana', 'nami', 'nasus', 'nautilus', 'neeko', 'nidalee', 'nocturne', 'nunu e willump', 'olaf', 'orianna', 'ornn', 'pantheon', 'poppy', 'pyke', 'qiyana', 'quinn', 'rakan', 'ranmus', 'rek sai', 'rell', 'renata glasc', 'renekton', 'rengar', 'riven', 'rumble', 'ryze', 'samira', 'sejuani', 'senna', 'seraphine','sett', 'shaco', 'shen', 'shyvana','singed','sion', 'sivir ','skarner', 'sona', 'soraka', 'swain', 'sylas', 'syndra', 'tahm kench', 'taliyah', 'talon', 'taric', 'teemo', 'thresh', 'tristana', 'trundle', 'tryndamere', 'twisted fate', 'twitch', 'udyr', 'urgot', 'varus', 'vayne', 'veigar', 'vel koz', 'vex', 'VI', 'viego', 'viktor', 'vladmir', 'voliber', 'warwick', 'wukong', 'xayah', 'xerath', 'xin zhao', 'yasuo', 'yone','yorick', 'yuumi', 'zac', 'zed', 'zeri', 'ziggs', 'zilean', 'zoe', 'zyra']
    sorteio = random.choice(campeoes)
    return sorteio.capitalize()

def sorteio_vava():
    agentes = ['Brimstone', 'Phoenix', 'Sage', 'Neon', 'Sova', 'Viper', 'Chypher', 'Reyna','Killjoy', 'Breach', 'Omen', 'Jett', 'Raze', 'Skye', 'Yoru', 'Astra', 'Kay/o', 'Chamber', 'Fade', 'Omen']
    sorteio = random.choice(agentes)
    return sorteio.capitalize()

def sorteio_vava_armas():
    armas = ['Stinger', 'Spectre', 'Bucky', 'Judge', 'Bulldog', 'Guardian', 'Phantom', 'Vandal', 'Marshal', 'Operator', 'Ares', 'Odin', 'Classic', 'Shorty', 'Frenzy', 'Ghost', 'Sheriff']
    sorteio = random.choice(armas)
    return sorteio.capitalize()

def emoji_sorteio():
    emoji = ['🤣','😂','😄','😅','😆','😍','😎','😋','😯','😪','😫','🙄','😏','😣','😥','😮','😛','😌','😴','🥱','🤑','😲','😰','😱','😳','😵','🤬','😡','😠','👿','👿','😈','👹','👺','💩','💀','☠']
    emoji_sorteio = random.choice(emoji)
    return emoji_sorteio.capitalize()

def frase_sorteio():
    texto = ['Escolha', 'jogue de', 'vai jogar de', 'pegue', 'jogue com', ]
    frase = random.choice(texto)
    return frase.capitalize()




bot.run('OTc1MTI1ODg1Njg0NDMyOTg2.GTNQRd.QMlydps9uYSKoWWbhwOXooY3u_-543YmHvEKw8')
