from pydantic import BaseModel

class Theme(BaseModel):
    name: str
    description: str

class Album(BaseModel):
    album_title: str
    artist_name: str
    album_description: str

class SpotifyAlbum(Album):
    spotify_url: str

class AlbumList(BaseModel):
    albums: list[Album]