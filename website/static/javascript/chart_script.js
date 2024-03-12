var ctx = document.getElementById('myChart').getContext('2d');

// Extract votes data from Flask passed candidates
var candidatesData = JSON.parse('{{ candidates_json | tojson | safe }}');
var votesData = candidatesData.map(candidate => candidate.votes); // Fix mapping

// Calculate step size for y-axis ticks
var maxVotes = Math.max(...votesData);
var stepSize = Math.ceil(maxVotes / 5); // Adjust divisor as needed

var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: candidatesData.map(candidate => candidate.name),
        datasets: [{
            label: 'Votes',
            data: votesData,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: stepSize
                }
            }
        }
    }
});
