

(function() {
  "use strict";

  // Grant your CesiumJS app access to your ion assets
  // This is your actual default access token, you can copy/paste this directly into your app code
  Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJkMzBlYjA2Ny1jMDYxLTQ4N2EtYjJmMS1lZGU3NjBmYTM0NmUiLCJpZCI6MzI3NywiaWF0IjoxNTM2NzUxNzY2fQ.epsDLR73UzhH-Zd-OeEBy3b2Cfk9AAh0fNP2hbwyvqU';

  var viewer = new Cesium.Viewer("cesium", {
    animation: false,
    timeline: false
  });

  var query = " select distinct * ";
  query += " where { ";
  query += " ?s <http://dbpedia.org/ontology/thumbnail> ?thumb . ";
  query += " ?s <http://www.w3.org/2003/01/geo/wgs84_pos#lat> ?lat . ";
  query += " ?s <http://www.w3.org/2003/01/geo/wgs84_pos#long> ?long . ";
  query += " optional { ?s rdfs:comment ?comment . } ";
  query += " } ";

  $.ajax({
    url:'https://dydra.com/ut-digital-archives/iiif/sparql',
    type:'POST',
    data:{
      query : query,
      format : "json"
    }
  })
  // Ajaxリクエストが成功した時発動
  .done( (data) => {

    var result = data.results.bindings;

    var result2 = new Object()
    for (var i = 0; i < result.length; i++) {
      var obj = result[i]
      var s = obj.s.value;
      if(!result2[s]){
        result2[s] = obj
      }
    }

    result = new Array()
    for(var s in result2){
      result.push(result2[s])
    }

    var pinBuilder = new Cesium.PinBuilder();

    for (var i = 0; i < result.length; i++) {
      var obj = result[i];

      var s = obj.s.value
      var str = s.split("/")
      var title = str[str.length-1];

      var bluePin = viewer.entities.add({
        name : title,
        position : Cesium.Cartesian3.fromDegrees(Number(obj.long.value),Number(obj.lat.value),0),
        billboard : {
          image : pinBuilder.fromColor(Cesium.Color.ROYALBLUE, 48).toDataURL(),
          verticalOrigin : Cesium.VerticalOrigin.BOTTOM
        }
      });

      var div = $("<div>")
      div.attr("style", "height : 500px;")

      if(obj.thumb){
        var p = $("<p>");
        div.append(p)
        var img = $("<img>");
        p.append(img)
        img.attr("style", "float:left; margin: 0 1em 1em 0;")
        img.attr("src", obj.thumb.value)
        img.attr("width", "144px")
      }

      if(obj.comment){
        var p = $("<p>");
        div.append(p)
        p.append(obj.comment.value);
      }

      var p = $("<p>");
      div.append(p)

      var url = "http://iiif2.dl.itc.u-tokyo.ac.jp/s/iiif/search?q=dcterms_subject_ss"+encodeURIComponent(":\""+title+"\"");

      var a = $("<a>")
      p.append(a)
      a.attr("style", "color: WHITE;")
      a.attr("target", "_blnak")
      a.attr("href", url)
      a.append("View")

      bluePin.description = div.html();
    }

    //viewer.zoomTo(viewer.entities);
    viewer.camera.flyTo({
      destination: Cesium.Cartesian3.fromDegrees(139.760346, 35.710930, 300000)
    })

  })
  // Ajaxリクエストが失敗した時発動
  .fail( (data) => {
    alert(data.statusText);
  })
  // Ajaxリクエストが成功・失敗どちらでも発動
  .always( (data) => {

  });


}());
