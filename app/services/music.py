from os import getenv
import requests


class MusicService:
    @staticmethod
    def find_albums(album: str, page: int = 1):
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
        return result
