_satellite.pushAsyncScript(function(event, target, $variables){
  var staging = _satellite.getVar('Marketing Environment')=="dev"; 
var fts = _satellite.getVar('busCustomerFTS') === "true"; 
var pagePath = window.location.pathname;
var orderConfirmation = /^\/groceries\/([a-zA-Z]{2})\-([a-zA-Z]{2})\/checkout\/confirmation$/.test(pagePath);
var isAmend = _satellite.getVar("busIsAmend")
var orderId = _satellite.getVar('busSiteStoreId')+":"+_satellite.getVar('busOrderIdNumber')+":"+_satellite.getVar('Country')
var bprice = _satellite.getVar('busGuidePrice');
var src; 
if(staging && fts){
src =  'https://r.turn.com/r/beacon?b2=Y9env4NSuGdrt9_ImNHSyKQ8J5CxFqNj6I-XW0bdHNE6GiIjpiexRfFmIy_e14teWeJ8BNspZa0FTfbW19YQmg&cid=' + orderId; 
}
if(!staging && fts){
    src = 'https://r.turn.com/r/beacon?b2=HjQkLox6FeIPOa67OUMxHO4eEKj4Eo7THjfaSQkcIlo6GiIjpiexRfFmIy_e14teeoH7-NJz4_PJ_uaOallcBQ&cid=' + orderId; 
}
if(staging && !fts){
    src = 'https://r.turn.com/r/beacon?b2=Mnrea2T3-WL2D6b0glebXaJU-tjraNFCakhVohXn7d46GiIjpiexRfFmIy_e14teE4HJ3o6gxmL3qUtBs-KRcg&cid=' + orderId + '&bprice=' + bprice; 
}
if(!staging && !fts){
    src = 'https://r.turn.com/r/beacon?b2=whSEwCTVft46SGQPtN8Y-04ZL9Il-SQrfWB89vSYDm06GiIjpiexRfFmIy_e14tedapjaPA0qi9vepPquulEkg&cid=' + orderId + '&bprice=' + bprice; 
}
src = encodeURI(src);
if(_satellite.getVar("Country")=="UK"){
      if(orderConfirmation && !isAmend){ 
       //console.log('Amobee conv - this is order conf, not amend')
         document.createElement("img").src=src;
         //console.log('this is the amobee pixel src from fts...', src);
      }
    }

});
