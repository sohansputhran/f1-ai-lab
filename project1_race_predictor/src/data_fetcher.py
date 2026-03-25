# src/data_fetcher.py
#
# Ergast API client for the F1 Race Predictor.
#
# The Ergast Motor Racing API (http://ergast.com/mrd/) is a free, public API
# that provides historical F1 data from 1950 to the present season.
# No API key required.
#
# This module provides a single class — ErgastClient — that handles:
#   - URL construction
#   - HTTP requests with error handling and retries
#   - Parsing raw JSON responses into clean pandas DataFrames

import time
import logging
from typing import Optional

import requests
import pandas as pd

# ----- Logging setup -----
# Using logging instead of print() is best practice in production code.
# Think of log levels like F1 radio messages:
#   DEBUG   = engineer chatter ("tyre temp nominal")
#   INFO    = driver updates ("box this lap")
#   WARNING = something's off but we continue ("front wing damage, monitor")
#   ERROR   = we have a problem ("retire the car")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ----- Constants -----
BASE_URL = "http://api.jolpi.ca/ergast/f1"
DEFAULT_TIMEOUT = 10        # seconds before we give up on a request
MAX_RETRIES = 3             # how many times to retry a failed request
RETRY_DELAY = 2             # seconds to wait between retries


class ErgastClient:
    """
    A client for the Ergast Motor Racing API.

    Fetches F1 race results, qualifying data, driver standings, and
    constructor standings, returning clean pandas DataFrames.

    Usage:
        client = ErgastClient()
        df = client.get_race_results(season=2023, round_number=1)
    """

    def __init__(self, base_url: str = BASE_URL, timeout: int = DEFAULT_TIMEOUT):
        """
        Initialise the client.

        Args:
            base_url: Root URL of the Ergast API. Rarely needs changing.
            timeout:  Seconds to wait for a response before raising an error.
        """
        self.base_url = base_url
        self.timeout = timeout
        # requests.Session reuses the underlying TCP connection across calls —
        # faster than opening a new connection for every request.
        self.session = requests.Session()

    def _get(self, endpoint: str) -> dict:
        """
        Internal helper: make a GET request with automatic retries.

        This is a private method (leading underscore = internal use only).
        All public methods call this so error-handling logic lives in one place.

        Args:
            endpoint: URL path to append to base_url, e.g. "/2023/1/results.json"

        Returns:
            Parsed JSON response as a Python dictionary.

        Raises:
            requests.HTTPError:   Server returned a 4xx or 5xx status code.
            requests.Timeout:     Server took too long to respond.
            requests.ConnectionError: Network is unreachable.
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Fetching: {url}")

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = self.session.get(url, timeout=self.timeout)
                # Raise an exception for HTTP error codes (4xx, 5xx)
                response.raise_for_status()
                return response.json()

            except requests.Timeout:
                logger.warning(
                    f"Timeout on attempt {attempt}/{MAX_RETRIES} for {url}"
                )
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
                else:
                    raise

            except requests.ConnectionError:
                logger.error(f"Connection error — check your internet: {url}")
                raise

            except requests.HTTPError as e:
                logger.error(f"HTTP error {e.response.status_code} for {url}")
                raise

    # ----- Public methods -----

    def get_race_results(
        self, season: int, round_number: int
    ) -> pd.DataFrame:
        """
        Fetch finishing results for a single race.

        Args:
            season:       Championship year, e.g. 2023.
            round_number: Race number in that season (1 = opener, e.g. Bahrain).

        Returns:
            DataFrame with one row per driver, columns:
            position, driver_id, driver_name, constructor, grid,
            laps, status, points, fastest_lap_rank, season, round
        """
        endpoint = f"/{season}/{round_number}/results.json"
        data = self._get(endpoint)

        # Navigate the nested JSON structure Ergast returns:
        # data → MRData → RaceTable → Races → [0] → Results
        races = data["MRData"]["RaceTable"]["Races"]

        if not races:
            logger.warning(f"No results found for season={season} round={round_number}")
            return pd.DataFrame()

        results = races[0]["Results"]

        # Flatten each result dict into a clean row.
        # We extract only the fields relevant to our predictor.
        rows = []
        for r in results:
            rows.append({
                "season":           season,
                "round":            round_number,
                "position":         int(r["position"]),
                "driver_id":        r["Driver"]["driverId"],
                "driver_name":      (
                    f"{r['Driver']['givenName']} {r['Driver']['familyName']}"
                ),
                "constructor":      r["Constructor"]["constructorId"],
                "grid":             int(r["grid"]),        # qualifying position
                "laps":             int(r["laps"]),
                "status":           r["status"],           # "Finished", "+1 Lap", etc.
                "points":           float(r["points"]),
                # Fastest lap rank is optional — not all results include it
                "fastest_lap_rank": int(
                    r.get("FastestLap", {}).get("rank", 0)
                ),
            })

        return pd.DataFrame(rows)

    def get_season_results(
        self, season: int, max_rounds: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Fetch race results for every round in a season by calling
        get_race_results() repeatedly and stacking the DataFrames.

        Args:
            season:     Championship year, e.g. 2023.
            max_rounds: Optional cap — useful for testing (set to 3 to fetch
                        only the first three rounds instead of all 23).

        Returns:
            DataFrame with all rounds stacked vertically (same schema as
            get_race_results).
        """
        # First, find out how many rounds this season had
        endpoint = f"/{season}.json"
        data = self._get(endpoint)
        races = data["MRData"]["RaceTable"]["Races"]
        total_rounds = len(races)

        if max_rounds:
            total_rounds = min(total_rounds, max_rounds)

        logger.info(f"Fetching {total_rounds} rounds for season {season}...")

        all_rounds = []
        for round_number in range(1, total_rounds + 1):
            df = self.get_race_results(season=season, round_number=round_number)
            if not df.empty:
                all_rounds.append(df)
            # Be polite to the API — don't hammer it with back-to-back requests.
            # Like waiting your turn in the pit lane entry.
            time.sleep(0.3)

        if not all_rounds:
            return pd.DataFrame()

        return pd.concat(all_rounds, ignore_index=True)

    def get_driver_standings(self, season: int) -> pd.DataFrame:
        """
        Fetch the final driver championship standings for a season.

        Args:
            season: Championship year, e.g. 2023.

        Returns:
            DataFrame with columns:
            position, driver_id, driver_name, constructor, points, wins
        """
        endpoint = f"/{season}/driverStandings.json"
        data = self._get(endpoint)

        standings_list = (
            data["MRData"]["StandingsTable"]["StandingsLists"]
        )

        if not standings_list:
            logger.warning(f"No standings found for season={season}")
            return pd.DataFrame()

        standings = standings_list[0]["DriverStandings"]

        rows = []
        for s in standings:
            rows.append({
                "season":       season,
                "position":     int(s["position"]),
                "driver_id":    s["Driver"]["driverId"],
                "driver_name":  (
                    f"{s['Driver']['givenName']} {s['Driver']['familyName']}"
                ),
                "constructor":  s["Constructors"][0]["constructorId"],
                "points":       float(s["points"]),
                "wins":         int(s["wins"]),
            })

        return pd.DataFrame(rows)
