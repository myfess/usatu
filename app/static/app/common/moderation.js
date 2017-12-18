function page_ReleaseComment(data) {
	if (data == 'cancel') {
    alert('cancel');
  }

	document.getElementById('comment_' + data).style.visibility = 'hidden';
}

function ReleaseComment(id) {
	var req = new MyRequest('mod/comments/release/' + id, '', page_ReleaseComment);
	req.Execute();
}

function page_DeleteComment(data) {
	if (data == 'cancel') {
    alert('cancel');
  }

	document.getElementById('comment_' + data).style.visibility = 'hidden';
}

function DeleteComment(id) {
	var req = new MyRequest('mod/comments/delete/' + id, '', page_DeleteComment);
	req.Execute();
}

