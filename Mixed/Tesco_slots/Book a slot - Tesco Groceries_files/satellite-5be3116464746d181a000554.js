_satellite.pushAsyncScript(function(event, target, $variables){
  if (/SK|CZ|HU|PL|MY/g.test(_satellite.getVar("Country"))) {
    if ((/\/orders\/[0-9]+\/confirmation$|.*\/checkout\/order confirmation$|.*\/checkout\/confirmation$/).test(location.pathname)) {
        var country = _satellite.getVar('Country');

        var awSearchRemarketing = {
            CZ: '//www.googleadservices.com/pagead/conversion/968020275/?value=0.00&label=&guid=ON&script=0',
            HU: '//www.googleadservices.com/pagead/conversion/965571872/?value=0.00&label=&guid=ON&script=0',
            MY: '//www.googleadservices.com/pagead/conversion/967773804/?value=0.00&label=&guid=ON&script=0',
            PL: '//www.googleadservices.com/pagead/conversion/970010003/?value=0.00&label=&guid=ON&script=0',
            SK: '//www.googleadservices.com/pagead/conversion/970365126/?value=0.00&label=&guid=ON&script=0',
            TH: '//www.googleadservices.com/pagead/conversion/968344661/?value=0.00&label=&guid=ON&script=0'
        };

        var ga_img_div_searchRemarketing = document.createElement('div');
        ga_img_div_searchRemarketing.style = "display:inline;"

        var ga_image_track2_searchRemarketing = document.createElement('img');
        ga_image_track2_searchRemarketing.height = "1";
        ga_image_track2_searchRemarketing.width = "1";
        ga_image_track2_searchRemarketing.style = "border-style:none;";
        ga_image_track2_searchRemarketing.alt = "";
        ga_image_track2_searchRemarketing.src = awSearchRemarketing[country];
        ga_img_div_searchRemarketing.appendChild(ga_image_track2_searchRemarketing);

        document.body.appendChild(ga_img_div_searchRemarketing);
    }
}


});
