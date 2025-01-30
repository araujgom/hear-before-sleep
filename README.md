# Hear Before you Sleep 🎶

The main goal of this project is to provide students and professionals with a simple and practical application for building AI agent systems. In this case, the system is designed to generate content for a daily music recommendation newsletter, helping users discover new styles and artists.

## Under the Hoods 🛠️

The project was built using the [Pydantic AI](https://ai.pydantic.dev/) framework, enabling the creation of a simple and efficient content generation system. To create the daily content, the system uses a workflow containing two agents:

* [Theme Agent](agents/theme_agent.py): It's responsible for selecting a daily theme for the music recommendations. In order to improve the agent creativiness, we also pass a group of random categories to be used as inspiration for the theme selection.
* [Curation Agent](agents/curation_agent.py): It's responsible for selecting a list of albums that have synergy with the daily theme. In order to improve the newsletter reader experience, we also enrich the selected album list with their respective Spotify links.

## Prerequisites 📋

To run this project, you will need to have the following environment variables set up:

* `SPOTIFY_CLIENT_ID`: The client ID for your Spotify API application.
* `SPOTIFY_CLIENT_SECRET`: The client secret for your Spotify API application.
* `OPENAI_API_KEY`: The API key for your OpenAI account.

Just take from `.env.example` file and create a `.env` file with your own credentials.

## Running It by Yourself 🚀

To run this project on your local machine, you can follow these simple steps:

1. Clone this repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Run the project by executing the `main.py` script: `python main.py`.

Also, you can run the project through the `uv` Python packaging tool. To do so, you can follow these steps:

1. Install the `uv` tool following the instructions on their [official docs page](https://docs.astral.sh/uv/getting-started/installation/).
2. Initialize a virtual environment through the `uv venv` command.
3. Add project dependencies by running `uv add -r requirements.txt`.
4. Run the project by executing the `uv run main.py` command.

## Subscribing to the Newsletter 📬

If you enjoyed the project, we also transcribe code outputs on our newsletter at a daily basis. Susbsribe on it [here](https://hearbeforeyousleep.beehiiv.com/)!



