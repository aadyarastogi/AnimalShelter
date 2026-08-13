document.addEventListener('DOMContentLoaded', () => {
    // Fetch the list of all animals from the API
    fetch('/api/staff/all-animals')
        .then(response => response.json())
        .then(animals => {
            // Find the table body by its ID
            const tableBody = document.getElementById('animal-table-body');
            tableBody.innerHTML = ''; // Clear static rows

            animals.forEach(animal => {
                const row = document.createElement('tr');
                
                // Added a new table cell (<td>) for Age
                row.innerHTML = `
                    <td>${animal.id}</td>
                    <td>${animal.name}</td>
                    <td>${animal.species}</td>
                    <td>${animal.breed}</td>
                    <td>${animal.age || 'N/A'}</td> <td><span class="status-pill ${animal.status_class}">${animal.status}</span></td>
                    <td>
                        <a href="animal_profile.html?id=${animal.id}" class="btn-action-link">
                            <i class="fa-solid fa-eye"></i> View Profile
                        </a>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching all animals:', error));
});