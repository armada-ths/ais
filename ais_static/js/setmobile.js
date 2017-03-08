(function() {

    var throttle = function(type, name, obj) {
        obj = obj || window;
        var running = false;
        var func = function() {
            if (running) { return; }
            running = true;
             requestAnimationFrame(function() {
                obj.dispatchEvent(new CustomEvent(name));
                running = false;
            });
        };
        obj.addEventListener(type, func);
    };

    var setMobile = function() {
    	var mobile = false;
    	if (window.innerWidth < 992 && mobile == false) {
    		var container = document.getElementsByClassName("container")[0];
    		container.className =  container.className.replace( /(?:^|\s)container(?!\S)/g , 'container-fluid' )    	
    		mobile = true;
    	} else if (window.innerWidth >= 992 && mobile == true) {
    		var container = document.getElementsByClassName("container-fluid")[0];
    		container.className = "container"
    		mobile = false;
    	}
    };

    setMobile();
    throttle("resize", "optimizedResize");
})();

window.addEventListener("optimizedResize", function() {
	setMobile()
});

