$(document).ready(function() {
    $('#game-table').DataTable( {
        "order": [[ 0, "asc" ]],
        "pagingType": "first_last_numbers",
    } );
} );

$('#sort-button').on('click', )