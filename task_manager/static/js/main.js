// CSRF token helper
function getCsrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : '';
}

// Flash message auto-dismiss
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.alert').forEach(function(alert) {
        setTimeout(function() { alert.remove(); }, 5000);
    });
});
