# Transcribe Live

Transcribe is a Python command-line application that utilizes OpenAI's Whisper model to transcribe audio. It can handle live audio from microphones as well as process pre-recorded audio files in various formats. The application offers a range of Whisper model sizes to balance between accuracy and performance based on user needs.

## Features

- Transcription of live audio from the microphone.
- Transcription of pre-recorded audio files.
- Support for multiple audio formats (mp3, m4a, wav, etc.).
- Selection of Whisper model sizes (tiny, base, small, medium, large) for varied accuracy.
- Interactive prompts to guide users through the configuration when arguments are not provided.
- Live recording to a file with optional MP3 encoding.
- Continuous transcription display during live audio processing.
- Ability to record and transcribe simultaneously.

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

### Interactive Mode

If no arguments or only partial arguments are provided, the program enters an interactive mode, which will guide you through the following configuration steps:

- **Model Selection**: The program will list all available Whisper models. You can select the desired model by typing its corresponding letter (e.g., 'b' for base).
- **Device Selection**: If the `--device` argument is not provided, the program will list all available audio input devices. You can then select the appropriate device by typing its number.
- **Record Selection**: If you wish to record the live audio, you will be prompted to confirm this by typing 'yes' or 'no'.

This mode is designed to be user-friendly, especially for those unfamiliar with command-line arguments.

### Non-Interactive Mode

For advanced users or automated setups, providing all necessary arguments enables a non-interactive mode. This allows the program to run end-to-end without additional input, ideal for scripting or batch processing.

To record live audio while transcribing, use the `--record` flag:

`python src/main.py --model base --device 0 --record`

### Command-Line Argument Details

- `--file`: Provide the path to an audio file for transcription. If this argument is used, the program will not enter live recording mode.
- `--model`: Select the Whisper model size (options: 'tiny', 'base', 'small', 'medium', 'large').
- `--device`: Specify the device number for audio input as listed by your operating system.
- `--record`: Record the live audio to a file while transcribing.

### Basic Usage

- To start the application without any arguments, run:

  `python src/main.py`

  This will prompt you to select the Whisper model size and, if live audio is chosen, the device number for audio input.

- To transcribe a pre-recorded audio file, use:

  `python src/main.py --file /path/to/audio/file`

### Command-Line Options

- `--model`: Select the Whisper model size (options: 'tiny', 'base', 'small', 'medium', 'large'). The larger the model, the more accurate but slower the transcription.
- `--device`: Specify the device number for audio input as listed by your operating system.

### Examples

- Transcribing live audio with the base model:

  `python src/main.py --model base`

- Transcribing an audio file with the large model:

  `python src/main.py --model large --file ./audio/sample.mp3`

- To record and transcribe live audio with the base model:

  `python src/main.py --model base --record`

## Configuration

The Transcribe application allows configuration through command-line arguments or interactive prompts:

- **Model Selection**: Choose between different Whisper model sizes based on accuracy and performance requirements. 'tiny' is the fastest but least accurate, while 'large' offers the highest accuracy at the cost of speed.
- **Device Selection**: Specify the particular input device by its number, which can be obtained from the system's audio settings or by running the application without the `--device` argument to list available devices.

## Contributing

Contributions to the Transcribe project are welcome. Please follow standard practices for code contributions: fork the repository, make your changes, and submit a pull request for review.
