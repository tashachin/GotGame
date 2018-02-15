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

$('#submit-blurb').on('click', submitBlurb);
$('#change-blurb').on('click', editBlurb);

// Edit profile info

$('#edit-profile').on('click', function() {
	
});