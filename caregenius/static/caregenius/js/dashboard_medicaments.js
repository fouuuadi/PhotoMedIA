console.log("medicaments.js");

const dropArea = document.getElementById('dropArea');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const preview = document.getElementById('preview');

dropArea.addEventListener('click', () => fileInput.click());
browseBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    fileInput.click();
});

dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropArea.style.background = '#e3f2fd';
});
dropArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropArea.style.background = '#f4fbff';
});
dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dropArea.style.background = '#f4fbff';
    const file = e.dataTransfer.files[0];
    handleFile(file);
});
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    handleFile(file);
});

function handleFile(file) {
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
            preview.innerHTML = `<img src="${e.target.result}" alt="Aperçu">`;
        };
        reader.readAsDataURL(file);
    } else {
        preview.innerHTML = '';
    }
}

// Loading et résultat
const form = document.getElementById('uploadForm');
const loadingContainer = document.getElementById('lottie-loading');
const resultat = document.getElementById('resultat');

// Initialisation de l'animation Lottie avec l'URL dynamique
const lottieUrl = loadingContainer.getAttribute('data-lottie-url');
let lottieInstance = lottie.loadAnimation({
    container: loadingContainer,
    renderer: 'svg',
    loop: true,
    autoplay: false,
    path: lottieUrl
});

function afficherLoading() {
    loadingContainer.style.display = 'block';
    resultat.innerHTML = '';
    lottieInstance.goToAndPlay(0, true);
}

function cacherLoading() {
    loadingContainer.style.display = 'none';
    lottieInstance.stop();
}

form.addEventListener('submit', function(e) {
    e.preventDefault();
    afficherLoading();
    // Simule un appel AJAX (remplace par ton fetch réel)
    fetch('/ta/route/api/', {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(data => {
        cacherLoading();
        resultat.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    })
    .catch(error => {
        cacherLoading();
        resultat.innerHTML = "<span style='color:red'>Erreur lors du traitement.</span>";
    });
});
