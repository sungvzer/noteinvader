from typing import List
from flask_pymongo import ObjectId
from app import app
from os import getenv
import requests
import json
from app.utils.db import get_db


class MusicService:
    @staticmethod
    def fill_albums(ids: List[ObjectId]):
        albums = get_db().music.find({"_id": {"$in": ids}})
        albums = list(albums)
        for idx, album in enumerate(albums):
            if album["needs_detail"]:
                album_url = album["url"]
                album_url = album_url.replace("https://www.last.fm/music/", "")
                artist, name = album_url.split("/")

                url = getenv("LASTFM_URL")
                api_key = getenv("LASTFM_API_KEY")
                method = "album.getinfo"
                format = "json"

                response = requests.get(
                    f"{url}?method={method}&artist={artist}&album={name}&api_key={api_key}&format={format}"
                )

                if not response.ok:
                    return None

                merged = {**album, **response.json()["album"]}
                merged["needs_detail"] = False
                get_db().music.update_one({"_id": album["_id"]}, {"$set": merged})

                albums[idx] = merged

        return albums

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

        if len(artist_and_names) != 0:
            existing_albums = get_db().music.find({"$or": artist_and_names})
            existing_albums = list(existing_albums)

            existing_albums = [
                {"artist": e["artist"], "name": e["name"]} for e in existing_albums
            ]

            # insert albums of which the pair name-artist is not already in existing
            to_insert = [
                {**album, "stars": 0, "needs_detail": True}
                for album in result["albummatches"]
                if {"artist": album["artist"], "name": album["name"]}
                not in existing_albums
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

    @staticmethod
    def get_album(album_id: ObjectId):
        album = get_db().music.find_one({"_id": album_id})
        if album is None:
            return None

        if album["needs_detail"]:
            album_url = album["url"]
            album_url = album_url.replace("https://www.last.fm/music/", "")
            artist, name = album_url.split("/")

            url = getenv("LASTFM_URL")
            api_key = getenv("LASTFM_API_KEY")
            method = "album.getinfo"
            format = "json"

            response = requests.get(
                f"{url}?method={method}&artist={artist}&album={name}&api_key={api_key}&format={format}"
            )

            if not response.ok:
                return None

            merged = {**album, **response.json()["album"]}
            merged["needs_detail"] = False
            get_db().music.update_one({"_id": album_id}, {"$set": merged})

            return merged

        return album
