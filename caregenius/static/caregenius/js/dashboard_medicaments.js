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