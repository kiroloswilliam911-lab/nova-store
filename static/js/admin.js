document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".delete-btn");

    deleteButtons.forEach(function (button) {
        button.addEventListener("click", function (event) {
            const confirmed = confirm("Are you sure you want to continue?");

            if (!confirmed) {
                event.preventDefault();
            }
        });
    });
});