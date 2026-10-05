import ast
import unittest
from unittest.mock import Mock, patch

import jarvis


class JarvisCommandTests(unittest.TestCase):
    def setUp(self):
        self.tts = Mock()
        self.jarvis = jarvis.MahiJarvis(recognizer=Mock(), tts=self.tts)

    def test_play_youtube(self):
        with patch.object(self.jarvis, "play_song") as play:
            self.jarvis.handle("play Believer on YouTube")
            play.assert_called_once_with("Believer", "youtube")

    def test_play_spotify(self):
        with patch.object(self.jarvis, "play_song") as play:
            self.jarvis.handle("play Perfect on Spotify")
            play.assert_called_once_with("Perfect", "spotify")

    def test_search(self):
        with patch.object(self.jarvis, "search") as search:
            self.jarvis.handle("search Python voice assistant")
            search.assert_called_once_with("Python voice assistant")

    def test_exit(self):
        self.jarvis.handle("stop listening")
        self.assertFalse(self.jarvis.running)

    def test_unknown_is_not_shell_command(self):
        with patch.object(self.jarvis, "run_command", create=True) as run:
            self.jarvis.handle("delete everything")
            run.assert_not_called()

    def test_source_parses(self):
        ast.parse(open("jarvis.py", encoding="utf-8").read())


if __name__ == "__main__":
    unittest.main()
