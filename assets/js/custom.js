/**
 * Main JS file for Scriptor behaviours
 */

// Responsive video embeds
let videoEmbeds = [
  'iframe[src*="youtube.com"]',
  'iframe[src*="vimeo.com"]'
];
reframe(videoEmbeds.join(','));

// Menu on small screens
let menuToggle = document.querySelectorAll('.menu-toggle');
if (menuToggle) {
  for (let i = 0; i < menuToggle.length; i++) {
    menuToggle[i].addEventListener('click', function (e) {
      document.body.classList.toggle('menu--opened');
      e.preventDefault();
    }, false);
  }
}

// Table of contents for posts
let tocRoot = document.querySelector('.post-toc');
let postContent = document.querySelector('.post-content');
if (tocRoot && postContent) {
  let headings = postContent.querySelectorAll('h2, h3, .statement--toc');
  if (postContent.querySelectorAll('h2, h3').length >= 2) {
    let list = document.createElement('ul');
    let currentItem = null;

    headings.forEach(function (heading) {
      if (!heading.id) return;
      let link = document.createElement('a');
      link.href = '#' + heading.id;
      if (heading.classList.contains('statement')) {
        let label = heading.querySelector('strong');
        link.textContent = label ? label.textContent.replace(/\.$/, '') : heading.id;
        link.classList.add('toc-statement');
      } else {
        link.textContent = heading.textContent;
      }

      let item = document.createElement('li');
      item.appendChild(link);

      if (heading.tagName === 'H2' || !currentItem) {
        list.appendChild(item);
        currentItem = item;
      } else {
        let subList = currentItem.querySelector('ul');
        if (!subList) {
          subList = document.createElement('ul');
          currentItem.appendChild(subList);
        }
        subList.appendChild(item);
      }
    });

    tocRoot.appendChild(list);

    let linkByHeadingId = {};
    tocRoot.querySelectorAll('a').forEach(function (link) {
      linkByHeadingId[link.getAttribute('href').slice(1)] = link;
    });

    // Recompute from scratch on every trigger, rather than trusting only the
    // headings named in a given IntersectionObserver batch: a fast scroll can
    // carry a heading past the watch band between samples, so it never gets
    // reported as intersecting even though it's the section we scrolled past.
    let updateActiveHeading = function () {
      // A heading and the theorem under it both sit near the top after a
      // click. Use a short band so the next item does not steal the highlight.
      let boundary = 48;
      let active = null;
      headings.forEach(function (heading) {
        if (heading.getBoundingClientRect().top <= boundary) {
          active = heading;
        }
      });
      tocRoot.querySelectorAll('a.is-active').forEach(function (l) { l.classList.remove('is-active'); });
      if (active && linkByHeadingId[active.id]) {
        linkByHeadingId[active.id].classList.add('is-active');
      }
    };

    let observer = new IntersectionObserver(updateActiveHeading, { rootMargin: '0px 0px -70% 0px' });
    headings.forEach(function (heading) { observer.observe(heading); });
  }
}
