$(document).ready(function() {
    $('#game-info-table').DataTable( {
    	retrieve: true,
        paging: false,
        searching: false,
    } );
} );

function confirmReview() {
	$('#review-form').empty();
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