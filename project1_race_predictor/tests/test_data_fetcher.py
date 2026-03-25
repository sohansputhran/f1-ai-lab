# tests/test_data_fetcher.py
#
# Unit tests for the ErgastClient.
#
# KEY CONCEPT — Mocking:
# We do NOT make real HTTP requests in unit tests. Why?
#   1. Tests would fail without internet
#   2. Tests would be slow
#   3. The API could be down — that's not our code's fault
#
# F1 Analogy: When Pirelli tests a new tyre compound in the simulator,
# they don't drive to Silverstone every time. They mock the track conditions
# in a controlled environment. unittest.mock does the same for HTTP calls.

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
import requests

from project1_race_predictor.src.data_fetcher import ErgastClient


# ----- Fixtures -----
# A pytest fixture is a reusable setup block. Instead of creating a new
# ErgastClient() in every test function, we define it once here.

@pytest.fixture
def client() -> ErgastClient:
    """Return a fresh ErgastClient for each test."""
    return ErgastClient()


# Minimal realistic API response for one race result (2 drivers for brevity)
MOCK_RACE_RESULTS_RESPONSE = {
    "MRData": {
        "RaceTable": {
            "Races": [
                {
                    "season": "2023",
                    "round": "1",
                    "Results": [
                        {
                            "position": "1",
                            "Driver": {
                                "driverId": "max_verstappen",
                                "givenName": "Max",
                                "familyName": "Verstappen",
                            },
                            "Constructor": {"constructorId": "red_bull"},
                            "grid": "1",
                            "laps": "57",
                            "status": "Finished",
                            "points": "25",
                            "FastestLap": {"rank": "1"},
                        },
                        {
                            "position": "2",
                            "Driver": {
                                "driverId": "sergio_perez",
                                "givenName": "Sergio",
                                "familyName": "Perez",
                            },
                            "Constructor": {"constructorId": "red_bull"},
                            "grid": "2",
                            "laps": "57",
                            "status": "Finished",
                            "points": "18",
                            # No FastestLap key — tests our .get() fallback
                        },
                    ],
                }
            ]
        }
    }
}

MOCK_EMPTY_RESPONSE = {
    "MRData": {"RaceTable": {"Races": []}}
}


# ----- Tests -----

class TestGetRaceResults:
    """Tests for ErgastClient.get_race_results()"""

    @patch("project1_race_predictor.src.data_fetcher.requests.Session.get")
    def test_returns_dataframe(self, mock_get: MagicMock, client: ErgastClient):
        """Happy path: valid response returns a non-empty DataFrame."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = MOCK_RACE_RESULTS_RESPONSE
        mock_get.return_value.raise_for_status = MagicMock()

        df = client.get_race_results(season=2023, round_number=1)

        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    @patch("project1_race_predictor.src.data_fetcher.requests.Session.get")
    def test_correct_columns(self, mock_get: MagicMock, client: ErgastClient):
        """DataFrame must contain the exact columns our model will rely on."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = MOCK_RACE_RESULTS_RESPONSE
        mock_get.return_value.raise_for_status = MagicMock()

        df = client.get_race_results(season=2023, round_number=1)

        expected_columns = {
            "season", "round", "position", "driver_id", "driver_name",
            "constructor", "grid", "laps", "status", "points", "fastest_lap_rank",
        }
        assert expected_columns.issubset(set(df.columns))

    @patch("project1_race_predictor.src.data_fetcher.requests.Session.get")
    def test_correct_row_count(self, mock_get: MagicMock, client: ErgastClient):
        """One row per driver — our mock has 2 drivers."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = MOCK_RACE_RESULTS_RESPONSE
        mock_get.return_value.raise_for_status = MagicMock()

        df = client.get_race_results(season=2023, round_number=1)
        assert len(df) == 2

    @patch("project1_race_predictor.src.data_fetcher.requests.Session.get")
    def test_missing_fastest_lap_defaults_to_zero(
        self, mock_get: MagicMock, client: ErgastClient
    ):
        """Driver without FastestLap key should get fastest_lap_rank = 0."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = MOCK_RACE_RESULTS_RESPONSE
        mock_get.return_value.raise_for_status = MagicMock()

        df = client.get_race_results(season=2023, round_number=1)
        # Perez (row index 1) has no FastestLap in our mock
        assert df.loc[1, "fastest_lap_rank"] == 0

    @patch("project1_race_predictor.src.data_fetcher.requests.Session.get")
    def test_empty_response_returns_empty_dataframe(
        self, mock_get: MagicMock, client: ErgastClient
    ):
        """If the API returns no races, we should get an empty DataFrame, not a crash."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = MOCK_EMPTY_RESPONSE
        mock_get.return_value.raise_for_status = MagicMock()

        df = client.get_race_results(season=2023, round_number=99)
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    @patch("project1_race_predictor.src.data_fetcher.requests.Session.get")
    def test_http_error_raises(self, mock_get: MagicMock, client: ErgastClient):
        """A 404 or 500 from the API should raise an HTTPError, not silently fail."""
        mock_get.return_value.raise_for_status.side_effect = requests.HTTPError(
            response=MagicMock(status_code=404)
        )

        with pytest.raises(requests.HTTPError):
            client.get_race_results(season=1800, round_number=1)