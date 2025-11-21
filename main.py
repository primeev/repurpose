import os
import random
import subprocess
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CommandHandler

TOKEN = os.environ.get("8508999864:AAHL1qmoQcNydfj3OrtvqXoSa-eZ9oksc3w")
bot = Bot(token=TOKEN)

app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0)

# ---------- FFmpeg Repurposing ----------
def repurpose_video(input_path, output_path):
    # Random light brightness change
    brightness = round(random.uniform(-0.05, 0.05), 3)

    # Random audio pitch change
    pitch = round(random.uniform(0.95, 1.05), 3)

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-vf", f"eq=brightness={brightness}",
        "-af", f"asetrate=44100*{pitch},aresample=44100",
        "-vcodec", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-metadata", "title=",
        "-metadata", "comment=",
        output_path
    ]

    subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# ---------- Handlers ----------
def start(update, context):
    update.message.reply_text("Send me a video and I’ll repurpose it like TikFusion 🔁")

def handle_video(update: Update, context):
    msg = update.message
    file = bot.getFile(msg.video.file_id)

    input_path = "input.mp4"
    output_path = f"out_{random.randint(1000,9999)}.mp4"

    file.download(input_path)

    msg.reply_text("Processing… 🔧 This can take a few seconds.")

    repurpose_video(input_path, output_path)

    bot.send_video(chat_id=msg.chat_id, video=open(output_path, "rb"))

    os.remove(input_path)
    os.remove(output_path)


# ---------- Bind handlers ----------
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.video, handle_video))


# ---------- Webhook endpoint ----------
@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"
