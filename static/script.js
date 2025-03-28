
const previewBtn = document.getElementById('previewTab')
const compareBtn = document.getElementById('compareTab')
const outputVideoOnly = document.getElementById('outputVideoOnly')
const compareVideo = document.getElementById('compareVideo')
const startDubbingBtn = document.getElementById('startDubbing')
const status = document.getElementById('status')
const downloadLink = document.getElementById('downloadLink')
const targetLanguage = document.getElementById('tarLang')
const originalVideoCompare = document.getElementById('originalVideoCompare')
const dubbedVideoCompare = document.getElementById('dubbedVideoCompare')
const dubbedVideoDisplay = document.getElementById('dubbedVideoDisplay')
const downloadLinkInput = document.getElementById("downloadYTLink")
const downloadForm = document.getElementById("downloadForm")
const toggleShowBtn = document.getElementById("toggleShow")
const transcribeText = document.getElementById("transcribeText")
const translatedText = document.getElementById("translatedText")
const toggleShowBtnDubbed = document.getElementById("toggleShowBtn")
const videoFrame = document.getElementById("videoFrame")

toggleShowBtn.addEventListener('click', ()=>{
    if(toggleShowBtn.innerHTML == "Show"){
        transcribeText.style.display = "block";
        toggleShowBtn.innerHTML = "Hide";
    }else{
        transcribeText.style.display = "none";
        toggleShowBtn.innerHTML = "Show";
    }
})

toggleShowBtnDubbed.addEventListener('click', ()=>{
    if(toggleShowBtnDubbed.innerHTML == "Show"){
        translatedText.style.display = "block";
        toggleShowBtnDubbed.innerHTML = "Hide";
    }else{
        translatedText.style.display = "none";
        toggleShowBtnDubbed.innerHTML = "Show";
    }
})

// Switch between tabs
previewBtn.addEventListener('click', () => {
    compareBtn.classList.remove('active');
    compareVideo.style.display = "none";
    previewBtn.classList.add('active');
    outputVideoOnly.style.display = "block";
});

compareBtn.addEventListener('click', () => {
    previewBtn.classList.remove('active');
    outputVideoOnly.style.display = "none";
    compareBtn.classList.add('active');
    compareVideo.style.display = "flex";
});

// Start dubbing
downloadForm.addEventListener('submit', async (e) => {
    e.preventDefault()
    startDubbingBtn.innerHTML = "Processing...";
    startDubbingBtn.disabled = "disabled"
    status.innerHTML = "Status: Please wait, its processing...";
    status.style.color = "green";
    let link = downloadLinkInput.value.split("https://youtu.be/");
    let videoId = link[1];
    let newLink = `https://www.youtube.com/embed/${videoId}`
    videoFrame.style.display = "block";
    videoFrame.src = newLink;
    originalVideoCompare.style.visibility = "visible";
    originalVideoCompare.src = newLink;
    
    try {
        // Start downloading video
        const downloadData = new FormData();
        downloadData.append('link', downloadLinkInput.value);
    
        let response = await fetch("/download", {
            method: 'POST',
            body: downloadData
        })
        let data = await response.json();

        if (!response.ok) throw new Error("Error during downloading video.");

        let videoName = data.videoName;
        status.innerHTML = "Status: " + data.message;
        status.style.color = "green";

        // Step 1: Start transcription
        const formData = new FormData();
        formData.append('video', videoName);

        response = await fetch('/start', {
            method: 'POST',
            body: formData
        });
        data = await response.json();

        if (!response.ok) throw new Error("Error during transcribing text.");

        transcribeText.innerHTML = data.text;
        let original_video_path = data.original_video_path;
        // let original_video_path = "./uploads/_How to Upload 3 Minute Shorts on YouTube (in Hindi).mp4";
        let filenameWithExtension = data.filenameWithExtension;
        // let filenameWithExtension = "_How to Upload 3 Minute Shorts on YouTube (in Hindi).mp4";
        status.innerHTML = "Status: " + data.message;
        status.style.color = "green";
        // let tx = "Agar aap youtube pe shorts "

        // Step 2: Request translation
        const textGeneratedData = new FormData();
        textGeneratedData.append('generatedText', data.text);
        textGeneratedData.append('targetLanguage', targetLanguage.value);

        response = await fetch('/translate', {
            method: 'POST',
            body: textGeneratedData
        });
        data = await response.json();

        if (!response.ok) throw new Error("Error during translating.");

        translatedText.innerHTML = data.text;
        status.innerHTML = "Status: " + data.message;
        status.style.color = "green";

        // Step 3: Final dubbing process
        const translatedData = new FormData();
        translatedData.append('translatedText', data.text);
        translatedData.append('filenameWithExtension', filenameWithExtension);
        translatedData.append('original_video_path', original_video_path);

        response = await fetch('/finish', {
            method: 'POST',
            body: translatedData
        });
        data = await response.json();

        if (!response.ok) throw new Error("Error in the process of dubbing.");

        status.innerHTML = "Status: " + data.message;
        status.style.color = "green";

        setTimeout(() => {
            status.innerHTML = '';
        }, 3000);

        filename = data.filename;
        downloadLink.href = data.dubbed_url;  // Use returned URL from backend
        downloadLink.download = data.filename;
        dubbedVideoCompare.style.visibility = "visible";
        dubbedVideoDisplay.style.display = "block";
        dubbedVideoCompare.src = data.dubbed_url;
        dubbedVideoDisplay.src = data.dubbed_url;
        startDubbingBtn.innerHTML = "Start Dubbing Process";
        startDubbingBtn.removeAttribute("disabled")

    } catch (err) {
        status.innerHTML = "Status: " + err.message;
        status.style.color = "red";
        console.error(err);

        setTimeout(() => {
            status.innerHTML = '';
        }, 3000);
    }
});
