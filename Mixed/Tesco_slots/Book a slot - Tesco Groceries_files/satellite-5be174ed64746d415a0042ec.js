
// Append Bing UET Script
(function (w, d, t, r, u) {
    if (_satellite.getVar('Country') === "UK") {

        var f, n, i;
        w[u] = w[u] || [], f = function () {
            var o = {
                ti: "4072320"
            };
            o.q = w[u], w[u] = new UET(o), w[u].push("pageLoad");
        },
            n = d.createElement(t), n.src = r, n.async = 1, n.onload = n.onreadystatechange = function () {
                var s = this.readyState;
                s && s !== "loaded" && s !== "complete" || (f(), n.onload = n.onreadystatechange = null);
            },
            i = d.getElementsByTagName(t)[0],
            i.parentNode.insertBefore(n, i);
    }
})(window, document, "script", "//bat.bing.com/bat.js", "uetq");

var productIds, pageType;
var _dtmPageUrl = window.location.href;



//************* Category | Shop Pages *************
if (_dtmPageUrl.indexOf("/categories/") > -1 || _dtmPageUrl.indexOf("/shop/") > -1) {
    productIds = _satellite.getVar('busArrayOfProducts') && _satellite.getVar('busArrayOfProducts').length ? _satellite.getVar('busArrayOfProducts').map(function (item) {
        return item["@id"];
    }) : null;
    pageType = 'category';
}

//************* Product Pages *************
if (_dtmPageUrl.indexOf("/products/") > -1) {
    productIds = _satellite.getVar('productID') ? _satellite.getVar('productID') : null; 
    pageType = 'product';
}


//************* Search Results pages *************
if (_dtmPageUrl.indexOf("/search") > -1) {
    productIds = _satellite.getVar('busArrayOfProducts') && _satellite.getVar('busArrayOfProducts').length ? _satellite.getVar('busArrayOfProducts').map(function (item) {
        return item["@id"];
    }) : null;
    pageType = 'searchresults';
}

//************** Promotion | Buy Lists | Favorites | Zones *****************
if (_dtmPageUrl.match(/promotions\/\w+/) || _dtmPageUrl.indexOf("/buylists/") > -1 || _dtmPageUrl.indexOf("/favorites") > -1) {
    productIds = _satellite.getVar('busArrayOfProducts') && _satellite.getVar('busArrayOfProducts').length ? _satellite.getVar('busArrayOfProducts').map(function (item) {
        return item["@id"];
    }) : null;
    pageType = 'other';
}

//************* Trolley Page *************
if (_dtmPageUrl.indexOf("/trolley") > -1 || _dtmPageUrl.indexOf("/review-trolley") > -1) {
    productIds = _satellite.getVar('busBasketItems') && _satellite.getVar('busBasketItems').length ? _satellite.getVar('busBasketItems').map(function (item) {
        return item.tpnb;
    }) : null;
    pageType = 'cart';
}
//************* Review Trolley *************
// if (_dtmPageUrl.indexOf("/review-trolley") > -1) {
//     productIds =  _satellite.getVar('busBasketItems');
//     pageType = 'cart';
// }

if (_dtmPageUrl.indexOf("/confirmation") > -1) {
    productIds = _satellite.getVar('busBasketItems') && _satellite.getVar('busBasketItems').length ? _satellite.getVar('busBasketItems').map(function (item) {
        return item.tpnb;
    }) : null;
    pageType = 'purchase';
}


window.uetq = window.uetq || [];
// window.uetq.push('event', '', { 'ecomm_prodid': productIds, 'ecomm_pagetype': pageType });
if (productIds && pageType) {
    window.uetq.push({ 'prodid': productIds, 'pagetype': pageType });
}