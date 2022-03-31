import os, logging, random, subprocess
from pyrogram import filters
from pytube import YouTube
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from client import Client

app = Client()


@app.on_message(filters.user(app.working_chat) & filters.command(["link"]))
async def import_link(app, msg):
    text = msg.text.split("\n")
    db = app.load()
    for i in range(len(text) - 1):
        if "youtu" in text[i]:
            db["unsent"].append({"link": text[i], "tags": text[i + 1]})
            app.dump(db)

            logging.warning(f" added link {text[i]}")


@app.on_message(filters.user(app.working_chat) & filters.command(["send_links"]))
async def send_links(app, msg):
    await msg.reply_document(f"{os.getcwd()}/{app.db}")
    logging.warning("sent links to user")


def download_audio(link, tags):
    vid = YouTube(link)
    path = vid.streams.filter(only_audio=True, file_extension="mp4").last().download()
    text = f"<a href='{link}'>{vid.title}</a>\n{tags}\n{vid.author}\n\n@katsu_asmr"
    logging.info(f" down video {vid.title} from {vid.author}")

    return path, text


def format_audio(mp4):
    mp4 = mp4.replace("/", '"/"')[1:] + '"'
    mp3 = mp4.replace(".mp4", ".mp3")

    ffmpeg = f"ffmpeg -i {mp4} {mp3}"
    subprocess.call(ffmpeg, shell=True)

    mp3 = mp3.replace('"', "")
    mp4 = mp4.replace('"', "")
    os.remove(mp4)
    return mp3


def send_audio():
    db = app.load()
    unsent = db["unsent"]
    try:
        random.shuffle(unsent)
        audio = unsent.pop()
        path, text = download_audio(audio["link"], audio["tags"])
        path = format_audio(path)

        app.send_audio(chat_id=app.working_chat, caption=text, audio=path)

        os.remove(path)
    except IndexError as e:
        print(e)
    finally:
        db["sent"].append(audio)
        db["unsent"] = unsent
        app.dump(db)


def scheduler_start():
    aps = AsyncIOScheduler()
    aps.add_job(send_audio, "interval", hours=3)
    aps.start()


if __name__ == "__main__":
    scheduler_start()
    app.run()
