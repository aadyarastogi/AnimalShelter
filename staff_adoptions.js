document.addEventListener('DOMContentLoaded', () => {
    // Fetch the list of all adoptions from the API
    fetch('/api/staff/all-adoptions')
        .then(response => response.json())
        .then(adoptions => {
            // Find the table body by its ID
            const tableBody = document.getElementById('adoptions-table-body');
            tableBody.innerHTML = ''; // Clear static rows

            adoptions.forEach(adoption => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${adoption.id}</td>
                    <td>${adoption.animal_name}</td>
                    <td>${adoption.adopter_name}</td>
                    <td>${adoption.contact}</td>
                    <td>${adoption.date}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching all adoptions:', error));
});