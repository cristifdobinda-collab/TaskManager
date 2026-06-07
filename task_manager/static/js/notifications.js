// Notification system
(function() {
    const bell = document.getElementById('notificationBell');
    const dropdown = document.getElementById('notifDropdown');
    const badge = document.getElementById('notifBadge');
    const notifList = document.getElementById('notifList');
    const markAllBtn = document.getElementById('markAllRead');

    if (!bell) return;

    // Toggle dropdown
    bell.addEventListener('click', function(e) {
        e.stopPropagation();
        dropdown.classList.toggle('hidden');
        if (!dropdown.classList.contains('hidden')) {
            fetchNotifications();
        }
    });

    document.addEventListener('click', function() {
        dropdown.classList.add('hidden');
    });
    dropdown.addEventListener('click', function(e) { e.stopPropagation(); });

    // Mark all read
    markAllBtn.addEventListener('click', function() {
        fetch('/notifications/read-all', {
            method: 'POST',
            headers: { 'X-CSRFToken': getCsrfToken() }
        }).then(function() {
            badge.textContent = '0';
            badge.classList.add('hidden');
            fetchNotifications();
        });
    });

    function fetchNotifications() {
        fetch('/notifications/unread')
            .then(function(r) { return r.json(); })
            .then(function(data) {
                badge.textContent = data.count;
                if (data.count > 0) {
                    badge.classList.remove('hidden');
                } else {
                    badge.classList.add('hidden');
                }

                if (data.notifications.length === 0) {
                    notifList.innerHTML = '<p class="notif-empty">No new notifications</p>';
                    return;
                }

                notifList.innerHTML = data.notifications.map(function(n) {
                    return '<div class="notif-item unread" data-id="' + n.id + '" data-link="' + (n.link || '') + '">' +
                        '<div>' + escapeHtml(n.message) + '</div>' +
                        '<div class="notif-time">' + n.created_at + '</div>' +
                        '</div>';
                }).join('');

                notifList.querySelectorAll('.notif-item').forEach(function(item) {
                    item.addEventListener('click', function() {
                        var id = this.dataset.id;
                        var link = this.dataset.link;
                        fetch('/notifications/' + id + '/read', {
                            method: 'POST',
                            headers: { 'X-CSRFToken': getCsrfToken() }
                        }).then(function() {
                            if (link) window.location.href = link;
                        });
                    });
                });
            });
    }

    function escapeHtml(text) {
        var div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Poll every 30 seconds
    setInterval(function() {
        fetch('/notifications/unread')
            .then(function(r) { return r.json(); })
            .then(function(data) {
                badge.textContent = data.count;
                if (data.count > 0) {
                    badge.classList.remove('hidden');
                } else {
                    badge.classList.add('hidden');
                }
            });
    }, 30000);
})();
