# Importing required libraries
import os 
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import asyncio
from custom_api.translate_text import TranslateText
import shutil
from custom_api.correct_text import CorrectText

class AudioTranscriber:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def transcribe_audio(self, path):
        """Recognize speech in a single audio file"""
        with sr.AudioFile(path) as source:
            audio_listened = self.recognizer.record(source)
            text = self.recognizer.recognize_google(audio_listened)
        return text

    def get_large_audio_transcription_on_silence(self, path, targetLanguage, sourceLanguage):
        print('Converting audio to text...')
        sound = AudioSegment.from_file(path)
        chunks = split_on_silence(sound,
            min_silence_len=500,
            silence_thresh=sound.dBFS - 10,
            keep_silence=500,
        )
        folder_name = "audio_chunks"
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        whole_text = ""
        for i, audio_chunk in enumerate(chunks, start=1):
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            try:
                text = self.transcribe_audio(chunk_filename)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                # text = CorrectText.correct_text(text)
                translated_text = asyncio.run(TranslateText().translate_text(text, targetLanguage, sourceLanguage))
                whole_text += translated_text
        
        if os.path.isdir(folder_name):
            shutil.rmtree(folder_name)
        if os.path.isfile("./extracted_audio.mp3"):
            os.remove("./extracted_audio.mp3")
        print('Text generated successfully! \n')
        return whole_text
