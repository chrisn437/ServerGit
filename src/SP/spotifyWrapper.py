import spotipy
from src.interfaces.observer import IObserver, ISubject

class SpotifyWrapper(IObserver):
    """ Spotify API wrapper """

    def __init__(self, client_id: str, client_secret: str):
        creds  = spotipy.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.spotify = spotipy.Spotify(client_credentials_manager=creds)
        

    def downloadTopTracks(self, lz_uri: str) -> None:
        """Get 30 second audio snippets of an artists top 5 tracks in Denmark

        Args:
            lz_uri (str): Spotify URI of an artist
        """
        results = self.spotify.artist_top_tracks(lz_uri, country="DK")
        id = None

        for track in results['tracks'][:5]:
            # Download the preview of the song
            dlUrl = track['preview_url']
            filename = track['name'].replace(" ", "") + ".mp3"
            urlretrieve(dlUrl, filename)
            id = track['id']

    def getTrackFeatures(self, id: str) -> str:
        """Get Spotify track features and dump them to a file

        Args:
            id (str): Song ID

        Returns:
            str: JSON string of audio features
        """

        meta = spotify.track(id)
        features = spotify.audio_features(id)
        tmp = spotify.audio_analysis(id)
        with open('audioFeatures.txt', 'w') as outfile:
            json.dump(features, outfile, indent=4, sort_keys=True)
        return features
            
    def update(self, subject: ISubject) -> None:
        """Callback from the subject

        Args:
            subject (Subject): [description]
        """
        if subject._state < 3:
            print("ConcreteObserverA: Reacted to the event")