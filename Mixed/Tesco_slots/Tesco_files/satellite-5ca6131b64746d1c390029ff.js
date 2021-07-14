_satellite.pushAsyncScript(function(event, target, $variables){
  if (_satellite.getVar("Country") == "UK") {
    var pageName = document.title;
    var authenticationStatus = _satellite.getVar("busCustomerLoggedIn")
      ? "logged in"
      : "anonymous";
    var basketValue = _satellite.getVar("busGuidePrice");
    var superDepartment = _satellite.getVar("busSuperDepartment");
    var department = _satellite.getVar("busDepartment");
    var aisle = _satellite.getVar("busAisle");
    var productGtin = _satellite.getVar("productIDGtin");
    var searchTerm = _satellite.getVar("busSearchTerm");
    var postCode = /\b((?:(?:gir)|(?:[a-pr-uwyz])(?:(?:[0-9](?:[a-hjkpstuw]|[0-9])?)|(?:[a-hk-y][0-9](?:[0-9]|[abehmnprv-y])?)))) ?([0-9][abd-hjlnp-uw-z]{2})\b/gi;
    var gps = /\..*\./g;
    var deliveryMethod = _satellite.getVar("busIntDelivMethod");
    var deliverySlot = _satellite.getVar("busIntSlotDateTime");
    var pagePath = window.location.pathname;
    var orderConfirmation = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/checkout\/confirmation$/.test(
      pagePath
    );
    var reviewTrolley = /\/review-trolley/.test(
      _satellite.getVar("Path Name No Lang")
    );
    var trolley = /\/trolley/.test(_satellite.getVar("Path Name No Lang"));
  
    var isAmend = _satellite.getVar("busIsAmend");
  
    var src =
      _satellite.getVar("Amobee Pixel") +
      "kv/pageName=" +
      pageName +
      ",authenticationStatus=" +
      authenticationStatus;
    if (/^\/shop.*|\/categories.*/.test(_satellite.getVar("Path Name No Lang"))) {
      //PLP
      department ? (src += ",department=" + department) : null;
      aisle ? (src += ",aisle=" + department) : null;
      superDepartment ? (src += ",superDepartment=" + superDepartment) : null;
    }
    if (/^\/products\/.*/.test(_satellite.getVar("Path Name No Lang"))) {
      //PDP
      productGtin ? (src += ",productGtin=" + productGtin) : null;
      department ? (src += ",department=" + department) : null;
      aisle ? (src += ",aisle=" + department) : null;
      superDepartment ? (src += ",superDepartment=" + superDepartment) : null;
    }
    if (/\/search/.test(_satellite.getVar("Path Name No Lang"))) {
      //search
      postCode.test(searchTerm) ? (searchTerm = "postcode") : null;
      gps.test(searchTerm) ? (searchTerm = "postcode") : null;
      searchTerm ? (src += ",searchTerm=" + searchTerm) : null;
    }
    if (
      (trolley && !isAmend) ||
      (orderConfirmation && !isAmend) ||
      (reviewTrolley && !isAmend)
    ) {
      basketValue ? (src += ",basketValue=" + basketValue) : null;
    }
    src += "/url/http://cm.g.doubleclick.net/pixel?google_nid=turn_dmp&google_cm";  
    src = encodeURI(src);
    document.createElement("img").src = src;
    //console.log("this is the amobee pixel src from data...", src);
  }
});
