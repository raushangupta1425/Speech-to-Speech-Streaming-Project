# Importing required libraries
from moviepy import VideoFileClip, AudioFileClip
import os

class MergeVideoAudio:
    # Step 5: Merge translated audio with original's video
    def merge_audio_with_video(self, video_path, audio_path, dubbedVideoPath= './dubbed_videos/dubbed_video.mp4'):
        try:
            print('Merging audio with video...')
            output_path = './dubbed_videos/' + dubbedVideoPath + '_dubbed.mp4'
            # Load the video and audio files
            video_clip = VideoFileClip(video_path)
            audio_clip = AudioFileClip(audio_path)

            # Set the audio for the video clip
            final_clip = video_clip.with_audio(audio_clip)

            # Write the combined clip to a new video file
            final_clip.write_videofile(output_path, fps=24)
            if os.path.isfile("./translatedAudio.mp3"):
                os.remove("./translatedAudio.mp3")
            print('\nNew dubbed video saved as dubbed_video.mp4')
            print('Audio merging with original video successfully!')
        except Exception as e:
            print(f" Error in mergeing! {e}")
