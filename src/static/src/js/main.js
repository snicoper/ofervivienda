$(document).ready(function () {
  // https://highlightjs.org/usage/
  $('pre code').each(function (i, block) {
    hljs.highlightBlock(block);
  });
});

// CSRF TOKEN DJANGO
$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
  }
});

// Delimitadores Vue en templates.
const vueDelimiters = ['${', '}'];

// tooltip por defecto.
$('[data-toggle="tooltip"]').tooltip();

// dropdown por defecto.
$('.dropdown-toggle').dropdown();

// csrf axios
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
