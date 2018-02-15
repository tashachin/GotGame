// Data Table configurations
$(document).ready(function() {
    $('#game-info-table').DataTable( {
    	retrieve: true,
        paging: false,
        searching: false,
    } );
} );

// Adding and editing game reviews
function confirmReview() {
	$('#review-form').empty();
	$('#review-status').remove();
	$('#review-notif').fadeIn(200).fadeOut(200).fadeIn(200);
}

function confirmEdit() {
	$('#update-review-form').empty();
	$('#edit-review-notif').fadeIn(200).fadeOut(200).fadeIn(200);
}

function submitNewReview(evt) {
	evt.preventDefault();
	evt.stopImmediatePropagation();

	let reviewData = $('#review-form').serialize();  // IMPORTANT FOR SERVER SIDE

	$.post('/new-review.json',
		   reviewData,  // IMPORTANT
		   confirmReview);	

	return false;
}

function editReview(evt) {
	evt.preventDefault();
	evt.stopImmediatePropagation();

	let reviewData = $('#update-review-form').serialize();

	$.post('/edit-review.json',
			reviewData,
			confirmEdit);

	return false;
}

$('#submit-review').on('click', submitNewReview);
$('#change-review').on('click', editReview);

// Faving and unfaving games

