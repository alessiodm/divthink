jQuery(document).ready(function($){

  var width = 700, height = 500;

  var cluster = d3.layout.tree()
      .size([width - 160, height - 100]);

  var diagonal = d3.svg.diagonal()
      .projection(function (d) {
      return [d.x, d.y];
  });

  $("#searchForm").submit(function(event) {
    event.preventDefault();
    var $form = $( this ),
    str = $form.find( 'input[name="search_string"]' ).val(),
    s3cret = $form.find( 'input[name="secret"]' ).val(),
    url = $form.attr( 'action' );
    
    var posting = $.post( url, { search_string: str, secret: s3cret } );
    
    d3.select("svg").remove();
    var svg = d3.select("#tree").append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", "translate(80,40)");

    posting.done(function( data ) {
      $( "#result" ).empty().append( data );
      
      data = JSON.parse(data);
      var nodes = cluster.nodes(data["crawled_paths"]),
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
              dy = d.y;
              if (isVisited(d)){
                dy += 5;
              }
              return "translate(" + d.x + "," + dy + ")";
          });

      node.append("circle")
        .attr("r", 10)
        .style("fill", function(d){
            return getNodeColor(d);
        })
        .on("mouseover", function() {
          d3.select(this)
              .transition()
              .duration(100)
              .attr("r", 15)
              .style("fill", function(d){
                return isVisited(d) ? "#a00" : "#FF9900"
              });
         d3.select(this.parentNode)
              .append("text")/*
                .attr("dx", function (d) {
                    return d.children ? 8 : 25;
                })*/
                .attr("dy", -20)
                .text(function (d) {
                    return d.name;
                });
        })
        .on("mouseout",  function(d) {
          var color = getNodeColor(d);
          d3.select(this)
              .transition()
              .duration(100)
              .attr("r", 10)
              .style("fill", color);
          d3.select(this.parentNode).selectAll("text")
              .remove();
        })
        .on("click", function(d){
          $("#aaa").html(d3.select(this.parentNode).selectAll("text").text());
        });

      function getNodeColor(d){
          return isVisited(d) ? "#a00" : "#eee";
      }

      function isVisited(d){
         return d.visited || (d.children !== undefined && d.children.length > 0)
      }

    }); // post done

  }); // serch form

}); // jQuery doc on load
