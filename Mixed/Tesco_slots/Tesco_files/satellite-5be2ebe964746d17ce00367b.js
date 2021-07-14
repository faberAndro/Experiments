_satellite.pushAsyncScript(function(event, target, $variables){
  if (/PL|CZ|SK|HU|MY|TH/g.test(_satellite.getVar("Country"))) {
    if ((/\/orders\/[0-9]+\/confirmation$|.*\/checkout\/order confirmation$|.*\/checkout\/confirmation$/).test(location.pathname)) {

        var country = _satellite.getVar('Country');

        var awDSA = {
            CZ: '//www.googleadservices.com/pagead/conversion/964762945/?value=0.00&label=&guid=ON&script=0',
            HU: '//www.googleadservices.com/pagead/conversion/966889653/?value=0.00&label=&guid=ON&script=0',
            MY: '//www.googleadservices.com/pagead/conversion/964180833/?value=0.00&label=&guid=ON&script=0',
            PL: '//www.googleadservices.com/pagead/conversion/979418962/?value=0.00&label=&guid=ON&script=0',
            SK: '//www.googleadservices.com/pagead/conversion/971380898/?value=0.00&label=&guid=ON&script=0',
            TH: '//www.googleadservices.com/pagead/conversion/971475218/?value=0.00&label=&guid=ON&script=0'
        };

        var ga_img_div_dsa = document.createElement('div');
        ga_img_div_dsa.style = "display:inline;"

        var ga_image_track2_dsa = document.createElement('img');
        ga_image_track2_dsa.height = "1";
        ga_image_track2_dsa.width = "1";
        ga_image_track2_dsa.style = "border-style:none;";
        ga_image_track2_dsa.alt = "";
        ga_image_track2_dsa.src = awDSA[country];
        ga_img_div_dsa.appendChild(ga_image_track2_dsa);

        document.body.appendChild(ga_img_div_dsa);
    }
}

});
