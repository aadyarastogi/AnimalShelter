// This file is very similar to admin_dashboard.js, but also loads the expense log table
document.addEventListener('DOMContentLoaded', () => {

    // --- 1. Fetch data for the 4 Stat Cards ---
    fetch('/api/admin/stats') // Using the same stats as the dashboard
        .then(response => response.json())
        .then(data => {
            // Find elements by ID and update them
            document.getElementById('stat-donations').innerText = data.donations;
            document.getElementById('stat-expenses').innerText = data.expenses;
            document.getElementById('stat-event-funds').innerText = data.event_funds;
            document.getElementById('stat-net-month').innerText = data.net_month;
        })
        .catch(error => console.error('Error fetching admin stats:', error));


    // --- 2. Fetch data and build the Pie Chart ---
    fetch('/api/admin/expense-breakdown')
        .then(response => response.json())
        .then(data => buildPieChart(data)) // buildPieChart is the same as in admin_dashboard.js
        .catch(error => console.error('Error fetching pie chart data:', error));

    // --- 3. Fetch data and build the Bar Chart ---
    fetch('/api/admin/monthly-expenses')
        .then(response => response.json())
        .then(data => buildBarChart(data)) // buildBarChart is the same as in admin_dashboard.js
        .catch(error => console.error('Error fetching bar chart data:', error));
        
    // --- 4. Fetch data for the "Recent Expense Log" table ---
    fetch('/api/admin/recent-expenses')
        .then(response => response.json())
        .then(expenses => {
            // Find the table body by its ID
            const tableBody = document.getElementById('expense-log-body');
            tableBody.innerHTML = ''; // Clear static rows
            
            expenses.forEach(expense => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${expense.id}</td>
                    <td>${expense.type}</td>
                    <td>₹${expense.amount.toFixed(2)}</td>
                    <td>${expense.date}</td>
                    <td>${expense.staff_name}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching recent expenses:', error));
});

//
// --- THESE FUNCTIONS ARE NEEDED FOR THE CHARTS ---
//

/**
 * Uses Chart.js to build the pie chart
 */
function buildPieChart(chartData) {
    const pieCanvasContainer = document.querySelector('.charts-grid .chart-wrapper:first-child .chart-container');
    pieCanvasContainer.innerHTML = '<canvas id="expensePieChart"></canvas>';
    const ctx = document.getElementById('expensePieChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Expense Breakdown',
                data: chartData.data,
                backgroundColor: ['rgba(239, 68, 68, 0.7)', 'rgba(59, 130, 246, 0.7)', 'rgba(245, 158, 11, 0.7)', 'rgba(22, 163, 74, 0.7)'],
                borderColor: '#fff',
                borderWidth: 1
            }]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });
}


function buildBarChart(chartData) {
    const barCanvasContainer = document.querySelector('.charts-grid .chart-wrapper:last-child .chart-container');
    barCanvasContainer.innerHTML = '<canvas id="expenseBarChart"></canvas>';
    const ctx = document.getElementById('expenseBarChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Total Expenses per Month',
                data: chartData.data,
                backgroundColor: 'rgba(74, 85, 162, 0.7)',
                borderColor: 'rgba(74, 85, 162, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: true } }
        }
    });
}