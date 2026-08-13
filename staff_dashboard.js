// This function runs as soon as the staff_dashboard.html page is loaded
document.addEventListener('DOMContentLoaded', () => {

    // --- 1. Fetch data for the 4 Stat Cards ---
    fetch('/api/staff/stats')
        .then(response => response.json())
        .then(data => {
            // Find the HTML elements by their IDs and update them
            document.getElementById('stat-animals-onsite').innerText = data.animals_onsite;
            document.getElementById('stat-pending-adoptions').innerText = data.pending_adoptions;
            document.getElementById('stat-checkups-today').innerText = data.checkups_today;
            document.getElementById('stat-volunteers-today').innerText = data.volunteers_today;
        })
        .catch(error => console.error('Error fetching staff stats:', error));

    // --- 2. Fetch data for the "Needs Attention" table ---
    fetch('/api/staff/needs-attention')
        .then(response => response.json())
        .then(animals => {
            // Find the table body by its ID
            const tableBody = document.querySelector('#needs-attention-table tbody');
            tableBody.innerHTML = ''; // Clear static rows

            animals.forEach(animal => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${animal.id}</td>
                    <td>${animal.name}</td>
                    <td>${animal.species}</td>
                    <td><span class="status-pill ${animal.status_class}">${animal.status}</span></td>
                    <td>
                        <a href="#" class="btn-action-link">
                            <i class="fa-solid fa-eye"></i> View Profile
                        </a>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching needs-attention table:', error));
    
    // --- 3. Fetch data for the "Recent Adoptions" table ---
    fetch('/api/staff/recent-adoptions')
        .then(response => response.json())
        .then(adoptions => {
            // Find the table body by its ID
            const tableBody = document.querySelector('#recent-adoptions-table tbody');
            tableBody.innerHTML = ''; // Clear static rows

            adoptions.forEach(adoption => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${adoption.id}</td>
                    <td>${adoption.animal_name}</td>
                    <td>${adoption.adopter_name}</td>
                    <td>${adoption.date}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching recent-adoptions table:', error));
});