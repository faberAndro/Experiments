if(_satellite.getVar('Country') === "UK"){
var script = document.createElement('script');
script.onload = function () {
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'AW-943890977'); //Remarketing only, on all pages

    //On order confirmation pages:
    if (location.href.indexOf("checkout/confirmation") > -1) {
        //Variable declaration
        var guidePrice = Number(_satellite.getVar('busGuidePrice'));

        //Order confirmation page pixel
        gtag('config', 'AW-951203243');
        gtag('event', 'conversion', {
            'send_to': 'AW-951203243/fjSZCK-j_lwQq-vIxQM',
            'value': guidePrice,
            'currency': 'GBP'
        });

    }
};
script.src = "https://www.googletagmanager.com/gtag/js?id=AW-943890977";

document.head.appendChild(script);
};