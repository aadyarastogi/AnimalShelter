document.addEventListener('DOMContentLoaded', () => {

    // --- NEW CODE ---
    // 1. Fetch the volunteer's profile to get their name
    fetch('/api/volunteer/profile')
        .then(response => response.json())
        .then(profile => {
            // Find the <h1> tag by its new ID and update the name
            document.getElementById('volunteer-name').innerText = `Welcome back, ${profile.name}!`;
        })
        .catch(error => console.error('Error fetching profile name:', error));

    // --- EXISTING CODE ---
    // 2. Fetch the volunteer's stats
    fetch('/api/volunteer/stats')
        .then(response => response.json())
        .then(data => {
            // Update the stat cards
            document.getElementById('stat-total-hours').innerText = data.total_hours;
            document.getElementById('stat-tasks-completed').innerText = data.tasks_completed;
            document.getElementById('stat-tasks-pending').innerText = data.tasks_pending;
        })
        .catch(error => console.error('Error fetching stats:', error));

    // --- EXISTING CODE ---
    // 3. Fetch the volunteer's task list
    fetch('/api/volunteer/tasks')
        .then(response => response.json())
        .then(tasks => {
            // Find the task table's body
            const tableBody = document.querySelector('.task-table tbody');
            tableBody.innerHTML = ''; // Clear the static "example" rows

            // Loop through the tasks from the API and build new rows
            tasks.forEach(task => {
                const row = document.createElement('tr');
                
                // Check if task is completed to disable the button
                const isCompleted = task.status === 'Completed';
                const buttonHTML = `
                    <button class="btn-action ${isCompleted ? 'disabled' : ''}" ${isCompleted ? 'disabled' : ''}>
                        <i class="fa-solid ${isCompleted ? 'fa-check' : 'fa-plus-circle'}"></i> 
                        ${isCompleted ? `Logged ${task.hours}h` : 'Log Hours'}
                    </button>
                `;
                
                // Set the HTML for the row
                row.innerHTML = `
                    <td>${task.date}</td>
                    <td>${task.description}</td>
                    <td>${task.animal_name}</td>
                    <td><span class="status-pill ${task.status.toLowerCase()}">${task.status}</span></td>
                    <td>${buttonHTML}</td>
                `;
                
                // Add the new row to the table
                tableBody.appendChild(row);
            });
            
            if (tasks.length === 0) {
                tableBody.innerHTML = '<tr><td colspan="5" style="text-align: center;">No tasks assigned.</td></tr>';
            }
        })
        .catch(error => console.error('Error fetching volunteer tasks:', error));
});