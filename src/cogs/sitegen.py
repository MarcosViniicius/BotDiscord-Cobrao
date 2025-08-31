"""
Cog para geração e gerenciamento de sites via IA
"""
import discord
from discord.ext import commands
import os
import uuid
import re
from openai import OpenAI
from config.settings import OPENAI_API_KEY, EMBED_COLORS

SITES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../sites'))

class SiteGen(commands.Cog):
    @commands.command(name='listarsites')
    async def listar_sites(self, ctx):
        """Lista todos os sites hospedados pelo bot"""
        sites = [f for f in os.listdir(SITES_DIR) if f.startswith('site_') and f.endswith('.html')]
        if not sites:
            embed = discord.Embed(
                title="🌐 Nenhum site hospedado",
                description="Ainda não há sites criados.",
                color=EMBED_COLORS['info']
            )
            await ctx.send(embed=embed)
            return
        ip_publico = 'localhost'
        try:
            import requests
            ip_publico = requests.get('https://api.ipify.org').text
        except Exception:
            pass
        links = [f"http://{ip_publico}:8000/site_{f[5:-5]}" for f in sites]
        desc = '\n'.join(links)
        embed = discord.Embed(
            title="🌐 Sites Hospedados",
            description=desc,
            color=EMBED_COLORS['success']
        )
        await ctx.send(embed=embed)
    def start_webserver(self):
        import threading
        import subprocess
        def run():
            subprocess.Popen(['python', os.path.join(os.path.dirname(__file__), '../webserver.py')])
        t = threading.Thread(target=run, daemon=True)
        t.start()
    def __init__(self, bot):
        self.bot = bot
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        if not os.path.exists(SITES_DIR):
            os.makedirs(SITES_DIR)
        self.start_webserver()

    @commands.command(name='criarsite')
    async def criar_site(self, ctx, *, pedido: str = None):
        """Gera um site com base no pedido do usuário e hospeda na porta 80"""
        # Limitações de segurança
        if not pedido or len(pedido.strip()) < 10:
            embed = discord.Embed(
                title="❌ Pedido Inválido",
                description="Forneça uma descrição detalhada (mínimo 10 caracteres) para o site. Exemplo: c.criarsite site de receitas de bolo",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return
        pedido_lower = pedido.lower()
        palavras_bloqueadas = ["proxy", "vpn", "ssh", "ftp", "root", "admin", "servidor", "porta", "socket", "exec", "bash", "powershell", "cmd", "python", "subprocess", "os.system", "delete", "remove", "shutdown", "kill", "firewall", "vps", "cloud", "database", "sql", "mysql", "postgres", "mongo", "upload", "download", "file", "system", "windows", "linux", "unix", "criar servidor", "abrir porta", "alterar porta", "excluir arquivo", "remover arquivo", "formatar", "destruir", "hack", "exploit", "malware", "virus", "trojan", "ransomware"]
        if any(p in pedido_lower for p in palavras_bloqueadas):
            embed = discord.Embed(
                title="🚫 Pedido Bloqueado",
                description="Seu pedido contém termos proibidos para segurança da VPS.",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return
        if len(pedido) > 300:
            embed = discord.Embed(
                title="❌ Pedido Muito Longo",
                description="O pedido deve ter no máximo 300 caracteres.",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="🌐 Gerando site...",
            description=f"Pedido: `{pedido[:200]}`\nAguarde alguns segundos...",
            color=EMBED_COLORS['info']
        )
        msg = await ctx.send(embed=embed)

        try:
            # Gera o código HTML/CSS/JS via IA (usando GPT-5, site moderno e avançado)
            prompt = (
                f"Crie um website avançado e moderno em HTML, CSS e JS conforme o pedido: {pedido}.\n"
                "Visual impactante: gradientes, sombras, tipografia elegante, paletas de cores vibrantes, efeitos visuais avançados.\n"
                "Design moderno: layout com grid/flexbox, animações CSS complexas (parallax, transições suaves, hover effects), responsivo (mobile-first, tablet, desktop).\n"
                "Funcionalidades avançadas: menu de navegação sticky com dropdowns, carrosséis de imagens, accordions, modais, tooltips, sliders interativos.\n"
                "Interações JS: validação de formulários em tempo real, animações on-scroll, efeitos de loading, feedback visual dinâmico, manipulação de DOM.\n"
                "Estrutura: pelo menos 4 seções principais (header, hero, conteúdo, footer), navegação intuitiva, call-to-actions proeminentes.\n"
                "Acessibilidade: contraste alto, navegação por teclado, alt text, estrutura semântica, foco visível.\n"
                "UX premium: micro-interações, feedback imediato, formulários com validação avançada, mensagens de sucesso/erro.\n"
                "Requisitos técnicos: arquivo único HTML autocontido, CSS em <style> no head, JS em <script> no final do body, código limpo, bem indentado e otimizado.\n"
                "Não use markdown, bibliotecas externas, backend ou scripts inseguros. Apenas o código HTML final puro."
            )
            import asyncio
            def gerar_site():
                try:
                    resp = self.openai_client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": prompt}],
                        max_completion_tokens=2048
                    )
                    return resp.choices[0].message.content
                except Exception as e:
                    print(f"[ERROR] {e}")
                    return ""
            site_code = await asyncio.to_thread(gerar_site)
            site_id = str(uuid.uuid4())[:8]
            site_path = os.path.join(SITES_DIR, f"site_{site_id}.html")
            if not site_code or len(site_code.strip()) < 10:
                site_code = "<html><body><h1>Erro ao gerar site via IA</h1><p>Tente novamente mais tarde ou ajuste o pedido.</p></body></html>"
            # Remove blocos markdown do início/fim
            for bloco in ["```html", "```css", "```js", "```", "\n```", "\r```"]:
                site_code = site_code.replace(bloco, "")
            site_code = site_code.strip()
            # Extrair apenas o HTML válido
            html_match = re.search(r'<!DOCTYPE html>.*?</html>', site_code, re.DOTALL | re.IGNORECASE)
            if html_match:
                site_code = html_match.group(0)
            else:
                site_code = "<html><body><h1>Erro: HTML inválido gerado</h1></body></html>"
            with open(site_path, "w", encoding="utf-8") as f:
                f.write(site_code)
            print(f"DEBUG: Site salvo em {site_path}")


            # Descobre o IP público da máquina
            import requests
            try:
                ip_publico = requests.get('https://api.ipify.org').text
            except Exception:
                ip_publico = 'IP não detectado'
            # O site será servido pelo servidor Flask único (src/webserver.py)

            link_site = f"http://{ip_publico}:8000/site_{site_id}"
            embed = discord.Embed(
                title="✅ Site Gerado!",
                description=(
                    f"IP público: `{ip_publico}`\n"
                    f"Link do site: {link_site}\n"
                    f"Use `c.excluirsite {site_id}` para remover.\n"
                    f"Acesse / para ver todos os sites disponíveis."
                ),
                color=EMBED_COLORS['success']
            )
            await msg.edit(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Erro na Geração",
                description=f"Erro ao gerar site: {str(e)[:200]}",
                color=EMBED_COLORS['error']
            )
            await msg.edit(embed=embed)

    @commands.command(name='excluirsite')
    async def excluir_site(self, ctx, site_id: str = None):
        """Exclui um site gerado pelo comando criarsite"""
        if not site_id:
            embed = discord.Embed(
                title="❌ ID Inválido",
                description="Forneça o ID do site para excluir. Exemplo: c.excluirsite abc12345",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return
        site_path = os.path.join(SITES_DIR, f"site_{site_id}.html")
        if os.path.exists(site_path):
            os.remove(site_path)
            embed = discord.Embed(
                title="🗑️ Site Excluído",
                description=f"Site `{site_id}` removido com sucesso!",
                color=EMBED_COLORS['success']
            )
        else:
            embed = discord.Embed(
                title="❌ Site Não Encontrado",
                description=f"Nenhum site com ID `{site_id}` encontrado.",
                color=EMBED_COLORS['error']
            )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SiteGen(bot))
