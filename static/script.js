
const previewBtn = document.getElementById('previewTab')
const compareBtn = document.getElementById('compareTab')
const outputVideoOnly = document.getElementById('outputVideoOnly')
const compareVideo = document.getElementById('compareVideo')
const uploaderBtn = document.getElementById('uploader')
const selectVideoInput = document.getElementById('selectVideo')
const startDubbingBtn = document.getElementById('startDubbing')
const status = document.getElementById('status')
const disUpVid = document.getElementById('disUpVid')
const downloadLink = document.getElementById('downloadLink')
const targetLanguage = document.getElementById('tarLang')
const sourceLanguage = document.getElementById('sourLang')
const originalVideoCompare = document.getElementById('originalVideoCompare')
const dubbedVideoCompare = document.getElementById('dubbedVideoCompare')
const dubbedVideoDisplay = document.getElementById('dubbedVideoDisplay')
const downloadLinkInput = document.getElementById("downloadYTLink")
const downloadForm = document.getElementById("downloadForm")
const downloadBtn = document.getElementById("downloadBtn")
const toggleShowBtn = document.getElementById("toggleShow")
const transcribeText = document.getElementById("transcribeText")
const translatedText = document.getElementById("translatedText")
const toggleShowBtnDubbed = document.getElementById("toggleShowBtn")

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

downloadForm.addEventListener('submit', (e) => {
    e.preventDefault()
    downloadBtn.innerHTML = "Please wait...";
    downloadBtn.disabled = "disabled"

    const formData = new FormData();
        formData.append('link', downloadLinkInput.value);
    
    fetch("/download", {
        method: 'POST',
        body: formData
    })
    .then(res=> res.json())
    .then(data=>{
        alert(data.message)
        downloadBtn.innerHTML = "Download";
        downloadBtn.removeAttribute("disabled")
    })
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

// Upload video functionality
let filename;
uploaderBtn.addEventListener('click', ()=>{
    const file = selectVideoInput.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            status.innerHTML = "Status: " + data.message;
            status.style.color= "green";
            setTimeout(()=>{
                status.innerHTML = '';
            },3000)
            filename = data.filename;
            disUpVid.src = data.video_url;  // Set the uploaded video URL from response
            originalVideoCompare.src = data.video_url;
            // disUpVid.load(); // Reload the video element with the new source
            // originalVideoCompare.load();
        })
        .catch(err => {
            status.innerHTML = "Status: Error in uploading.";
            status.style.color= "red";
            setTimeout(()=>{
                status.innerHTML = '';
            },3000)
            console.error(err)
        });
    } else {
        alert('No file selected');
    }
})

// Start dubbing
let filenameWithExtension;
let original_video_path;

startDubbingBtn.addEventListener('click', async () => {
    status.innerHTML = "Status: Please wait, it takes approximately 10 minutes...";
    status.style.color = "green";

    try {
        // Step 1: Start transcription
        const formData = new FormData();
        formData.append('video', filename);

        let response = await fetch('/start', {
            method: 'POST',
            body: formData
        });
        let data = await response.json();

        if (!response.ok) throw new Error("Error during transcribing text.");

        transcribeText.innerHTML = data.text;
        original_video_path = data.original_video_path;
        filenameWithExtension = data.filenameWithExtension;
        status.innerHTML = "Status: " + data.message;
        status.style.color = "green";

        // Step 2: Request translation
        const textGeneratedData = new FormData();
        textGeneratedData.append('generatedText', data.text);
        textGeneratedData.append('targetLanguage', targetLanguage.value);
        textGeneratedData.append('sourceLanguage', sourceLanguage.value);

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
        dubbedVideoCompare.src = data.dubbed_url;
        dubbedVideoDisplay.src = data.dubbed_url;

    } catch (err) {
        status.innerHTML = "Status: " + err.message;
        status.style.color = "red";
        console.error(err);

        setTimeout(() => {
            status.innerHTML = '';
        }, 3000);
    }
});
