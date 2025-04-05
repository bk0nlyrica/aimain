import requests
from twitchio.ext import commands

# إعدادات تويتش
BOT_NICK = 'not_bk0nlyrica'
TOKEN = 'oauth:n7v7rwxdzle2b9191j72wt3sql6l23'
PREFIX = '!'
CHANNEL = 'sodv_'

# إعدادات HuggingFace
HUGGINGFACE_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-alpha"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_TOKEN}"
}

def ask_gpt_like_bot(message_text):
    payload = {
        "inputs": f"<|user|> {message_text} <|assistant|>",
        "parameters": {
            "max_new_tokens": 80,    # تقييد عدد الكلمات المولدة ليتناسب مع 500 حرف
            "temperature": 0.7,
            "top_p": 0.95,
            "repetition_penalty": 1.1
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        try:
            output = response.json()[0]['generated_text']
            # تحديد رد مختصر لا يتعدى 500 حرف
            return output.split("<|assistant|>")[-1].strip()[:500]
        except:
            return "صار في مشكلة مع فهمي للرد 🤕"
    else:
        print("HuggingFace Error:", response.status_code, response.text)
        return "الذكاء الصناعي راح يتمشى شوي، جرب بعدين 😂"

class SmartBot(commands.Bot):

    def __init__(self):
        super().__init__(token=TOKEN, prefix=PREFIX, initial_channels=[CHANNEL])

    async def event_ready(self):
        print(f"✅ Logged in as {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return

        user_input = message.content.strip()
        print(f"{message.author.name}: {user_input}")

        # لا يرد إلا إذا تم منشنه (@اسم البوت)
        if BOT_NICK.lower() not in message.content.lower():
            return

        await message.channel.send("قاعد أفكر... 🤔")
        reply = ask_gpt_like_bot(user_input)
        await message.channel.send(f"@{message.author.name} {reply}")

bot = SmartBot()
bot.run()
