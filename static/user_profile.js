// Create drag-and-drop functionality

let userTags = new Array();

$('.user-tags-drag').draggable({
	helper: 'original',
	containment: '#drag-and-drop-tags',
	revert: 'invalid',
});

$('#delete-tags-field').droppable({
	accept: '.user-tags-drag',
	drop: function (event, ui) {
		userTags.push((ui.draggable.attr('id'))); // .push() is JS' .append()
	}
});

//////////////////////////////////////
// Edit user tags

function showTags() {
	location.reload();
}

function createTags(evt) {
	evt.preventDefault();
	evt.stopImmediatePropagation();

	let tagData = $('#new-tags').val();

	$.post('/create-tags.json',
		   {data: tagData},
		   showTags);

	return false;
}

function deleteTags(evt) {
	evt.preventDefault();
	evt.stopImmediatePropagation();

	$.post('/delete-tags.json',
		   {data: userTags},
		   showTags);

	return false;
}

$('#create-tags').on('click', createTags);
$('#delete-tags').on('click', deleteTags);
