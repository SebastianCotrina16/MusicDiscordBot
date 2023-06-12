from .player import Player
from youtubesearchpython import VideosSearch

class YouTubePlayer(Player):
    def play(self, query):
        videos_search = VideosSearch(query, limit=1)
        results = videos_search.result()

        if not results['result']:
            print("No videos found.")
            return None
        else:
            # Return the first result's url
            return results['result'][0]['link']
