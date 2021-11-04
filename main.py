#!/usr/bin/bash

# Example input variables
from lib.SP.audioVisualEditor import AudioVisualEditor
from lib.SP.questionnaireManager import QuestionnaireManager
from lib.SP.spotifyWrapper import SpotifyWrapper


CLIENT_ID = "a451ba718e744322b8abb62344acb98c"
CLIENT_SECRET = "611f8a37335847569357c461f89c05ab"


def main():
    avEditor = AudioVisualEditor()
    qMngr = QuestionnaireManager()
    spotify = SpotifyWrapper(CLIENT_ID, CLIENT_SECRET)


if __name__ == '__main__':
    main()