// If a bootstrap popover is speciefied
$('.has-popover').popover({'trigger':'hover'});

// Hide extra fields from start
$('#externalTransportChosen').hide();
$('#armadaTransportChosen').hide();

// If a certain field is selected show more fields
$('#transportFromFairType').children().change(function() {
  var selected = $(this).val();
  if(selected == 'armada_transport') {
    $('#armadaTransportChosen').show();
  } else {
    $('#armadaTransportChosen').hide();
  }
});
$('#transportToFairType').children().change(function() {
  var selected = $(this).val();
  if(selected == 'external_transport') {
    $('#externalTransportChosen').show();
  } else {
    $('#externalTransportChosen').hide();
  }
});
// if armada transport is chosen on load
$(document).ready(function(){
  $("#submit-button").hide();
  setBackButton(true);
  showImage();
  var selected = $('#id_transport_from_fair_type').val();
  if(selected == 'armada_transport') {
    $('#armadaTransportChosen').show();
  } else {
    $('#armadaTransportChosen').hide();
  }
});

// Exhibitor profile
var showImage = function() {
  var a = $("#fileUpload > a");
  if ( a != undefined ) {
    a.hide();
    var img = document.createElement( "img" );
    img.src = a[0].href;
    $('#logo-clear_id').before(img);
  }
    
}

// Edit button in Confirm and Save tab
$('#editOrganisationTrigger').click(function() {
  $('#organistaionEditable').toggleClass('hidden visible');
  $('#organisationNoEditable').toggleClass('visible hidden');
});
$('#editContactTrigger').click(function() {
  $('#contactEditable').toggleClass('hidden visible');
  $('#contactNoEditable').toggleClass('visible hidden');
});

$('#editInvoiceToggle').click(function() {
  $('#invoiceEditable').toggleClass('hidden visible');
  $('#invoiceNoEditable').toggleClass('visible hidden');
});
$('#editArmadaTransportTrigger').click(function() {
  $('#armadaTransportEditable').toggleClass('hidden visible');
  $('#armadaTransportNoEditable').toggleClass('visible hidden');
});

$('.no-editable-form').find('input').prop( "disabled", true );
$('.no-editable-form').find('select').prop( "disabled", true );
$('.no-editable-form').find('input').attr('disabled', 'disabled');
$('.no-editable-form').find('select').attr('disabled', 'disabled');
$('.editable-form').find('input').prop( "disabled", false );
$('.editable-form').find('select').prop( "disabled", false );

// Back and Next button logic
$('.btnNext').click(function(){
  $('.nav-tabs > .active').next('li').find('a').trigger('click');
  // Check if on confirm and save
  checkIfOnConformAndSubmit();
  // Check if on start
  checkIfOnStart();
});

$('.btnBack').click(function(){
  $('.nav-tabs > .active').prev('li').find('a').trigger('click');
  checkIfOnConformAndSubmit();
  checkIfOnStart();
});

$("li.nav").click(function(){
  if (this.id == "confirm-li") {
    setConfirmAndSubmit(true);
    calcProducts();
    checkTermsCheckbox();
  } else {
    setConfirmAndSubmit(false);
    setSaveButton(true);
  }
  if (this.id == "start-li") {
    setBackButton(true);
  } else {
    setBackButton(false);
  }
})
$('#id_accept_terms').click(function() {
  if (this.checked) {
    setSubmitButton(true);
    setSaveButton(false);
  } else {
    setSubmitButton(false);
    setSaveButton(true);
  }
});

var checkIfOnConformAndSubmit = function () {
  if ($("#confirm-li").hasClass("active")) {
    setConfirmAndSubmit(true);
    checkTermsCheckbox();
  } else {
    setConfirmAndSubmit(false);
  }; 
}

var setConfirmAndSubmit = function(bool) {
  if (bool) {
    $("#next-button").hide();
    $("#submit-button").show().addClass("btn-armada-green");
  } else {
    $("#next-button").show();
    $("#submit-button").hide();
  }
}

