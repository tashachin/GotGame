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
	evt.stopImmediatePropagation();  // Stops double AJAX call

	let reviewData = $('#update-review-form').serialize();

	$.post('/edit-review.json',
			reviewData,
			confirmEdit);

	return false;
}

$('#submit-review').on('click', submitNewReview);
$('#change-review').on('click', editReview);

// Faving and unfaving games

// Adding tags to games

function confirmTags(results) {
	$('#tag-notif').show();

	for (let result of results) {  // Grabbing all the new tag objects
		let tag = "<span id='" + result.tag_id +
      		      "' class='badge badge-secondary'" + 
      		      "name='" + result.tag_id + 
      		      "'data-draggable='draggable'>" +
      		      result.tag +
      		      "</span>";

		$('#tag-field').append(tag);
	}
}

function addTags(evt) {
	debugger;
	evt.preventDefault();
	evt.stopImmediatePropagation();

	let tagData = $('#create-tags-form').serialize();

	$.post('/create-tags.json',
		   tagData,
		   confirmTags);

	return false;
}

$('#create-tags').on('click', addTags);


// Drag-and-drop functionality of tags

