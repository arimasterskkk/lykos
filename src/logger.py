import datetime
import time

from src import config

def logger(file, write=True, display=True):
    if file is not None:
        open(file, "a").close() # create the file if it doesn't exist
    def log(*output, write=write, display=display):
        output = " ".join([str(x) for x in output]).replace("\u0002", "").replace("\\x02", "") # remove bold
        if config.Main.get("debug.enabled"):
            write = True
            display = True
        timestamp = get_timestamp()
        if display:
            print(timestamp + output, file=utf8stdout)
        if write and file is not None:
            with open(file, "a", errors="replace") as f:
                f.seek(0, 2)
                f.write(timestamp + output + "\n")

    return log

# FIXME: read the logging section of the config instead of hardcoding this
stream_handler = logger(None)
debuglog = logger("debug.log", write=False, display=False)
errlog = logger("errors.log")
plog = stream_handler # use this instead of print so that logs have timestamps

# replace characters that can't be encoded with '?'
# since windows likes to use weird encodings by default
utf8stdout = open(1, 'w', errors="replace", closefd=False) # stdout

def get_timestamp(use_utc=None, ts_format=None):
    """Return a timestamp with timezone + offset from UTC."""
    if use_utc is None:
        use_utc = True # FIXME: botconfig
    if ts_format is None:
        ts_format = "[%Y-%m-%d %H:%M:%S{tzoffset}]" # FIXME: botconfig
    if use_utc:
        tmf = datetime.datetime.utcnow().strftime(ts_format)
        tz = "UTC"
        offset = "+0000"
    else:
        tmf = time.strftime(ts_format)
        tz = time.tzname[0]
        offset = "+"
        if datetime.datetime.utcnow().hour > datetime.datetime.now().hour:
            offset = "-"
        offset += str(time.timezone // 36).zfill(4)
    return tmf.format(tzname=tz, tzoffset=offset).strip().upper() + " "

def stream(output, level="normal"):
    if config.Main.get("debug.enabled"):
        plog(output)
    elif level in ("warning", "error"):
        plog(output)
