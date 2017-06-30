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
  var selected = $('#id_transport_from_fair_type').val();
  if(selected == 'armada_transport') {
    $('#armadaTransportChosen').show();
  } else {
    $('#armadaTransportChosen').hide();
  }
});


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
  } else {
    setConfirmAndSubmit(false);
  }
  if (this.id == "start-li") {
    setBackButton(true);
  } else {
    setBackButton(false);
  }
})

var checkIfOnConformAndSubmit = function () {
  if ($("#confirm-li").hasClass("active")) {
    setConfirmAndSubmit(true);
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

// hides back button if bool = true
var setBackButton = function(bool) {
  if (bool) {
    $("#back-button").addClass('invisible');
  } else {
    $("#back-button").removeClass('invisible');
  }
}