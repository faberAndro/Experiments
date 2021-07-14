_satellite.pushAsyncScript(function(event, target, $variables){
  var pagePath = window.location.pathname;
if ((/SK|PL|HU|CZ|TH|MY/g.test(_satellite.getVar("Country"))) && (/^\/groceries\/.*/.test(location.pathname))) {
    var productPageTrue = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/products\/.*/.test(
        pagePath
    );
    var checkoutReview = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/((checkout\/review\-trolley)|(trolley))(.*)/.test(
        pagePath
    );
    var checkoutSummary = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/checkout\/order\-summary(.*)/.test(
        pagePath
    );
    var checkoutPaymentOptions = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/checkout\/payment\-options$/.test(
        pagePath
    );
    var orderConfirmation = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/checkout\/confirmation$/.test(
        pagePath
    );
    var checkoutRegArray = [];
    var px_amendMode = _satellite.getVar("busCustomerAmendMode");
    var px_isAmend = _satellite.getVar("busIsAmend");
    checkoutRegArray.push(
        checkoutReview,
        checkoutSummary,
        checkoutPaymentOptions
    );
    (function (i, s, o, g, r, a, m) {
        i["GoogleAnalyticsObject"] = r;
        (i[r] =
            i[r] ||
            function () {
                (i[r].q = i[r].q || []).push(arguments);
            }),
            (i[r].l = 1 * new Date());
        (a = s.createElement(o)), (m = s.getElementsByTagName(o)[0]);
        a.async = 1;
        a.src = g;
        m.parentNode.insertBefore(a, m);
    })(
        window,
        document,
        "script",
        "https://www.google-analytics.com/analytics.js",
        "ga"
    );
  
    var gaID = _satellite.getVar("PX - iGHS Propert ID");
    ga("create", gaID, "auto", "iLego");
    ga("iLego.require", "displayfeatures");
    // Enable RLSA Beta:
    ga("iLego.require", "adfeatures");
    // Cross Domain
    ga("iLego.allowLinker", "true");
    ga("iLego.require", "linker");
    ga(
        "iLego.linker:autoLink",
        [
            "tesco.pl",
            "tesco.hu",
            "itesco.cz",
            "tesco.com",
            "tesco.com.my",
            "kipa.com.tr",
            "tesco.sk",
            "itesco.sk",
            "tescolotus.com",
            "klikni-a-vyzvedni.cz",
            "clubcard.cz",
            "tescorecepty.cz"
        ],
        false,
        true
    );
    // USER ID
    //CUSTOM DIMENSION
    var px_ghs_custom_dimensions = {};
    var px_tool_fts = _satellite.getVar("busCustomerFTS");
    var px_tool_uuid = _satellite.getVar("Customer ID : Hashed UUID");
    if (px_tool_fts != undefined) {
        if (px_tool_fts == true) {
            px_ghs_custom_dimensions.dimension2 = "true";
        } else if (px_tool_fts == false) {
            px_ghs_custom_dimensions.dimension2 = "false";
        }
    }
    if (px_tool_uuid != undefined && px_tool_uuid != "") {
        px_ghs_custom_dimensions.dimension3 = px_tool_uuid;
        ga("iLego.set", "userId", px_tool_uuid);
    }
    // ENHANCED ECOMMERCE
    //load the plugin first
    ga("iLego.require", "ec");
    //ADD PRODUCT VISITS CODE HERE
    if (productPageTrue == true) {
        var productDName = _satellite.getVar("busPageTitle");
        var productDCat1 = _satellite.getVar("busSuperDepartment");
        var productDCat2 = _satellite.getVar("busDepartment");
        var productDCat3 = _satellite.getVar("busAisle");
        var productDCategory = productDCat1 + "/" + productDCat2 + "/" + productDCat3;
        if (_satellite.getVar('gaPdpProdId')) {
          var productDId = _satellite.getVar('gaPdpProdId');
          _satellite.setVar('gaPdpProdId',false)
        }
        ga("iLego.ec:addProduct", {
            id: productDId,
            name: productDName,
            category: productDCategory
        });
        ga("iLego.ec:setAction", "detail");
    }
    // ------- END OF PRODUCT VIEW -------
    //ADD CHECKOUT STEPS HERE
    function addCheckoutStepsObjects(step) {
        var basketItems = _satellite.getVar("busBasketItems");
        if (_satellite.getVar("busBasketItems")) {
            var checkoutBasketItems = _satellite.getVar("busBasketItems");
            for (var l = 0; l < checkoutBasketItems.length; l++) {
                var id = basketItems[l].tpnb;
                var name = basketItems[l].productName;
                var price = basketItems[l].priceBreakdown.unitPrice.price;
                var qty = basketItems[l].qty;
                ga("iLego.ec:addProduct", {
                    id: id,
                    name: name,
                    price: price,
                    quantity: qty
                });
            }
        }
        ga("iLego.ec:setAction", "checkout", {
            step: step
        });
    }
    for (var i = 0; i < checkoutRegArray.length; i++) {
        if (checkoutRegArray[i] == true && px_amendMode != "amend") {
            //console.log("%c this is a checkout page", "background:#000; color:#fff");
            addCheckoutStepsObjects(i + 1);
        }
    }
    // ------- END OF CHECKOUT STEPS -------
    // ADD TRANSACTION CONFIRMATION DATA HERE
    if (orderConfirmation == true) {
        if (px_isAmend != true) {
            // console.log("%c this is a order confirmation page", "background:#000; color:#fff");
            var trolleyDataArray = _satellite.getVar("busTrolleyData");
            var orderId = _satellite.getVar("busOrderIdNumber");
            var guidePrice = _satellite.getVar("busGuidePrice");
            var shippingPrice = _satellite.getVar("busDelivCharge");
            var deliverySlot = _satellite.getVar("busSlotStart");
            var deliveryMethod = _satellite.getVar("busDelivMethod");
            if (trolleyDataArray) {
                for (var t = 0; t < trolleyDataArray.length; t++) {
                    var productID = trolleyDataArray[t].tpnb;
                    var productName = trolleyDataArray[t].productName;
                    var productPrice = trolleyDataArray[t].priceBreakdown.unitPrice.price;
                    var productQty = trolleyDataArray[t].qty;
                    var productCoupon = trolleyDataArray[t]["tesco:promotion"].promotionName;
                    ga("iLego.ec:addProduct", {
                        id: productID,
                        name: productName,
                        category: "Groceries",
                        brand: "Tesco",
                        price: productPrice,
                        coupon: productCoupon,
                        quantity: productQty
                    });
                }
            }
            ga("iLego.ec:setAction", "purchase", {
                id: orderId,
                affiliation: "GHS",
                revenue: guidePrice,
                shipping: shippingPrice
            });
            if (/SK|PL|HU|CZ/g.test(_satellite.getVar("Country"))) {
                if (px_tool_fts == "true") {
                    // console.log("%c this is a order FTS confirmation page", "background:#000; color:#fff");
                    ga("iLego.send", {
                        hitType: "event",
                        eventCategory: "OrderConfirmation",
                        eventAction: "NewBuyer",
                        eventLabel: "New",
                        eventValue: Math.round(guidePrice)
                    });
                }
            }
        } else {
            var orderID =
                _satellite.getVar("busOrderIdNumber") +
                ":" +
                _satellite.getVar("busSiteCountry");
            ga(
                "iLego.send",
                "event",
                "amend orders",
                orderID + " | " + _satellite.getVar("busPageTimestamp"),
                _satellite.getVar("busGuidePrice")
            );
        }
    }
    // ------- END OF TRANSACTION CONFIRMATION ----------
    // SAFE FUNCTION TO CHECK OBJECT SIZE:
    Object.size = function (obj) {
        var size = 0;
        for (var key in obj) {
            if (obj.hasOwnProperty(key)) size++;
        }
        return size;
    };
    // ADD CUSTOM DIMENSIONS TO PAGEVIEW HIT IF PRESENT:
    if (Object.size(px_ghs_custom_dimensions)) {
        ga("iLego.send", "pageview", px_ghs_custom_dimensions);
    } else {
        ga("iLego.send", "pageview");
    }
    //AMEND ORDER EVENT
    if (px_isAmend == true) {
        var orderID =
            _satellite.getVar("busOrderIdNumber") +
            ":" +
            _satellite.getVar("busSiteCountry");
        ga(
            "iLego.send",
            "event",
            "amend orders",
            orderID + " | " + _satellite.getVar("busPageTimestamp"),
            _satellite.getVar("busGuidePrice")
        );
    }
}
});
