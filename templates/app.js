async function postForm(url, form, responseEl) {
  const formData = new FormData(form);
  try {
    const res = await fetch(url, { method: "POST", body: formData });
    const data = await res.json();

    if (res.ok) {
      responseEl.className = "response success";
      responseEl.textContent = JSON.stringify(data, null, 2);
    } else {
      responseEl.className = "response error";
      responseEl.textContent = data.error || "Something went wrong";
    }
  } catch (err) {
    responseEl.className = "response error";
    responseEl.textContent = "Network error: " + err.message;
  }
}

// Capture form
document.getElementById("captureForm").addEventListener("submit", function (e) {
  e.preventDefault();
  postForm("/capture", this, document.getElementById("captureResponse"));
});

// Match form
document.getElementById("matchForm").addEventListener("submit", function (e) {
  e.preventDefault();
  postForm("/match", this, document.getElementById("matchResponse"));
});
