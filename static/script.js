document.getElementById('userForm').addEventListener('submit', function(e) {
    e.preventDefault();

    let height = document.getElementById('height').value;
    // Example conversion: if user inputs 5'11, convert it to inches (5*12 + 11)
    let feetInches = height.split("'");
    if (feetInches.length === 2) {
        height = parseInt(feetInches[0]) * 12 + parseInt(feetInches[1]);
    }

    const weight = document.getElementById('weight').value;
    const sex = document.getElementById('sex').value;
    const goals = document.getElementById('goals').value;
    const activity = document.getElementById('activity').value;

    fetch('/ask_ai', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ height, weight, sex, goals, activity }),
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('response').textContent = data.response;
        })
        .catch(error => console.error('Error:', error));
});
