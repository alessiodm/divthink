jQuery(document).ready(function($){

  $("#searchForm").submit(function(event) {
    event.preventDefault();
    var $form = $( this ),
    str = $form.find( 'input[name="search_string"]' ).val(),
    s3cret = $form.find( 'input[name="secret"]' ).val(),
    url = $form.attr( 'action' );
    
    var posting = $.post( url, { search_string: str, secret: s3cret } );
    
    posting.done(function( data ) {
      //var content = $( data ).find( '#content' );
      //$( "#result" ).empty().append( content );
      $( "#result" ).empty().append( data );
    });
  });

});
