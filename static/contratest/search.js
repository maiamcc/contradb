var letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"];
var letterCount = 0

$(document).ready(function() {
    firstForm = $('#id_movename')[0];
    firstForm.setAttribute('onchange', "openSubforms(this.parentNode.getAttribute('data-formNo'), this.parentNode.getAttribute('data-formLet'), this.value)");
    firstForm.setAttribute("name", "movename0a")
    openSubforms(firstForm.parentNode.getAttribute('data-formNo'), firstForm.parentNode.getAttribute('data-formLet'), firstForm.value);
} );
// currently doesn't support back button to multiple forms

function openSubforms(formNo, formLet, val){
    thisForm = $('#subform' + formNo + formLet)
    thisForm.html(extraforms[val]);
    components = thisForm.find('select')
    updateName(components, formNo, formLet)
}

function updateName(fields, formNo, formLet){
    fields.each( function() {
        curName = $(this).attr("name");
        $(this).attr("name", curName+formNo+formLet);
    });
}

function addForm(){
    var newForm = $('#form0a').clone();
    formCount = countForms();
    formLet = letters[letterCount]
    newForm.attr("data-formLet", formLet)
    newForm.attr("id", "form" + formCount + formLet); //change ID of mama
    newForm.attr("data-formNo", formCount); // change form-no of mama
    newForm.find('#id_movename').attr("name", "movename" + formCount + formLet) // update 'name' of movename dropdown with appropriate form number
    newForm.find('.babyform').attr("id", "subform" + formCount + formLet); // change id of baby
    newForm.find('.babyform').html(""); // clear baby
    $('#searchform').append(newForm);
}

function removeForm(){
    var allForms = $('.mamaform');
    if (allForms.length > 1) {
        allForms[allForms.length-1].remove();
        curLet = allForms[allForms.length-1].getAttribute('data-formLet')
        prevLet = allForms[allForms.length-2].getAttribute('data-formLet')
        if (curLet != prevLet) {
            letterCount--
        }
    }
    // there's probably a more elegant way to do this
}

function newAndForm(){
    letterCount++
    addForm()
    var allForms = $('.mamaform');
    allForms.eq(allForms.length-1).prepend("<p>---AND---</p>")
}

function countForms(){
    return document.getElementsByClassName("mamaform").length;
}