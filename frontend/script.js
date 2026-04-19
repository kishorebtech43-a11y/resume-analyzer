async function analyze() {
    let resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "⏳ Analyzing... Please wait";

    let fileInput = document.getElementById("resume");
    let jobDesc = document.getElementById("jobDesc").value;

    let formData = new FormData();
    formData.append("resume", fileInput.files[0]);
    formData.append("job_desc", jobDesc);

    let response = await fetch("https://resume-analyzer-backend-7h2h.onrender.com/analyze", {
        method: "POST",
        body: formData
    });

    let data = await response.json();

    resultDiv.innerHTML = `
    <h2>Score: ${data.match_percentage}%</h2>
    <h3>Status: ${data.rating}</h3>

    <p><b>✅ Matched Skills:</b><br>
    ${data.matched_skills.join(", ") || "None"}</p>

    <p><b>❌ Missing Skills:</b><br>
    ${data.missing_skills.join(", ") || "None"}</p>
`;
}