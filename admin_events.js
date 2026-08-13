document.addEventListener('DOMContentLoaded', () => {
    // Fetch the list of all events from the API
    fetch('/api/admin/all-events')
        .then(response => response.json())
        .then(events => {
            // Find the table body by its ID
            const tableBody = document.getElementById('events-table-body');
            tableBody.innerHTML = ''; // Clear static rows

            // Loop through the events and build the table
            events.forEach(event => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${event.name}</td>
                    <td>${event.date}</td>
                    <td>${event.staff_name}</td>
                    <td>₹${event.funds_raised.toFixed(2)}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching events:', error));
});