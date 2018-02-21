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

function createTags(evt) {
	evt.preventDefault();
	evt.stopImmediatePropagation();

	let tagData = $('#new-tags').val();

	$.post('/create-tags.json',
		   {data: tagData},
		   confirmNewTags);

	return false;
}

$('#create-tags').on('click', createTags);

// $('#delete-tags').on('click', deleteTags); FIX ME!!!!

//////////////////////////////////////
// Drag-and-drop functionality of tags

// FIX ME: Droppable field does not grow dynamically to contain all tags
// FIX ME: Tags do not shift over when neighbors are moved to droppable field

let userTags = new Array();
let gameTags = new Array();

$('.adding-drag').draggable({
	opacity: 0.8,
	helper: 'original',
	containment: '#drag-and-drop-tags',
	snap: '#attach-tags-field',
	revert: 'invalid',
});

$('#attach-tags-field').droppable({
	accept: '.adding-drag',
	drop: function (event, ui) {
		userTags.push((ui.draggable.attr('id')));  // .push() is JS' .append()
	}
});

$('.deleting-drag').draggable({
	opacity: 0.8,
	helper: 'original',
	containment: '#delete-tags-row',
	snap: '#delete-tags-field',
	stack: ".deleting-drag",
	revert: 'invalid',
});

$('#delete-tags-field').droppable({
	accept: '.deleting-drag',
	drop: function (event, ui) {
		gameTags.push((ui.draggable.attr('id')));
		console.log(gameTags);
	}
});


function showGameTags(results) {
	for (let result of results) {
		let vg_tag = "<span id='" + 
				  result.vg_tag_id +
      		      "' class='badge badge-secondary draggable'" + 
      		      "name='" + 
      		      result.tag + 
      		      "'>" +
      		      result.tag +
      		      "</span>";

      	$('#game-tags').append(vg_tag);
	}
}

function updateGameTags(evt) {
	evt.preventDefault();
	evt.stopImmediatePropagation();

	$.post('/update-tags.json',
		   {data: userTags,
		    game: $('#current-game').val()
		   },
		   showGameTags
	);

	return false;
}

function removeGameTags(results) {
	for (let result of results) {
		if (result.vg_tag_id in $('#game-tags')) {
			$('#' + result.vg_tag_id).remove();
		}
	}

}

function deleteGameTags(evt) {
	evt.preventDefault();
	evt.stopImmediatePropagation();

	$.post('/delete-game-tags.json',
		   {data: gameTags,
		    game: $('#current-game-2').val()
		   },
		   removeGameTags
	);

	return false;
}

$('#tag-game').on('click', updateGameTags);
$('#delete-game-tags').on('click', deleteGameTags);
