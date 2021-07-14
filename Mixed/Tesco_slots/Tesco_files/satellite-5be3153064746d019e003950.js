_satellite.pushAsyncScript(function(event, target, $variables){
  if (/UK/g.test(_satellite.getVar("Country"))) {
    if ((/^\/groceries\/.*/).test(location.pathname)) {

        //console.log("px staging tag fires");

        var px_isAmend = _satellite.getVar('busIsAmend');
        var px_amendMode = _satellite.getVar('busCustomerAmendMode')

        var px_customDimensionAmendOrder;
        if (px_isAmend || px_amendMode == "amend") {
            px_customDimensionAmendOrder = "true";
        } else {
            px_customDimensionAmendOrder = "false";
        }
        // global vars - to be added into dc
        var px_isAppUser = (_satellite.getVar('App_Visitor_ID') || _satellite.getVar('App Consumer') == "ghsnativeapp-uk") ? "Y" : "N";
        var px_amendDifference = _satellite.getVar('px_guidePriceChange') ? _satellite.getVar('px_guidePriceChange') : undefined

        var px_query = document.location.search.length ? "&" + document.location.search.substring(1) : '';
        px_query = px_query.length ? '?' + px_query.replace(/&[^&@]+@[^&]+/g, '').substring(1) : '';
        px_query = px_query.length <= 1 ? '' : px_query;

        var px_userId = _satellite.getVar('Customer ID');
        var px_fTS = "placeholder";
        var loyaltyType = _satellite.getVar('busCustomerLoyaltyType');
        px_fTS = (loyaltyType != null) ? (loyaltyType == "first-time" ? "Y" : "N") : undefined;

        var px_gaClientId = _satellite.getVar('PX - GA Client ID');
        var px_playwell = 1;
        //custom dimension best practice
        var px_custom_dimension_obj = {};
        px_custom_dimension_obj.dimension4 = "GHS";
        px_custom_dimension_obj.dimension26 = px_customDimensionAmendOrder;
        px_custom_dimension_obj.dimension27 = px_isAppUser;
        px_custom_dimension_obj.metric3 = px_amendDifference;
        if (typeof px_userId != undefined && px_userId != "") {
            px_custom_dimension_obj.dimension1 = px_userId;
        }
        if (typeof px_fTS != undefined && px_fTS != "") {
            px_custom_dimension_obj.dimension2 = px_fTS;
        }
        if (typeof px_gaClientId != undefined && px_gaClientId != "") {
            px_custom_dimension_obj.dimension7 = px_gaClientId;
        }
        if (typeof px_playwell != undefined && px_playwell != "") {
            px_custom_dimension_obj.dimension8 = px_playwell;
        }
        var pagePath = window.location.pathname;
        // page regex:
        var productPageTrue = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/products\/.*/.test(pagePath);
        //var checkoutSlotPage = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/slots$/.test(pagePath);
        var checkoutReview = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/((checkout\/review\-trolley)|(trolley))(.*)/.test(pagePath);
        var checkoutSummary = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/checkout\/order\-summary(.*)/.test(pagePath);
        var checkoutPaymentOptions = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/checkout\/payment\-options$/.test(pagePath);
        var checkoutRegArray = [];
        //checkoutRegArray.push(checkoutSlotPage, checkoutReview, checkoutSummary, checkoutPaymentOptions);
        checkoutRegArray.push(checkoutReview, checkoutSummary, checkoutPaymentOptions);
        //order confirmation
        var orderConfirmation = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/checkout\/confirmation$/.test(pagePath);
        (function (i, s, o, g, r, a, m) {
            i['GoogleAnalyticsObject'] = r; i[r] = i[r] || function () {
                (i[r].q = i[r].q || []).push(arguments)
            }, i[r].l = 1 * new Date(); a = s.createElement(o),
                m = s.getElementsByTagName(o)[0]; a.async = 1; a.src = g; m.parentNode.insertBefore(a, m)
        })(window, document, 'script', 'https://www.google-analytics.com/analytics.js', 'ga');
        //set the tracker name here:
        ga('create', 'UA-17489144-30', 'auto', 'ukLego');
        // advertisement features
        ga('ukLego.require', 'displayfeatures');
        ga('ukLego.require', 'adfeatures');
        //cross domain tracking
        ga('ukLego.require', 'linker');
        ga('ukLego.linker:autoLink', ['tesco.com', 'tescoliving.com', 'clothingattesco.com'], false, true);
        //to enable unique user ID view - google recommended method
        ga('ukLego.set', 'userId', px_userId);

        // ENHANCED ECOMMERCE
        //load the plugin first
        ga('ukLego.require', 'ec');
        //ADD PRODUCT VISITS CODE HERE
        if (productPageTrue == true) {
            //console.log("%c this is a PDP!", "background: #000; color: #fff");
            var productDName = _satellite.getVar("busPageTitle");
            var productDCat1 = _satellite.getVar("busSuperDepartment");
            var productDCat2 = _satellite.getVar("busDepartment");
            var productDCat3 = _satellite.getVar("busAisle");
            var productDCategory = productDCat1 + "/" + productDCat2 + "/" + productDCat3;
            if (_satellite.getVar('gaPdpProdId')) {
                var productDId = _satellite.getVar('gaPdpProdId');
                _satellite.setVar('gaPdpProdId',false)
            }
            ga('ukLego.ec:addProduct', {
                'id': productDId,
                'name': productDName,
                'category': productDCategory,
            });
            ga('ukLego.ec:setAction', 'detail');
        }
        // ------- END OF PRODUCT VIEW -------
        //ADD CHECKOUT STEPS HERE
        function addCheckoutStepsObjects(step) {
            if (_satellite.getVar("busBasketItems")) {
                var checkoutBasketItems = _satellite.getVar("busBasketItems");
                for (var l = 0; l < checkoutBasketItems.length; l++) {
                    var id = _satellite.getVar("busBasketItems")[l].tpnb;
                    var name = _satellite.getVar("busBasketItems")[l].productName;
                    var price = _satellite.getVar("busBasketItems")[l].priceBreakdown.unitPrice.price;
                    var qty = _satellite.getVar("busBasketItems")[l].qty;
                    ga('ukLego.ec:addProduct', {
                        'id': id,
                        'name': name,
                        'price': price,
                        'quantity': qty
                    });
                }
            }
            ga('ukLego.ec:setAction', 'checkout', {
                'step': step,
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
                //console.log("%c this is a order confirmation page", "background:#000; color:#fff");
                var trolleyDataArray = _satellite.getVar("busTrolleyData");
                var orderId = _satellite.getVar('busOrderIdNumber');
                var guidePrice = _satellite.getVar('busGuidePrice');
                var shippingPrice = _satellite.getVar('busDelivCharge');
                var deliverySlot = _satellite.getVar('busSlotStart');
                var deliveryMethod = _satellite.getVar('busDelivMethod');
                px_custom_dimension_obj.dimension13 = deliverySlot;
                px_custom_dimension_obj.dimension14 = deliveryMethod;
                if (trolleyDataArray) {
                    for (var t = 0; t < trolleyDataArray.length; t++) {
                        var productID = _satellite.getVar("busTrolleyData")[t].tpnb;
                        var productName = _satellite.getVar("busTrolleyData")[t].productName;
                        var productPrice = _satellite.getVar("busTrolleyData")[t].priceBreakdown.unitPrice.price;
                        var productQty = _satellite.getVar("busTrolleyData")[t].qty;
                        var productCoupon = _satellite.getVar("busTrolleyData")[t]["tesco:promotion"].promotionName;

                        ga('ukLego.ec:addProduct', {
                            'id': productID,
                            'name': productName,
                            'category': 'Groceries',
                            'brand': 'Tesco',
                            'price': productPrice,
                            'coupon': productCoupon,
                            'quantity': productQty
                        });
                    }
                }
                ga('ukLego.ec:setAction', 'purchase', {
                    'id': orderId,
                    'affiliation': 'GHS',
                    'revenue': guidePrice,
                    'shipping': shippingPrice,
                });
            }
            else {
                var orderID = _satellite.getVar("busOrderIdNumber") + ":" + _satellite.getVar("busSiteCountry");
                ga('ukLego.send', 'event', 'amend orders', orderID + ' | ' + _satellite.getVar("busPageTimestamp"), _satellite.getVar("busGuidePrice"));
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
        //custom dimensions and pageview sent with correct current pathname
        var ga_page = document.location.pathname + px_query;
        ga('ukLego.set', 'page', ga_page);

        if (Object.size(px_custom_dimension_obj)) {
            ga('ukLego.send', 'pageview', px_custom_dimension_obj);
        } else {
            ga('ukLego.send', 'pageview');
            //console.log("%c pageview without custom dimensions", "background:#000; color:#fff");
        }

    }

}




});
