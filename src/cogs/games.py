"""
Cog de sorteios e jogos
"""
from discord.ext import commands
import random

class Sorteio(commands.Cog):
    """Comandos de sorteio para jogos"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='sorteio', help='Sorteio de jogos. Opções: lol, valorant, armas')
    async def sorteio(self, ctx, tipo_sorteio=None):
        if not tipo_sorteio:
            await ctx.channel.send("Escolha um tipo de sorteio: **lol**, **valorant** ou **armas**\nExemplo: `c.sorteio lol`")
            return
            
        name = ctx.author.mention
        
        if tipo_sorteio.lower() == 'lol':
            response = f'{name}, {self._frase_sorteio()} {self._sorteio_lol()} {self._emoji_sorteio()}'
        elif tipo_sorteio.lower() == 'valorant':
            response = f'{name}, {self._frase_sorteio()} {self._sorteio_valorant()} {self._emoji_sorteio()}'
        elif tipo_sorteio.lower() == 'armas':
            response = f'{name}, você irá jogar de {self._sorteio_armas_valorant()} neste round.'
        else:
            response = f'Não existe sorteio de **{tipo_sorteio}**.\nOpções disponíveis: **lol**, **valorant**, **armas**'

        await ctx.channel.send(response)

    def _sorteio_lol(self): 
        """Sorteia um campeão do League of Legends"""
        campeoes = [
            'Ahri', 'Akali', 'Akshan', 'Amumu', 'Alistar', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 
            'Aurelion Sol', 'Aatrox', 'Azir', 'Bardo', 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 
            'Camille', 'Cassiopeia', 'Cho Gath', 'Corki', 'Darius', 'Diana', 'Dr Mundo', 'Draven', 
            'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'Fiddlesticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 
            'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 
            'Janna', 'Jarvan IV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'Kai Sa', 'Kalista', 'Karma', 'Karthus', 
            'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Kha Zix', 'Kindred', 'Kled', 'Kog Maw', 
            'LeBlanc', 'Lee Sin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 
            'Malzahar', 'Maokai', 'Master Yi', 'Miss Fortune', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 
            'Nautilus', 'Neeko', 'Nidalee', 'Nocturne', 'Nunu', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 
            'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', 'Rek Sai', 'Rell', 'Renata Glasc', 
            'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 
            'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 
            'Swain', 'Sylas', 'Syndra', 'Tahm Kench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 
            'Tristana', 'Trundle', 'Tryndamere', 'Twisted Fate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 
            'Vayne', 'Veigar', 'Vel Koz', 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 
            'Warwick', 'Wukong', 'Xayah', 'Xerath', 'Xin Zhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 
            'Zac', 'Zed', 'Zeri', 'Ziggs', 'Zilean', 'Zoe', 'Zyra'
        ]
        return random.choice(campeoes)

    def _sorteio_valorant(self):
        """Sorteia um agente do Valorant"""
        agentes = [
            'Brimstone', 'Phoenix', 'Sage', 'Neon', 'Sova', 'Viper', 'Cypher', 'Reyna',
            'Killjoy', 'Breach', 'Omen', 'Jett', 'Raze', 'Skye', 'Yoru', 'Astra', 
            'Kay/O', 'Chamber', 'Fade', 'Harbor', 'Gekko', 'Deadlock', 'Iso', 'Clove'
        ]
        return random.choice(agentes)

    def _sorteio_armas_valorant(self):
        """Sorteia uma arma do Valorant"""
        armas = [
            'Stinger', 'Spectre', 'Bucky', 'Judge', 'Bulldog', 'Guardian', 
            'Phantom', 'Vandal', 'Marshal', 'Operator', 'Ares', 'Odin', 
            'Classic', 'Shorty', 'Frenzy', 'Ghost', 'Sheriff'
        ]
        return random.choice(armas)

    def _emoji_sorteio(self):
        """Retorna um emoji aleatório"""
        emojis = [
            '🤣', '😂', '😄', '😅', '😆', '😍', '😎', '😋', '😯', '😪',
            '😫', '🙄', '😏', '😣', '😥', '😮', '😛', '😌', '😴', '🥱',
            '🤑', '😲', '😰', '😱', '😳', '😵', '🤬', '😡', '😠', '👿',
            '😈', '👹', '👺', '💩', '💀', '☠'
        ]
        return random.choice(emojis)

    def _frase_sorteio(self):
        """Retorna uma frase de sorteio"""
        frases = ['escolha', 'jogue de', 'vai jogar de', 'pegue', 'jogue com']
        return random.choice(frases).capitalize()

async def setup(bot):
    print("🔧 Carregando Sorteio...")
    await bot.add_cog(Sorteio(bot))
    print("✅ Sorteio carregado com sucesso!")