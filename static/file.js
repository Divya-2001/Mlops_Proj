let btnDownload = document.querySelector('body div button');
// let img = document.querySelector('body figure img');
let img = document.getElementById("bigFilteredImage")


// Must use FileSaver.js 2.0.2 because 2.0.3 has issues.
btnDownload.addEventListener('click', () => {
    let imagePath = img.getAttribute("src")
    let fileName = getFileName(imagePath);
    saveAs(imagePath, fileName);
});

function getFileName(str) {
    return str.substring(str.lastIndexOf('/') + 1)
}