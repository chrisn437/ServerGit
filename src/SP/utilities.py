class Utilities():
    @staticmethod
    def mp3ToWav(filePath: str):
        """Converts an MP3 file to .WAV

        Args:
            filePath (str): Relative path to the audio object
        """
        from pydub import AudioSegment
        import os

        # Create an MP3 handle
        sound = AudioSegment.from_mp3(filePath)
        # Replace file extension and export
        newExt = os.path.splitext(filePath)[0] + ".wav"
        sound.export(newExt, format="wav")
