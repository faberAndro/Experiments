var country = _satellite.getVar("Country"); // "UK"
!function (f, b, e, v, n, t, s) {
    if (f.fbq) return; n = f.fbq = function () {
        n.callMethod ?
            n.callMethod.apply(n, arguments) : n.queue.push(arguments);
    };
    if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0';
    n.queue = []; t = b.createElement(e); t.async = !0;
    t.src = v; s = b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t, s)
}(window, document, 'script',
    'https://connect.facebook.net/en_US/fbevents.js');
var pixelIDList = {
    "HU": ["2011219315796774"],
    "SK": ["606848083022513"],
    "CZ": ["178726922754452"],
    "TH": ["472685362901377"],
    "UK": ["1648591638712092", "2376396922605677"],
    "MY": ["2246039922297003"],
    "PL": ["1811122922529799"]
};

for (var x = 0; x < pixelIDList[country].length; x++) {
    var pixelID = pixelIDList[country][x] || ""
    // var pixelID = pixelIDList.hasOwnProperty(country) ? pixelIDList[country] : "";
    fbq('set', 'autoConfig', false, pixelID); //This stops automatic events
    fbq('init', pixelID);
}

fbq('track', 'PageView');
var pagePath = window.location.pathname;
var searchPageTrue = /\/search/.test(pagePath);
var orderSummaryPageTrue = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/checkout\/order-summary$/.test(pagePath);
var productPageTrue = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/products\/.*/.test(pagePath);
var orderConfirmation = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/checkout\/confirmation$/.test(pagePath);
var isAmend = _satellite.getVar('busIsAmend');
var productIds = [];
if (country !== "UK") {
    productIds = _satellite.getVar('busProductIdsList');
}
//Content view tracking
if (productPageTrue) {
    fbq('track', 'ViewContent', {
        content_ids: [location.pathname.split('/')[4]], //array of one or more product ids in the page
        content_type: 'product', //either 'product' or 'product_group'
        content_category: _satellite.getVar('busDepartment'),
        content_name: _satellite.getVar('busPageTitle'),
        currency: _satellite.getVar("Currency Code")
        // busdept often blank
    });
}
if (searchPageTrue && (_satellite.getVar("Country") === "TH") && (_satellite.getVar('busArrayOfProducts') != "")) {
    var productIDs = _satellite.getVar('busArrayOfProducts').map(function (x) {
        return x["@id"]
    })
    fbq('track', 'Search', {
        search_string: _satellite.getVar('busSearchTerm'),
        content_ids: productIDs,
        content_type: 'product',
    });
    _satellite.setVar('busArrayOfProducts', "");

}

// initiate Checkout
if (orderSummaryPageTrue && (_satellite.getVar("Country") === "TH")) {
    fbq('track', 'InitiateCheckout', {
        value: _satellite.getVar('busGuidePrice'),
        currency: _satellite.getVar("Currency Code")
    });
}

// Purchase Tracking
if (orderConfirmation && !isAmend) {
    fbq('track', 'Purchase', {
        content_ids: productIds,
        content_type: 'product',
        value: _satellite.getVar('busGuidePrice'),
        currency: _satellite.getVar("Currency Code"),
    });
}