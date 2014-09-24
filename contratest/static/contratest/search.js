var letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"];
var letterCount = 0;

$(document).ready(function() {
  $firstForm = $('#id_movename').eq(0);
  $firstForm.attr('onchange', "openSubforms($(this).parent().attr('data-formnum'), $(this).parent().attr('data-formlet'), $(this).val())");
  $firstForm.attr("name", "movename0a");
  openSubforms($firstForm.parent().attr('data-formnum'), $firstForm.parent().attr('data-formlet'), $firstForm.val());
} );
// currently doesn't support back button to multiple forms

function openSubforms(formnum, formlet, val){
  // When value of a 'movename' form is changed, opens the subforms corresponding to that move
  $thisForm = $('#subform' + formnum + formlet);
  $thisForm.html(extraforms[val]);
  $components = $thisForm.find('select');
  updateName($components, formnum, formlet);
}

function updateName(fields, formnum, formlet){
  // Updates 'name' of each subform dropdown to reflect that form's number and letter
    // e.g. "who1b"
  fields.each( function() {
    curName = $(this).attr("name");
    $(this).attr("name", curName + formnum + formlet);
  });
}

function addForm(){
  // Adds a form to the bottom of current formstack,
    // changing values to reflect that form's letter/number
  var $newForm = $('#form0a').clone();
  var formCount = countForms();
  var formlet = letters[letterCount];
  $newForm.attr("data-formlet", formlet); // set letter of form
  $newForm.attr("id", "form" + formCount + formlet); // change ID of mama
  $newForm.attr("data-formnum", formCount); // change form-no of mama
  $newForm.find('#id_movename').attr("name", "movename" + formCount + formlet); // update 'name' of movename dropdown with appropriate form number
  $newForm.find('.babyform').attr("id", "subform" + formCount + formlet); // change id of baby
  $newForm.find('.babyform').html(""); // clear baby
  $('#searchform').append($newForm);
}

function removeForm(){
  // Removes the bottom-most form
  var $allForms = $('.mamaform');
  if ($allForms.length > 1) { // only if there is more than one form on the page
    $allForms[$allForms.length-1].remove();

    // if the removed form was on the border between two form letters, decrement
      // the current letter
    curLet = $allForms[$allForms.length-1].getAttribute('data-formlet');
    prevLet = $allForms[$allForms.length-2].getAttribute('data-formlet');
    if (curLet != prevLet) {
      letterCount--;
      }
  }
}

function newAndForm(){
  // Makes a new 'and' form, i.e., begins a form of the next letter.
  letterCount++;
  addForm();
  var $allForms = $('.mamaform');
  $allForms.eq($allForms.length-1).prepend("<p>---AND---</p>");
}

function countForms(){
  // Returns number of forms on the page
  return $('.mamaform').length;
}