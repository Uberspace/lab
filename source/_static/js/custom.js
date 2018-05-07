$(function () {
  function checkLogoHeight () {
    var logo = $('div[itemprop="articleBody"] > .sidebar')
    var hr = $('div[itemprop="articleBody"] > .section > hr')
    var logoEnd = 0
    var hrPosition = 0
    if (logo.length) {
      logoEnd = logo.offset().top + logo.outerHeight()
    }
    if (hr.length) {
      hrPosition = hr.offset().top
    }
    console.log('[logo] ' + logoEnd + ' vs ' + hrPosition)
    if (logoEnd > hrPosition) {
      var marginTop = parseInt(hr.css('margin-top'), 10)
      var marginBottom = parseInt(hr.css('margin-bottom'), 10)
      var offset = Math.ceil((logoEnd - hrPosition) / 2)
      hr.css('margin-top', marginTop + offset + 'px')
      hr.css('margin-bottom', marginBottom + offset + 'px')
      console.log('[logo] pushed first break down by ' + offset * 2)
    }
  }

  console.log('UberLab launched…')

  // fix spacing between border and text
  checkLogoHeight()
})
