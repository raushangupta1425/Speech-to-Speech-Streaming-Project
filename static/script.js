
const previewBtn = document.getElementById('previewTab')
const compareBtn = document.getElementById('compareTab')
const outputVideoOnly = document.getElementById('outputVideoOnly')
const compareVideo = document.getElementById('compareVideo')
const uploaderBtn = document.getElementById('uploader')
const selectVideoInput = document.getElementById('selectVideo')
const startDubbingBtn = document.getElementById('startDubbing')
const status = document.getElementById('status')

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