import unittest
import os
import argparse
from unittest.mock import patch, MagicMock
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import main

class TestTranscribeCLI(unittest.TestCase):

    def setUp(self):
        self.test_file = './tests/sample.m4a'
        self.expected_output = 'output/sample.txt'

    def tearDown(self):
        if os.path.exists(self.expected_output):
            os.remove(self.expected_output)

    def test_audio_file_transcription(self):
        """Test transcription of an audio file."""
        test_args = argparse.Namespace(model='b', file=self.test_file, source=None, device=None)
        with patch('main.whisper.load_model') as mock_load_model:
            mock_model = MagicMock()
            mock_load_model.return_value = mock_model
            with patch('main.transcribe_audio_file') as mock_transcribe:
                main.main(test_args)
                mock_transcribe.assert_called_once_with(mock_model, self.test_file)

    def test_argument_parsing(self):
        """Test command-line argument parsing."""
        test_args = ['--model', 'b', '--source', 'o', '--device', '0']
        with patch('sys.argv', ['main.py'] + test_args):
            args = main.setup_argparse()
            self.assertEqual(args.model, 'b')
            self.assertEqual(args.source, 'o')
            self.assertEqual(args.device, 0)

    def test_incompatible_arguments(self):
        """Test mixing file transcription with live audio source arguments."""
        test_args = argparse.Namespace(model='b', source='o', device=0, file=self.test_file)
        with self.assertRaises(SystemExit):
            main.main(test_args)

    def test_output_file_creation(self):
        """Test that transcription creates the expected output file."""
        with patch('main.whisper.load_model') as mock_load_model:
            mock_model = MagicMock()
            mock_model.transcribe.return_value = {"text": "mock transcription"}
            mock_load_model.return_value = mock_model
            main.transcribe_audio_file(mock_model, self.test_file)
            self.assertTrue(os.path.exists(self.expected_output))

if __name__ == '__main__':
    unittest.main()
