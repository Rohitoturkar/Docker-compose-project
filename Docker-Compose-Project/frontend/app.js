document.getElementById('nameForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const name = document.getElementById('nameInput').value;

    const response = await fetch('http://65.0.131.1:5000/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name })
    });

    const result = await response.json();

    document.getElementById('response').innerText = result.message;

    // Clear input field
    document.getElementById('nameInput').value = '';
});
