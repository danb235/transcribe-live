import argparse
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from unittest.mock import patch
import main

class TestMain(unittest.TestCase):

    @patch('main.setup_argparse')
    @patch('main.get_device_choice')
    def test_main_no_args(self, mock_get_device_choice, mock_setup_argparse):
        mock_setup_argparse.return_value = argparse.Namespace(model=None, file=None, device=None, record=False)
        mock_get_device_choice.return_value = 'Mocked Device Name'
        with patch('builtins.input', return_value='0'), \
            patch('main.record_live_audio'), \
            patch('main.process_audio_chunks'), \
            patch('main.sd.InputStream'):
            main.main()
            mock_setup_argparse.assert_called_once()

    @patch('main.setup_argparse')
    @patch('main.transcribe_audio_file')
    @patch('main.whisper.load_model', return_value='mock_model')
    def test_main_with_file(self, mock_load_model, mock_transcribe_audio_file, mock_setup_argparse):
        test_args = argparse.Namespace(file='test.wav', model='b', device=None, record=False)
        mock_setup_argparse.return_value = test_args
        with patch('main.setup_argparse', return_value=test_args):
            main.main()
            mock_transcribe_audio_file.assert_called_once_with('mock_model', 'test.wav')

    @patch('main.list_devices')
    def test_list_devices_input(self, mock_list_devices):
        mock_list_devices.return_value = [{'name': 'input_device', 'max_input_channels': 2}]
        devices = main.list_devices('input')
        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]['name'], 'input_device')

    @patch('main.list_devices')
    def test_list_devices_output(self, mock_list_devices):
        mock_list_devices.return_value = [{'name': 'output_device', 'max_output_channels': 2}]
        devices = main.list_devices('output')
        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]['name'], 'output_device')

    @patch('main.setup_argparse')
    @patch('main.transcribe_audio_file')
    @patch('main.whisper.load_model')
    def test_main_transcribe_existing_file(self, mock_load_model, mock_transcribe_audio_file, mock_setup_argparse):
        # Create a mock model object
        mock_model = unittest.mock.Mock()
        mock_load_model.return_value = mock_model

        # Set up the mock arguments to include a file path
        test_args = argparse.Namespace(file='mock_audio.wav', model='b', device=None, record=False)
        mock_setup_argparse.return_value = test_args

        # Patch the setup_argparse function to return the test arguments
        with patch('main.setup_argparse', return_value=test_args):
            # Call the main function, which should in turn call transcribe_audio_file
            main.main()
            # Assert that transcribe_audio_file was called with the mock model and file path
            mock_transcribe_audio_file.assert_called_once_with(mock_model, 'mock_audio.wav')

if __name__ == '__main__':
    unittest.main()