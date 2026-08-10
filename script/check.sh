#!/usr/bin/env bash
# Builds the site and asserts facts about the generated HTML and CSS.
set -uo pipefail
cd "$(dirname "$0")/.."

FAIL=0
pass() { printf '  ok    %s\n' "$1"; }
fail() { printf '  FAIL  %s\n' "$1"; FAIL=1; }

assert_contains() {
  if grep -qF -- "$2" "$1" 2>/dev/null; then pass "$3"; else fail "$3"; fi
}
assert_absent() {
  if grep -qF -- "$2" "$1" 2>/dev/null; then fail "$3"; else pass "$3"; fi
}
assert_file() {
  if [ -f "$1" ]; then pass "$2"; else fail "$2"; fi
}
assert_missing() {
  if [ -e "$1" ]; then fail "$2"; else pass "$2"; fi
}

echo "==> build"
if ! bundle exec jekyll build --quiet; then
  echo "  BUILD FAILED"
  exit 1
fi

CSS=_site/assets/css/style.css
HOME=_site/index.html
BLOGS=_site/blogs/index.html
POST='_site/Ordered-Set-data-structure-in-C++.html'

echo "==> assertions"
assert_file "$HOME" "homepage is generated"
assert_file "$POST" "post page is generated"
assert_contains "$POST" 'class="katex' "post still renders KaTeX server-side"

assert_contains "$CSS" "color-scheme:light" "css pins the light colour scheme"
assert_contains "$CSS" "--accent:" "css defines the accent token"
assert_contains "$CSS" "#fffdf9" "css uses the warm white background"
assert_absent "$CSS" "light-dark(" "no dark-mode branch remains"

assert_contains "$CSS" "--font-display:" "css defines the display font token"
assert_contains "$HOME" "Fraunces" "homepage loads Fraunces"
assert_contains "$HOME" "Source+Serif+4" "homepage loads Source Serif 4"
assert_absent "$CSS" "1.66667rem" "old compiled 18px type scale is gone"

assert_absent "$CSS" "border: 15px solid" "blue viewport frame is gone"
assert_absent "$CSS" "FontAwesome" "icon font is gone"
assert_absent "$POST" "renderToString" "broken inline KaTeX script is gone"
assert_absent "$POST" "disqus" "Disqus is gone"
assert_absent "$HOME" "Page 1 of" "pagination chrome is gone"
assert_missing "assets/fonts/fontawesome.woff" "icon font file is deleted"

assert_contains "$CSS" "--measure:" "css defines the prose measure"
assert_contains "$CSS" ".wide" "css defines the breakout class"

assert_file "_data/categories.yml" "categories data file exists"
assert_file "_includes/post-entry.html" "post entry include exists"

assert_contains "$BLOGS" "Data Structures and Algorithms" "archive shows the category heading"
assert_contains "$BLOGS" "cat-blurb" "archive shows the category blurb"
assert_contains "$BLOGS" "Ordered Set data structure" "archive lists the post"

assert_contains "$HOME" "hub-intro" "homepage has the intro block"
assert_contains "$HOME" "All writing" "homepage links to the full archive"
assert_contains "$HOME" "Projects" "homepage has a projects section"
assert_missing "_includes/post-card.html" "old post-card include is deleted"

assert_absent "$POST" "cpp-binary" "stock feature image is gone from the post"
assert_contains "$CSS" "--code-keyword" "prism tokens use custom properties"
assert_missing "images/cpp-binary.jpg" "stock feature image file is deleted"

exit $FAIL
