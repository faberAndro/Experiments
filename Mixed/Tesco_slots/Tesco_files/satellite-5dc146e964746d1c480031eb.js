_satellite.pushAsyncScript(function(event, target, $variables){
  var path = window.location.pathname;
var country = _satellite.getVar('Country') || null;
var isBrowsePage = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/(shop|categories)\/.*/.test(path);
var isConfirmationPage = path.indexOf("/checkout/confirmation") >= 0;
var aisle = _satellite.getVar("busAisle")? _satellite.getVar("busAisle").replace(/,/g,''): null;
var department = _satellite.getVar("busDepartment") ? _satellite.getVar("busDepartment").replace(/,/g, ''): null;
var superDepartment = _satellite.getVar("busSuperDepartment") ?  _satellite.getVar("busSuperDepartment").replace(/,/g, '') : null;
var tpnbs = _satellite.getVar('busProductIdsList') || null;
var categories = [];
var src = '';
var amobeePixel = null;
var hash = parseInt(9999999999 * Math.random());

// browse page
if (country === 'UK') {
    amobeePixel= document.createElement("img");
    if (isBrowsePage) {
        superDepartment ? categories.push(superDepartment) : null;
        department ? categories.push(department) : null;
        aisle ? categories.push(aisle) : null;
        if (superDepartment || department || aisle) {
            amobeePixel.src = 'https://d.turn.com/r/dd/id/L21rdC8xNDA3L2NpZC8xNzQ4Nzc4MzY3L3QvMg/cat/' + encodeURIComponent(categories.join(',')) + '/qry/browse?' + hash;
        }
    }

    if (isConfirmationPage) {
        amobeePixel.src = "https://d.turn.com/r/dd/id/L21rdC8xNDA3L2NpZC8xNzQ4Nzc4MzY1L3QvMg/kv/TPNB_CH=" + encodeURIComponent(tpnbs.join(',TPNB_CH=')) + '/rnd/' + '?' + hash;
    }

}
});
