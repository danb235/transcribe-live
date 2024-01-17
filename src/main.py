import whisper
import sounddevice as sd
import numpy as np
import queue
import threading
import warnings
import os
import datetime
import argparse
import pyaudio
import wave

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

def setup_argparse():
    parser = argparse.ArgumentParser(
        description="""
        Transcribe audio using Whisper. This program can either live record audio or process an existing audio file.
        To determine the model, source, and device choices for live recording, run the program once without arguments.
        Example for live recording: python main.py --model b --source o --device 0
        Example for processing a file: python main.py --file /path/to/file.mp3""",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--model", choices=['t', 'b', 's', 'm', 'l'], help="Whisper model size.")
    parser.add_argument("--source", choices=['i', 'o'], help="Audio source for live recording.")
    parser.add_argument("--device", type=int, help="Device number for live audio source.")
    parser.add_argument("--file", help="Path to an existing audio file to transcribe.")
    parser.add_argument("--record", action='store_true', help="Record live audio to a file.")
    return parser.parse_args()

def list_devices(kind='input'):
    devices = sd.query_devices()
    input_devices = [device for device in devices if device['max_input_channels'] > 0]
    output_devices = [device for device in devices if device['max_output_channels'] > 0]

    if kind == 'input':
        print("Available input devices:")
        for i, device in enumerate(input_devices):
            print(f"{i}: {device['name']}")
        return input_devices
    else:
        if args.device is None:
            print("Available output devices:")
            for i, device in enumerate(output_devices):
                print(f"{i}: {device['name']}")
        return output_devices

def get_device_choice(devices, provided_choice=None):
    if provided_choice is not None:
        return devices[provided_choice]['name']
    choice = int(input("Select device number: "))
    return devices[choice]['name']

def transcribe_audio_file(model, file_path):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_file_name = os.path.splitext(os.path.basename(file_path))[0] + ".txt"
    output_file_path = os.path.join(output_dir, output_file_name)

    print(f"Transcribing {file_path}...")
    result = model.transcribe(file_path)
    with open(output_file_path, 'w') as file:
        file.write(result["text"])
    print(f"Transcription completed. Output saved to {output_file_path}")

audio_queue = queue.Queue()
stop_signal = threading.Event()

def audio_callback(indata, frames, time, status):
    audio_queue.put(indata.copy())

def process_audio_chunks(model, output_file):
    accumulated_audio = np.array([], dtype=np.float32)
    try:
        while not stop_signal.is_set():
            try:
                audio_chunk = audio_queue.get(timeout=1)
            except queue.Empty:
                continue

            if audio_chunk is not None:
                accumulated_audio = np.concatenate((accumulated_audio, np.array(audio_chunk, dtype=np.float32).flatten()))

                if len(accumulated_audio) >= 5 * 16000:
                    result = model.transcribe(accumulated_audio, language="en")
                    # Move the cursor up one line and clear the line
                    print("\033[A\033[K", end='')
                    print("Transcription:", result["text"])
                    # Move the cursor back down and print the stop message
                    print("(Press Enter to stop)")
                    with open(output_file, 'a') as file:
                        file.write(result["text"] + "\n")
                    accumulated_audio = np.array([], dtype=np.float32)
    except Exception as e:
        print("An error occurred in processing:", e)

def record_live_audio(output_file_path):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    print("Recording... (Press Enter to stop)")

    frames = []
    while not stop_signal.is_set():
        data = stream.read(1024)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(output_file_path.replace('.txt', '.wav'), 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"Recording completed. Output saved to {output_file_path.replace('.txt', '.wav')}")

if __name__ == "__main__":
    args = setup_argparse()

    model_map = {
        "t": "tiny",
        "b": "base",
        "s": "small",
        "m": "medium",
        "l": "large"
    }

    if args.file and (args.source or args.device):
        print("Error: Cannot mix file transcription with live audio source arguments.")
        exit(1)

    if args.model in model_map:
        model_choice = model_map[args.model]
    else:
        print("Available Whisper model sizes:")
        for key, model in model_map.items():
            print(f"{key}: {model} ({'fastest, least accurate' if model == 'tiny' else 'slowest, most accurate' if model == 'large' else 'balanced'})")
        model_key = input("Select model size (e.g., 'b' for base): ").lower()
        model_choice = model_map.get(model_key, "base")

        if args.live_record or input("Do you want to record live audio? (y/n): ").lower() == 'y':
            recording_thread = threading.Thread(target=record_live_audio, args=(output_file,))
            recording_thread.start()

    # Prompt for live recording if the --record argument is not provided
    if not args.record:
        user_wants_to_record = input("Do you want to record live audio? (y/n): ").lower() == 'y'
    else:
        user_wants_to_record = True

    if args.file:
        model = whisper.load_model(model_choice)
        transcribe_audio_file(model, args.file)
    else:
        model = whisper.load_model(model_choice)
        if args.source:
            source = 'o' if args.source.lower() == 'o' else 'i'
        else:
            source = input("Choose audio source - Input (i) or Output (o): ").lower()

        devices = list_devices('output' if source == 'o' else 'input')
        device_num = args.device if args.device is not None else None
        device = get_device_choice(devices, device_num)
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        output_file = os.path.join(output_dir, f"{timestamp}.txt")

        if user_wants_to_record:
            recording_thread = threading.Thread(target=record_live_audio, args=(output_file,))
            recording_thread.start()

        processing_thread = threading.Thread(target=process_audio_chunks, args=(model, output_file))
        processing_thread.start()

        try:
            with sd.InputStream(device=device, channels=1, callback=audio_callback, samplerate=16000):
                print("Listening... (Press Enter to stop)")
                input()
                print("\nStopping and exiting...")
                stop_signal.set()
        except KeyboardInterrupt:
            print("\nStopped listening.")
        except Exception as e:
            print("An error occurred:", e)
        finally:
            processing_thread.join()

        if user_wants_to_record:
            recording_thread.join()