var checkIfOnStart = function () {
  if ($("#start-li").hasClass("active")) {
    setBackButton(true);
  } else {
    setBackButton(false);
  };
}

var checkTermsCheckbox = function() {
  var checkbox = $('#id_accept_terms');
  if (checkbox[0].checked == true) {
    setSubmitButton(true);
    setSaveButton(false);
  } else {
    setSubmitButton(false);
    setSaveButton(true);
  }
}

var setSubmitButton = function(bool) {
  if (bool) {
    $("#submit-button").show().addClass("btn-armada-green");
  } else {
    $("#submit-button").hide();
  }
}
var setSaveButton = function(bool) {
  if (bool) {
    $("#save-button").show().addClass("btn-armada-green");
  } else {
    $("#save-button").hide();
  }
}
// hides back button if bool = true
var setBackButton = function(bool) {
  if (bool) {
    $("#back-button").addClass('invisible');
  } else {
    $("#back-button").removeClass('invisible');
  }
}

// hard coding of all ids to input field where orders are placed
var productIds = [
  '#id_product_selection_rooms_0',
  '#id_product_selection_rooms_1',
  '#id_event_armada_run',
  '#id_event_custom_events',
  '#id_event_individual_meetings',
  '#id_event_innovation_night',
  '#id_event_lunch__breakfast_lecture',
  '#id_event_the_internship_pitch',
  '#id_banquet_banquet_table_excluding_two_tickets_from_the_base_kit',
  '#id_banquet_banquet_table_including_two_tickets_from_the_base_kit',
  '#id_banquet_banquet_ticket__exhibitor_representative',
  '#id_banquet_banquet_ticket__exhibitor',
  '#id_banquet_banquet_ticket__student',
  '#id_banquet_drink_coupon',
  '#id_banquet_drink_coupons',
  '#id_product_selection_nova_0',
  '#id_product_selection_additional_stand_area',
  '#id_product_selection_additional_stand_height',
  '#id_lunch_additional_lunch_tickets_day_1',
  '#id_lunch_lunch_tickets_day_1',
  '#id_lunch_lunch_day_1',
  '#id_lunch_additional_lunch_tickets_day_2',
  '#id_lunch_lunch_tickets_day_2',
  '#id_lunch_lunch_day_2',
];
// hard coded information about each product
var productDict = {
  '#id_lunch_additional_lunch_tickets_day_1': {
    'type': 'number',
    'title': 'Additional lunch tickets day 1',
    'price': 125
  },
  '#id_lunch_lunch_tickets_day_1': {
    'type': 'number',
    'title': 'Additional lunch tickets day 1',
    'price': 125
  },
  '#id_lunch_lunch_day_1': {
    'type': 'number',
    'title': 'Additional lunch tickets day 1',
    'price': 125
  },
  '#id_lunch_additional_lunch_tickets_day_2': {
    'type': 'number',
    'title': 'Additional lunch tickets day 2',
    'price': 125
  },
  '#id_lunch_lunch_tickets_day_2': {
    'type': 'number',
    'title': 'Additional lunch tickets day 2',
    'price': 125
  },
  '#id_lunch_lunch_day_2': {
    'type': 'number',
    'title': 'Additional lunch tickets day 2',
    'price': 125
  },
  '#id_banquet_banquet_table_excluding_two_tickets_from_the_base_kit': {
    'type': 'number',
    'title': 'Banquet table, excluding two tickets from the base kit',
    'price': 12900
  },
  '#id_banquet_banquet_table_including_two_tickets_from_the_base_kit': {
    'type': 'number',
    'title': 'Banquet table, including two tickets from the base kit',
    'price': 9900
  },
  '#id_banquet_banquet_ticket__exhibitor_representative': {
    'type': 'number',
    'title': 'Banquet ticket - Exhibitor representative',
    'price': 1190
  },
  '#id_banquet_banquet_ticket__exhibitor': {
    'type': 'number',
    'title': 'Banquet ticket - Exhibitor representative',
    'price': 1190
  },
  '#id_banquet_banquet_ticket__student': {
    'type': 'number',
    'title': 'Banquet ticket - Student',
    'price': 1190
  },
  '#id_banquet_drink_coupon': {
    'type': 'number',
    'title': 'Drink coupons',
    'price': 85
  },
  '#id_banquet_drink_coupons': {
    'type': 'number',
    'title': 'Drink coupons',
    'price': 85
  },
  '#id_product_selection_nova_0': {
    'type': 'checkbox',
    'title': 'Nova Exclusive offer',
    'price': 10000
  },
  '#id_product_selection_rooms_0': {
    'type': 'checkbox',
    'title': 'Diversity room',
    'price': 10000
  },
  '#id_product_selection_rooms_1': {
    'type': 'checkbox',
    'title': 'Green room',
    'price': 10000
  },
  '#id_event_armada_run': {
    'type': 'number',
    'title': 'Armada run',
    'price': 500
  },
  '#id_event_custom_events': {
    'type': 'number',
    'title': 'Custom events',
    'price': 0
  },
  '#id_event_individual_meetings': {
    'type': 'number',
    'title': 'Individual meetings',
    'price': 10000
  },
  '#id_event_innovation_night': {
    'type': 'number',
    'title': 'Innovation night',
    'price': 15000
  },
  '#id_event_lunch__breakfast_lecture': {
    'type': 'number',
    'title': 'Lunch / breakfast lecture',
    'price': 29000
  },
  '#id_event_the_internship_pitch': {
    'type': 'number',
    'title': 'The internship pitch',
    'price': 2000
  },
  '#id_product_selection_additional_stand_area': { // ----------------- additoinal stand area
    'type': 'select',
    'title': 'Additional stand area',
    'price': 0
  },
  '#id_product_selection_additional_stand_height': {
    'type': 'select',
    'title': '',
    'price': 0
  },
  'stand_area_2x4': {
    'type': 'select',
    'title': 'Additional stand area - 2x4 m',
    'price': 14000
  },
  'stand_area_2x5': {
    'type': 'select',
    'title': 'Additional stand area - 2x5 m',
    'price': 26000
  },
  'stand_area_2x6': {
    'type': 'select',
    'title': 'Additional stand area - 2x6 m',
    'price': 36000
  },
  'stand_area_2x7': {
    'type': 'select',
    'title': 'Additional stand area - 2x7 m',
    'price': 44000
  },
  'stand_height_3': {
    'type': 'select',
    'title': 'Additional stand height - 2,31-3m ',
    'price': 1000
  },
  'stand_height_5': {
    'type': 'select',
    'title': 'Additional stand height - 3,01-5m ',
    'price': 2000
  },
}
// iterates through the list of input ids and check amount of orders for each product
var calcProducts = function() {
  var orderedProducts = [];
  var orderedProductsDict = {};
  var order = {};
  orderedProducts.push('baseKit');
  orderedProductsDict['baseKit'] = {
        'id': 'baseKit',
        'amount': 1,
        'price': 39500,
        'title': 'Base kit',
        'totalPrice': 39500
      }
  for (var i=0; i<productIds.length; i++) {
    var productId = productIds[i];
    var prod = $(productId);
    var amount = 0;
    if (prod != undefined) {
      
      if (productDict[productId].type == 'checkbox') {
        amount = checkProductCheckbox(prod);
      } else if (productDict[productId].type == 'number') {
        amount = checkProductNumber(prod);
      } else if (productDict[productId].type == 'select') {
        order = checkProductSelect(prod, productDict);
        productId = order.id;
        amount = order.amount;
      }

      // if amount > 0, it has been ordered
      try {
        if (productDict[productId].type == 'select' && amount>0) {
          orderedProductsDict[productId] = order;
          orderedProducts.push(productId);
        } else if (amount>0) {
          orderedProducts.push(productId);
          order = {
            'id': productId,
            'amount': amount,
            'price': productDict[productId].price,
            'title': productDict[productId].title,
            'totalPrice': productDict[productId].price*amount
          }
          orderedProductsDict[productId] = order;
        }
        
      } 
      catch(err) {
        console.log(err.message);
      }
    }
  } // end for 
  addOrdersToUI(orderedProducts, orderedProductsDict);
};
// calculates total price for all products
var calcTotalPrice = function(orderedProducts, orderedProductsDict) {
  var totalPrice = 0;
  for (var i=0; i<orderedProducts.length; i++) {
    var productId = orderedProducts[i];
    totalPrice += orderedProductsDict[productId].totalPrice;
  }
  return totalPrice;
}
var checkProductNumber = function(product) {
  return product.val();
}
// grabs value from this type of product
var checkProductCheckbox = function(product) {
  try {

    if (product[0].checked) {
      return 1;
    } else {
      return 0;
    }
  } 
  catch(err) {
      console.log(err.message);
      return 0;
  }
}
var checkProductSelect = function(product, productDict) {
  var val = product.val();
  var productId = '';
  if (val.search("2x3") != -1) {
    return { 'id': 'x', 'amount': 0 };
  } else if (val.search("2x4") != -1) {
    productId = 'stand_area_2x4';
  } else if (val.search("2x5") != -1) {
    productId = 'stand_area_2x5';
  } else if (val.search("2x6") != -1) {
    productId = 'stand_area_2x6';
  } else if (val.search("2x7") != -1) {
    productId = 'stand_area_2x7';
  } else if (val.search("00-2_3") != -1) {
    return { 'id': 'x', 'amount': 0 };
  } else if (val.search("2_31-3") != -1) {
    productId = 'stand_height_3';
  } else if (val.search("3_01-5") != -1 || val.search("3-5") != -1) {
    productId = 'stand_height_5';
  } else {
    return { 'id': 'x', 'amount': 0 };
  }

  var order = {
        'id': productId,
        'amount': 1,
        'price': productDict[productId].price,
        'title': productDict[productId].title,
        'totalPrice': productDict[productId].price
      }
  return order;
}

