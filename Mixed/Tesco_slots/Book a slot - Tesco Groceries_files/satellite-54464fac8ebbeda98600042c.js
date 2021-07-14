_satellite.pushAsyncScript(function(event, target, $variables){
  var dtm_ighs_dispatcher = window.dispatcher;

function getProducts(trolley) {
  var previousProducts = [];
  for(var i = 0; i < trolley.items.length; i++) {
    var trolleyItem = trolley.items[i];
    previousProducts.push({
      id: trolleyItem.product.id,
      quantity: trolleyItem.quantity,
      unit: trolleyItem.customerUnitChoice
    });
  }
  return previousProducts;
}

function findProduct(products, productId) {
  for(var i = 0; i < products.length; i++) {
    if(products[i].id === productId) {
      return true;
    }
  }
}
                    

if (dtm_ighs_dispatcher) {
  dtm_ighs_dispatcher.register(function (payload) {
    
    /* OLD BASKET ADD/REMOVE METHOD */
    if (payload.action.command == "trolley:update" && payload.action.requestWas){
         if (!payload.action.requestWas.items) {        
           // One
        		var dtm_payload_request_array = [payload.action.requestWas];         	
      		} else {
        	// Many (favourites)
        	var dtm_payload_request_array = payload.action.requestWas.items;       
      	}
      
      for (var i = 0; i < dtm_payload_request_array.length; ++i) {          
        	var dtm_payload_request = dtm_payload_request_array[i];
          var newvalue = dtm_payload_request.newValue;
          var v = dtm_payload_request.oldValue || 0;
          _satellite.setVar("sku_update",dtm_payload_request);  
          if (newvalue > v) {
              _satellite.track("BASKET_ADD");
          }
          else if (newvalue < v) {
              _satellite.track("BASKET_REMOVE");

          }
   				_satellite.setVar("sku_update","");  
      }      
    }
    
    /* NEW RESPONSIVE BASKET ADD/REMOVE METHOD */
    if (payload.action.action == "analytics:trolley-change" && payload.action.value) {

      var diff = payload.action.value.diff;
      var currentProducts = getProducts(payload.action.value.trolley);
      
      if(diff.length === 0) {
        var previousProducts;
        
        try {
          previousProducts = JSON.parse(window.sessionStorage.getItem('trolley_products'));
        } catch(err) {}
        
        if(previousProducts) {
          for(var index = 0; index < previousProducts.length; index++) {
            if(!findProduct(currentProducts, previousProducts[index].id)) {
               var previousProduct = previousProducts[index];
               _satellite.setVar('sku_update', {
                 id: previousProduct.id,
                 oldUnitChoice: previousProduct.unit,
                 oldValue: previousProduct.quantity,
                 newUnitChoice: previousProduct.unit,
                 newValue: 0
                 
               });
               _satellite.track('BASKET_REMOVE');
            }
          }
        }
      }
      
      try {
        window.sessionStorage.setItem('trolley_products', JSON.stringify(currentProducts));
      } catch(err) {}
  
      var dtm_payload_request_array = payload.action.value.diff;

      for (var i = 0; i < dtm_payload_request_array.length; ++i) {
          var dtm_payload_request = dtm_payload_request_array[i];
          var newvalue = dtm_payload_request.newValue;
          var v = dtm_payload_request.oldValue || 0;
          _satellite.setVar("sku_update",dtm_payload_request);  
					//console.log(newvalue);
        	//console.log(v);        
          if (newvalue > v) {
              _satellite.track("BASKET_ADD");
          }
          else if (newvalue < v) {
              _satellite.track("BASKET_REMOVE");
          }
          _satellite.setVar("sku_update","");
      }
    }
    if (payload.action.action == "analytics:taxonomy-change" && payload.action.value) {
      var taxonomyName = payload.action.value.name;
      var taxonomyType = payload.action.value.type;
      if (taxonomyType === "superdepartment"){
      	sessionStorage.setItem('Taxonomy Super Dept', payload.action.value.name);  
      }
      if (taxonomyType === "department"){
      	sessionStorage.setItem('Taxonomy Dept', payload.action.value.name);  
      }                 
      _satellite.track("CLP_PAGE_VIEW");      
    }
    
    if (payload.action.type == "clubcard:synced") {
      _satellite.track("CLUBCARD_ADD");
    }
    
    return true;
  });
}
});
