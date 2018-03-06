// Data Table configurations
$(document).ready(function() {
    $('#game-info-table').DataTable( {
    	retrieve: true,
        paging: false,
        searching: false,
        sorting: false,
    } );

    $('.sorting').removeClass();

} );

//////////////////////////////////////
// Updating game review

function updateReview(evt) {
	evt.preventDefault();
	evt.stopImmediatePropagation();  // Stops double AJAX call

	let reviewData = $('#review-form').serialize();
	console.log(reviewData);

	$.post('/review.json',
			reviewData,
			function() {
				location.reload();
			});

	return false;
}

$('#submit-review').on('click', updateReview);

//////////////////////////////////////
// Dialogs for tags

$.ui.dialog.prototype._focusTabbable = function(){};

$(".badge-dialog").dialog({ 
	autoOpen: false,
	modal: true,
	show: "fade",
	height: "auto",
	dialogClass: "no-close no-title",
});

$(".badge").click(function(){
	$("#badge-dialog-"+$(this).attr('id')).dialog("open");
})

$.extend( $.ui.dialog.prototype.options.classes, {
    "ui-dialog": "modal-content",
    "ui-dialog-titlebar": "modal-header",
    "ui-dialog-title": "modal-title",
    "ui-dialog-titlebar-close": "close",
    "ui-dialog-content": "modal-body",
    "ui-dialog-buttonpane": "modal-footer"
});



//////////////////////////////////////
// Drag-and-drop functionality of tags

// FIX ME: Droppable field does not grow dynamically to contain all tags
// FIX ME: Tags do not shift over when neighbors are moved to droppable field

let gameTags = new Array();

$('.adding-drag').draggable({
	opacity: 0.8,
	helper: 'original',
	containment: '#drag-and-drop-tags',
	revert: 'invalid',
});

$('#attach-tags-field').droppable({
	accept: '.adding-drag',
	drop: function (event, ui) {
		gameTags.push((ui.draggable.attr('id')));  // .push() is JS' .append()
	}
});

$('.deleting-drag').draggable({
	opacity: 0.8,
	helper: 'original',
	stack: '.deleting-drag',
	containment: '#delete-tags-wrap',
	revert: 'invalid',
});

$('#delete-tags-field').droppable({
	accept: '.deleting-drag',
	drop: function (event, ui) {
		gameTags.push((ui.draggable.attr('id')));
		console.log(gameTags);
	}
});

function refreshTags(results) {
	$('.placeholder').hide();
	location.reload();

}

function addGameTags(evt) {
	evt.preventDefault();
	evt.stopImmediatePropagation();

	$.post('/update-tags.json',
		   {data: gameTags,
		    game: $('#current-game').val()
		   },
		   refreshTags
	);

	return false;
}

function deleteGameTags(evt) {
	evt.preventDefault();
	evt.stopImmediatePropagation();

	$.post('/delete-game-tags.json',
		   {data: gameTags,
		    game: $('#current-game-2').val()
		   },
		   refreshTags
	);

	return false;
}

$('#tag-game').on('click', addGameTags);
$('#untag-game').on('click', deleteGameTags);
