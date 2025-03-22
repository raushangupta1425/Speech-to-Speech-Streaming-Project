# Importing required libraries
import ffmpeg
import os 
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import asyncio
from googletrans import Translator

# Step 1: Extract audio from video
def extract_audio(video_path, output_audio_path):
    print('Extracting audio from video...')
    ffmpeg.input(video_path).output(output_audio_path).run()
    print('Audio extracted successfully!')
    return output_audio_path

# Step 2: Convert audio file to text

# create a speech recognition object
r = sr.Recognizer()

# Transcribe the audio file to text
def transcribe_audio(path):
    """ a function to recognize speech in the audio file, so that we don't repeat ourselves in in other functions """
    # use the audio file as the audio source
    with sr.AudioFile(path) as source:
        audio_listened = r.record(source)
        # try converting it to text
        text = r.recognize_google(audio_listened)
    return text

# a function that splits the audio file into chunks on silence and applies speech recognition
def get_large_audio_transcription_on_silence(path):
    print('Converting audio to text...')
    
    """Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks"""
    # open the audio file using pydub
    sound = AudioSegment.from_file(path)  
    # split audio sound where silence is 500 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-10,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio_chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        try:
            text = transcribe_audio(chunk_filename)
        except sr.UnknownValueError as e:
            print("Error:", str(e))
        else:
            text = f"{text.capitalize()}. "
            print(chunk_filename, ":", text)
            translated_text = asyncio.run(translate_text(text))
            whole_text += translated_text
    print('Text generated successfully! \n')
    # return the text for all chunks detected
    return whole_text

# Step 3
# Translator method for translation
translator = Translator()

# Source and target languages
from_lang = 'hi'
to_lang = 'en'

# Translate the text
async def translate_text(source_text):
    async with Translator() as translator:
        result = await translator.translate(source_text, src=from_lang, dest=to_lang)
        return result.text
    
# Run the app
# Step 1
fileName = 'video'
inputPath = './' + fileName + '.mp4'
outputPath = './' + fileName + '.mp3'

outputFileName = extract_audio(inputPath, outputPath)

# Step 2
generated_text = get_large_audio_transcription_on_silence(outputFileName)
print(generated_text)