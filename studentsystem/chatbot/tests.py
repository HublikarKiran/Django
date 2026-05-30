import json
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase, override_settings

from .views import build_study_answer, extract_gemini_text


class ChatbotGeminiTests(SimpleTestCase):
    def test_extract_gemini_text_combines_text_parts(self):
        data = {
            'candidates': [
                {
                    'content': {
                        'parts': [
                            {'text': 'First part'},
                            {'text': 'Second part'},
                        ]
                    }
                }
            ]
        }

        self.assertEqual(extract_gemini_text(data), 'First part\nSecond part')

    @override_settings(GEMINI_API_KEY='test-key', GEMINI_MODEL='gemini-test')
    @patch('chatbot.views.urlrequest.urlopen')
    def test_build_study_answer_uses_gemini_response(self, mock_urlopen):
        response = MagicMock()
        response.read.return_value = json.dumps({
            'candidates': [
                {
                    'content': {
                        'parts': [{'text': 'Gemini answer'}],
                    }
                }
            ]
        }).encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = response

        self.assertEqual(build_study_answer('Explain DBMS'), 'Gemini answer')

    @override_settings(GEMINI_API_KEY='')
    def test_build_study_answer_falls_back_without_api_key(self):
        answer = build_study_answer('DBMS')

        self.assertIn('Topic: DBMS', answer)
