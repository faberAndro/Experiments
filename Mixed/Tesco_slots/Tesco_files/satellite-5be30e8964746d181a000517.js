_satellite.pushAsyncScript(function(event, target, $variables){
  if (/SK|CZ|HU|PL|MY/g.test(_satellite.getVar("Country"))) {
    if ((/\/orders\/[0-9]+\/confirmation$|.*\/checkout\/order confirmation$|.*\/checkout\/confirmation$/).test(location.pathname)) {

        var country = _satellite.getVar('Country');

        var awSearch = {
            CZ: '//www.googleadservices.com/pagead/conversion/967628968/?value=0.00&label=&guid=ON&script=0',
            HU: '//www.googleadservices.com/pagead/conversion/968287536/?value=0.00&label=&guid=ON&script=0',
            PL: '//www.googleadservices.com/pagead/conversion/985304386/?value=0.00&label=&guid=ON&script=0',
            SK: '//www.googleadservices.com/pagead/conversion/968997721/?value=0.00&label=&guid=ON&script=0'
        };

        var ga_img_div_search = document.createElement('div');
        ga_img_div_search.style = "display:inline;"

        var ga_image_track2_search = document.createElement('img');
        ga_image_track2_search.height = "1";
        ga_image_track2_search.width = "1";
        ga_image_track2_search.style = "border-style:none;";
        ga_image_track2_search.alt = "";
        ga_image_track2_search.src = awSearch[country];
        ga_img_div_search.appendChild(ga_image_track2_search);

        document.body.appendChild(ga_img_div_search);
    }
}
});
