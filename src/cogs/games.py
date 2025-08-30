from discord.ext import commands
import random

class Sorteio(commands.Cog):
    """Work with sorted champion"""


    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='sorteio', help='sorteio de jogos. [sorteios disponíveis: lol, valorant, armas(valorant)]')
    async def sorteio(self, ctx, tipo_sorteio):
        if tipo_sorteio == 'lol':
            name = ctx.author.mention

            response = f'{name}, {frase_sorteio()} {sorteio_lol()} {emoji_sorteio()}'
            await ctx.channel.send(response)

        elif tipo_sorteio == 'valorant':
            name = ctx.author.mention

            response = f'{name}, {frase_sorteio()} {sorteio_vava()} {emoji_sorteio()}'
            await ctx.channel.send(response)

        elif tipo_sorteio == 'armas':
            name = ctx.author.mention

            response = f'{name}, você irá jogar de {sorteio_vava_armas()} neste round.'
            await ctx.channel.send(response)

        else:
            await ctx.channel.send(f'Não existe nenhum sorteio de **{tipo_sorteio}.**\nConfira o comando **c.ajuda** para ver os sorteios disponíveis.')


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

async def setup(bot):
    print("🔧 Carregando Sorteio...")
    await bot.add_cog(Sorteio(bot))
    print("✅ Sorteio carregado com sucesso!")