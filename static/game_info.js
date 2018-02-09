$(document).ready(function() {
    $('#game-info-table').DataTable( {
        "order": [[ 0, "asc" ]],
        "pagingType": "first_last_numbers",
    } );
} );

function confirmReview() {
	$('#review-status').remove();
	$('#review-notif').fadeIn(200).fadeOut(200).fadeIn(200);
}

function submitReview(evt) {
	evt.preventDefault();
	evt.stopImmediatePropagation();

	let reviewData = $("#review-form").serialize();  // IMPORTANT FOR SERVER SIDE

	$.post('/new-review.json',
		   reviewData,  // IMPORTANT
		   confirmReview);	

	return false;
}

$('#submit-review').on('click', submitReview);