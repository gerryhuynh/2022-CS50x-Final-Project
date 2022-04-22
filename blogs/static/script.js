// Validate Register page
var emailPattern = /[\w_.+]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}/;
var passwordPattern = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^a-zA-Z0-9]).{8,}$/;

function checkValidity(element, regexPattern, errorMessageId, errorMessage) {
  if (!regexPattern.test(element.value)) {
    element.setCustomValidity(errorMessage)
    document.getElementById(errorMessageId).innerHTML = errorMessage;
  }
  else {
    element.setCustomValidity('');
  }
};

function validateConfirm(confirmation) {
  var password = document.getElementById('password');

  if (confirmation.value !== password.value) {
    confirmation.setCustomValidity('Passwords do not match.');
    document.getElementById('invalid-confirmation').innerHTML = 'Passwords do not match.';
  } 
  else {
    checkValidity(confirmation, passwordPattern, 'invalid-confirmation', 'Please enter a valid password')
  }
};

function validateEmail(email) {
  checkValidity(email, emailPattern, 'invalid-email', 'Please enter a valid email')
};

function validatePassword(password) {
  checkValidity(password, passwordPattern, 'invalid-password', 'Please enter a valid password')
  validateConfirm(document.getElementById('confirmation'));
};

/*
[RESOURCES]

JavaScript Syntax
- https://www.w3resource.com/javascript/operators/logical-operator.php

Regex in JavaScript
- https://www.w3schools.com/jsref/jsref_obj_regexp.asp

Key up event
- https://www.w3schools.com/jsref/event_onkeyup.asp

Validation
- https://stackoverflow.com/questions/10777970/can-i-mark-a-field-invalid-from-javascript
- https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation#Customized_error_messages
- https://developer.mozilla.org/en-US/docs/Web/API/HTMLObjectElement/setCustomValidity
- https://developer.mozilla.org/en-US/docs/Web/API/ValidityState/patternMismatch
- https://w3resource.com/javascript/form/password-validation.php
- https://www.w3schools.com/js/js_validation_api.asp
- https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#the-constraint-validation-api
- https://medium.com/the-ui-files/form-validation-with-javascript-4fcf4dd32846
- https://www.w3schools.com/csSref/sel_invalid.asp

Understanding Bootstrap's validation below
- https://getbootstrap.com/docs/5.1/forms/validation/
- https://flaviocopes.com/javascript-iife/

Validating email vs. database
- https://stackoverflow.com/questions/13192643/is-it-possible-to-access-an-sqlite-database-from-javascript
- https://github.com/sql-js/sql.js

Debugging
- https://www.analyticsmania.com/post/how-to-pause-javascript-and-inspect-an-element-that-quickly-disappears/

*/

// https://getbootstrap.com/docs/5.1/forms/validation/
(function () {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {

        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
          form.classList.add('was-validated')
        }

      }, false)
    })
})()

// https://getbootstrap.com/docs/5.1/components/tooltips/
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

// https://getbootstrap.com/docs/5.1/components/popovers/
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
})
var popover = new bootstrap.Popover(document.querySelector('.popover-dismiss'), {
  trigger: 'focus'
})

// https://getbootstrap.com/docs/5.1/components/modal/
var myModal = document.getElementById('myModal')
var myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', function () {
  myInput.focus()
})