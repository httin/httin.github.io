# Wrap formal statements so they share one CSS class, `.statement`.
# Kinds come from _data/statements.yml. Add a label there; do not add CSS.
module StatementFrames
  FALLBACK_KINDS = %w[Theorem Lemma Corollary Claim Definition].freeze

  module_function

  def kinds(site)
    listed = site&.data&.dig("statements", "kinds")
    list = Array(listed).map(&:to_s).reject(&:empty?)
    list.empty? ? FALLBACK_KINDS : list
  end

  def toc_kinds(site)
    listed = site&.data&.dig("statements", "toc")
    list = Array(listed).map(&:to_s).reject(&:empty?)
    list.empty? ? %w[Theorem] : list
  end

  def label_rx(kinds)
    alt = kinds.map { |kind| Regexp.escape(kind) }.join("|")
    /\A<p><strong>((#{alt})(?:\s+\d+)?\.)<\/strong>/
  end

  def apply(html, kinds = FALLBACK_KINDS, toc_kinds = %w[Theorem])
    rx = label_rx(kinds)
    out = +""
    i = 0
    seen = Hash.new(0)

    while (j = html.index("<p><strong>", i))
      out << html[i...j]
      block, after = extract_p(html, j)
      unless block
        out << html[j..]
        return out
      end

      m = block.match(rx)
      unless m
        out << block
        i = after
        next
      end

      kind = m[2].downcase
      slug = m[1].downcase.gsub(/[^a-z0-9]+/, "-").gsub(/^-|-$/, "")
      seen[slug] += 1
      slug = "#{slug}-#{seen[slug]}" if seen[slug] > 1

      blocks = [block]
      unless plain_text(block).end_with?(".")
        loop do
          nxt, nxt_after = extract_p(html, after)
          break unless nxt
          break unless display_math?(nxt) || nxt == "<p>and</p>"
          blocks << nxt
          after = nxt_after
        end
      end

      toc_class = toc_kinds.include?(m[2]) ? " statement--toc" : ""
      out << %(<div class="statement statement--#{kind}#{toc_class}" id="#{slug}" role="region" aria-label="#{m[1].delete_suffix('.')}">#{blocks.join}</div>)
      i = after
    end

    out << html[i..]
    out
  end

  def extract_p(html, start)
    pos = start
    pos += 1 while pos < html.length && html[pos] =~ /\s/
    return [nil, start] unless html[pos, 3] == "<p>"
    depth = 0
    i = pos
    while i < html.length
      if html[i, 2] == "<p" && (html[i + 2] == ">" || html[i + 2] == " ")
        depth += 1
        i += 2
      elsif html[i, 4] == "</p>"
        depth -= 1
        i += 4
        return [html[pos...i], i] if depth.zero?
      else
        i += 1
      end
    end
    [nil, start]
  end

  def plain_text(html)
    html.gsub(/<[^>]+>/, "").gsub(/\s+/, " ").strip
  end

  def display_math?(html)
    html.start_with?('<p><span class="katex-display">')
  end
end

Jekyll::Hooks.register :posts, :post_render do |post|
  post.output = StatementFrames.apply(
    post.output,
    StatementFrames.kinds(post.site),
    StatementFrames.toc_kinds(post.site)
  )
end
