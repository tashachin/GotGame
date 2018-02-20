// Data Table configurations
$(document).ready(function() {
    $('#game-info-table').DataTable( {
    	retrieve: true,
        paging: false,
        searching: false,
    } );
} );

//////////////////////////////////////
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

//////////////////////////////////////
// Faving and unfaving games

//////////////////////////////////////
// Adding tags to games

function confirmNewTags(results) {
	$('#tag-notif').show();

	for (let result of results) {  // Grabbing all the new tag objects
		let tag = "<span id='" + 
				  result.tag_id +
				  // Remember single quotes '' when concatenating variables
      		      "' class='badge badge-secondary draggable'" + 
      		      "name='" + 
      		      result.tag_id + 
      		      "'>" +
      		      result.tag +
      		      "</span>";

		$('#tag-field').append(tag);
	}
}

function addTags(evt) {
	evt.preventDefault();
	evt.stopImmediatePropagation();

	let tagData = $('#create-tags-form').serialize();

	$.post('/create-tags.json',
		   tagData,
		   confirmNewTags);

	return false;
}

$('#create-tags').on('click', addTags);

//////////////////////////////////////
// Drag-and-drop functionality of tags

// FIX ME: Droppable field does not grow dynamically to contain all tags
// FIX ME: Tags do not shift over when neighbors are moved to droppable field


$('.draggable').draggable({
	axis: 'y',
	opacity: 0.8,
	helper: 'original',
	containment: '#drag-and-drop-tags',
	snap: '#attach-tags-field',
});

let userTags = new Array();

$('.droppable').droppable({
	accept: '.draggable',
	drop: function (event, ui) {
		userTags.push((ui.draggable.attr('id')));  // .push() is JS' .append()
	}
});

function showTags(results) {
	for (let result of results) {  // Grabbing all the new tag objects
		let tag = "<span id='" + 
				  result.tag_id +
				  // Remember single quotes '' when concatenating variables
      		      "' class='badge badge-secondary draggable'" + 
      		      "name='" + 
      		      result.tag + 
      		      "'>" +
      		      result.tag +
      		      "</span>";

		$('#game-tags').append(tag);
	}
}

function updateTags(evt) {
	evt.preventDefault();
	evt.stopImmediatePropagation();

	$.post('/update-tags.json',
		    {data: userTags,
		     game: $('#current-game').val()},
		    showTags
	);

	return false;
}

$('#edit-tags').on('click', updateTags);
