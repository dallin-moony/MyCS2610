document.addEventListener('DOMContentLoaded', function() {
    let activityElements = document.querySelectorAll('#activity');
    activityElements.forEach(activity => {
        activity.addEventListener('click', () => {
            console.log("Activity clicked:", activity);
            let link = activity.querySelector('a');
            if (link) {
                window.location.href = link.href;
            }
        });
    });

    let deleteButtons = document.querySelectorAll('.delete-btn');
    if (deleteButtons) {
        deleteButtons.forEach(deleteButton => {
            deleteButton.addEventListener('click', () => {
                if (confirm("Are you sure you want to delete this activity? This action cannot be undone.")) {
                    fetch(deleteButton.dataset.url, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken'),
                    },
                })
                .then(response => {
                    if (response.ok) {
                        window.location.href = '/';
                    } else {
                        alert("Failed to delete the activity.");
                    }
                });
            }
        });
    });
};
});