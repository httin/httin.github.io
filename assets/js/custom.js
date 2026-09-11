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

// Home page writing feed: render the next posts as the reader scrolls down.
let feed = document.querySelector('.js-post-feed');
let feedMarker = document.querySelector('.js-post-feed-marker');
if (feed && feedMarker) {
  let batchSize = 5;
  let band = 200;
  let nextIndex = feed.querySelectorAll('.entry').length;
  let filling = false;

  // Mirrors _includes/post-entry.html. Keep the two in step.
  let buildEntry = function (post) {
    let item = document.createElement('li');
    item.className = 'entry';

    if (post.thumbnail) {
      let thumb = document.createElement('img');
      thumb.className = 'entry-thumb';
      thumb.src = post.thumbnail;
      thumb.alt = post.title;
      thumb.loading = 'lazy';
      item.appendChild(thumb);
    }

    let body = document.createElement('div');
    body.className = 'entry-body';

    let title = document.createElement('a');
    title.className = 'entry-title';
    title.href = post.url;
    title.textContent = post.title;
    body.appendChild(title);

    if (post.description) {
      let desc = document.createElement('p');
      desc.className = 'entry-desc';
      desc.textContent = post.description;
      body.appendChild(desc);
    }

    let meta = document.createElement('p');
    meta.className = 'entry-meta';
    let stamp = document.createElement('time');
    stamp.setAttribute('datetime', post.date_attr);
    stamp.textContent = post.date_label;
    meta.appendChild(stamp);

    post.tags.forEach(function (tag, i) {
      meta.appendChild(document.createTextNode(i === 0 ? ' \u00b7 ' : ', '));
      let link = document.createElement('a');
      link.href = tag.url;
      link.textContent = tag.name;
      meta.appendChild(link);
    });

    body.appendChild(meta);
    item.appendChild(body);
    return item;
  };

  // Read the index at load, so revealing a batch never waits on the network.
  // A failed request gives an empty index, which stops the feed and leaves the
  // "All writing" link as the way to the rest of the posts.
  let indexRequest = fetch(feedMarker.dataset.src)
    .then(function (response) { return response.ok ? response.json() : []; })
    .catch(function () { return []; });

  let markerInReach = function () {
    return feedMarker.getBoundingClientRect().top <= window.innerHeight + band;
  };

  // Add batches while the marker stays in reach. The loop matters because
  // IntersectionObserver reports only changes in state: once the marker sits
  // on a page the reader cannot scroll past, it never leaves the band and no
  // further callback arrives.
  let fill = function () {
    if (filling) return;
    filling = true;
    indexRequest.then(function (posts) {
      while (nextIndex < posts.length && markerInReach()) {
        let batch = posts.slice(nextIndex, nextIndex + batchSize);
        batch.forEach(function (post) { feed.appendChild(buildEntry(post)); });
        nextIndex += batch.length;
      }
      filling = false;
      if (nextIndex >= posts.length) {
        observer.disconnect();
        feedMarker.remove();
      }
    });
  };

  let observer = new IntersectionObserver(function (entries) {
    if (entries.some(function (entry) { return entry.isIntersecting; })) fill();
  }, { rootMargin: band + 'px' });

  observer.observe(feedMarker);
}
