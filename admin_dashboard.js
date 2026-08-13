// This function runs as soon as the admin_dashboard.html page is loaded
document.addEventListener('DOMContentLoaded', () => {

    // --- 1. Fetch data for the 4 Stat Cards ---
    fetch('/api/admin/stats')
        .then(response => response.json())
        .then(data => {
            // Find the HTML elements by their IDs and update them
            document.getElementById('stat-donations').innerText = data.donations;
            document.getElementById('stat-expenses').innerText = data.expenses;
            document.getElementById('stat-staff').innerText = data.staff;
            document.getElementById('stat-volunteers').innerText = data.volunteers;
        })
        .catch(error => console.error('Error fetching admin stats:', error));


    // --- 2. Fetch data and build the Pie Chart ---
    fetch('/api/admin/expense-breakdown')
        .then(response => response.json())
        .then(data => {
            buildPieChart(data);
        })
        .catch(error => console.error('Error fetching pie chart data:', error));

    // --- 3. Fetch data and build the Bar Chart ---
    fetch('/api/admin/monthly-expenses')
        .then(response => response.json())
        .then(data => {
            buildBarChart(data);
        })
        .catch(error => console.error('Error fetching bar chart data:', error));
});


/**
 * Uses Chart.js to build the pie chart
 */
function buildPieChart(chartData) {
    const pieCanvasContainer = document.querySelector('.charts-grid .chart-wrapper:first-child .chart-container');
    
    // Clear the placeholder text ("Pie Chart Will Load Here")
    pieCanvasContainer.innerHTML = '<canvas id="expensePieChart"></canvas>';
    const ctx = document.getElementById('expensePieChart').getContext('2d');

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Expense Breakdown',
                data: chartData.data,
                backgroundColor: [
                    'rgba(239, 68, 68, 0.7)',  // Red
                    'rgba(59, 130, 246, 0.7)', // Blue
                    'rgba(245, 158, 11, 0.7)', // Amber
                    'rgba(22, 163, 74, 0.7)',  // Green
                ],
                borderColor: '#fff',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
        }
    });
}

/**
 * Uses Chart.js to build the bar chart
 */
function buildBarChart(chartData) {
    const barCanvasContainer = document.querySelector('.charts-grid .chart-wrapper:last-child .chart-container');
    
    // Clear the placeholder text
    barCanvasContainer.innerHTML = '<canvas id="expenseBarChart"></canvas>';
    const ctx = document.getElementById('expenseBarChart').getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Total Expenses per Month',
                data: chartData.data,
                backgroundColor: 'rgba(74, 85, 162, 0.7)', // --primary-color
                borderColor: 'rgba(74, 85, 162, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}