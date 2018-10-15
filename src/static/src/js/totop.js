// to-top
(function () {
  const offset = 220;
  const duration = 500;
  const toTop = $('.to-top');

  $(window).scroll(function () {
    if ($(this).scrollTop() > offset) {
      toTop.removeClass('hidden');
    } else {
      toTop.addClass('hidden');
    }
  });

  toTop.click(function (event) {
    event.preventDefault();
    $('html, body').animate({ scrollTop: 0 }, duration);
    return false;
  });
})();
