# kramdown gives every post heading an id (auto_ids). Wrap the heading text
# in a link to that same id, so the title itself is the permalink, the way
# GitHub renders Markdown headings.
Jekyll::Hooks.register :posts, :post_render do |post|
  post.output = post.output.gsub(/<(h[2-6]) id="([^"]+)">(.*?)<\/\1>/) do
    tag, id, text = Regexp.last_match(1), Regexp.last_match(2), Regexp.last_match(3)
    %(<#{tag} id="#{id}"><a class="heading-anchor" href="##{id}">#{text}</a></#{tag}>)
  end
end
