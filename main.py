from flask import Flask, request, redirect
import streamlink
import validators

app = Flask(__name__)


def get_stream_obj(query):
    try:
        links = streamlink.streams(query)
        qualities = list(links.keys())
        return (links, qualities)
    except Exception:
        return f"Could not get the link, Streamlink couldn't read {query}"


@app.route("/")
def index():
    return "This program permits you to get direct access to streams by using Streamlink. How does that work ? Simply add '/iptv-query?streaming-ip=*insert url*' at the page URL to make it work. Thanks to @keystroke3 from GitHub for helping me code this tool. Enjoy ! LaneSh4d0w"


@app.route("/iptv-query")
def home():
    if request.args:
        query = request.args.get("streaming-ip")
        if not query:
            return "No streaming IP found. Reason: streaming-ip string is empty"

        valid = validators.url(query)
        if not valid:
            return "The URL you've entered is not valid."

        # get stream data or exit with error message
        stream_obj = get_stream_obj(query)
        if type(stream_obj) == str:
            return stream_obj

        # Use specified quality or "best"
        quality = request.args.get("quality")
        if not quality:
            return redirect(stream_obj[0]["best"].url)
        elif quality in stream_obj[1]:
            return redirect(stream_obj[0][quality].url)
        else:
            # if quality invalid, list available qualities
            qualities = ",".join(stream_obj[1])
            return f"Available qualities are: {qualities}"
    else:
        return "You provided nothing to me."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
