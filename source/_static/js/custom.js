$(function () {
  function checkLogoHeight() {
    var logo = $('div[itemprop="articleBody"] > .sidebar');
    var hr = $('div[itemprop="articleBody"] > section > hr');
    var logoEnd = 0;
    var hrPosition = 0;
    if (logo.length) {
      logoEnd = logo.offset().top + logo.outerHeight();
    }
    if (hr.length) {
      hrPosition = hr.offset().top;
    }
    console.log("[logo] " + logoEnd + " vs " + hrPosition);
    if (logoEnd > hrPosition) {
      var marginTop = parseInt(hr.css("margin-top"), 10);
      var marginBottom = parseInt(hr.css("margin-bottom"), 10);
      var offset = Math.ceil((logoEnd - hrPosition) / 2);
      hr.css("margin-top", marginTop + offset + "px");
      hr.css("margin-bottom", marginBottom + offset + "px");
      console.log("[logo] pushed first break down by " + offset * 2);
    }
  }

  function circleRatio() {
    $(".circle").each(function () {
      $(this).height($(this).width());
    });
  }

  function autoLinks(match, link, offset, string) {
    const reMail = new RegExp(
      /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i
    );
    const reURL = new RegExp(
      /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi
    );
    if (link.match(reMail)) {
      link = `<a href="mailto:${link}">${link}</a>`;
    } else if (link.match(reURL)) {
      link = `<a href="${link}">${link}</a>`;
    }
    return `<span class="autolink">${link}</span>`;
  }

  function formatAuthor(ele) {
    const text = ele.html().trim();
    const idx = text.search(
      /[^A-Za-z\sÂÀÅÃÄâàáåãäÇçćčđÉÊÈËéêèëÓÔÒÕØÖóôòõöŠšßÚÛÙÜúûùüÝŸýÿŽž]/
    );
    const author = $('<span class="author"></span>');
    const extra = $("<small></small>");
    let extraText = "";
    ele.html("");
    if (idx >= 0) {
      author.text(text.slice(0, idx).trim());
      extraText = text.slice(idx).trim();
      extraText = extraText.replace(/&lt;([^>]+?)&gt;/g, autoLinks);
      extra.append(extraText);
    } else {
      author.text(text.trim());
    }
    ele.append(author, " ", extra);
  }

  function addTagListToToc() {
    let toc_tags = $(
      '<li class="toctree-l1"><a class="reference internal" href="/tags/">Tags</a></li>'
    );
    let toc_01 = $('[aria-label="main navigation"] > ul > li:eq(0)');
    toc_01.after(toc_tags);
  }

  // Auf gehts…

  console.log("UberLab launched…");

  // add a link to the teg list view to the side navigation
  addTagListToToc();

  // fix spacing between border and text
  checkLogoHeight();

  // "hall of fame" stuff…
  if ($("#hall-of-fame").length) {
    console.log('Welcome to the "Hall of Fame"!');
    // fix score circle
    let selector = "#hall-of-fame > ol > li > div:first-child";
    $(selector).each(function () {
      $(this).wrapInner('<div class="circle"></div>');
    });
    circleRatio();
    $(window).resize(circleRatio);
    // format author lines
    selector = "#hall-of-fame > ol > li > div:nth-child(2)";
    $(selector).each(function () {
      formatAuthor($(this));
    });
  }
});
