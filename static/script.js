document.getElementById('userForm').addEventListener('submit', function(e) {
    e.preventDefault();

    let heightFeet = document.getElementById('heightFeet').value;
    let heightInches = document.getElementById('heightInches').value;

    // Validation
    if(isNaN(heightFeet) || isNaN(heightInches) || heightFeet < 0 || heightInches < 0 || heightInches >= 12) {
        alert('Please enter a valid height in feet and inches.');
        return;
    }

    let weight = document.getElementById('weight').value;
    if(isNaN(weight) || weight <= 0) {
        alert('Please enter a valid weight.');
        return;
    }

    // Calculate height in inches
    let height = parseInt(heightFeet) * 12 + parseInt(heightInches);

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
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while processing your request.');
        });
});
