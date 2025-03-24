from custom_api.extract_audio import ExtractAudioFromVideo
from custom_api.audio_to_text import AudioTranscriber
from custom_api.text_to_speech import TextToSpeech
from custom_api.merge_video_with_speech import MergeVideoAudio

# Step 1
extract = ExtractAudioFromVideo()
original_video_path = "video.mp4"
extractedAudioFileName = extract.extract_audio(original_video_path)

# Step 2 and 3
translated_text = AudioTranscriber().get_large_audio_transcription_on_silence(extractedAudioFileName)

# Step 4
audioFileName = TextToSpeech().text_to_speech(translated_text) # must give text as argument

# Step 5
merger = MergeVideoAudio()
merger.merge_audio_with_video(original_video_path, audioFileName)