// if (/PL|CZ|SK|HU/g.test(_satellite.getVar("Country"))) {
//     var _dtmPageUrl = window.location.href;
//     var _dtmPagePath = window.location.pathname;
//     _dtmPagePath = _dtmPagePath.split("/");
//     var _dtmPagePop = _dtmPagePath.pop();
//     var _dtmCategory = _satellite.getVar('busPageTitle');
//     var _dtmPageHierarchy = _satellite.getVar('busPageHierOrig');
//     var _dtmSuperDepartment = _satellite.getVar('busSuperDepartment');
//     var _dtmDepartment = _satellite.getVar('busDepartment');
//     var _dtmAisle = _satellite.getVar('busAisle');
//     var _dtmCountry = _satellite.getVar('Country');
//     var _dtmAuth = _satellite.getVar('busCustomerAuthenticated');
//     if (_dtmAuth) {
//         var _dtmAuthenticated = _dtmAuth.toString();
//     };
//     var _dtmSuperDepartmentId = _satellite.getVar('busSuperDepartmentId');
//     var _dtmDepartmentId = _satellite.getVar('busDepartmentId');
//     var _dtmAisleId = _satellite.getVar('busAisleId');
//     var _dtmCustomerId = _satellite.getVar("Customer ID : Hashed UUID");
//     var _dtmHashedEmail = _satellite.getVar('busCustomerHashedEmail');
//     var sociomanticId = "";
//     var sociomanticHost = "";
//     var sociomanticTrolleyData = "";
//     var sociomanticTransaction = "";
//     var sociomanticGuidePrice = "";
//     var sociomanticSlotStart = "";
//     var sociomanticCurrency = "";
//     var sociomanticIdentifier = "";
//     var promotionName = "";
//     // var asia = (/TH|MY/g.test(_satellite.getVar("Country")));
//     //setting up empty sonar vars for asia 
//     var sonar_basket;
//     var sonar_customer;
//     var sonar_product;
//     //*****territory identifier ******
//     if (_dtmCountry === "SK") {
//         // sociomanticCurrency = "";
//         sociomanticId = "tesco-sk";
//         sociomanticHost = "eu-sonar.sociomantic.com";
//         sociomanticCurrency = "EUR";
//     } else if (_dtmCountry === "PL") {
//         //  sociomanticCurrency = "";
//         sociomanticId = "tesco-pl";
//         sociomanticHost = "eu-sonar.sociomantic.com";
//         sociomanticCurrency = "PLN";
//     } else if (_dtmCountry === "HU") {
//         //  sociomanticCurrency = "";
//         sociomanticId = "tesco-hu";
//         sociomanticHost = "eu-sonar.sociomantic.com";
//         sociomanticCurrency = "HUF";
//     } else if (_dtmCountry === "CZ") {
//         //  sociomanticCurrency = "";
//         sociomanticId = "tesco-cz";
//         sociomanticHost = "eu-sonar.sociomantic.com";
//         sociomanticCurrency = "CZK";
//     }
//     //*****set customer data if logged in ******
//     if (_dtmAuthenticated === "logged in") {
//         var customer = {
//             identifier: _dtmCustomerId,
//             mhash: _dtmHashedEmail
//         }// cID             
//         // asia ? sonar_customer = { mhash: _dtmHashedEmail } : null;
//     };
//     //************* Category / Shop Pages *************
//     if (_dtmPageUrl.indexOf("/categories/") > -1 || _dtmPageUrl.indexOf("/shop/") > -1) {
//      /*sonar_product*/ var product = { category: [_satellite.getVar('busSuperDepartment'), _satellite.getVar('busDepartment'), _satellite.getVar('busAisle')] };
//         //  asia ? sonar_product = product : null;
//     };
//     // Promotion pages
//     if (_dtmPageUrl.indexOf("/promotions") > -1 || _dtmPageUrl.indexOf("/buy-lists/") > -1) {
//         promotionName = document.getElementsByClassName('heading query')[0].innerHTML;
//         var product = { category: [decodeURI(promotionName)] };
//         // asia ? sonar_product = product : null;
//     }
//     //************* Product Page *************
//     if (_dtmPageUrl.indexOf("/products/") > -1) {
//         var _dtmProductId = location.pathname.split('/')[4];
//         var product = {
//             identifier: _dtmProductId
//         };
//         // asia ? sonar_product = { identifier: _dtmProductId, category: _satellite.getVar('busAisle') } : null;
//     }
//     //CE and Asia don't have favourite sections 
//     if (_dtmPageUrl.indexOf("/favorites") > -1) {
//         var product = {
//             category: ['Favorites']
//         };
//         // asia ? sonar_product = product : null;
//     };
//     if (_dtmPageUrl.indexOf("/search") > -1) {
//         var product = {
//             category: ['Search']
//         };
//         // asia ? sonar_product = product : null;
//     };
//     // begin rest of script 
//     // _satellite.notify("Sociomantic Product: " + _dtmProductId);
//     // var product = {
//     //   identifier : _dtmProductIdStr 
//     // };
//     // var _dtmProductId = location.pathname.split('/')[4];
//     // _satellite.notify("Sociomantic Product: " + _dtmProductId);
//     // var product = {
//     //   identifier : _dtmProductId 
//     // };
//     // var sonar_product = product; r
//     //end rest of script 
//     //registration confirmation
//     if (_dtmPageUrl.indexOf("/register/confirmation") > -1) {
//         var rdmTransactionId = Math.random().toString().slice(2, 12);
//         var lead = {
//             transaction: rdmTransactionId
//         };
//     };
//     //************* Trolley Page *************
//     if (_dtmPageUrl.indexOf("/trolley") > -1) {
//         sociomanticTrolleyData = _satellite.getVar('busSociomanticProductString');
//         if (sociomanticTrolleyData != "") {
//             var basket = {
//                 products: sociomanticTrolleyData
//             };
//             var sonar_basket = basket;
//         };
//     }
//     //************* Review Trolley / payment options page *************
//     if (_dtmPageUrl.indexOf("/review-trolley") > -1 || _dtmPageUrl.indexOf("/payment-ptions") > -1) {
//         var eeSocioProductArray = _satellite.getVar('busBasketItems');
//         var addProductDetailsArray = [];
//         if ((typeof eeSocioProductArray != "undefined") && (eeSocioProductArray != "")) {
//             for (i = 0; i < eeSocioProductArray.length; i++) {
//                 var socTpnb = eeSocioProductArray[i].tpnb;
//                 var socAmt = parseFloat(eeSocioProductArray[i].priceBreakdown.unitPrice.price).toFixed(2);
//                 var socQty = eeSocioProductArray[i].qty;
//                 addProductDetailsArray.push({
//                     identifier: socTpnb,
//                     amount: socAmt,
//                     currency: sociomanticCurrency,
//                     quantity: socQty
//                 })
//                 var basket = {
//                     products: addProductDetailsArray
//                 };
//                 //   asia ? sonar_basket = basket : null;
//             }
//         }
//     }
//     if (_dtmPageUrl.indexOf("checkout/confirmation") > -1 && _dtmPageUrl.indexOf("action=amend") <= -1) {
//         sociomanticTrolleyData = _satellite.getVar('busSociomanticProductString');
//         sociomanticTransaction = _satellite.getVar('busOrderIdNumber');
//         sociomanticGuidePrice = Number(_satellite.getVar('busGuidePrice'));
//         sociomanticSlotStart = Date.parse(_satellite.getVar('busSlotStart')) / 1000;
//         var basket = {
//             products: sociomanticTrolleyData,
//             transaction: sociomanticTransaction,
//             amount: sociomanticGuidePrice,
//             currency: sociomanticCurrency,
//             date: sociomanticSlotStart.toString()
//         };
//         //  asia ? sonar_basket = basket : null;
//     };
//     //************* Inclusion Tag *************
//     (function () {
//         var s = document.createElement('script');
//         var x = document.getElementsByTagName('script')[0];
//         s.type = 'text/javascript';
//         s.async = true;
//         s.src = 'https://' + sociomanticHost + '/js/2010-07-01/adpan/' + sociomanticId;
//         x.parentNode.insertBefore(s, x);
//     })();
// }