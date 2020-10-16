import discord
import asyncio
import re
from discord.ext import commands

Color_code_re = re.compile(r"^[0-9a-fA-F]{6}$")
Chr_list = ['\U0001f1e6', '\U0001f1e7']
Check_list = ['\U00002b55', '\U0000274c']


class Create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, ctx):
        # DBから取得
        all_channel_name = []  # すべてのチャンネル名
#         all_channel_pass = []  # すべてのパスワード
        all_channel_owner = []  # すべてのチャンネルオーナー
        # イベントループを取得
        loop = asyncio.get_event_loop()
        dm = await ctx.author.create_dm()
        # 既に作成済みの場合
        if ctx.author.id in all_channel_owner:
            await ctx.send('あなたははすでにチャンネルを作成しています。')
            return
        else:
            await dm.send("※テキストチャンネルで設定すると情報漏洩の原因となりますのでDMで設定します。\nご了承ください。\n**注意： 全ての入力は1分経過するとタイムアウトとなり、やり直しになります。\n事前に入力内容を決めておき、メモ帳に書いておく等することをお勧めします。**")

        # チャンネル名
        # 取得
        await dm.send("グローバルチャットチャンネルを設定します。\nまず追加したいグローバルチャンネル名を記入してください。\nなるべく被らないものにしてください。")

        def check1(m):
            return m.content and m.author == ctx.author and m.channel == dm
        try:
            cname = await self.bot.wait_for("message", timeout=60.0, check=check1)
        except asyncio.TimeoutError:
            await dm.send('タイムアウトしました。\nもう一度最初からお試しください。')
            return

        # 例外
        if cname.content in all_channel_name:
            await dm.send('既に作られているチャンネル名です。\nもう一度お試しください。')

            def checkA(m):
                return m.content and m.author == ctx.author and m.channel == dm
            try:
                cname = await self.bot.wait_for("message", timeout=60.0, check=checkA)
            except asyncio.TimeoutError:
                await dm.send('タイムアウトしました。\nもう一度最初からお試しください。')
                return
            if cname.content in all_channel_name:
                await dm.send('既に作られているチャンネル名です。\nもう一度最初からお試しください。')
                return

        # 出力
        await dm.send('チャンネル名を`' + cname.content + '`に設定します。')

        # レイアウト選択
        # 取得
        await dm.send('次はデザイン選択です。\n次の2つから一つ選んでください。\n埋め込みの色は設定出来ます。')
        msg = await dm.send(':regional_indicator_a:：ノーマル(Webhook)\n:regional_indicator_b:：埋め込み')
        await msg.add_reaction(Chr_list[0])
        await msg.add_reaction(Chr_list[1])

        def check2(r, u):
            if r.message.id != msg.id or u.bot:
                return False
            elif r.count <= 1 or r.emoji not in Chr_list:
                loop.create_task(r.message.remove_reaction(r.emoji, u))
                return False
            else:
                return True
        try:
            layout_type_react, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=check2)
        except asyncio.TimeoutError:
            await dm.send('タイムアウトしました。\nもう一度お試しください。')
            return

        # 色選択
        if layout_type_react.emoji == Chr_list[1]:
            # 取得
            await dm.send('次はカラー選択です。\nカラーコードを入力してください。\nカラーコードに#は不要です。')

            def checkB(m):
                return m.content and m.author == ctx.author and m.channel == dm and Color_code_re.match(m.content)
            try:
                color = await self.bot.wait_for("message", timeout=60.0, check=checkB)
            except asyncio.TimeoutError:
                await dm.send('タイムアウトしました。\nもう一度お試しください。')
                return
            layout = "埋め込み - #" + color.content.upper()
        # 出力
        else:
            layout = "ノーマル(Webhook)"

        await dm.send('レイアウトを`' + layout + '`\nに設定します')

        # 公開
        # 取得
        await dm.send('次に公開の設定をします。\nパスワードを設定すると参加するときにパスワードが必要になります。')
        await dm.send('まず、パスワードの有無を指定してください。')
        msg = await dm.send(':o:：設定する\n:x:：設定しない')
        await msg.add_reaction(Check_list[0])
        await msg.add_reaction(Check_list[1])

        def check3(r, u):
            if r.message.id != msg.id or u.bot:
                return False
            elif r.count <= 1 or r.emoji not in Check_list:
                loop.create_task(r.message.remove_reaction(r.emoji, u))
                return False
            else:
                return True
        try:
            need_pass, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=check3)
        except asyncio.TimeoutError:
            await dm.send('タイムアウトしました。\nもう一度お試しください。')
            return

        # パスワード設定
        if need_pass.emoji == Check_list[0]:
            # 取得
            await dm.send('パスワードを設定します。\n被りにくいものにしてください。')

            def check4(m):
                return m.content and m.author == ctx.author and m.channel == dm
            try:
                password = await self.bot.wait_for("message", timeout=60.0, check=check4)
            except asyncio.TimeoutError:
                await dm.send('タイムアウトしました。\nもう一度お試しください。')
                return

#             # 例外
#             if password.content in all_channel_pass:
#                 # 取得
#                 await dm.send('文字数が範囲外か、既に使われているパスワードです。\nもう一度お試しください。')
#
#                 def checkC(m):
#                     return m.content and m.author == ctx.author and m.channel == dm
#                 try:
#                     password = await self.bot.wait_for("message", timeout=60.0, check=checkC)
#                 except asyncio.TimeoutError:
#                     await dm.send('タイムアウトしました。\nもう一度最初からお試しください。')
#                     return
#
#                 # 例外
#                 if password.content in all_channel_pass:
#                     await dm.send('文字数が範囲外か、既に使われているパスワードです。\nもう一度最初からお試しください。')
#                     return
#                 else:
#                     password = password.content
#             else:
            password = password.content

        # パスワードなし
        else:
            password = "(なし)"

        # 出力
        await dm.send('パスワードを`' + password + '`に設定します。')

        # 確認
        # 取得
        await dm.send('最終確認です。')
        embed = discord.Embed(title='ユーザー名：' + str(ctx.author),
                              description=f"チャンネル名： `{cname.content}`\nレイアウト： `{layout}`\nパスワード：`{password}`", color=discord.Colour.from_rgb(255, 255, 255))
        await dm.send(embed=embed)
        msg = await dm.send('上記でよろしいでしょうか？\n:o:を選択した場合、利用規約に同意したものとみなします。\n:o:：はい、利用規約に同意します。\n:x:：いいえ')
        await msg.add_reaction(Check_list[0])
        await msg.add_reaction(Check_list[1])

        def check5(r, u):
            if r.message.id != msg.id or u.bot:
                return False
            elif r.count <= 1 or r.emoji not in Check_list:
                loop.create_task(r.message.remove_reaction(r.emoji, u))
                return False
            else:
                return True
        try:
            agree, _ = await self.bot.wait_for("reaction_add", check=check5)
        except asyncio.TimeoutError:
            await dm.send('タイムアウトしました。\nもう一度最初からお試しください。')
            return
        # 同意
        if not agree.emoji == Check_list[0]:
            await dm.send('お手数ですがもう一度最初からお試しください。')
            return
        await dm.send('設定完了しました。')
        # ~~~~~~~~ここに色々最終処理~~~~~~~~~


def setup(bot):
    bot.add_cog(Create(bot))
