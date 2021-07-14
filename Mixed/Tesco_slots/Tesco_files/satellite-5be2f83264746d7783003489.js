_satellite.pushAsyncScript(function(event, target, $variables){
  if (/PL|CZ|SK|HU|MY|TH/g.test(_satellite.getVar("Country"))) {
    if ((/\/orders\/[0-9]+\/confirmation$|.*\/checkout\/order confirmation$|.*\/checkout\/confirmation$/).test(location.pathname)) {
      	var country = _satellite.getVar('Country');

        var awDisplay = {
            CZ: '//www.googleadservices.com/pagead/conversion/969616435/?value=0.00&label=&guid=ON&script=0',
            HU: '//www.googleadservices.com/pagead/conversion/971686223/?value=0.00&label=&guid=ON&script=0',
            MY: '//www.googleadservices.com/pagead/conversion/971452958/?value=0.00&label=&guid=ON&script=0',
            PL: '//www.googleadservices.com/pagead/conversion/971430398/?value=0.00&label=&guid=ON&script=0',
            SK: '//www.googleadservices.com/pagead/conversion/966710121/?value=0.00&label=&guid=ON&script=0',
            TH: '//www.googleadservices.com/pagead/conversion/965441531/?value=0.00&label=&guid=ON&script=0'
        };

        var ga_img_div_display = document.createElement('div');
        ga_img_div_display.style = "display:inline;"

        var ga_image_track2_display = document.createElement('img');
        ga_image_track2_display.height = "1";
        ga_image_track2_display.width = "1";
        ga_image_track2_display.style = "border-style:none;";
        ga_image_track2_display.alt = "";
        ga_image_track2_display.src = awDisplay[country];
        ga_img_div_display.appendChild(ga_image_track2_display);

        document.body.appendChild(ga_img_div_display);
    }
}
});
