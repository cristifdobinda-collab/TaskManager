// Task status update
function updateStatus(taskId, status) {
    fetch('/tasks/' + taskId + '/status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({ status: status })
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        if (data.success) {
            document.querySelectorAll('.status-buttons .btn').forEach(function(btn) {
                btn.classList.remove('btn-primary');
                btn.classList.add('btn-outline');
                if (btn.dataset.status === status) {
                    btn.classList.add('btn-primary');
                    btn.classList.remove('btn-outline');
                }
            });
            document.querySelectorAll('.status-badge').forEach(function(badge) {
                badge.className = 'status-badge status-' + status;
                badge.textContent = data.label;
            });
        }
    });
}

// Comment delete
function deleteComment(commentId) {
    if (!confirm('Delete this comment?')) return;
    fetch('/tasks/comment/' + commentId + '/delete', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken(),
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        if (data.success) {
            var el = document.getElementById('comment-' + commentId);
            if (el) el.remove();
        }
    });
}

// Reply toggle
function toggleReply(commentId) {
    var form = document.getElementById('reply-form-' + commentId);
    if (form) form.classList.toggle('hidden');
}

// @mention autocomplete
document.addEventListener('DOMContentLoaded', function() {
    var input = document.getElementById('commentInput');
    var dropdown = document.getElementById('mentionDropdown');
    if (!input || !dropdown || typeof allUsers === 'undefined') return;

    var activeIdx = -1;

    input.addEventListener('input', function() {
        var val = this.value;
        var cursor = this.selectionStart;
        // Find the @ symbol before cursor
        var textBefore = val.substring(0, cursor);
        var match = textBefore.match(/@([\w.\-]*)$/);

        if (match) {
            var query = match[1].toLowerCase();
            var filtered = allUsers.filter(function(u) {
                return u.name.toLowerCase().indexOf(query) !== -1 ||
                       u.display.toLowerCase().indexOf(query) !== -1;
            }).slice(0, 6);

            if (filtered.length > 0) {
                activeIdx = 0;
                dropdown.innerHTML = filtered.map(function(u, i) {
                    return '<div class="mention-option' + (i === 0 ? ' active' : '') + '" data-username="' + u.name + '">' +
                        '<strong>@' + u.name + '</strong> <span class="text-muted">' + u.display + '</span></div>';
                }).join('');
                dropdown.classList.remove('hidden');

                dropdown.querySelectorAll('.mention-option').forEach(function(opt) {
                    opt.addEventListener('mousedown', function(e) {
                        e.preventDefault();
                        insertMention(opt.dataset.username, match.index);
                    });
                });
                return;
            }
        }
        dropdown.classList.add('hidden');
        activeIdx = -1;
    });

    input.addEventListener('keydown', function(e) {
        if (dropdown.classList.contains('hidden')) return;
        var items = dropdown.querySelectorAll('.mention-option');
        if (items.length === 0) return;

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            activeIdx = Math.min(activeIdx + 1, items.length - 1);
            updateActive(items);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            activeIdx = Math.max(activeIdx - 1, 0);
            updateActive(items);
        } else if (e.key === 'Enter' || e.key === 'Tab') {
            if (activeIdx >= 0 && activeIdx < items.length) {
                e.preventDefault();
                var textBefore = input.value.substring(0, input.selectionStart);
                var match = textBefore.match(/@([\w.\-]*)$/);
                if (match) insertMention(items[activeIdx].dataset.username, match.index);
            }
        } else if (e.key === 'Escape') {
            dropdown.classList.add('hidden');
        }
    });

    input.addEventListener('blur', function() {
        setTimeout(function() { dropdown.classList.add('hidden'); }, 150);
    });

    function insertMention(username, atIndex) {
        var before = input.value.substring(0, atIndex);
        var after = input.value.substring(input.selectionStart);
        input.value = before + '@' + username + ' ' + after;
        var newPos = atIndex + username.length + 2;
        input.setSelectionRange(newPos, newPos);
        input.focus();
        dropdown.classList.add('hidden');
    }

    function updateActive(items) {
        items.forEach(function(item, i) {
            item.classList.toggle('active', i === activeIdx);
        });
    }
});

// Drag and drop for task board
document.addEventListener('DOMContentLoaded', function() {
    var cards = document.querySelectorAll('.task-card[draggable]');
    var columns = document.querySelectorAll('.column-body');

    cards.forEach(function(card) {
        card.addEventListener('dragstart', function(e) {
            card.classList.add('dragging');
            e.dataTransfer.setData('text/plain', card.dataset.taskId);
        });
        card.addEventListener('dragend', function() {
            card.classList.remove('dragging');
        });
    });

    columns.forEach(function(col) {
        col.addEventListener('dragover', function(e) {
            e.preventDefault();
            col.style.background = 'rgba(37,99,235,.05)';
        });
        col.addEventListener('dragleave', function() {
            col.style.background = '';
        });
        col.addEventListener('drop', function(e) {
            e.preventDefault();
            col.style.background = '';
            var taskId = e.dataTransfer.getData('text/plain');
            var newStatus = col.dataset.status;

            fetch('/tasks/' + taskId + '/status', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({ status: newStatus })
            })
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (data.success) {
                    var card = document.querySelector('[data-task-id="' + taskId + '"]');
                    if (card) {
                        col.appendChild(card);
                        document.querySelectorAll('.task-column').forEach(function(column) {
                            var body = column.querySelector('.column-body');
                            var count = column.querySelector('.column-count');
                            if (count && body) count.textContent = body.children.length;
                        });
                    }
                }
            });
        });
    });

    // Live search with debounce
    var searchInput = document.getElementById('taskSearch');
    if (searchInput) {
        var timeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(function() {
                searchInput.form.submit();
            }, 500);
        });
    }
});
