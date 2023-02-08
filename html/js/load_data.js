function titleCase(str) {
  str = str.toLowerCase().split(' ');
  for (var i = 0; i < str.length; i++) {
    str[i] = str[i].charAt(0).toUpperCase() + str[i].slice(1); 
  }
  return str.join(' ');
}

PROGRESS_BAR_COLORS = {}
if(data.length != 0){
	singledev = data[0]
	for(var skill_index in data[0].skills){
		category = Object.keys(data[0].skills[skill_index])[0]
		if(category == "frontend") PROGRESS_BAR_COLORS[category] = "progress-bar-success";
		else if(category == "backend") PROGRESS_BAR_COLORS[category] = "progress-bar-info";
		else if(category == "writer") PROGRESS_BAR_COLORS[category] = "progress-bar-warning";
		else PROGRESS_BAR_COLORS[category] = "progress-bar-danger";
	}
}

for(var i in data){
	var card = document.createElement('div');
	card.className = "col-md-3";
	if(data[i].avatar_url == null || data[i].avatar_url.trim() == "") data[i].avatar_url = "img/github_profile.png";

	commit_star = "";
	for(var star=1; star<=5; star++)
		commit_star += '<span class=" ' + ( star<=data[i].commit_star ? "glyphicon glyphicon-star" : "glyphicon glyphicon-star-empty" ) + ' "></span>'
	
	progress_bar = "";
	for(var skill_index in data[i].skills){
		category = Object.keys(data[i].skills[skill_index])[0]
		percentage = data[i].skills[skill_index][category]
		progress_bar += '\
		<div class="row">\
			<div class="col-md-3"><b>' + titleCase(category) + '</b></div>\
			<div class="col-md-9"><div class="progress">\
				<div class="progress-bar ' + PROGRESS_BAR_COLORS[category] + '" role="progressbar" aria-valuenow="' + percentage + '" style="width:' + percentage + '%" >\
					' + percentage + '% ' + titleCase(category) + '\
				</div>\
			</div></div>\
		</div>\
		'
	}

	card.innerHTML = '\
		<div class="panel panel-default">\
    		<div class="panel-body">\
    		<p><img src="' + data[i].avatar_url + '" class="img-thumbnail" style="width: 300px;"></p>\
          	<div class="text-left">\
          		<h1 class="page-header">' + data[i].name + '<br/ ><small>' + (( data[i].username == null || data[i].username.trim() == "" ) ? "&nbsp;" : data[i].username) + '</small></h1>\
            	\
            	<div><h3> Commits: ' + data[i].commit + "&nbsp;&nbsp;&nbsp;&nbsp;" + commit_star + '</h3></div>\
            	' + progress_bar + '\
				<div style="overflow-y: auto; height: 70px;"><p>' + data[i].bio + '<p></div><br />\
            	<p><span class="glyphicon glyphicon-envelope" aria-hidden="true"></span> ' + data[i].email + '<p>\
            	<p><span class="glyphicon glyphicon-map-marker" aria-hidden="true"></span> ' + data[i].location + '<p>\
            	<p><span class="glyphicon glyphicon-link" aria-hidden="true"></span> ' + data[i].website + '<p>\
            </div>\
            </div>\
      	</div>';
	document.getElementById('main-row').appendChild(card);
}