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
POST2='_site/Line-Sweep-Algorithm.html'
POST3='_site/Coordinate-Compression.html'
POST4='_site/Stack-Queue-Deque.html'

echo "==> assertions"
assert_file "$HOME" "homepage is generated"
assert_file "$POST" "post page is generated"
assert_contains "$POST" 'class="katex' "post still renders KaTeX server-side"

assert_contains "$CSS" "color-scheme:light" "css pins the light colour scheme"
assert_contains "$CSS" "--accent:" "css defines the accent token"
assert_contains "$CSS" "#fffdf9" "css uses the warm white background"
assert_contains "$CSS" "math-manuscript-background-light.webp" "css uses the manuscript background"
assert_contains "$CSS" ".has-manuscript::before" "css scopes the wallpaper to hub pages"
assert_file "_site/images/math-manuscript-background-light.webp" "manuscript background is copied into the site"
assert_contains "$HOME" 'class="has-manuscript"' "homepage shows the manuscript wallpaper"
assert_contains "_site/about/index.html" 'class="has-manuscript"' "about page shows the manuscript wallpaper"
assert_contains "_site/tags/index.html" 'class="has-manuscript"' "tags page shows the manuscript wallpaper"
assert_absent "$BLOGS" 'class="has-manuscript"' "writing index omits the manuscript wallpaper"
assert_absent "$POST2" 'class="has-manuscript"' "post pages omit the manuscript wallpaper"
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
assert_contains "$BLOGS" "entry-thumb" "archive shows a thumbnail for the post that sets one"

assert_contains "$HOME" "hub-intro" "homepage has the intro block"
assert_contains "$HOME" "All writing" "homepage links to the full archive"
assert_contains "$HOME" "Projects" "homepage has a projects section"
assert_missing "_includes/post-card.html" "old post-card include is deleted"

assert_absent "$POST" "cpp-binary" "stock feature image is gone from the post"
assert_contains "$CSS" "--code-keyword" "code tokens use custom properties"
assert_missing "images/cpp-binary.jpg" "stock feature image file is deleted"

assert_contains "$CSS" ".highlight .k," "css maps rouge keyword tokens to a color"
assert_absent "$CSS" ".token." "old prismjs token selectors are gone"
assert_contains "$POST2" 'class="language-cpp' "C++ code block is highlighted"
assert_contains "$POST2" 'class="heading-anchor"' "section headings are self-links"

assert_file "$POST3" "coordinate compression post is generated"
assert_contains "$POST3" 'class="katex' "coordinate compression post renders KaTeX"
assert_contains "$POST3" "rank-fold.gif" "post embeds the rank GIF"
assert_contains "$POST3" "maze-compress.gif" "post embeds the maze GIF"
assert_contains "$BLOGS" "Coordinate Compression" "archive lists the new post"

assert_file "$POST4" "stack queue deque post is generated"
assert_contains "$POST4" 'class="katex' "stack queue deque post renders KaTeX"
assert_contains "$POST4" "dfs-stack.gif" "post embeds the DFS GIF"
assert_contains "$POST4" "bfs-queue.gif" "post embeds the BFS GIF"
assert_contains "$POST4" "sliding-window-deque.gif" "post embeds the window GIF"
assert_contains "$POST4" "zero-one-bfs.gif" "post embeds the 0-1 BFS GIF"
assert_contains "$BLOGS" "Stack, Queue, and Deque" "archive lists the stack queue deque post"

exit $FAIL
