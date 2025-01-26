from pydantic_ai import Agent
from models import Theme

class ThemeAgent:
    def __init__(self):
        self.agent = Agent('openai:gpt-4o-mini', result_type=Theme)

    def generate_theme(self, constraints: list, examples: list) -> Theme:
        theme_prompt = (
            'Recommend me a music theme for a daily music recommendation newsletter. '
            f'Consider these aspects: {", ".join(constraints)}. '
            f'Example themes: {", ".join(examples)}. '
            'The theme should be specific, culturally relevant, and appeal to music enthusiasts. '
            'Your output should only include the theme name and a brief description of it.'
        )
        theme_result = self.agent.run_sync(theme_prompt, result_type=Theme, model_settings={'temperature': 0.8})
        return theme_result.data