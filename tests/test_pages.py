"""Render every page with an invalid Gemini key and no network."""

import os
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "main.py")
MODELS = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
]


class PageRenderTests(unittest.TestCase):
    def setUp(self):
        os.environ["GEMINI_API_KEY"] = "invalid-key"
        os.environ["GOOGLE_API_KEY"] = ""
        self.models = patch(
            "gemini_utility.get_available_models",
            return_value=list(MODELS),
        )
        self.status = patch("gemini_utility.check_api_key", return_value=False)
        self.models.start()
        self.status.start()
        self.addCleanup(self.models.stop)
        self.addCleanup(self.status.stop)

    def _run(self, page=None):
        app = AppTest.from_file(APP, default_timeout=20)
        app.run()
        self.assertEqual(len(app.exception), 0, app.exception)
        if page:
            app.switch_page(page).run()
            self.assertEqual(len(app.exception), 0, app.exception)
        return app

    def _assert_sidebar(self, app):
        self.assertEqual(app.sidebar.selectbox[0].label, "Model")
        self.assertEqual(
            [slider.label for slider in app.sidebar.slider],
            ["Temperature", "Max tokens"],
        )
        self.assertEqual(app.sidebar.slider[0].value, 0.7)
        self.assertEqual(app.sidebar.slider[1].value, 1000)
        captions = [item.value for item in app.sidebar.caption]
        self.assertIn("Gemini API unavailable", captions)

    def test_chat_page(self):
        app = self._run()
        self._assert_sidebar(app)
        self.assertEqual(app.title[0].value, "Chat")
        self.assertIn("Messages stay in this session", app.caption[0].value)
        labels = [button.label for button in app.button]
        self.assertEqual(labels, ["Clear chat", "Save chat", "Chat stats", "Voice input"])
        self.assertEqual(app.toggle[0].label, "Stream")
        self.assertEqual(len(app.chat_input), 1)

        app.button[3].click().run()
        self.assertEqual(len(app.exception), 0, app.exception)
        self.assertTrue(any("not available yet" in item.value for item in app.caption))

        app.button[2].click().run()
        self.assertEqual(len(app.exception), 0, app.exception)
        self.assertTrue(any("messages in this chat" in item.value for item in app.caption))

    def test_stories_page(self):
        app = self._run("views/stories.py")
        self._assert_sidebar(app)
        self.assertEqual(app.title[0].value, "Stories")
        self.assertEqual(
            [tab.label for tab in app.tabs],
            ["Image and text", "Text", "Creative writing"],
        )
        self.assertEqual(len(app.file_uploader), 1)
        button_labels = [button.label for button in app.button]
        self.assertIn("Generate story", button_labels)
        self.assertIn("Generate poem", button_labels)
        self.assertTrue(any(box.label == "Include a moral" for box in app.checkbox))
        self.assertTrue(any(box.label == "Generate audio" for box in app.checkbox))

    def test_comic_video_page(self):
        app = self._run("views/comic_video.py")
        self._assert_sidebar(app)
        self.assertEqual(app.title[0].value, "Comic video")
        self.assertIn("ADOPLE/Video-Generator-AI", app.caption[0].value)
        self.assertEqual(
            sorted(button.label for button in app.button),
            ["Generate video", "Preview"],
        )
        self.assertEqual(len(app.text_area), 1)

    def test_assistant_page(self):
        app = self._run("views/assistant.py")
        self._assert_sidebar(app)
        self.assertEqual(app.title[0].value, "Assistant")
        self.assertEqual(app.selectbox[0].label, "Assistant")
        self.assertEqual(app.selectbox[0].value, "Writing")
        self.assertEqual(app.selectbox[1].label, "Task")
        self.assertEqual(app.button[0].label, "Improve Text")
        self.assertEqual(len(app.text_area), 1)

        app.selectbox[0].set_value("Research").run()
        self.assertEqual(len(app.exception), 0, app.exception)
        self.assertTrue(any("not available yet" in item.value for item in app.caption))
        self.assertEqual(len(app.text_area), 0)

    def test_missing_api_key_stops_before_pages(self):
        os.environ["GEMINI_API_KEY"] = ""
        os.environ["GOOGLE_API_KEY"] = ""
        app = AppTest.from_file(APP, default_timeout=20).run()
        self.assertEqual(len(app.exception), 0, app.exception)
        self.assertTrue(any("GEMINI_API_KEY" in item.value for item in app.error))
        self.assertEqual(len(app.title), 0)
        self.assertEqual(len(app.sidebar.selectbox), 0)


if __name__ == "__main__":
    unittest.main()
