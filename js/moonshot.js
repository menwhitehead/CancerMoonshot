
var points = "";
var titles = {};
var keywords = {};
var snippet_length = 100;

function loadTitles() {
    Papa.parse("viz_images/cancer_titles.dat", {
	download: true,
	complete: function(results) {
	    var data = results["data"];
	    for (var i = 0; i < data.length; i++) {
		var curr = data[i];
		var key = curr[0].split(" ")[0];
		var title = curr[0].split(" ").slice(1).join(" ");

		//titles[tokens[0]] = tokens.slice(1).join(" ");

		for (var j = 1; j < curr.length; j++) {
		    title += ", " + curr[j];
		}
		if (title.length > snippet_length) {
		    titles[key] = title.slice(0, snippet_length) + "...";
		} else {
		    titles[key] = title;		    
		}
	    }
	}
    });
}

function loadKeywords() {

    Papa.parse("viz_images/keywords.dat", {
	download: true,
	complete: function(results) {
	    for (var i = 0; i < results["data"].length; i++) {
		var tokens = results["data"][i][0].split(" ");
		keywords[tokens[0]] = 1;
	    }
	    $('#patent').html("");
	}
    });

}


$('#main').click(function (e) { //Offset mouse Position
    var posX = $(this).offset().left,
        posY = $(this).offset().top;
    var clickx = e.pageX - posX;
    var clicky = e.pageY - posY;

    var datapoints = points["data"];

    var dist_threshold = 7;
    var min_dist = 9999999;
    var min_doc = "";
    var min_x = 0;
    var min_y = 0;
    var my_canvas = $('#main');
    
    for (var i = 0; i < datapoints.length; i++) {
        var patent_id = datapoints[i][0];
        var x = datapoints[i][1];
        var y = datapoints[i][2];
        var dist = Math.sqrt(Math.pow((x - clickx), 2) + Math.pow((y - clicky), 2));
        if (dist < min_dist) {
	    min_dist = dist;
	    min_doc = patent_id;
	    min_x = x;
	    min_y = y;
        }
    }

    if (min_dist < dist_threshold) {
        console.log("SELECTED: " + min_doc);
	removeSelection();
	var google_link = 'Patent <a target="_blank" href="https://www.google.com/patents/US' + min_doc.slice(1) + '">' + min_doc.slice(1) + '</a>';
	var title = titles[min_doc];
	$('#patent').html(google_link + " : " + title);

	my_canvas.drawArc({
	    layer: true,
	    name: "dotlayer",
	    strokeStyle: 'rgb(255, 100, 200)',
	    strokeWidth: 2,
	    fillStyle: 'rgba(255, 100, 200, 0.1)',
	    x: min_x, y: min_y,
	    radius: 12
	})
	
    }
    else {
        removeSelection();
    }
});


function removeSelection() {
  var my_canvas = $('#main');
  my_canvas.removeLayer('dotlayer').drawLayers();
  var google_link = '';
  $('#patent').html(google_link);
}


function loadImage(path, width, height, target) {
    var my_canvas = $('#main'); 
    clearResults();
    my_canvas.drawImage({
	source: path,
	layer: true,
	name: "imagelayer",
	fromCenter: false
	//x: 0, y: 0
    });
}

function clearResults() {
  var my_canvas = $('#main');
  //my_canvas.removeLayer('dotlayer');
  removeSelection();
  my_canvas.removeLayer('imagelayer')
  my_canvas.drawLayers();
}


function runQuery() {
    var keyword = document.getElementById("query").value;
    keyword = keyword.strip();
    if (keyword in keywords) {
	var base_path = "viz_images/" + keyword;
	var img_path = base_path + ".png";
	var dat_path = base_path + ".dat";
	loadImage(img_path, 800, 600, "#main");
	
	Papa.parse(dat_path, {
	    download: true,
	    complete: function(results) {
		console.log(results);
		points = results;
	    }
	});
    }
    else {
	clearResults();
	$('#patent').html("Search term not found");
    }
}


// MAIN
loadTitles();
loadKeywords();
