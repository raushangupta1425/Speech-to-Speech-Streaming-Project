# Importing required libraries
import ffmpeg
import os 
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import asyncio
from googletrans import Translator
import asyncio
import edge_tts
from moviepy import VideoFileClip, AudioFileClip

# Step 1: Extract audio from video
def extract_audio(video_path, output_audio_path):
    print('Extracting audio from video...')
    ffmpeg.input(video_path).output(output_audio_path).run()
    print('Audio extracted successfully!')
    return output_audio_path

# Step 2: Convert audio file to text
# Transcribe the audio file to text
def transcribe_audio(path):
    # create a speech recognition object
    r = sr.Recognizer()
    
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

# Step 3: Translate the text
async def translate_text(source_text):
    # Translator method for translation
    translator = Translator()

    # Source and target languages
    from_lang = 'hi'
    to_lang = 'en'
    
    async with Translator() as translator:
        result = await translator.translate(source_text, src=from_lang, dest=to_lang)
        return result.text

# Step 4: Convert Text to speech
# Top most used voices
Voices = {
    "Spanish": {"male": "es-ES-AlvaroNeural", "female": "es-ES-ElviraNeural"},
    "French": {"male": "fr-FR-HenriNeural", "female": "fr-FR-DeniseNeural"},
    "German": {"male": "de-DE-ConradNeural", "female": "de-DE-KatjaNeural"},
    "Hindi": {"male": "hi-IN-MadhurNeural", "female": "hi-IN-SwaraNeural"},
    "Tamil": {"male": "ta-IN-ValluvarNeural", "female": "ta-IN-PallaviNeural"},
    "Arabic": {"male": "ar-SA-FareedNeural", "female": "ar-SA-ZariyahNeural"},
    "Bengali": {"male": "bn-IN-BashkarNeural", "female": "bn-IN-TanishaaNeural"},
    "Chinese": {"male": "zh-CN-YunxiNeural", "female": "zh-CN-XiaoxiaoNeural"},
    "Portuguese": {"male": "pt-PT-FernandoNeural", "female": "pt-PT-FernandaNeural"},
    "Russian": {"male": "ru-RU-DmitryNeural", "female": "ru-RU-SvetlanaNeural"},
    "English": {"male": "en-US-GuyNeural", "female": "en-US-JennyNeural"}
}

# Convert text to speech
async def text_to_speech(text, output_file, lang="English", gender="male"):
    print('Converting text to speech...')
    try:
        voice = Voices[lang][gender.lower()]
        communicate = edge_tts.Communicate(text, voice, rate="-10%")  # Decrease speed by 10%
        await communicate.save(output_file)
        print(f"Speech saved as {output_file}")
        print('Text converted to speech successfully!')
    except Exception as e:
        print(f"Error while generating speech: {e}")

# Step 5: Merge translated audio with original's video
def merge_audio_with_video(video_path, audio_path, output_path):
    print('Merging audio with video...')
    # Load the video and audio files
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    # Set the audio for the video clip
    final_clip = video_clip.with_audio(audio_clip)

    # Write the combined clip to a new video file
    final_clip.write_videofile(output_path, fps=24)
    print('\nNew dubbed video saved as dubbed_video.mp4')
    print('Audio merging with original video successfully!')
    

# Run the app
# Step 1
fileName = 'video'
inputPath = './' + fileName + '.mp4'
outputPath = './' + fileName + '.mp3'

outputFileName = extract_audio(inputPath, outputPath)

# Step 2 and 3
generated_text = get_large_audio_transcription_on_silence(outputFileName)

# Step 4
output_file = "translatedAudio.mp3"
mytext = f"""{generated_text}"""

# Run the async function
asyncio.run(text_to_speech(mytext, output_file))

# Step 5
original_video_path = inputPath
translated_audio_path = output_file
output_video_path = './dubbed_video.mp4'
merge_audio_with_video(original_video_path, translated_audio_path, output_video_path)