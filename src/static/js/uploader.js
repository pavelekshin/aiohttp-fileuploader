var form = document.querySelector("form");
var fileInput = document.querySelector("input");
var submitButton = document.querySelector("button");
var statusMessage = document.getElementById("statusMessage");
var fileListMetadata = document.getElementById("fileListMetadata");
var fileNum = document.getElementById("fileNum");
var progressBar = document.querySelector("progress");
var dropArea = document.getElementById("dropArea");

form.addEventListener("submit", handleSubmit);
fileInput.addEventListener("change", handleInputChange);
dropArea.addEventListener("drop", handleDrop);

initDropAreaHighlightOnDrag();

function load_page(event, pathname){
    event.preventDefault();
    const url = window.location.origin + pathname
    let con = document.getElementById("content");
    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function(e) {
        if(xhr.readyState == 4 && xhr.status == 200) {
        var parser = new DOMParser();
        var doc = parser.parseFromString(xhr.responseText, "text/html");
        var elem = doc.getElementById("content");
        con.replaceWith(elem);
        }
     }


    xhr.open("GET", url, true);
        xhr.setRequestHeader('Content-type', 'text/html');
    xhr.send();
 }

function handleSubmit(event) {
  event.preventDefault();
  showPendingState();
  uploadFiles(fileInput.files);
}

function handleDrop(event) {
  const fileList = event.dataTransfer.files;
  resetFormState();

  try {
    assertFilesValid(fileList);
  } catch (err) {
    updateStatusMessage(err.message);
    return;
  }

  showPendingState();
  uploadFiles(fileList);
}

function handleInputChange(event) {
  resetFormState();

  try {
    assertFilesValid(event.target.files);
  } catch (err) {
    updateStatusMessage(err.message);
    return;
  }

  submitButton.disabled = false;
}

function formatBytes(bytes) {
    var marker = 1024; // Change to 1000 if required
    const decimal = 2; // Change as required
    var kiloBytes = marker; // One Kilobyte is 1024 bytes
    var megaBytes = marker * marker; // One MB is 1024 KB
    var gigaBytes = marker * marker * marker; // One GB is 1024 MB

    // return bytes if less than a KB
    if (bytes < kiloBytes) return bytes + " Bytes";
    // return KB if less than a MB
    else if (bytes < megaBytes) return (bytes / kiloBytes).toFixed(decimal) + " KB";
    // return MB if less than a GB
    else if (bytes < gigaBytes) return (bytes / megaBytes).toFixed(decimal) + " MB";
    // return GB if less than a TB
    else return (bytes / gigaBytes).toFixed(decimal) + " GB";
}

function uploadFiles(files) {
  const url = window.location.origin + window.location.pathname + 'upload'
  const method = "POST";

  const xhr = new XMLHttpRequest();

  xhr.upload.addEventListener("progress", (event) => {
    var loaded = event.loaded;
    var total = event.total;
    updateStatusMessage(`⏳ Загружено ${formatBytes(loaded)} из ${formatBytes(total)}`);
//    updateStatusMessage(`⏳ Uploaded ${event.loaded} bytes of ${event.total}`);
    updateProgressBar(loaded/total);
  });

  xhr.addEventListener("loadend", () => {
    if (xhr.status === 200) {
      updateStatusMessage("✅ Файл успешно загружен");
      renderJSONResponse(files, xhr.response);
//      renderFilesMetadata(fileList);
    } else {
      updateStatusMessage("❌ Возникла ошибка: " + xhr.responseText);
    }

    updateProgressBar(0);
  });

  const data = new FormData();

  for (const file of files) {
    data.append("file", file);
  }

  xhr.open(method, url);
  xhr.send(data);
}

function renderFilesMetadata(fileList) {
  const fileTypes = ["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"];
  fileNum.textContent = fileList.length;
  fileListMetadata.textContent = "";

  for (const file of fileList) {
    const name = file.name;
    let type = file.type;
    const size = formatBytes(file.size);

    if (fileTypes.includes(type)) type = "Excel";

    fileListMetadata.insertAdjacentHTML(
      "beforeend",
      `
        <li>
          <p><strong>Файл:</strong> ${name}</p>
          <p><strong>Тип:</strong> ${type}</p>
          <p><strong>Размер:</strong> ${size}</p>
        </li>`
    );
  }
}

function renderJSONResponse(fileList, response) {
  const json_obj = JSON.parse(response);
  fileNum.textContent = fileList.length;
  fileListMetadata.textContent = "";

  for (const file of json_obj) {
    const name = file.filename;
    let rows = file.rows;

    fileListMetadata.insertAdjacentHTML(
      "beforeend",
      `
        <li>
          <p><strong>Файл:</strong> ${name}</p>
          <p><strong>Строк:</strong> ${rows}</p>
        </li>`
    );
  }
}

function assertFilesValid(fileList) {
  const allowedTypes = ["text/csv", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"];
  const sizeLimit = 1024 * 1024 * 150; // 150 megabyte

  for (const file of fileList) {
    const { name: fileName, size: fileSize } = file;

    if (!allowedTypes.includes(file.type)) {
      console.log(file.type)
      throw new Error(
        `❌ Файл "${fileName}" не может быть загружен. Поддерживаемый формат файлов: CSV, XLS, XLSX`
      );
    }

    if (fileSize > sizeLimit) {
      throw new Error(
        `❌ Файл "${fileName}" не может быть загружен. Максимальный размер файлов - 150 MB`
      );
    }
  }
}

function updateStatusMessage(text) {
  statusMessage.textContent = text;
}

function updateProgressBar(value) {
  const percent = value * 100;
  progressBar.value = Math.round(percent);
}

function showPendingState() {
  submitButton.disabled = true;
  updateStatusMessage("⏳ Pending...");
}

function resetFormState() {
  fileListMetadata.textContent = "";
  fileNum.textContent = "0";

  submitButton.disabled = true;
  updateStatusMessage("🤷‍♂ Пока нет загруженных файлов");
}

function initDropAreaHighlightOnDrag() {
  let dragEventCounter = 0;

  dropArea.addEventListener("dragenter", (event) => {
    event.preventDefault();

    if (dragEventCounter === 0) {
      dropArea.classList.add("highlight");
    }
    dragEventCounter += 1;
  });

  dropArea.addEventListener("dragover", (event) => {
    event.preventDefault();

    // in case of non triggered dragenter!
    if (dragEventCounter === 0) {
      dragEventCounter = 1;
    }
  });

  dropArea.addEventListener("dragleave", (event) => {
    event.preventDefault();

    dragEventCounter -= 1;
    if (dragEventCounter <= 0) {
      dragEventCounter = 0;
      dropArea.classList.remove("highlight");
    }
  });

  dropArea.addEventListener("drop", (event) => {
    event.preventDefault();
    dragEventCounter = 0;
    dropArea.classList.remove("highlight");
  });
}
