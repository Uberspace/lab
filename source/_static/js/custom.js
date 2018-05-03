$(function() {

  function check_logo_height() {
    var logo = $('div[itemprop="articleBody"] > .sidebar');
    var hr = $('div[itemprop="articleBody"] > .section > hr');
    var logo_end = 0;
    var hr_position = 0;
    if (logo.length) {
      logo_end = logo.offset().top + logo.outerHeight();
    }
    if (hr.length) {
      hr_position = hr.offset().top;
    }
    console.log('[logo] ' + logo_end + " vs " + hr_position)
    if (logo_end > hr_position) {
      var margin_top = parseInt(hr.css('margin-top'), 10);
      var margin_bottom = parseInt(hr.css('margin-bottom'), 10);
      var offset = Math.ceil((logo_end - hr_position) / 2);
      hr.css('margin-top', margin_top + offset + 'px');
      hr.css('margin-bottom', margin_bottom + offset + 'px');
      console.log('[logo] pushed first break down by ' + offset * 2);
    }
  };

  console.log('UberLab launched…');
  check_logo_height();

});
