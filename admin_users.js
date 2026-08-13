document.addEventListener('DOMContentLoaded', () => {
    // Fetch the list of all users from the API
    fetch('/api/admin/all-users')
        .then(response => response.json())
        .then(users => {
            const tableBody = document.getElementById('user-table-body');
            tableBody.innerHTML = ''; // Clear static rows

            // Loop through the users and build the table
            users.forEach(user => {
                const row = document.createElement('tr');
                
                // MODIFICATION: The 'full_name' cell is removed
                row.innerHTML = `
                    <td>${user.username}</td>
                    <td><span class="role-pill ${user.role.toLowerCase()}">${user.role}</span></td>
                    <td class="actions-cell">
                        <a href="#" class="btn btn-edit"><i class="fa-solid fa-pencil-alt"></i></a>
                        <a href="#" class="btn btn-delete" data-username="${user.username}">
                            <i class="fa-solid fa-trash-alt"></i>
                        </a>
                    </td>
                `;
                tableBody.appendChild(row);
            });
            
            // After creating the buttons, add click listeners to them
            addDeleteButtonListeners();
        })
        .catch(error => console.error('Error fetching users:', error));
});

/**
 * Finds all delete buttons and adds a click event to them.
 */
function addDeleteButtonListeners() {
    const deleteButtons = document.querySelectorAll('.btn-delete');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault(); // Stop the a tag from jumping
            
            const username = event.currentTarget.dataset.username;

            if (confirm(`Are you sure you want to delete the user '${username}'?`)) {
                
                fetch(`/api/admin/delete_user/${username}`, {
                    method: 'DELETE'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload(); // Reload the page
                    } else {
                        alert("Error deleting user: " + data.error);
                    }
                })
                .catch(error => console.error('Error deleting user:', error));
            }
        });
    });
}