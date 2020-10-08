total_tf = 0
total_mc = 0
order = 0
$("#id_tf-0-order").val(order);
$("#id_mc-0-order").val(order);
$("#base-tf-form").hide();
$("#base-mc-form").hide();
$("#post-quiz").hide();
order++;

// Add a TrueFalse Question Form
$(document).on('click', '#add-tf', function(e){
  e.preventDefault();
  $("#post-quiz").show()
  var form = $("#base-tf-form");
  cloneTF(form);
  $("#id_tf-" + (total_tf-1) + "-order").val(order);
  order++;
  return false;
});

// Add a MultiChoice Question Form
$(document).on('click', '#add-mc', function(e){
  e.preventDefault();
  $("#post-quiz").show()
  var form = $("#base-mc-form");
  cloneMC(form);
  $("#id_mc-" + (total_mc-1) + "-order").val(order);
  order++;
  return false;
});

$("form").submit(function(e){
  // For tf forms
  $("input[name='tf-TOTAL_FORMS']").each(function() {
      this.value = total_tf;
  });
  $("input[name='tf-INITIAL_FORMS']").each(function() {
      this.value = 0;
  });
  $("input[name='tf-MIN_NUM_FORMS']").each(function() {
      this.value = 0;
  });
  $("input[name='tf-MAX_NUM_FORMS']").each(function() {
      this.value = 1000;
  });
  // For mc forms
  $("input[name='mc-TOTAL_FORMS']").each(function() {
      this.value = total_mc;
  });
  $("input[name='mc-INITIAL_FORMS']").each(function() {
      this.value = 0;
  });
  $("input[name='mc-MIN_NUM_FORMS']").each(function() {
      this.value = 0;
  });
  $("input[name='mc-MAX_NUM_FORMS']").each(function() {
      this.value = 1000;
  });
  if (total_tf != 0) $("#base-tf-form").remove();
  if (total_mc != 0) $("#base-mc-form").remove();
  $(this).submit();
});

  function cloneTF(selector) {
  // clone the selected part of the form
  var newElement = $(selector).clone(true);

  if (total_tf >= 1) {
    // Empty the fields
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
          var name = $(this).attr('name').replace('-0-', '-' + total_tf + '-');
          var id = 'id_' + name;
          $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
      });
    // Update the number of tf questions in the labels
    newElement.find('label').each(function() {
      var forValue = $(this).attr('for');
      if (forValue) {
        forValue = forValue.replace('-0-', '-' + total_tf + '-');
        $(this).attr({'for': forValue});
        }
    });
  }
  total_tf++;
  newElement.removeAttr('id').show();
  $('#forms').append(newElement);
  
  return false;  
}

function cloneMC(selector) {
  // clone the selected part of the form
  var newElement = $(selector).clone(true);

  if (total_mc >= 1) {
    // Empty the fields
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
          var name = $(this).attr('name').replace('-0-', '-' + total_mc + '-');
          var id = 'id_' + name;
          $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
      });
    // Update the number of tf questions in the labels
    newElement.find('label').each(function() {
      var forValue = $(this).attr('for');
      if (forValue) {
        forValue = forValue.replace('-0-', '-' + total_mc + '-');
        $(this).attr({'for': forValue});
        }
    });
  }
  total_mc++;
  newElement.removeAttr('id').show();
  $('#forms').append(newElement);
  
  return false;  
}