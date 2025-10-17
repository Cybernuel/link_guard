document.getElementById('scanBtn').addEventListener('click', scanUrl);

async function scanUrl() {
  const url = document.getElementById('urlInput').value;
  const resultDiv = document.getElementById('result');

  if (!url) {
    alert('Please enter a URL');
    return;
  }

  resultDiv.textContent = 'Scanning...';
  resultDiv.className = '';
  resultDiv.style.display = 'block';

  try {
    const response = await fetch('http://localhost:5000/api/check-url', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });

    const data = await response.json();

    if (data.suspicious) {
      resultDiv.className = 'danger';
      resultDiv.innerHTML = `
        <strong>⚠️ SUSPICIOUS!</strong><br>
        Score: ${data.score}/100<br>
        ${data.reasons.join('<br>')}
      `;
    } else {
      resultDiv.className = 'safe';
      resultDiv.innerHTML = '<strong>✅ Safe</strong><br>No threats detected';
    }
  } catch (error) {
    resultDiv.className = 'danger';
    resultDiv.textContent = 'Error: Could not connect to API';
  }
}