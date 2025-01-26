from pydantic_ai import Agent
from models import AlbumList, Theme

class CurationAgent:
    def __init__(self):
        self.agent = Agent('openai:gpt-4o-mini', result_type=AlbumList)

    def curate_albums(self, theme: Theme) -> AlbumList:
        prompt = (
            f'For the theme "{theme.name}" ({theme.description}), curate 10 albums from distinct artists that perfectly exemplify this specific theme. '
            'Each album should clearly demonstrate the thematic elements mentioned. '
            'Consider albums that are highly rated, culturally significant, and directly connect to the theme\'s core concepts. '
            'Explain how each album fits the theme in the description. '
            'Your output should only include for each album the album title, artist name, and album description.'
        )
        albums_result = self.agent.run_sync(prompt, result_type=AlbumList, model_settings={'temperature': 0.3})
        return albums_result.data