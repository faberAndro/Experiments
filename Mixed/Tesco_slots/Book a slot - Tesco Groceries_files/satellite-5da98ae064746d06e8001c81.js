_satellite.pushAsyncScript(function(event, target, $variables){
  var country = _satellite.getVar('Country');
var inValidPages = /\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/(account|register).*/
var siteApplication = _satellite.getVar("busSiteApplication");
var dataEnvironment = document.documentElement.getAttribute("data-environment");
var rand = Date.now();

if (
    siteApplication == "prd" ||
    dataEnvironment == "live" ||
    dataEnvironment == "container"
  ) {
	if(!inValidPages.test(document.location.pathname)){

		if(country == "CZ"){
		    var src = "//secure.adnxs.com/seg?add=19461918&t=2&src.rand="+rand;    
		    src = encodeURI(src);
		    var adnxs = document.createElement("img");
		    adnxs.src = src;
		    document.body.appendChild(adnxs);

		    src = "//cz-gmtdmp.mookie1.com/t/v2/activity?tagid=V2_739559&src.rand="+rand;  
		    src = encodeURI(src);
		    var mookie = document.createElement("img")
		    mookie.src = src;
		    document.body.appendChild(mookie);
		}

		if(country == "HU"){
			// This one might not work
		    var src = "//hu-gmtdmp.mookie1.com/t/v2/activity?tagid=V2_737599&src.rand="+rand;  
		    src = encodeURI(src);
		    var mookie = document.createElement("img")
		    mookie.src = src;
		    document.body.appendChild(mookie);
		}

		if(country == "SK"){
		    var src = "//secure.adnxs.com/seg?add=19471024&t=2&src.rand="+rand;    
		    src = encodeURI(src);
		    var adnxs = document.createElement("img");
		    adnxs.src = src;
		    document.body.appendChild(adnxs);
		}

		if(country == "PL"){
			// This one might not work
		   	var src = "//secure.adnxs.com/seg?add=18224220&t=1&src.rand="+rand;  
		    src = encodeURI(src);
		    var adnxs = document.createElement("img");
		    adnxs.src = src;
		    adnxs.type = 'text/javascript';
		    document.body.appendChild(adnxs);

		    // This one might not work
		    src = "//secure.adnxs.com/seg?add=18224249&t=1&src.rand="+rand;  
		    src = encodeURI(src);
		    adnxs = document.createElement("img");
		    adnxs.src = src;
		    adnxs.type = 'text/javascript';
		    document.body.appendChild(adnxs);

		    src = "//secure.adnxs.com/px?id=1125644&t=2&src.rand="+rand;  
		    src = encodeURI(src);
		    adnxs = document.createElement("img");
		    adnxs.src = src;
		    document.body.appendChild(adnxs);
			
		    src = "//secure.adnxs.com/seg?add=18275012&t=2&src.rand="+rand;  
		    src = encodeURI(src);
		    adnxs = document.createElement("img");
		    adnxs.src = src;
		    document.body.appendChild(adnxs);

		    src = "//secure.adnxs.com/seg?add=18224081&t=2&src.rand="+rand;  
		    src = encodeURI(src);
		    adnxs = document.createElement("img");
		    adnxs.src = src;
		    document.body.appendChild(adnxs);

		    src = "//pl-gmtdmp.mookie1.com/t/v2/activity?tagid=V2_736808&src.rand="+rand;  
		    src = encodeURI(src);
		    var mookie = document.createElement("img")
		    mookie.src = src;
		    document.body.appendChild(mookie);
		}
	}
}

});
