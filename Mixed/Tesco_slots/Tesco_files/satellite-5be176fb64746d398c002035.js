if (_satellite.getVar("Country") === "UK") {
  var script = document.createElement("script");
  script.onload = function() {
    //variable declaration
    var uuid = _satellite.getVar("busCustomerUUID");
    var deliveryType = _satellite.getVar("busDelivMethod");
    var price = _satellite.getVar("busGuidePrice");
    var quantity = _satellite.setVar("busTotalItemsCount");
    var slotTime = _satellite.getVar("busSlotStart");
    var slotDate = _satellite.getVar("busSlotDateTime");
    var storeId = _satellite.getVar("busSiteStoreId");
    var deliveryCharge = _satellite.getVar("busDelivCharge");
    var orderId = _satellite.getVar("busOrderIdNumber");
    var fts = "fts_placeholder";
    var platformType = _satellite.getVar("bus.customerData.deviceOptimisation");
    var isFirstTimeShopper = _satellite.getVar("busCustomerFTS") == "true";
    var isConfirmationPage =
      location.href.indexOf("/checkout/confirmation") > -1;

    // negative and positive amend difference
    var px_amendPriceChange = _satellite.getVar("px_guidePriceChange");
    if (px_amendPriceChange < 0) {
      var amendDifference_Negative = Math.abs(px_amendPriceChange);
    } else {
      var amendDifference_Positive = px_amendPriceChange;
    }
    //App User
    var px_isAppUser =
      _satellite.getVar("App_Visitor_ID") ||
      _satellite.getVar("App Consumer") == "ghsnativeapp-uk"
        ? "Y"
        : "N";

    var px_isAmend = _satellite.getVar("busIsAmend") ? "Y" : "N";

    var loyaltyType = _satellite.getVar("busCustomerLoyaltyType");
    fts =
      loyaltyType != null
        ? loyaltyType == "first-time"
          ? "Y"
          : "N"
        : undefined;

    //gtag global code initialisation
    window.dataLayer = window.dataLayer || [];
    function gtag() {
      dataLayer.push(arguments);
    }
    gtag("js", new Date());

    gtag("config", "DC-5118014"); //Configuring all pages unique counter

    //tracking all pages unique counter
    gtag("event", "conversion", {
      allow_custom_scripts: true,
      u1: "[ghs]",
      u2: uuid,
      u3: "[AUID]",
      u4: "[Lego ID]",
      u5: "[Top Category]",
      u6: "[Category]",
      u7: "[Sub Category]",
      u10: "[Product]",
      u11: "[Product ID]",
      u12: "[Price]",
      u13: "[Quantity]",
      u21: "[GA ID]",
      u22: px_isAppUser,
      send_to: "DC-5118014/ghspa0/ghsal0+unique"
    });

    function checkoutScript(pixel) {
      //Sales counter for order confirmation page
      var gtagObj = {
        allow_custom_scripts: true,
        u1: "[ghs]",
        u2: uuid,
        u3: "[AUID]",
        u4: "[Top Category]",
        u5: "[Product]",
        u6: "[Product ID]",
        u7: "[Price]",
        u8: quantity,
        u9: deliveryType,
        u10: storeId,
        u11: slotDate,
        u12: slotTime,
        u13: "[Coupon Cost]",
        u14: deliveryCharge,
        u15: px_isAmend,
        u16: fts,
        u17: "[Product Category]",
        u18: "[Product Sub Category]",
        u19: "[Number of Shops]",
        u20: "[Lego ID]",
        u21: "[GA ID]",
        u22: platformType,
        u25: px_isAppUser,
        transaction_id: orderId,
        quantity: 1,
        value: price,
        send_to: pixel
      };

      amendDifference_Positive
        ? (gtagObj["u23"] = amendDifference_Positive)
        : null;
      amendDifference_Negative
        ? (gtagObj["u24"] = amendDifference_Negative)
        : null;

      gtagObjOrdered = {};

      Object.keys(gtagObj)
        .sort()
        .forEach(function(key) {
          gtagObjOrdered[key] = gtagObj[key];
        });

      //console.log('this is the ga obj', gtagObjOrdered);

      gtag("config", "DC-4906386");
      gtag("event", "purchase", gtagObjOrdered);
    }

     var conversionPixelFTS = "DC-4906386/ghsfl0/ghs-p00+transactions"; 
     var conversionPixel = "DC-4906386/ghsfl0/ghs-p0+transactions";

     if (isConfirmationPage) {
       // console.log("confirmation page FTS FALSE");
       checkoutScript(conversionPixel);
     }

     if (isConfirmationPage && isFirstTimeShopper) {
       // console.log("confirmation page FTS TRUE");
       checkoutScript(conversionPixelFTS);
     }

  };

 
  script.src = "https://www.googletagmanager.com/gtag/js?id=DC-5118014";

  document.head.appendChild(script);
}
