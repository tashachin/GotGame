function confirmBlurb() {
	$('#blurb-form').empty();
	$('#blurb-notif').html('Your bio has been updated.');
	$('#blurb-notif').fadeIn(200).fadeOut(200).fadeIn(200);
}

function confirmEdit() {
	$('#edit-blurb-form').empty();
	$('#blurb-notif').html('Your bio has been updated.');
	$('#edit-blurb-notif').fadeIn(200).fadeOut(200).fadeIn(200);
}

function submitNewBlurb(evt) {
	evt.preventDefault();
	evt.stopImmediatePropagation();

	let blurbData = $('#blurb-form').serialize();  // IMPORTANT FOR SERVER SIDE

	$.post('/new-blurb.json',
		   blurbData,  // IMPORTANT
		   confirmBlurb);	

	return false;
}

function editBlurb(evt) {
	evt.preventDefault();
	evt.stopImmediatePropagation();

	let blurbData = $('#update-blurb-form').serialize();

	$.post('/edit-blurb.json',
			blurbData,
			confirmEdit);

	return false;
}

$('#submit-blurb').on('click', submitNewBlurb);
$('#change-blurb').on('click', editBlurb);

// Edit profile info

$('#edit-profile').on('click', function() {
	
});

// Edit user tags

let userTags = new Array();

$('.user-tags-drag').draggable({
	helper: 'original',
	containment: '#drag-and-drop-tags',
	revert: 'invalid',
});

$('#delete-tags-field').droppable({
	accept: '.user-tags-drag',
	drop: function (event, ui) {
		userTags.push((ui.draggable.attr('id')));  // .push() is JS' .append()
	}
});

function showDeletedTags() {
	location.reload();
}

function createTags(evt) {
	evt.preventDefault();
	evt.stopImmediatePropagation();

	let tagData = $('#new-tags').val();

	$.post('/create-tags.json',
		   {data: tagData},
		   confirmNewTags);

	return false;
}

function deleteTags(evt) {
	evt.preventDefault();
	evt.stopImmediatePropagation();

	$.post('/delete-tags.json',
		   {data: userTags},
		   showDeletedTags);

	return false;
}

$('#create-tags').on('click', createTags);
$('#delete-tags').on('click', deleteTags);