import os, logging, random, subprocess
from pyrogram import filters
from pytube import YouTube
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from client import Client

app = Client()


@app.on_message(filters.user(app.katsu) & filters.command(["link"]))
def import_link(app, msg):
    text = msg.text.split("\n")
    db = app.load()
    for i in range(len(text) - 1):
        if "youtu" in text[i]:
            db["unsent"].append({"link": text[i], "tags": text[i + 1]})
            app.dump(db)

            txt = f" Acqiured link: {text[i]}\nwith tags: {text[i + 1]}"
            msg.reply(
                txt,
                disable_web_page_preview=True,
                disable_notification=True,
            )
            logging.warning(txt)


@app.on_message(filters.user(app.katsu) & filters.command(["send_links"]))
def send_links(app, msg):
    msg.reply_document(f"{os.getcwd()}/{app.db}")
    logging.warning("Sent links to user")


@app.on_message(filters.user(app.katsu) & filters.command(["make_job"]))
def send_links(_, msg):
    text = " Manually send post to channel."
    msg.reply(text)
    logging.warning(text)
    send_asmr()


def download_audio(link, tags):
    vid = YouTube(link)
    path = vid.streams.filter(only_audio=True, file_extension="mp4").last().download()
    text = f"<a href='{link}'>{vid.title}</a>\n{tags}\n{vid.author}\n\n@katsu_asmr"
    logging.info(f" down video {vid.title} from {vid.author}")

    return path, text, vid.title, vid.author


add_quotes = lambda x: x.replace("/", '"/"')[1:] + '"'
rm_quotes = lambda x: x.replace('"', "")


def format_audio(mp4):
    mp4 = add_quotes(mp4)
    mp3 = mp4.replace(".mp4", ".mp3")

    ffmpeg = f"ffmpeg -i {mp4} {mp3}"
    subprocess.call(ffmpeg, shell=True)

    os.remove(rm_quotes(mp4))
    return rm_quotes(mp3)


def send_asmr():
    db = app.load()
    unsent = db["unsent"]
    try:
        random.shuffle(unsent)
        audio = unsent.pop()
        path, text, title, author = download_audio(audio["link"], audio["tags"])
        audio["title"] = title
        audio["author"] = author

        path = format_audio(path)

        app.send_audio(chat_id=app.working_chat, caption=text, audio=path)

        os.remove(path)
        db["sent"].append(audio)
    except IndexError as e:
        print(e)
    finally:
        db["unsent"] = unsent
        app.dump(db)


def scheduler_start():
    aps = AsyncIOScheduler()
    aps.add_job(send_asmr, "interval", hours=3, id="send_asmr")
    aps.start()


if __name__ == "__main__":
    scheduler_start()
    app.run()
