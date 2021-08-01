import logging

from pyapp.app import CliApplication
from . import __version__

app = CliApplication(
    prog="Transfer Market Scraper",
    description="Application to scrape and analyse an online game's transfer market",
    version=__version__
)
main = app.dispatch

logger = logging.getLogger("Transfer Market Scraper")


@app.command
def scrape(
):
    """
    Command to scrape the games transfer market
    :return:
    """

    logger.info("Beginning Transfer Market Scrape")
    logger.info("Finished Transfer Market Scrape")
