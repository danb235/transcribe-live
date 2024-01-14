# Transcribe Live

Transcribe is a Python command-line application that utilizes OpenAI's Whisper model to transcribe audio. It's capable of handling live audio from microphones as well as processing pre-recorded audio files in various formats. The application offers a range of Whisper model sizes to balance between accuracy and performance based on user needs.

## Features

- Live audio transcription from microphone.
- Transcription of pre-recorded audio files.
- Support for multiple audio formats (mp3, m4a, wav, etc.).
- Selection of Whisper model sizes (tiny, base, small, medium, large) for varied accuracy.
- Adjustable audio source and device selection.

## Installation

### Prerequisites

- Python 3.7 or higher.
- pip (Python package manager).

### Steps

1. Clone the repository:

`git clone https://github.com/your-username/transcribe.git`

2. Navigate to the cloned directory:

`cd transcribe`

3. Install the required Python packages:

`pip install -r requirements.txt`

4. Run the application:

`python src/main.py`

### Troubleshooting

Ensure you have the latest version of Python and pip. If you encounter any issues, check for any error messages in the console, which typically indicate missing dependencies or syntax errors.

## Usage

### Basic Usage

- To transcribe live audio from the microphone, simply run:

`python src/main.py`

- To transcribe a pre-recorded audio file, use:

`python src/main.py --file /path/to/audio/file`

### Command-Line Options

- `--model`: Select the Whisper model size (options: 'tiny', 'base', 'small', 'medium', 'large'). The larger the model, the more accurate but slower the transcription.
- `--source`: Choose the audio source - 'i' for input (microphone), 'o' for output (system audio).
- `--device`: Specify the device number for audio input/output as listed by your operating system.

### Examples

- Transcribing live audio with the base model:

`python src/main.py --model base --source i`

- Transcribing an audio file with the large model:

`python src/main.py --model large --file ./audio/sample.mp3`

## Configuration

The Transcribe application allows configuration through command-line arguments:

- Model Selection: Choose between different Whisper model sizes based on accuracy and performance requirements. 'tiny' is the fastest but least accurate, while 'large' offers the highest accuracy at the cost of speed.
- Audio Source: Toggle between live audio input (microphone) and system audio output for transcription.
- Device Selection: Specify the particular input/output device by its number, which can be obtained from the system's audio settings.

## Contributing

Contributions to the Transcribe project are welcome. Please follow standard practices for code contributions: fork the repository, make your changes, and submit a pull request for review.
