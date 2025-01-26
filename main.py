import os
import random
import re
from dotenv import load_dotenv
from handlers.duckdb_handler import DuckDBHandler
from services.spotify_service import SpotifyService
from agents.theme_agent import ThemeAgent
from agents.curation_agent import CurationAgent

load_dotenv()

# Initialize Services
duckdb_handler = DuckDBHandler()
spotify_service = SpotifyService()

# Initialize Agents
theme_agent = ThemeAgent()
curation_agent = CurationAgent()

THEME_CATEGORIES = [
    ("Geography", ["Brazilian", "Latin", "Japanese", "African", "Indian", "Middle Eastern", "Caribbean", "Mediterranean", "Eastern European"]),
    ("Decade", ["60s", "70s", "80s", "90s", "2000s", "2010s", "2020s"]),
    ("Mood", ["Melancholic", "Upbeat", "Atmospheric", "Energetic", "Dreamy", "Mystical", "Nostalgic", "Euphoric", "Introspective", "Hypnotic", "Meditative"]),
    ("Genre", ["Jazz", "Rock", "Electronic", "Folk", "Classical", "Hip-Hop", "Soul", "Blues", "Ambient", "Metal", "Funk", "Reggae", "World Music", "Post-Rock"]),
    ("Style", ["Experimental", "Progressive", "Fusion", "Alternative", "Traditional", "Psychedelic", "Avant-garde", "Lo-fi", "Minimalist", "Abstract", "Orchestral"])
]

welcome_message = """Hey! Are you tired from Spotify playlists with repetitive and non-surprising content? 😞

Look no further and enjoy a beautiful daily collection of **Albums to Hear Before you Sleep**! 🥳

*And the chosen mood for today is...* 🥁

"""

def get_random_theme_constraints():
    selected_cats = random.sample(THEME_CATEGORIES, k=random.randint(2, 3))
    constraints = []
    examples = []

    for category, options in selected_cats:
        choice = random.choice(options)
        constraints.append(f"{category}: {choice}")
        examples.append(f"{choice} {random.choice([cat[1][0] for cat in THEME_CATEGORIES if cat[0] != category])}")

    return constraints, examples

def main():
    constraints, examples = get_random_theme_constraints()
    theme = theme_agent.generate_theme(constraints, examples)
    print(theme)

    albums = curation_agent.curate_albums(theme)

    # Enriching Agent outputs with Spotify data
    enriched_albums = []
    for album in albums.albums:
        if album.artist_name != album.album_title:
            spotify_album = spotify_service.get_spotify_data(album)
            if spotify_album:
                enriched_albums.append(spotify_album)

    # Generating post outputs...
    markdown_content = welcome_message + f"# {theme.name} 🎶\n\n{theme.description}\n\n"
    for album in enriched_albums:
        markdown_content += f"## {album.album_title} by {album.artist_name}\n"
        markdown_content += f"{album.album_description}\n\n"
        markdown_content += f"[Listen on Spotify]({album.spotify_url})\n\n"

    # Basic validations and writing outputs
    os.makedirs("output", exist_ok=True)
    if len(enriched_albums) >= 2:
        safe_filename = re.sub(r'[^\w\s-]', '', theme.name)
        safe_filename = safe_filename.replace(' ', '_').lower()
        output_path = os.path.join("output", f"{safe_filename}.md")

        if duckdb_handler.is_playlist_recent(safe_filename):
            print(f"Theme '{theme.name}' was already suggested in the last 90 days. Stopping execution.")
            exit()
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            duckdb_handler.log_playlist(safe_filename)
        except IOError as e:
            print(f"Error writing to file: {e}")
    else:
        print(f"Could not generate recommendation newsletter: found only {len(enriched_albums)} albums with Spotify data. Minimum required is 2.")

if __name__ == "__main__":
    main()