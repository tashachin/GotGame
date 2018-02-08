// Data Table properties
$(document).ready(function() {
    $('#game-table').DataTable( {
        "order": [[ 0, "asc" ]],
        "pagingType": "first_last_numbers",
    } );
} );

function confirmReview() {
	$.flash('Your review has been added.')
}

function submitReview(evt) {
	evt.preventDefault();

	let reviewFormInputs = {
		"game_id": $("#game-id").val(),
		"user_score": $("#new-score").val(),
		"review": $("#new-review").val(),
	};

	$.post('/new-review',
		   reviewFormInputs,
		   confirmReview);

})

$('#sort-button').on('submit', submitReview)