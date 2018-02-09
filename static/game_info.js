function confirmReview() {
	$('#review-notif').fadeIn(200).fadeOut(200).fadeIn(200);
}

function submitReview(evt) {
	evt.preventDefault();

	let reviewData = $("#review-form").serialize();  // IMPORTANT FOR SERVER SIDE

	$.post('/new-review.json',
		   reviewData,  // IMPORTANT
		   confirmReview);

	$('#review-status').remove();
}

$('#review-form').on('submit', submitReview);