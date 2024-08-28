import os
import sys
import torch
import argparse
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from pydub import AudioSegment
import numpy as np
import warnings
import logging
from transformers import logging as transformers_logging
from io import StringIO

def time_to_ms(time_str):
    if time_str is None:
        return 0
    parts = time_str.split(':')
    if len(parts) == 1:
        return int(float(parts[0]) * 1000)
    elif len(parts) == 2:
        return int((int(parts[0]) * 60 + float(parts[1])) * 1000)
    elif len(parts) == 3:
        return int((int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])) * 1000)
    else:
        raise ValueError("Неверный формат времени")

def suppress_output(func):
    def wrapper(*args, **kwargs):
        verbose = kwargs.get('verbose', False)
        if not verbose:
            # Перенаправляем stdout и stderr
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = StringIO()
            sys.stderr = StringIO()
            
            # Устанавливаем переменные окружения для подавления предупреждений TensorFlow
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
            
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            if not verbose:
                # Восстанавливаем stdout и stderr
                sys.stdout = old_stdout
                sys.stderr = old_stderr
    return wrapper

@suppress_output
def transcribe_audio(file_path, model_size="base", chunk_length_s=30, start_time=None, end_time=None, language=None, verbose=False):
    if not verbose:
        warnings.filterwarnings("ignore")
        transformers_logging.set_verbosity_error()
        logging.getLogger("pydub.converter").setLevel(logging.ERROR)

    processor = WhisperProcessor.from_pretrained(f"openai/whisper-{model_size}")
    model = WhisperForConditionalGeneration.from_pretrained(f"openai/whisper-{model_size}")
    
    if language:
        model.config.forced_decoder_ids = processor.get_decoder_prompt_ids(language=language)
    else:
        model.config.forced_decoder_ids = None

    audio = AudioSegment.from_file(file_path)
    
    start_ms = time_to_ms(start_time)
    end_ms = time_to_ms(end_time) if end_time else len(audio)
    audio = audio[start_ms:end_ms]
    
    audio = audio.set_channels(1).set_frame_rate(16000)

    chunk_length_ms = chunk_length_s * 1000
    chunks = [audio[i:i+chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

    transcription = ""

    for i, chunk in enumerate(chunks):
        if verbose:
            print(f"Обработка чанка {i+1}/{len(chunks)}...")
        
        chunk_array = np.array(chunk.get_array_of_samples()).astype(np.float32) / 32768.0
        input_features = processor(chunk_array, sampling_rate=16000, return_tensors="pt").input_features

        predicted_ids = model.generate(input_features)

        chunk_transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        transcription += chunk_transcription + " "

    return transcription.strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Транскрибация аудио с помощью Whisper")
    parser.add_argument("-n", "--name", required=True, help="Путь к аудио файлу")
    parser.add_argument("-s", "--start", help="Начальное время (формат: SS, MM:SS, или HH:MM:SS)")
    parser.add_argument("-e", "--end", help="Конечное время (формат: SS, MM:SS, или HH:MM:SS)")
    parser.add_argument("-l", "--language", help="Ожидаемый язык аудио (например, 'ru' для русского)")
    parser.add_argument("-m", "--model", default="base", help="Размер модели Whisper (tiny, base, small, medium, large)")
    parser.add_argument("-o", "--output", help="Имя выходного файла для сохранения транскрипции")
    parser.add_argument("-v", "--verbose", action="store_true", help="Выводить подробные логи")

    args = parser.parse_args()

    result = transcribe_audio(
        args.name,
        model_size=args.model,
        start_time=args.start,
        end_time=args.end,
        language=args.language,
        verbose=args.verbose
    )

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        if args.verbose:
            print(f"Транскрипция сохранена в файл: {args.output}")
    else:
        print(result)
