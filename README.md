
# WhisperCLI: Audio Transcription Tool

[English](README.md) | [Русский](README.ru.md)

WhisperCLI is a powerful command-line tool for transcribing audio and video files based on the Whisper model by OpenAI. This tool allows you to easily convert speech to text with support for multiple languages and the ability to process specific segments of a file.

## Features

- Support for various audio and video file formats (MP3, MP4, WAV, etc.)
- Choice of Whisper model (tiny, base, small, medium, large)
- Transcription of specific time intervals
- Support for multiple languages
- Silent mode with an option for detailed logs
- Save results to a file
- Simple command-line interface

## Requirements

- Python 3.7+
- PyTorch
- Transformers
- Pydub
- NumPy

## Installation

1. Clone the repository:

```
git clone https://github.com/Hole-code/WhisperCLI.git

cd WhisperCLI
```

3. Install the dependencies:

```
pip install -r requirements.txt
```

## System Installation

To use WhisperCLI as a system utility, follow these steps:

1. Create a `whispercli` file with the following content:
   ```bash
   #!/bin/bash
   python3 /full/path/to/whisper_cli.py "$@"
   ```

Replace /full/path/to/whisper_cli.py with the actual path to your script.

2. Make the file executable:
```
chmod +x whispercli
```

3. Move the file to a directory that is in the system PATH:
```
sudo mv whispercli /usr/local/bin/
```
4. Now you can run the utility from any directory by simply typing whispercli:

```
whispercli -n path/to/audio_file.mp3
```

Note: Make sure you have administrative rights to create a symbolic link in the system directory.

## Usage

Basic usage:

```
whispercli -n path/to/your/audio_file.mp3
```

### Parameters

- `-n`, `--name`: Path to the audio file (required)
- `-s`, `--start`: Start time for transcription (format: SS, MM:SS, or HH:MM:SS)
- `-e`, `--end`: End time for transcription (format: SS, MM:SS, or HH:MM:SS)
- `-l`, `--language`: Expected language of the audio (e.g., 'en' for English)
- `-m`, `--model`: Whisper model size (tiny, base, small, medium, large)
- `-o`, `--output`: Output file name to save the transcription
- `-v`, `--verbose`: Output detailed logs

### Examples

1. Transcribe the entire file:
```
whispercli -n audio.mp3
```

2. Transcribe a specific segment:

```
whispercli -n video.mp4 -s 5:30 -e 10:00
```

3. Specify language and model:
```
whispercli -n audio.wav -l en -m medium
```

4. Save the result to a file:

```
whispercli -n audio.mp3 -o transcription.txt
```

5. Use all options with detailed logs:

```
whispercli -n long_video.mp4 -s 1:00:00 -e 1:30:00 -l en -m large -o result.txt -v
```

## Notes

- Working with MP3 files may require installing ffmpeg.
- Large Whisper models may require significant computational resources.
- On the first run, the script will download the selected Whisper model, which may take some time.

## Contributing

We welcome contributions! If you have ideas for improvements or have found a bug, please create an issue or submit a pull request.

## License

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file.

## Acknowledgments

- OpenAI for creating the Whisper model
- The developers of PyTorch, Transformers, and Pydub libraries
