# Import required libraries
from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
import os
import yt_dlp

# Import custom APIs libraries
from custom_api.extract_audio import ExtractAudioFromVideo
from custom_api.audio_to_text import AudioTranscriber
from custom_api.text_to_speech import TextToSpeech
from custom_api.merge_video_with_speech import MergeVideoAudio

app = Flask(__name__)

@app.route('/dubbed_videos/<path:filename>')
def dubbed_videos(filename):
    return send_from_directory('dubbed_videos', filename)

@app.route('/')
def home():
    return render_template('index.html')

UPLOAD_FOLDER = 'uploads'  # adjust according to your project structure
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        video_url = url_for('uploaded_file', filename=filename)
        return jsonify({
            'message': 'Video uploaded successfully.',
            'filename': filename,
            'video_url': video_url
        })
    else:
        return jsonify({'message': 'No file uploaded'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.form.get("link")
        current_folder = os.path.dirname(os.path.abspath(__file__))
        output_path = current_folder+"/downloads/"

        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",  # Forces MP4 format
            "merge_output_format": "mp4",  # Ensures final output is MP4
            "outtmpl": f"{output_path}/%(title)s.%(ext)s",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({'message': 'Download successfully!'})
    except Exception as e:
        return jsonify({'message': 'File already exist!'})


@app.route('/start', methods=['POST'])
def start():
    filenameWithExtension = request.form.get('video')
    targetLanguage = request.form.get('targetLanguage')
    sourceLanguage = request.form.get('sourceLanguage')
    videoPath = './uploads/' + filenameWithExtension
    # Step 1
    extract = ExtractAudioFromVideo()
    original_video_path = videoPath
    extractedAudioFileName = extract.extract_audio(original_video_path)

    # Step 2 and 3
    translated_text = AudioTranscriber().get_large_audio_transcription_on_silence(extractedAudioFileName, targetLanguage, sourceLanguage)
    # print(translated_text)
    
    # Step 4
    audioFileName = TextToSpeech().text_to_speech(translated_text) # must give text as argument

    # Step 5
    filenameWithoutExtension = filenameWithExtension.split('.')
    dubbedVideoPath = filenameWithoutExtension[0]
    merger = MergeVideoAudio()
    dubbedVideoFilename = merger.merge_audio_with_video(original_video_path, audioFileName, dubbedVideoPath)
    # Process dubbing logic here...
    dubbed_url = url_for('dubbed_videos', filename=dubbedVideoFilename)  # Generates the correct URL

    return jsonify({
        'message': 'Dubbing completed successfully.',
        'filename': dubbedVideoFilename,
        'dubbed_url': dubbed_url
    })

    
# Run the app
if __name__ == '__main__':
    app.run(debug=True)
