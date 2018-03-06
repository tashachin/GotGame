// Data Table properties

$(document).ready(function() {
    $('#game-search-table').DataTable( {
        "order": [[ 0, "asc" ]],
        "pagingType": "first_last_numbers",
        "pageLength": 10,
        "deferRender": true,
    } );

} );

function showGameInfo() {
	
}

////////////////////////////////////// NEW FEATURE
// $('select td by game_id').on('mouseOver', showGameInfo)