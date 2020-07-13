
//hide the basic forms:
$("#base-tf-form").hide();
$("#base-mc-form").hide();

var order = 0;


function cloneTF(selector) {
  // get the current total number of tf questions
  total_tf = $('#id_tf-TOTAL_FORMS').val();

  // clone the selected part of the form
  var newElement = $(selector).clone(true);
  // change its name and id
  newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
      var name = $(this).attr('name').replace('-' + (total_tf-1) + '-', '-' + total_tf + '-');
      var id = 'id_' + name;
      $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
  // remove its id (useful later):
  $('#base-tf-form').removeAttr('id');
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
  //place it in the div intended for it
  $('#forms').append(newElement);
  
  // Change the value of the hidden input order
  id_order = "id_tf-" + order + "-order";
  order = document.getElementById(id_order);
  order++;
  $(order).val(order);
  return false;  
}

function cloneMC(selector) {
  console.log(selector);
  // get the current total number of mc questions
  total_mc = $('#id_mc-TOTAL_FORMS').val();

  // change its name and id
  var newElement = $(selector).clone(true);
  newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
      var name = $(this).attr('name').replace('-' + (total_mc-1) + '-', '-' + total_mc + '-');
      var id = 'id_' + name;
      $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
  // remove its id (useful later):
  $('#base-mc-form').removeAttr('id');
  newElement.find('label').each(function() {
    var forValue = $(this).attr('for');
    if (forValue) {
      forValue = forValue.replace('-' + (total_mc-1) + '-', '-' + total_mc + '-');
        $(this).attr({'for': forValue});
      }
  });
  total_mc++;
  $('#id_mc-TOTAL_FORMS').val(total_mc);
  $('#forms').append(newElement);

  // Change the value of the hidden input order
  id_order = "id_mc-" + order + "-order";
  order = document.getElementById(id_order);
  order++;
  $(order).val(order);

    return false;
}