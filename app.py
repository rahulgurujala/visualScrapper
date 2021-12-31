import requests
from bs4 import BeautifulSoup
from flask import Flask, flash, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/scrape")
def scrape():

    url = request.args.get("url")

    try:
        response = requests.get(url)
        content = BeautifulSoup(response.text, "lxml").prettify()
    except Exception:
        flash('Failed to retrieve URL "%s"' % url, "danger")
        content = ""

    return render_template("scrape.html", content=content)


@app.route("/results")
def results():
    results = []

    args = [
        {
            "tag": request.args.getlist("tag")[index],
            "css": request.args.getlist("css")[index],
            "attr": request.args.getlist("attr")[index],
        }
        for index in range(len(request.args.getlist("tag")))
    ]

    response = requests.get(request.args.get("url"))
    content = BeautifulSoup(response.text, "lxml")

    item = {
        arg["css"]: [one.text for one in content.findAll(arg["tag"], arg["css"])]
        for arg in args
    }

    for index in range(len(item[next(iter(item))])):
        row = {key: '"' + value[index] + '"' for key, value in item.items()}

        results.append(row)

    return render_template("results.html", results=results)


if __name__ == "__main__":
    app.secret_key = "NyM8Z!`J`raV^2[_"
    app.run(debug=True, threaded=True)
