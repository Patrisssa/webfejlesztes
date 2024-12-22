document.addEventListener('DOMContentLoaded', function() {
    const logoutLinks = document.querySelectorAll('.logout-link');

    logoutLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            if (confirm("Biztosan ki szeretnél jelentkezni?")) {
                window.location.href = link.href;
            }
        });
    });
});
