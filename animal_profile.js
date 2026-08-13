document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Get the Animal ID from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const animalId = urlParams.get('id');

    if (!animalId) {
        // If no ID, stop and show an error
        document.getElementById('animal-name').innerText = "Error";
        document.getElementById('animal-species-breed').innerText = "No animal ID provided.";
        return;
    }

    // 2. Fetch all data for this specific animal
    fetch(`/api/animal_profile/${animalId}`)
        .then(response => response.json())
        .then(data => {
            
            // 3. Populate the Animal Details card
            const details = data.details;
            document.getElementById('animal-name').innerText = details.Name;
            document.getElementById('animal-species-breed').innerText = `${details.Species} | ${details.Breed}`;
            document.getElementById('animal-id').innerText = details.AnimalID;
            document.getElementById('animal-status').innerText = details.Status;
            document.getElementById('animal-dob').innerText = details.DOB ? details.DOB.split('T')[0] : 'N/A'; // Format date
            document.getElementById('animal-breed').innerText = details.Breed;

            // 4. Populate the Health Records table
            const healthTable = document.getElementById('health-table-body');
            healthTable.innerHTML = ''; // Clear any loading text
            data.health.forEach(record => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${record.CheckupDate.split('T')[0]}</td>
                    <td>${record.Weight} kg</td>
                    <td>${record.Diagnosis}</td>
                    <td>${record.Medication}</td>
                    <td>${record.NextVisit ? record.NextVisit.split('T')[0] : 'N/A'}</td>
                `;
                healthTable.appendChild(row);
            });
            if (data.health.length === 0) {
                healthTable.innerHTML = '<tr><td colspan="5">No health records found.</td></tr>';
            }

            // 5. Populate the Treatments table
            const treatmentTable = document.getElementById('treatment-table-body');
            treatmentTable.innerHTML = ''; // Clear any loading text
            data.treatments.forEach(record => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${record.DateGiven.split('T')[0]}</td>
                    <td>${record.TreatmentType}</td>
                    <td>${record.StaffName || 'N/A'}</td>
                    <td>${record.Veterinarian}</td>
                    <td>${record.Notes}</td>
                `;
                treatmentTable.appendChild(row);
            });
            if (data.treatments.length === 0) {
                treatmentTable.innerHTML = '<tr><td colspan="5">No treatments found.</td></tr>';
            }
            
        })
        .catch(error => console.error('Error fetching animal profile:', error));
});