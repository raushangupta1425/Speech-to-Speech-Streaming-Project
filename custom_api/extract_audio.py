# Importing required library
import ffmpeg

# Extract audio from video
class ExtractAudioFromVideo:
    """ Extracting audio file from given video file"""
    
    def extract_audio(self, video_path):
        try:
            output_audio_path = "./extracted_audio.mp3"
            print('Extracting audio from video...')
            ffmpeg.input(video_path).output(output_audio_path).run()
            print('Audio extracted successfully!')
            return output_audio_path
        except Exception as e:
            print(f" File not found! {e}")

# Note to use :
# from custom_api.extract_audio import Extract

# extract = ExtractAudioFromVideo()
# path = extract.extract_audio("video.mp4")
# print(path)