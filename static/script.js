jQuery(document).ready(function($){

  var width = 800, height = 600;

  var cluster = d3.layout.tree()
      .size([height, width - 160]);

  var diagonal = d3.svg.diagonal()
      .projection(function (d) {
      return [d.y, d.x];
  });

  $("#searchForm").submit(function(event) {
    event.preventDefault();
    var $form = $( this ),
    str = $form.find( 'input[name="search_string"]' ).val(),
    s3cret = $form.find( 'input[name="secret"]' ).val(),
    url = $form.attr( 'action' );
    
    var posting = $.post( url, { search_string: str, secret: s3cret } );
    
    d3.select("svg").remove();
    var svg = d3.select("body").append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", "translate(40,0)");

    posting.done(function( data ) {
      $( "#result" ).empty().append( data );
      
      data = JSON.parse(data);
      var nodes = cluster.nodes(data["crawled_paths"][0]),
          links = cluster.links(nodes);

      var link = svg.selectAll(".link")
          .data(links)
          .enter().append("path")
          .attr("class", "link")
          .attr("d", diagonal);

      var node = svg.selectAll(".node")
          .data(nodes)
          .enter().append("g")
          .attr("class", "node")
          .attr("transform", function (d) {
              return "translate(" + d.y + "," + d.x + ")";
          });

      node.append("circle")
          .attr("r", 10);

      node.append("text")
          .attr("dx", function (d) {
              return d.children ? 8 : 15;
          })
          .attr("dy", function (d){
              return d.children ? -20 : 3;
          })
          .style("display", function(d){
            if (d.children.length == 0)
              return "none"
            else return "inline";
          })
          .style("text-anchor", function (d) {
              return d.children ? "end" : "start";
          })
          .text(function (d) {
              return d.name;
          });

    }); // post done

  }); // serch form

}); // jQuery doc on load
