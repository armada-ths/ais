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


// Back and Next button logic
$('.btnNext').click(function(){
  $('.nav-tabs > .active').next('li').find('a').trigger('click');
});

$('.btnBack').click(function(){
  $('.nav-tabs > .active').prev('li').find('a').trigger('click');
});
