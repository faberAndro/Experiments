_satellite.pushAsyncScript(function(event, target, $variables){
  if (/PL|CZ|SK|HU|MY|TH/g.test(_satellite.getVar("Country"))) {
    if ((/\/orders\/[0-9]+\/confirmation$|.*\/checkout\/order confirmation$|.*\/checkout\/confirmation$/).test(location.pathname)) {
        var country = _satellite.getVar('Country');

        var awDisplayRemarketing = {
          CZ :  '//www.googleadservices.com/pagead/conversion/964910274/?value=0.00&label=&guid=ON&script=0',
          HU :  '//www.googleadservices.com/pagead/conversion/967284559/?value=0.00&label=&guid=ON&script=0',
          MY :  '//www.googleadservices.com/pagead/conversion/972207575/?value=0.00&label=&guid=ON&script=0',
          PL :  '//www.googleadservices.com/pagead/conversion/966688041/?value=0.00&label=&guid=ON&script=0',
          SK :  '//www.googleadservices.com/pagead/conversion/968254421/?value=0.00&label=&guid=ON&script=0',
          TH :  '//www.googleadservices.com/pagead/conversion/979594647/?value=0.00&label=&guid=ON&script=0'
        };
        
        var ga_img_div_displayRemarketing = document.createElement('div');
        ga_img_div_displayRemarketing.style = "display:inline;"
        
        var ga_image_track2_displayRemarketing = document.createElement('img');
        ga_image_track2_displayRemarketing.height = "1";
        ga_image_track2_displayRemarketing.width = "1";
        ga_image_track2_displayRemarketing.style = "border-style:none;";
        ga_image_track2_displayRemarketing.alt = "";
        ga_image_track2_displayRemarketing.src = awDisplayRemarketing[country];
        ga_img_div_displayRemarketing.appendChild(ga_image_track2_displayRemarketing);
        
        document.body.appendChild(ga_img_div_displayRemarketing);
    }
}
});
