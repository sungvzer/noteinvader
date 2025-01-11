from app import app
from os import getenv
import requests
import json
from app.utils.db import get_db


class MusicService:
    @staticmethod
    def find_albums(album: str, page: int = 1):
        MOCK_ALBUMS = False

        if MOCK_ALBUMS:
            print("WARNING: Using mock albums")
            with open(app.root_path + "/mocks/albums.json") as f:
                return json.load(f)

        url = getenv("LASTFM_URL")
        api_key = getenv("LASTFM_API_KEY")
        method = "album.search"
        format = "json"

        response = requests.get(
            f"{url}?method={method}&album={album}&api_key={api_key}&format={format}&page={page}"
        )

        result = {
            "totalResults": response.json()["results"]["opensearch:totalResults"],
            "startIndex": response.json()["results"]["opensearch:startIndex"],
            "itemsPerPage": response.json()["results"]["opensearch:itemsPerPage"],
            "albummatches": [],
        }

        if (
            "results" in response.json()
            and "albummatches" in response.json()["results"]
        ):
            result["albummatches"] = response.json()["results"]["albummatches"]["album"]

        # Cache the result
        artist_and_names = [
            {"artist": album["artist"], "name": album["name"]}
            for album in result["albummatches"]
        ]

        existing_albums = get_db().music.find({"$or": artist_and_names})
        existing_albums = list(existing_albums)

        existing_albums = [
            {"artist": e["artist"], "name": e["name"]} for e in existing_albums
        ]

        # insert albums of which the pair name-artist is not already in existing
        to_insert = [
            {**album, "stars": 0}
            for album in result["albummatches"]
            if {"artist": album["artist"], "name": album["name"]} not in existing_albums
        ]

        if len(to_insert) != 0:
            get_db().music.insert_many(to_insert)

        for idx, match in enumerate(result["albummatches"]):
            found = get_db().music.find_one(
                {"artist": match["artist"], "name": match["name"]}
            )
            if found is not None:
                result["albummatches"][idx] = {**match, **found}

        return result
