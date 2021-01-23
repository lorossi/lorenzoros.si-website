import logging
from scraper import Scraper
from flask import Flask, render_template, jsonify
from apscheduler.schedulers.background import BackgroundScheduler


s = Scraper()
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


def main():
    logfile = "logging.log"
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",
                        level=logging.INFO, filename=logfile,
                        filemode="w")

    # scheduler setup
    scheduler = BackgroundScheduler()
    scheduler.start()
    # run app
    logging.info("App started!")


@app.route("/")
@app.route("/homepage")
def index():
    return render_template("index.html", repos=s.repos)


main()
if __name__ == "__main__":
    app.run()
