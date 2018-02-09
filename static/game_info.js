function submitReview(evt) {
	evt.preventDefault();

	let reviewData = $("#review-form").serialize();  // IMPORTANT FOR SERVER SIDE

	$.post('/new-review.json',
		   reviewData,  // IMPORTANT
		   confirmReview);

	// disableForm();	
}

// function disableForm() {
// 	$('#submit-review').prop('disabled', true);
// 	$('#submit-review').val('Submitting form...');
// }

function confirmReview() {
	$('#review-status').remove();
	$('#review-notif').fadeIn(200).fadeOut(200).fadeIn(200);
}

$('#review-form').on('submit', submitReview);