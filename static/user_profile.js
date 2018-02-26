// Edit user tags

let userTags = new Array();

$('.user-tags-drag').draggable({
	helper: 'original',
	containment: '#drag-and-drop-tags',
	revert: 'invalid',
});

$('#delete-tags-field').droppable({
	accept: '.user-tags-drag',
	drop: function (event, ui) {
		userTags.push((ui.draggable.attr('id')));
		console.log(userTags);  // .push() is JS' .append()
	}
});

function confirmNewTags(results) {
	$('#tag-notif').show();

	for (let result of results) {  // Grabbing all the new tag objects
		let tag = "<span id='" + 
				  result.tag_id +
				  // Remember single quotes '' when concatenating variables
      		      "' class='badge badge-secondary user-tags-drag'" + 
      		      "name='" + 
      		      result.tag_id + 
      		      "'>" +
      		      result.tag +
      		      "</span>";

		$('#tag-field').append(tag);
	}

}

function showDeletedTags() {
	location.reload();
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

function deleteTags(evt) {
	evt.preventDefault();
	evt.stopImmediatePropagation();

	$.post('/delete-tags.json',
		   {data: userTags},
		   showDeletedTags);

	return false;
}

$('#create-tags').on('click', createTags);
$('#delete-tags').on('click', deleteTags);
