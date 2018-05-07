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

  function replaceEntities (text) {
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    return text
  }

  function formatExtra (text) {
    text = replaceEntities(text)
    // TODO: auto–links
    return text
  }

  function formatAuthor (ele) {
    const text = ele.html().trim()
    const idx = text.search(/[^\w\s]/)
    const author = $('<span class="author"></span>')
    const extra = $('<small></small>')
    ele.html('')
    if (idx >= 0) {
      author.text(text.slice(0, idx).trim())
      extra.text(formatExtra(text.slice(idx).trim()))
    } else {
      author.text(text.trim())
    }
    ele.append(author, ' ', extra)
  }

  // Auf gehts…

  console.log('UberLab launched…')

  // fix spacing between border and text
  checkLogoHeight()

  // "hall of fame" stuff…
  if ($('#hall-of-fame').length) {
    console.log('Welcome to the "Hall of Fame"!')
    // format author lines
    const authors = '#hall-of-fame > ol > li > div:nth-child(2)'
    $(authors).each(function () {
      formatAuthor($(this))
    })
  }
})
