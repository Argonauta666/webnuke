window.wn_getNgResourceClasses = function(){
	var resource_classes = [];
	var deps = wn_getAllAngularDeps();
	
	if(typeof angular !== 'undefined'){
		angular.forEach(deps, function(m){
			var contains_ngresource = false;
			angular.forEach(m['deps'], function(mm){
				if(mm == 'ngResource'){
					var namespace = m['namespace']
					
					var angular_classes = wn_getAngularClasses(namespace);
					angular.forEach(angular_classes, function(angular_classname){
						resource_classes.push(angular_classname['name']);
					});
				}
			});
		});
	}
	return resource_classes;
};

window.wn_testNgResourceClasses = function(){
	console.log('webnuke: AngularJS Testing ngResource Classes');
	console.log('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-');
	var angular_classes = wn_getNgResourceClasses();
	console.log("w00p");
	console.log(angular_classes);

	if(typeof angular !== 'undefined'){
		angular.forEach(angular_classes, function(m){
			console.log('Testing '+m)
			// try get method
			try {
				var classtotest = m;
				var res = angular.element(document.body).injector().get(classtotest);
				if(typeof res['get'] == 'function'){
					res.get({}, function(data){
						console.log("Received data for "+classtotest);
						//console.log(data);
					}, function(data){
						console.log("error receiving data for "+classtotest);
					});
				}
			}
			catch(err) {
				console.log("Error with '"+m+"' class - "+err.message);
			}
			
			
			// try query method
			try {
				var classtotest = m;
				var res = angular.element(document.body).injector().get(classtotest);
				if(typeof res['query'] == 'function'){
					res.query({}, function(data){
						console.log("Received data for "+classtotest);
						//console.log(data);
					}, function(data){
						console.log("Error receiving data for "+classtotest);
					});
				}
			}
			catch(err) {
				console.log("Error with '"+m+"' class - "+err.message);
			}			
		});
	}
	else{
		console.log("Angular UNDEFINED!!!");
	}
};
