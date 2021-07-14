_satellite.pushAsyncScript(function(event, target, $variables){
  var country = _satellite.getVar("Country");
if (/PL|CZ|SK|HU/g.test(country)) {
    var pagePath = window.location.pathname;
    //   var searchPageTrue = /\/search/.test(pagePath);
    var productPageTrue = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/products\/.*/.test(pagePath);
    var plpTrue = window.location.pathname.indexOf("/categories/") > -1 || window.location.pathname.indexOf("/shop/") > -1;
    //     var orderSummary = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/checkout\/order-summary.*/.test(pagePath);
    var orderConfirmation = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/checkout\/confirmation$/.test(pagePath);
    var reviewTrolley = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/checkout\/review-trolley$/.test(pagePath);
    var isAmend = _satellite.getVar('busIsAmend');
    var orderConfirmationIDs = _satellite.getVar('busProductIdsList');
    var customerID = _satellite.getVar('busCustomerUUID');
    var productIdsObject;
    var gtagObj;
    var adwordsIDList = {
        "HU": "AW-859683922",
        "SK": "AW-968997721",
        "PL": "AW-985304386",
        "CZ": "AW-967628968"
    };
    var adwordsID = adwordsIDList.hasOwnProperty(country) ? adwordsIDList[country] : "";
    var adwordsConversionIDList = {
        "HU": "AW-859683922/l9WxCPDXr3kQ0vj2mQM",
        "SK": "AW-968997721/8ZA6CLXbk3kQ0NLb1wM",
        "PL": "AW-985304386/CfYiCNaCp3kQwprq1QM",
        "CZ": "AW-967628968/CJ_gCNXdjnkQwKHe2AM"
    };
    var adwordsConversionID = adwordsConversionIDList.hasOwnProperty(country) ? adwordsConversionIDList[country] : "";
    var src = "https://www.googletagmanager.com/gtag/js?id=" + adwordsID;
    var imported = document.createElement('script');
    imported.src = src
    document.head.appendChild(imported);
    window.dataLayer = window.dataLayer || [];
    function gtag() { dataLayer.push(arguments); }
    gtag('js', new Date());
    gtag('config', adwordsID);
    //Purchase Tracking
    if (orderConfirmation && !isAmend) {
        gtag('event', 'conversion', {
            'send_to': adwordsConversionID,
            'value': _satellite.getVar('busGuidePrice'),
            'currency': _satellite.getVar("Currency Code"),
            'transaction_id': ''
        });


        //adwords for order confirmation 
        if (orderConfirmationIDs) {
            productIDsObject = orderConfirmationIDs.map(function (x) {
                return {
                    'id': x,
                    'google_business_vertical': 'retail'
                };
            });
            gtagObj = {
                'send_to': adwordsID,
                'user_id': customerID,
                'items': productIDsObject
            };
            gtag('event', 'purchase', gtagObj);

        }
    }

    //adwords for PDPs 
    if (productPageTrue) {
        // console.log('---log - gtag pdp code hit ')
        productIDsObject = {
            'id': location.pathname.split('/')[4],
            'google_business_vertical': 'retail'
        };
        gtagObj = {
            'send_to': adwordsID,
            'user_id': customerID,
            'items': [productIDsObject]
        };
        gtag('event', 'view_item', gtagObj);
        // console.log('log - this is the gtag obj', gtagObj);
    }
    //adwords for PLP
    if (plpTrue) {
        // console.log('---log - gtag trolley code hit ')
        var trolleyProducts = _satellite.getVar('busArrayOfProducts');
        productIDsObject = trolleyProducts.map(function (x) {
            return {
                'id': x["@id"],
                'google_business_vertical': 'retail'
            };
        });
        gtagObj = {
            'send_to': adwordsID,
            'user_id': customerID,
            'items': productIDsObject
        };
        gtag('event', 'view_item_list', gtagObj);
        // console.log('log - this is the gtag obj', gtagObj);
    }
    //adwords for review trolley 
    if (reviewTrolley) {
        // console.log('---log - gtag trolley code hit ')
        var trolleyProducts = _satellite.getVar('busArrayOfProducts');
        productIDsObject = trolleyProducts.map(function (x) {
            return {
                'id': x["@id"],
                'google_business_vertical': 'retail'
            };
        });
        gtagObj = {
            'send_to': adwordsID,
            'user_id': customerID,
            'items': productIDsObject
        };
        gtag('event', 'trolley', gtagObj);
        // console.log('log - this is the gtag obj', gtagObj);
    }

}
});
