document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. Fetch Donations Log ---
    fetch('/api/staff/all-donations')
        .then(response => response.json())
        .then(donations => {
            // Find the table body by its ID
            const tableBody = document.getElementById('donations-table-body');
            tableBody.innerHTML = ''; // Clear static rows

            donations.forEach(donation => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${donation.id}</td>
                    <td>${donation.donor_name}</td>
                    <td>${donation.amount}</td>
                    <td>${donation.type}</td>
                    <td>${donation.date}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching donations:', error));

    // --- 2. Fetch Supply Inventory ---
    fetch('/api/staff/all-supplies')
        .then(response => response.json())
        .then(supplies => {
            // Find the table body by its ID
            const tableBody = document.getElementById('supplies-table-body');
            tableBody.innerHTML = ''; // Clear static rows

            supplies.forEach(supply => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${supply.id}</td>
                    <td>${supply.name}</td>
                    <td>${supply.quantity}</td>
                    <td>${supply.date}</td>
                    <td>${supply.donation_id}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching supplies:', error));
});