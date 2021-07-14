_satellite.pushAsyncScript(function(event, target, $variables){
  try {
    if (_satellite.getVar("Country") == "CZ") {
        var rtgId = 11716;
        if (rtgId) {
            var src =
                "//c.imedia.cz/retargeting?" +
                "id=" +
                rtgId +
                "&url=" +
                encodeURIComponent(location.href);
        }
        var rtgId2 = 40472;
        var src2;
        if (rtgId2) {
            src2 = [
                "//c.imedia.cz/retargeting?",
                "id=" + rtgId2,
                "",
                "&url=" + encodeURIComponent(location.href)
            ];
        }
        document.createElement("img").src = src;

        var isAmend = _satellite.getVar("busIsAmend");

        var pagePath = window.location.pathname;

        var productPageTrue = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/products\/.*/.test(
            pagePath
        );

        // define PDP specific params

        if (productPageTrue) {
            var itemId = pagePath.split("/")[4];
            src2[2] = "&itemId=" + encodeURIComponent(itemId) + "&pageType=offerdetail";
        }

        var productListingPageTrue = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/shop\/.*/.test(
            pagePath
        );

        // define PLP specific params
        if (productListingPageTrue) {
            var category =
                _satellite.getVar("busAisle") ||
                _satellite.getVar("busDepartment") ||
                _satellite.getVar("busSuperDepartment");

            src2[2] =
                "&category=" + encodeURIComponent(category) + "&pageType=category";
        }

        document.createElement("img").src = src2.join("");

        var orderConfirmation = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/checkout\/confirmation$/.test(
            pagePath
        );
        if (orderConfirmation && !isAmend) {
            var iframe = document.createElement("iframe");
            iframe.style.display = "none";
            iframe.src =
                "//c.imedia.cz/checkConversion?c=100024299&amp;color=ffffff&amp;v=";
            document.body.appendChild(iframe);
            var iframe2 = document.createElement("iframe");
            iframe2.style.display = "none";
            iframe2.src =
                "//c.imedia.cz/checkConversion?c=99997549&amp;color=ffffff&amp;v=";
            document.body.appendChild(iframe2);
        }
    }
} catch (e) {
    console.log("DTM error ", e);
}
});
