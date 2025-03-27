
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
const downloadLinkInput = document.getElementById("downloadLink")
const downloadForm = document.getElementById("downloadForm")
const downloadBtn = document.getElementById("downloadBtn")

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
startDubbingBtn.addEventListener('click', () => {
    status.innerHTML = "Status: Please wait it's take time approx 10 minutes...";
    status.style.color= "green";
    const formData = new FormData();
        formData.append('video', filename);
        formData.append('targetLanguage', targetLanguage.value);
        formData.append('sourceLanguage', sourceLanguage.value);

        fetch('/start', {
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
            downloadLink.href = data.dubbed_url;  // Use returned URL from backend
            downloadLink.download = data.filename;
            dubbedVideoCompare.src = data.dubbed_url;
            dubbedVideoDisplay.src = data.dubbed_url;
            // dubbedVideoCompare.load();
            // dubbedVideoDisplay.load();
        })
        .catch(err => {
            status.innerHTML = "Status: Error in process of dubbing.";
            status.style.color= "red";
            setTimeout(()=>{
                status.innerHTML = '';
            },3000)
            console.error(err)
        });
})