// add ordered products to ui
var addOrdersToUI = function(orderedProducts, orderedProductsDict) {
  var containerDiv = $('#orderConfirmation');
  containerDiv.empty();
  var ul = document.createElement( "ul" );
  ul.className = 'list-unstyled order-list';

  for (var i=0; i<orderedProducts.length; i++) {
    var productId = orderedProducts[i];
    var productTitle = orderedProductsDict[productId].title;
    var productPrice = orderedProductsDict[productId].price;
    var productAmount = orderedProductsDict[productId].amount;
    var productTotalPrice = orderedProductsDict[productId].totalPrice;

    var li = document.createElement( "li" );
    var span = document.createElement('span');
    var div1 = document.createElement('div');
    var div2 = document.createElement('div');
    div2.className = 'price-tag';

    var spanTitle = document.createElement('span');
    spanTitle.className = 'ordered-product-title';
    var spanPrice = document.createElement('span');
    spanPrice.className = 'ordered-product-price';
    var spanAmount = document.createElement('span');
    spanAmount.className = 'ordered-product-amount';
    var spanTotalPrice = document.createElement('span');
    spanTotalPrice.className = 'ordered-product-total-price';

    spanTitle.append(productTitle);
    spanPrice.append(productPrice);
    spanAmount.append(productAmount);
    spanTotalPrice.append(productTotalPrice);

    div1.append(spanTitle);
    div1.append(" x ");
    div1.append(spanAmount);
    div1.append(' á ');
    div1.append(spanPrice);
    div2.append(spanTotalPrice);
    div2.append(' SEK');

    li.append(div1);
    li.append(div2);
    ul.append(li);
  } // end for loop
  containerDiv.append(ul);
  
  var ordersTotalPrice = calcTotalPrice(orderedProducts, orderedProductsDict);
  var h4 = document.createElement('h4');
  h4.append('Total price: ');
  h4.append(ordersTotalPrice);
  h4.append(' SEK');
  containerDiv.append(h4);
}
