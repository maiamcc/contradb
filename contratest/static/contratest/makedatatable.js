$(document).ready(function() {
  function expandAll(){
    var $rows = $('#example tr'); // this will include extraneous rows, so start
      // for loop at i=2
    for (i = 2; i < $rows.length; i++) {
      var $tr = $rows.eq(i);
      var row = table.row( $tr );

      var id = $tr.attr("data-id");
      secrettext = window.extrainfo[id];

      // Open this row
      row.child( "<table><tr><td>" + secrettext + "</td></tr></table>" ).show();
      $tr.addClass('shown');
      $tr.find('.details').html("");
      $tr.find('.details').html("HIDE");
    }
  }

  function collapseAll(){
    var $rows = $('#example tr'); // this will include extraneous rows
    for (i = 2; i < $rows.length; i++) {
      var $tr = $rows.eq(i);
      var row = table.row( $tr );

      if ( row.child.isShown() ) {
        // This row is already open - close it
        row.child.hide();
        $tr.removeClass('shown');
        $tr.find('.details').html("");
        $tr.find('.details').html("SHOW");
      }
    }
  }

  var table = $('#example').DataTable( {
    "dom": 'l<"clear"><"horiz_container"Tf>tip',
    "oTableTools": {
      "aButtons": [
        {
          "sExtends": "text",
          "sButtonText": "Expand All",
          "fnClick": function () {
            expandAll();
          }
        },

        {
          "sExtends": "text",
          "sButtonText": "Collapse All",
          "fnClick": function () {
            collapseAll();
          }
        }
      ]
    }
  });

  $('#example tbody').on('click', 'td.details', function () {
    var $tr = $(this).closest('tr');
    var row = table.row( $tr );

    var id = $tr.attr("data-id");
    secrettext = window.extrainfo[id];

    if ( row.child.isShown() ) {
      // This row is already open - close it
      row.child.hide();
      $tr.removeClass('shown');
      $tr.find('.details').html("");
      $tr.find('.details').html("SHOW");

    }
    else {
      // Open this row
      row.child( "<table><tr><td>" + secrettext + "</td></tr></table>" ).show();
      $tr.addClass('shown');
      $tr.find('.details').html("");
      $tr.find('.details').html("HIDE");
    }
  });
});