const input = document.querySelector("#image-input");
const dropzone = document.querySelector("#dropzone");
const uploadState = document.querySelector("#upload-state");
const processingState = document.querySelector("#processing-state");
const resultState = document.querySelector("#result-state");
const errorMessage = document.querySelector("#error-message");
const sourceImage = document.querySelector("#source-image");
const resultImage = document.querySelector("#result-image");
const fileName = document.querySelector("#file-name");
const comparison = document.querySelector("#comparison");
const downloadButton = document.querySelector("#download-button");
const themeToggle = document.querySelector(".theme-toggle");
let downloadUrl = null;

function setError(message = "") { errorMessage.textContent = message; errorMessage.hidden = !message; }
function setSplit(value) { const split = Math.max(0, Math.min(100, value)); comparison.style.setProperty("--split", `${split}%`); comparison.setAttribute("aria-valuenow", String(Math.round(split))); }
function updateSplit(event) { const rect = comparison.getBoundingClientRect(); setSplit(((event.clientX - rect.left) / rect.width) * 100); }

comparison.addEventListener("pointerdown", (event) => { comparison.setPointerCapture(event.pointerId); updateSplit(event); });
comparison.addEventListener("pointermove", (event) => { if (comparison.hasPointerCapture(event.pointerId)) updateSplit(event); });
comparison.addEventListener("keydown", (event) => { const current = Number(comparison.getAttribute("aria-valuenow")); const moves = { ArrowLeft: current - 2, ArrowRight: current + 2, Home: 0, End: 100 }; if (event.key in moves) { event.preventDefault(); setSplit(moves[event.key]); } });
downloadButton.addEventListener("click", () => { if (!downloadUrl) return; const link = document.createElement("a"); link.href = downloadUrl; link.download = "cutout.png"; link.click(); });

async function processImage(file) {
  if (!file) return;
  if (!["image/jpeg", "image/png", "image/webp"].includes(file.type)) { setError("Upload a PNG, JPEG or WEBP image."); return; }
  if (file.size > 15 * 1024 * 1024) { setError("The image exceeds the 15 MB upload limit."); return; }
  setError(); uploadState.hidden = true; resultState.hidden = true; processingState.hidden = false;
  const sourceUrl = URL.createObjectURL(file);
  try {
    const form = new FormData(); form.append("image", file);
    const response = await fetch("/api/remove-background", { method: "POST", body: form });
    if (!response.ok) { const body = await response.json().catch(() => ({})); throw new Error(body.detail || "The image could not be processed."); }
    const resultBlob = await response.blob();
    if (downloadUrl) URL.revokeObjectURL(downloadUrl);
    downloadUrl = URL.createObjectURL(resultBlob);
    sourceImage.src = sourceUrl; resultImage.src = downloadUrl; fileName.textContent = file.name; setSplit(50);
    processingState.hidden = true; resultState.hidden = false;
  } catch (error) {
    URL.revokeObjectURL(sourceUrl); processingState.hidden = true; uploadState.hidden = false; setError(error.message);
  }
}
input.addEventListener("change", () => processImage(input.files[0]));
["dragenter", "dragover"].forEach((name) => dropzone.addEventListener(name, (event) => { event.preventDefault(); dropzone.classList.add("dragover"); }));
["dragleave", "drop"].forEach((name) => dropzone.addEventListener(name, (event) => { event.preventDefault(); dropzone.classList.remove("dragover"); }));
dropzone.addEventListener("drop", (event) => processImage(event.dataTransfer.files[0]));

const savedTheme = localStorage.getItem("cutout-theme");
if (savedTheme === "dark") document.documentElement.dataset.theme = "dark";
function updateThemeControl() { const dark = document.documentElement.dataset.theme === "dark"; themeToggle.setAttribute("aria-pressed", String(dark)); themeToggle.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode"); }
themeToggle.addEventListener("click", () => { const dark = document.documentElement.dataset.theme === "dark"; document.documentElement.dataset.theme = dark ? "light" : "dark"; localStorage.setItem("cutout-theme", dark ? "light" : "dark"); updateThemeControl(); });
updateThemeControl();
