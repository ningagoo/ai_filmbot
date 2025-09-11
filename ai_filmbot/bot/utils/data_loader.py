import json

def get_movie_by_code(code: str, db_path="bot/data/media/movies.json") -> dict | None:
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(code)
    except Exception:
        return None