if (_satellite.getVar('Country') === "UK") {
    // set source cookie
    var iCookieLength = 30; // Cookie length in days
    var sCookieName = sSourceParameterName = "source"; // Name of the first party cookie to utilise for last click referrer de-duplication
    var customerType = _satellite.getVar('busCustomerLoyaltyType')
    if (customerType == "first-time") {
        var commissionCode = "NEW_FT";
    }
    else {
        var commissionCode = "EXISTING";
    }
    var orderRef = _satellite.getVar('busOrderIdNumber');


    //  cookie problems - any other cookies?
    var _getQueryStringValue = function (sParameterName) {
        var aQueryStringPairs = document.location.search.substring(1).split("&");
        for (var i = 0; i < aQueryStringPairs.length; i++) {
            var aQueryStringParts = aQueryStringPairs[i].split("=");
            if (sParameterName.toLowerCase() == aQueryStringParts[0].toLowerCase()) {
                return aQueryStringParts[1];
            }
        }
    };

    var _getCookie = function (sCookieName) {
        sCookieName += "=";
        var aCookies = document.cookie.split(";");
        for (var i = 0; i < aCookies.length; i++) {
            while (aCookies[i].charAt(0) == " ") aCookies[i] = aCookies[i].substring(1);
            if (aCookies[i].indexOf(sCookieName) != -1) {
                return aCookies[i].substring(sCookieName.length, aCookies[i].length);
            }
        }
    };

    var _setCookie = function (sCookieName, sCookieContents, iCookieLength) {
        var dCookieExpires = new Date();
        dCookieExpires.setTime(dCookieExpires.getTime() + (iCookieLength * 24 * 60 * 60 * 1000));
        document.cookie = sCookieName + "=" + sCookieContents + "; expires=" + dCookieExpires.toGMTString() + "; path=/;";
    };

    var qs = _getQueryStringValue(sSourceParameterName);
    if (qs) {
        _setCookie(sCookieName, qs, iCookieLength);
    }

    function loadAwin() {
        var awin_lib = document.createElement('script');
        awin_lib.src = 'https://www.dwin1.com/7052.js';
        awin_lib.defer = 'defer';
        awin_lib.type = 'text/javascript';
        awin_lib.async = true;
        document.body.appendChild(awin_lib);
    }


    var isAmend = _satellite.getVar('busIsAmend');


    if ((location.href.indexOf("/checkout/confirmation") > -1) && (isAmend !== true)) {

        var totalAmount = Number(_satellite.getVar('busGuidePrice'));
        var AWIN = {};
        AWIN.Tracking = {};
        AWIN.Tracking.Sale = {};
        /*** Set your transaction parameters ***/
        AWIN.Tracking.Sale.amount = totalAmount;
        //AWIN.Tracking.Sale.channel = _getCookie(sCookieName) || "na";
        AWIN.Tracking.Sale.channel = "aw"; //temporary hardcoding
        AWIN.Tracking.Sale.currency = "GBP";
        AWIN.Tracking.Sale.custom = [_satellite.getVar('Customer ID')];
        AWIN.Tracking.Sale.orderRef = orderRef;
        AWIN.Tracking.Sale.parts = commissionCode + ":" + totalAmount;
        AWIN.Tracking.Sale.test = _satellite.settings.isStaging ? "1" : "0";
        //AWIN.Tracking.Sale.plt = [];
        //var accountPrefix = 'AW:P|7052|' + orderRef + '|';

        loadAwin();

    } else {
        loadAwin();
    }
}