console.log("dashboard_medicaments.js");

// Helpers pour afficher/cacher via les classes .none / .visible
function show(el) {
  el.classList.remove('none');
  el.classList.add('visible');
}
function hide(el) {
  el.classList.remove('visible');
  el.classList.add('none');
}

// Récupération des éléments
const uploadScreen   = document.getElementById('upload-screen');
const loadingScreen  = document.getElementById('loading-screen');
const resultScreen   = document.getElementById('result-screen');
const resetBtn       = document.getElementById('resetBtn');

const dropArea       = document.getElementById('dropArea');
const fileInput      = document.getElementById('fileInput');
const browseBtn      = document.getElementById('browseBtn');
const preview        = document.getElementById('preview');

const form           = document.getElementById('uploadForm');
const loadingDiv     = document.getElementById('lottie-loading');
const resultat       = document.getElementById('resultat');

const overlay = document.getElementById('page-overlay');


// Créer ou récupérer le container d’erreur sous le preview
let uploadError = document.getElementById('uploadError');
if (!uploadError) {
  uploadError = document.createElement('div');
  uploadError.id = 'uploadError';
  uploadError.style.color = 'red';
  uploadError.style.marginTop = '0.5em';
  preview.after(uploadError);
}

// Initialisation de lottie
const lottieUrl = loadingDiv.getAttribute('data-lottie-url');
const lottieInstance = lottie.loadAnimation({
  container: loadingDiv,
  renderer: 'svg',
  loop: true,
  autoplay: false,
  path: lottieUrl
});

// Fonctions pour passer d’un écran à l’autre
function showUpload() {
  show(uploadScreen);
  hide(loadingScreen);
  hide(resultScreen);
  hide(resetBtn);
  overlay.classList.add('none');
  uploadError.textContent = '';   // reset erreur
}

function showLoading() {
  hide(uploadScreen);
  show(loadingScreen);
  hide(resultScreen);
  hide(resetBtn);
  overlay.classList.remove('none');
  lottieInstance.goToAndPlay(0, true);
}

function showResult(dataHTML) {
  hide(uploadScreen);
  hide(loadingScreen);
  show(resultScreen);
  show(resetBtn);
  lottieInstance.stop();
  resultat.innerHTML = dataHTML;
  overlay.classList.add('none');
}

// Drag & drop + preview
dropArea.addEventListener('click',  () => fileInput.click());
browseBtn.addEventListener('click', e => { e.stopPropagation(); fileInput.click(); });

dropArea.addEventListener('dragover', e => {
  e.preventDefault();
  dropArea.style.background = '#e3f2fd';
});
dropArea.addEventListener('dragleave', e => {
  e.preventDefault();
  dropArea.style.background = '#f4fbff';
});
dropArea.addEventListener('drop', e => {
  e.preventDefault();
  dropArea.style.background = '#f4fbff';
  handleFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener('change', e => handleFile(e.target.files[0]));

function handleFile(file) {
  if (file && file.type.startsWith('image/')) {
    uploadError.textContent = '';
    const reader = new FileReader();
    reader.onload = e => {
      preview.innerHTML = `<img src="${e.target.result}" style="max-width:100%;">`;
    };
    reader.readAsDataURL(file);
  } else {
    preview.innerHTML = '';
  }
}

// Soumission du formulaire avec validation
form.addEventListener('submit', e => {
  e.preventDefault();
  // **Validation : y a-t-il un fichier ?**
  if (!fileInput.files.length) {
    uploadError.textContent = "Veuillez sélectionner une image avant de valider.";
    return;
  }

  showLoading();
  fetch(form.action, {
    method: 'POST',
    body: new FormData(form)
  })
  .then(r => r.json())
  .then(data => {
    let html;
    if (data.result) {
        html = `<pre class="result-block">${data.result}</pre>`;
      } else {
        html = `<pre class="result-block"><span style="color:red">Erreur : ${data.error||'Analyse impossible'}</span></pre>`;
      }
    showResult(html);
  })
  .catch(() => {
    showResult(`<span style="color:red">Erreur lors du traitement.</span>`);
  });
});

// Bouton reset
resetBtn.addEventListener('click', () => {
  form.reset();
  preview.innerHTML = '';
  uploadError.textContent = '';
  showUpload();
});

// Au chargement de la page, on démarre sur l’écran d’upload
document.addEventListener('DOMContentLoaded', showUpload);
