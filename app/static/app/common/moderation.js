function callback_realese_delete(data, comment) {
    if (comment) {
        var el = document.getElementById('comment_' + data.message_id);
        if (el !== null) {
            el.style.visibility = 'hidden';
        }
    } else {
        location.reload();
    }
}

/**
 * Удаление новости или комментария
 * @param {*} id
 * @param {*} comment
 */

function delete_message(id, comment) {
    $.ajax({
        type: 'POST',
        dataType: 'json',
        contentType: "application/json",
        url: '/api_usatu',
        data: JSON.stringify({
            'method': 'delete_message',
            'data': {'id': id}
        }),
        async: true,
        success: function(data) {
            callback_realese_delete(data, comment);
        }
    });
}


function release_message(id, comment) {
    $.ajax({
        type: 'POST',
        dataType: 'json',
        contentType: "application/json",
        url: '/api_usatu',
        data: JSON.stringify({
            'method': 'release_message',
            'data': {'id': id}
        }),
        async: true,
        success: function(data) {
            callback_realese_delete(data, comment);
        }
    });
}


function release_teacher(id) {
    $.ajax({
        type: 'POST',
        dataType: 'json',
        contentType: "application/json",
        url: '/api_usatu',
        data: JSON.stringify({
            'method': 'release_teacher',
            'data': {'id': id}
        }),
        async: true,
        success: function(data) {
            location.reload();
        }
    });
}


function delete_teacher(id) {
    $.ajax({
        type: 'POST',
        dataType: 'json',
        contentType: "application/json",
        url: '/api_usatu',
        data: JSON.stringify({
            'method': 'delete_teacher',
            'data': {'id': id}
        }),
        async: true,
        success: function(data) {
            location.reload();
        }
    });
}
