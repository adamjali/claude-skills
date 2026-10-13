# Jina AI API Reference

> **API key**: this skill reads `JINA_API_KEY` from the environment. Get a free key at https://jina.ai (a new email = a fresh free token grant).
>
> **Free no-key fallback** (verified 2026-06): `r.jina.ai` (Reader) works with NO `Authorization` header (free, per-IP rate-limited) — use it to scrape/read a page when the key 402s; its clean markdown often beats Claude Code's built-in `WebFetch`. `s.jina.ai` (Search) REQUIRES a key (keyless = 401) — when the key's dead, do the search with **Claude Code's built-in `WebSearch` tool** (no key, no cost), then scrape the chosen URLs with keyless `r.jina.ai`. Or mint a fresh free key at https://jina.ai.

## s.jina.ai - Search API

Search the web and get structured results.

### Endpoint
```
GET https://s.jina.ai/?q={query}
```

### Headers
| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | Yes | `Bearer $JINA_API_KEY` |
| `X-Respond-With` | No | `no-content` to skip page content |
| `X-With-Favicons` | No | `true` to include favicons |
| `X-Return-Format` | No | `markdown`, `html`, `text`, `screenshot`, `pageshot` |

### Response Format
Returns JSON with search results including:
- `title` - Page title
- `url` - Page URL
- `description` - Page description/snippet
- `content` - Page content (if not using no-content)

### Example
```bash
curl "https://s.jina.ai/?q=unsplash+sunset+beach" \
  -H "Authorization: Bearer $JINA_API_KEY" \
  -H "X-Respond-With: no-content"
```

---

## r.jina.ai - Reader API

Convert any URL to clean, readable markdown.

### Endpoint
```
GET https://r.jina.ai/{url}
```

### Headers
| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | No | `Bearer $JINA_API_KEY` (Reader also works keyless) |
| `X-Engine` | No | `browser` for JS-heavy pages |
| `X-With-Generated-Alt` | No | `true` to generate alt text |
| `X-With-Images-Summary` | No | `true` for images summary |
| `X-With-Links-Summary` | No | `true` for links summary |
| `X-Return-Format` | No | `markdown`, `html`, `text`, `screenshot`, `pageshot` |
| `X-Target-Selector` | No | CSS selector to target specific content |
| `X-Wait-For-Selector` | No | Wait for element before scraping |

### Response Format
Returns GitHub-flavored markdown with:
- Page title and metadata
- Content converted to markdown
- Images as `![alt](url)` format
- Links preserved
- Optional summaries appended

### Image URL Pattern
Images from stock sites typically have URLs like:
```
https://images.unsplash.com/photo-{ID}?w={width}&h={height}&...
https://images.pexels.com/photos/{ID}/pexels-photo-{ID}.jpeg?...
```

### Example
```bash
curl "https://r.jina.ai/https://unsplash.com/s/photos/nature" \
  -H "Authorization: Bearer $JINA_API_KEY" \
  -H "X-Engine: browser" \
  -H "X-With-Images-Summary: true"
```

---

## Best Practices

### For Image Search
1. Use `unsplash+keyword` for high-quality free images
2. Use `X-Engine: browser` for JavaScript-rendered pages
3. Use `X-With-Images-Summary: true` to get all images at once
4. Extract URLs matching `images.unsplash.com` or similar patterns

### For Web Scraping
1. Use `X-Target-Selector` to focus on specific content
2. Use `X-Wait-For-Selector` for dynamic content
3. Set appropriate timeouts for complex pages

### Rate Limits
- Be respectful of API limits
- Cache results when possible
- Use `X-Respond-With: no-content` when you only need URLs

---

## Troubleshooting

### Empty Results
- Check if the URL is accessible
- Try `X-Engine: browser` for JS-heavy sites
- Verify the `JINA_API_KEY` environment variable is set

### Missing Images
- Use `X-With-Images-Summary: true`
- Some sites block scraping - try alternative sources
- Check if images are lazy-loaded (need browser engine)

### Timeout Issues
- Add `X-Wait-For-Selector` for dynamic content
- Increase timeout if needed
- Try simpler queries with fewer results
