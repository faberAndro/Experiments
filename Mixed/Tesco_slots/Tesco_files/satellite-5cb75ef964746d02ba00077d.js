_satellite.pushAsyncScript(function(event, target, $variables){
  var src; if (_satellite.getVar("Country") == "UK") {
  if (_satellite.getVar("Customer Type") == "logged in" && _satellite.settings.isStaging == false) {
	//if (_satellite.getVar("Customer Type") == "logged in") {
      src = "https://d.turn.com/r/dd/id/L21rdC8xNDA3L2NpZC8xNzQ4MTQ0NDcxL3QvMg/dpuid/"+_satellite.getVar('UUID')+"/cat/1/url/http://cm.g.doubleclick.net/pixel?google_nid=turn_dmp&google_cm";
       var amobee = document.createElement("img")
       amobee.src = src
       document.body.appendChild(amobee);
   
    }
 }
});
