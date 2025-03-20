# INFOSYS_STSS_APP
This project help us to dubbed any video to our preference languages. If we have any video which is in another language,  which we can't able to understand then we can dubbed that video language into our understanding languages.

## Steps for completing project.
1. Audio extraction - ffmpeg package
2. Audio to text
3. text to translated text
4. text to audio
5. mergea audio with original video

## Follow the instruction
1. Audio extraction - ffmpeg package
    - First, you have to download and setup its file in windows or any operating system that you have. For that, click on this link : https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z  the file will be downloaded for windows operating system. For any other operating system, click on this link : https://ffmpeg.org/download.html  then choose your operating system and download the file.

    - Second, Extract the downloaded file and move it in C drive and rename it as "ffmpeg" directory name.

    - Third, Open command prompt as Run as adminstration and type the command setx /m PATH "C:\ffmpeg\bin;%PATH%"  for setup environment variables

    - Fourth, Restart the pc
    
    - Fifth, then in vs terminal run this command "pip install ffmpeg-python" and follow the above code, Now you are ready to extract audios file from videos.
    
github education
claude