_satellite.pushAsyncScript(function(event, target, $variables){
  if(_satellite.getVar("Country")=="CZ"){
  if((/\/orders\/[0-9]+\/confirmation$|.*\/checkout\/order confirmation$|.*\/checkout\/confirmation$/).test(location.pathname)){
    var ga_img_div_dsa2 = document.createElement('div');
    ga_img_div_dsa2.style = "display:inline;"
    
    var ga_image_track2_dsa2 = document.createElement('img');
    ga_image_track2_dsa2.height = "1";
    ga_image_track2_dsa2.width = "1";
    ga_image_track2_dsa2.style = "border-style:none;";
    ga_image_track2_dsa2.alt = "";
    ga_image_track2_dsa2.src = "//www.googleadservices.com/pagead/conversion/972207575/?value=0.00&label=&guid=ON&script=0";
    ga_img_div_dsa2.appendChild(ga_image_track2_dsa2);
    
    document.body.appendChild(ga_img_div_dsa2);
  }
}

});
