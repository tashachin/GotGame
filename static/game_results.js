// Data Table properties
$(document).ready(function() {
    $('#game-table').DataTable( {
        "order": [[ 0, "asc" ]],
        "pagingType": "first_last_numbers",
    } );
} );