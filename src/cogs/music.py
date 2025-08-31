import discord
from discord.ext import commands
import yt_dlp
import asyncio

# Suppress noise about console usage from errors
yt_dlp.utils.bug_reports_message = lambda *args, **kwargs: ''

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}

    def get_queue(self, ctx):
        if ctx.guild.id not in self.queues:
            self.queues[ctx.guild.id] = []
        return self.queues[ctx.guild.id]

    def play_next(self, ctx):
        queue = self.get_queue(ctx)
        if len(queue) > 0:
            source = queue.pop(0)
            ctx.voice_client.play(source, after=lambda e: self.play_next(ctx))
            asyncio.run_coroutine_threadsafe(ctx.send(f'Tocando agora: {source.title}'), self.bot.loop)

    @commands.command(name='join')
    async def join(self, ctx):
        """Entra no canal de voz do usuário."""
        if not ctx.author.voice:
            return await ctx.send("Você não está em um canal de voz.")
        
        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        
        await channel.connect()

    @commands.command(name='leave')
    async def leave(self, ctx):
        """Sai do canal de voz."""
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

    @commands.command(name='play')
    async def play(self, ctx, *, url: str = None):
        """Toca uma música do YouTube ou a adiciona na fila."""
        if not url:
            return await ctx.send("Por favor, insira o nome ou URL da música que você quer tocar. Ex: `c.play never gonna give you up`")

        if not ctx.voice_client:
            await ctx.invoke(self.join)

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            queue = self.get_queue(ctx)
            
            if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                queue.append(player)
                await ctx.send(f'Adicionado à fila: {player.title}')
            else:
                ctx.voice_client.play(player, after=lambda e: self.play_next(ctx))
                await ctx.send(f'Tocando agora: {player.title}')

    @commands.command(name='queue')
    async def queue(self, ctx):
        """Mostra a fila de músicas."""
        queue = self.get_queue(ctx)
        if len(queue) == 0:
            return await ctx.send("A fila está vazia.")

        embed = discord.Embed(title="Fila de Músicas", color=0x00ff00)
        for i, source in enumerate(queue):
            embed.add_field(name=f"{i+1}. {source.title}", value=f"URL: [Click here]({source.url})", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='stop')
    async def stop(self, ctx):
        """Para a música e limpa a fila."""
        if ctx.voice_client:
            ctx.voice_client.stop()
            self.queues[ctx.guild.id] = []
            await ctx.send("Música parada e fila limpa.")

    @commands.command(name='skip')
    async def skip(self, ctx):
        """Pula a música atual."""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Música pulada.")

    @commands.command(name='pause')
    async def pause(self, ctx):
        """Pausa a música atual."""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Música pausada.")

    @commands.command(name='resume')
    async def resume(self, ctx):
        """Continua a música pausada."""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Música retomada.")

    @commands.command(name='np', aliases=['nowplaying'])
    async def now_playing(self, ctx):
        """Mostra a música que está tocando."""
        if ctx.voice_client and ctx.voice_client.source:
            await ctx.send(f"Tocando agora: {ctx.voice_client.source.title}")
        else:
            await ctx.send("Não estou tocando nada no momento.")

async def setup(bot):
    await bot.add_cog(Music(bot))
