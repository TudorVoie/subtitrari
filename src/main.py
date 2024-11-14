import time
import math
import ffmpeg
from translate import Translator

from faster_whisper import WhisperModel

input_video = "test.mp4"
input_video_name = input_video.replace(".mp4", "")

tt = Translator(to_lang='ro')

def extract_audio():
    extracted_audio = f"audio-{input_video_name}.wav"
    stream = ffmpeg.input(input_video)
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream, overwrite_output=True)
    return extracted_audio

def transcribe(audio):
    model = WhisperModel("small", device='cpu')
    segments, info = model.transcribe(audio)
    language = info[0]
    print("Transcription language", info[0])
    segments = list(segments)
    for segment in segments:
        # print(segment)
        print("[%.2fs -> %.2fs] %s" %
              (segment.start, segment.end, segment.text))
    return language, segments

def format_time(seconds):

    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"

    return formatted_time

def remove_diacritics(text):
    # Define a translation table for Romanian diacritics
    translation_table = str.maketrans({
        "ă": "a", "Ă": "A",
        "â": "a", "Â": "A",
        "î": "i", "Î": "I",
        "ș": "s", "Ș": "S",
        "ţ": "t", "Ț": "T",
        "ț": "t", "Ţ": "T"
    })
    
    # Apply the translation
    return text.translate(translation_table)


def generate_subtitle_file(language, segments):

    subtitle_file = f"sub-{input_video_name}.{language}.srt"
    text = ""
    for index, segment in enumerate(segments):
        segment_start = format_time(segment.start)
        segment_end = format_time(segment.end)
        text += f"{str(index+1)} \n"
        text += f"{segment_start} --> {segment_end} \n"
        cuvant = tt.translate(segment.text)
        cuvant_bun = remove_diacritics(cuvant)
        text += f"{cuvant_bun}\n"
        text += "\n"
        
    f = open(subtitle_file, "w")
    f.write(text)
    f.close()

    return subtitle_file

def run():

    extracted_audio = extract_audio()
    language, segments = transcribe(audio=extracted_audio)
    subtitle_file = generate_subtitle_file(
    language=language,
    segments=segments
    )
    
run()