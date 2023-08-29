$("#id_user").change(function(){
  let user_name = $(this).val());
  $('#id_first_name').val(user_name);
});
