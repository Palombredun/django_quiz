$("#tf-form").hide();
$("#mc-form").hide();

function cloneTF(selector) {
  // change the current total number of tf questions
  total_tf = $('#id_tf-TOTAL_FORMS').val();

  // clone the selected part of the form
  var newElement = $(selector).clone(true);
  newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
      var name = $(this).attr('name').replace('-' + (total_tf-1) + '-', '-' + total_tf + '-');
      var id = 'id_' + name;
      $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
  // Update the number of tf questions in the labels
  newElement.find('label').each(function() {
    var forValue = $(this).attr('for');
    if (forValue) {
      forValue = forValue.replace('-' + (total_tf-1) + '-', '-' + total_tf + '-');
      $(this).attr({'for': forValue});
      }
  });
  total_tf++;
  // change the id value of the new tf question
  $('#id_mc-TOTAL_FORMS').val(total_tf);
  //place it after the form
  $(selector).after(newElement);
  
  // Change the value of the hidden input order
  id_order = "id_tf-" + order + "-order";
  current_order = document.getElementById(id_order);
  order++;
  $(current_order).val(order);
  return false;  
}

function cloneMC(selector) {
  
  total_mc = $('#id_mc-TOTAL_FORMS').val();

  var newElement = $(selector).clone(true);
  newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
      var name = $(this).attr('name').replace('-' + (total_mc-1) + '-', '-' + total_mc + '-');
      var id = 'id_' + name;
      $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
  newElement.find('label').each(function() {
    var forValue = $(this).attr('for');
    if (forValue) {
      forValue = forValue.replace('-' + (total_mc-1) + '-', '-' + total_mc + '-');
        $(this).attr({'for': forValue});
      }
  });
  total_mc++;
  $('#id_mc-TOTAL_FORMS').val(total_mc);
  $(selector).after(newElement);

    return false;
}

// Add a TrueFalse Question Form
$(document).on('click', '.add-tf-form', function(e){
    e.preventDefault();
    var form = $(".tf-form").last();
    cloneTF(form);
    return false;
});
// Add a MultiChoice Question Form
$(document).on('click', '.add-mc-form', function(e){
    e.preventDefault();
    var form = $(".mc-form").last();
    cloneTF(form);
    return false;
});