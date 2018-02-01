// If a bootstrap popover is speciefied
$('.has-popover').popover({'trigger':'hover'});

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
  //  checkIfOnConformAndSubmit();
  // Check if on start
  //checkIfOnStart();
});

$('.btnBack').click(function(){
  $('.nav-tabs > .active').prev('li').find('a').trigger('click');
  checkIfOnConformAndSubmit();
  checkIfOnStart();
});

// Select all links with hashes, This listener is used for when navigation tabs are clicked
$('a[href*="#"]')
  // Remove links that don't actually link to anything
  .not('[href="#"]')
  .not('[href="#0"]')
  .click(function(event) {
    // On-page links
    if (
      location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') 
      && 
      location.hostname == this.hostname
    ) {
      console.error(this)
      console.error(this.href.split('#')[1])
      if (this.href.split('#')[1] == "confirm-and-submit") {
        setConfirmAndSubmit(true);
      } else {
        setConfirmAndSubmit(false);
        setSaveButton(true);
      }
      if (this.href.split('#')[1] == "start") {
        setBackButton(true);
      } else {
        setBackButton(false);
      }
      // Figure out element to scroll to
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      // Does a scroll target exist?
      if (target.length) {
        // Only prevent default if animation is actually gonna happen
        event.preventDefault();
        $('html, body').animate({
          scrollTop: target.offset().top -90
        }, 10, function() {
          // Callback after animation
          // Must change focus!
          var $target = $(target);
          $target.focus();
          if ($target.is(":focus")) { // Checking if the target was focused
            return false;
          } else {
            $target.attr('tabindex','-1'); // Adding tabindex for elements not focusable
            $target.focus(); // Set focus again
          };
        });
      }
    }
  });


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

