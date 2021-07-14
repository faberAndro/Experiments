if(_satellite.getVar('Country') === "UK") {
    var _dtmPageUrl = window.location.href;
    var _dtmPagePath = window.location.pathname;
    _dtmPagePath = _dtmPagePath.split("/");
    var _dtmPagePop = _dtmPagePath.pop();
    var _dtmCategory = _satellite.getVar('busPageTitle');
    var _dtmPageHierarchy = _satellite.getVar('busPageHierOrig');
    var _dtmSuperDepartment = _satellite.getVar('busSuperDepartment');
    var _dtmDepartment = _satellite.getVar('busDepartment');
    var _dtmAisle = _satellite.getVar('busAisle');
    var _dtmCountry = _satellite.getVar('Country');
    var _dtmAuth = _satellite.getVar('busCustomerAuthenticated');
    if(_dtmAuth) {
        var _dtmAuthenticated = _dtmAuth.toString();
    };
    var UUID = _satellite.readCookie('UUID');
    var sociomanticId = "";
    var sociomanticHost = "";
    var sociomanticTrolleyData = "";
    var sociomanticTransaction = "";
    var sociomanticGuidePrice = "";
    var sociomanticSlotStart = "";
    var sociomanticCurrency = "";
    var sociomanticIdentifier = "";
    //*****territory identifier ******
    if(_dtmCountry === "UK") {
        sociomanticCurrency = "";
        sociomanticId = "tesco-uk";
        sociomanticHost = "eu-sonar.sociomantic.com";
        sociomanticCurrency = "GBP";
    }
    //*****set customer data if logged in ******
    _satellite.notify("Sociomantic Auth: " + _dtmAuthenticated);
    _satellite.notify("Sociomantic ID: " + UUID);
    if(_dtmAuthenticated === "logged in") {
        var sonar_customer = {
            identifier: UUID
        }// cID
    };
    //************* UK ONLY Category / Buy List / Zone / Promotion Pages *************
    if(_dtmPageUrl.indexOf("/categories/") > -1 || _dtmPageUrl.indexOf("/buy-lists/") > -1 || _dtmPageUrl.indexOf("/zones/") > -1 || _dtmPageUrl.indexOf("/promotions/") > -1 || _dtmPageUrl.indexOf("/shop/") > -1) {
        var sonar_product = {category: [_satellite.getVar('busSuperDepartment'), _satellite.getVar('busDepartment'), _satellite.getVar('busAisle')]};
    };
    if(_dtmPageUrl.indexOf("/favorites") > -1) {
        var sonar_product = {
            category: ['Favorites']
        };
    };
    //************* Product Page *************
    if(_dtmPageUrl.indexOf("/products/") > -1) {
        var _dtmProductId = _satellite.getVar('productID');
        _satellite.notify("Sociomantic Product: " + _dtmProductId);
        var sonar_product = {
            identifier: _dtmProductId,
            category: _satellite.getVar('busAisle')
        };
    };
    //************* Trolley Page *************
    if(_dtmPageUrl.indexOf("/order-summary") > -1) {
        sociomanticTrolleyData = _satellite.getVar('busSociomanticProductString');
        _satellite.notify("BERTIE 3 :" + sociomanticTrolleyData);
        var sonar_basket = {
            products: sociomanticTrolleyData
        };
    }
    if(_dtmPageUrl.indexOf("confirmation") > -1) {
        sociomanticTrolleyData = _satellite.getVar('busSociomanticProductString');
        sociomanticTransaction = _satellite.getVar('busOrderIdNumber');
        sociomanticGuidePrice = Number(_satellite.getVar('busGuidePrice'));
        sociomanticSlotStart = Date.parse(_satellite.getVar('busSlotStart')) / 1000;
        //sociomanticSlotStart1 = sociomanticSlotStart.toString();
        var sonar_basket = {
            products: sociomanticTrolleyData,
            transaction: sociomanticTransaction,
            amount: sociomanticGuidePrice,
            currency: sociomanticCurrency,
            date: sociomanticSlotStart.toString()
        };
    }
    //************* set UK only data ************* 
    //************* Amend Start *************
    var _dtmAmendStart = _satellite.getVar('bus.CustomerData.AmendStart');
    if(_dtmAmendStart === "true") {
        _satellite.notify("Sociomantic Amend: " + _dtmAmendStart);
        var sonar_product = {
            category: ['Start Amend']
        };
    };
    //************* Amend Complete *************
    if(_satellite.getVar('busIsAmend')) {
        _satellite.notify("Sociomantic Amend: Complete");
        var sonar_product = {
            category: ['Complete Amend']
        }
    };
    //*** Delivery on page refresh, please note separate event base rule for Ajax call ***
    if(_dtmPagePop === "slots") {
        _satellite.notify("Sociomantic Book a Slot: " + _dtmPagePop);
        var sonar_product = {
            category: ['Book a Slot']
        }
    } else if(_dtmPagePop === "delivery") {
        _satellite.notify("Sociomantic Home Delivery: " + _dtmPagePop);
        var sonar_product = {
            category: ['Home Delivery']
        }
    } else if(_dtmPagePop === "collection") {
        _satellite.notify("Sociomantic Click and Collect: " + _dtmPagePop);
        var sonar_product = {
            category: ['Click and Collect']
        }
    }
    //************* end of UK only data ************* 
    //************* Product Page *************
    //************* Inclusion Tag *************
    (function () {
        var s = document.createElement('script');
        var x = document.getElementsByTagName('script')[0];
        s.type = 'text/javascript';
        s.async = true;
        s.src = 'https://' + sociomanticHost + '/js/2010-07-01/adpan/' + sociomanticId;
        x.parentNode.insertBefore(s, x);
    }
    )
        ();
} 
