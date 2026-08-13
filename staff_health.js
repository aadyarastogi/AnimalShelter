document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. Fetch Recent Treatments ---
    fetch('/api/staff/all-treatments')
        .then(response => response.json())
        .then(treatments => {
            // Find the table body by its ID
            const tableBody = document.getElementById('treatments-table-body');
            tableBody.innerHTML = ''; // Clear static rows

            treatments.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.animal_name}</td>
                    <td>${item.treatment}</td>
                    <td>${item.date}</td>
                    <td>${item.staff_name}</td>
                    <td>${item.vet}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching treatments:', error));

    // --- 2. Fetch Health Checkups ---
    fetch('/api/staff/all-checkups')
        .then(response => response.json())
        .then(checkups => {
            // Find the table body by its ID
            const tableBody = document.getElementById('checkups-table-body');
            tableBody.innerHTML = ''; // Clear static rows

            checkups.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.animal_name}</td>
                    <td>${item.date}</td>
                    <td>${item.weight} kg</td>
                    <td>${item.diagnosis}</td>
                    <td>${item.next_visit}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching checkups:', error));
});