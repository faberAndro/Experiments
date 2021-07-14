_satellite.pushAsyncScript(function(event, target, $variables){
  if(_satellite.getVar('Country') === "TH"){ 
  if(!(/\/orders$|\/slots\/|\/ShoppingCart\/Details|\/checkout\/payment\-options|\/checkout\/review\-trolley|\/Order\/AbortAmend|\/account$|\/Delivery\/UnReserveSlot|\/slots$|\/refresh-confirmation|\/order-confirmation\?/).test(location.pathname)){
    
  var ga_img_div = document.createElement('div');
  ga_img_div.style = "display:inline;"
   
  var ga_img_track = document.createElement('img');
  ga_img_track.height = "1";
  ga_img_track.width = "1";
  ga_img_track.style = "border-style:none;";
  ga_img_track.alt = "";
  ga_img_track.src = "//googleads.g.doubleclick.net/pagead/viewthroughconversion/952316500/?value=0&guid=ON&script=0";
  ga_img_div.appendChild(ga_img_track);
  
  if (location.pathname.indexOf ("/checkout/confirmation") >= 0) {
    /* confirmation page only */
    var ga_image_track2 = document.createElement('img');
    ga_image_track2.height = "1";
    ga_image_track2.width = "1";
    ga_image_track2.style = "border-style:none;";
    ga_image_track2.alt = "";
    ga_image_track2.src = "//www.googleadservices.com/pagead/conversion/952316500/?value=0.00&currency_code=THB&label=aWU7CLu66WYQ1OSMxgM&guid=ON&script=0";
    ga_img_div.appendChild(ga_image_track2);
  } 
  
  if (location.pathname.indexOf ("/register/confirmation") >= 0) {
    /* confirmation page only */
    var ga_image_track2 = document.createElement('img');
    ga_image_track2.height = "1";
    ga_image_track2.width = "1";
    ga_image_track2.style = "border-style:none;";
    ga_image_track2.alt = "";
    ga_image_track2.src = "//www.googleadservices.com/pagead/conversion/952316500/?value=0.00&currency_code=THB&label=b4_2CK2qgGsQ1OSMxgM&guid=ON&script=0";
    ga_img_div.appendChild(ga_image_track2);
  } 
  
  document.body.appendChild(ga_img_div);
  }
}
});
