---
name: jina-image-search
description: "Find and scrape images from the web using Jina AI. Use this skill when the user asks to find images, search for photos, get pictures from Unsplash/Pexels/Pixabay, needs stock photos for presentations, websites, or designs, or mentions finding images online."
---

# Jina AI Image Search & Web Scraping

<objective>
Find high-quality images from the web using Jina AI's search (s.jina.ai) and reader (r.jina.ai) APIs. Stateless one-shot tool — search, scrape, return URLs. Useful for presentations, web design, visual art, and documents.
</objective>

<execution_context>
- 🟢 Auto-execute: search, scrape, parse, return URLs
- Stateless — no history file, no recovery
- Auth: Bearer token read from the `JINA_API_KEY` environment variable
</execution_context>

## Overview

Jina AI provides two endpoints:
- **s.jina.ai** - Search the web and return structured results
- **r.jina.ai** - Scrape any URL and convert to GitHub-flavored markdown with embedded images

## Authentication

This skill reads your Jina key from the `JINA_API_KEY` environment variable. **Get a free key at https://jina.ai** (no credit card; a new email address gets a fresh free token grant). Then set it in your shell profile:

```bash
export JINA_API_KEY="your-key"
```

Send it as a Bearer token:
```bash
Authorization: Bearer $JINA_API_KEY
```

### Free no-key fallback (verified 2026-06)
If the key returns **402** (`InsufficientBalanceError` = balance exhausted), or to avoid spending it:
- **Reader `r.jina.ai` works WITHOUT a key** — drop the `Authorization` header (free, per-IP rate-limited). Use it to scrape/read a page; its clean-markdown output often beats Claude Code's built-in `WebFetch`, so prefer it (or use both).
- **Search `s.jina.ai` REQUIRES a key** (keyless = 401). When the key is dead, do the search half with **Claude Code's built-in `WebSearch` tool** (no key, no cost), then scrape the chosen URLs with keyless `r.jina.ai`.
- The 402 is tied to the *key's balance*, not your IP, so keyless Reader works even when the key is broke.

Recovery order: (1) reads → keyless Reader; (2) search → built-in `WebSearch`, or mint a fresh free key at https://jina.ai and update `JINA_API_KEY`; (3) pay to top up only as a last resort.

## Image Search Workflow

### Step 1: Search for Images

Use s.jina.ai to search image sites:

```bash
curl "https://s.jina.ai/?q=unsplash+mountains+landscape" \
  -H "Authorization: Bearer $JINA_API_KEY" \
  -H "X-Respond-With: no-content" \
  -H "X-With-Favicons: true"
```

Returns JSON with URLs to image pages on Unsplash, Pexels, etc.

### Step 2: Scrape Image URLs

Use r.jina.ai to extract actual image URLs from the pages:

```bash
curl "https://r.jina.ai/https://unsplash.com/s/photos/mountains" \
  -H "Authorization: Bearer $JINA_API_KEY" \
  -H "X-Engine: browser" \
  -H "X-With-Generated-Alt: true" \
  -H "X-With-Images-Summary: true" \
  -H "X-With-Links-Summary: true"
```

Returns markdown with embedded image URLs like:
```markdown
[![Image 1: Mountain landscape](https://images.unsplash.com/photo-ID?w=800)](https://unsplash.com/photos/ID)
```

### Step 3: Extract and Use Images

Parse the markdown output to extract direct image URLs (images.unsplash.com, etc.) for use in:
- Presentations (pptx)
- Web pages (HTML/React)
- Documents (docx)
- Visual designs (canvas)

## Common Image Sources

| Source | Search Query | License |
|--------|-------------|---------|
| **Unsplash** | `unsplash+KEYWORD` | Free, no attribution required |
| **Pexels** | `pexels+KEYWORD` | Free, no attribution required |
| **Pixabay** | `pixabay+KEYWORD` | Free, attribution appreciated |

## API Headers Reference

### s.jina.ai (Search)
| Header | Value | Purpose |
|--------|-------|---------|
| `X-Respond-With` | `no-content` | Return metadata only, not full content |
| `X-With-Favicons` | `true` | Include site favicons |

### r.jina.ai (Reader)
| Header | Value | Purpose |
|--------|-------|---------|
| `X-Engine` | `browser` | Use browser rendering for JS-heavy pages |
| `X-With-Generated-Alt` | `true` | Generate alt text for images |
| `X-With-Images-Summary` | `true` | Include summary of all images |
| `X-With-Links-Summary` | `true` | Include summary of all links |

## Quick Reference Scripts

For scripted image searches, see:
- `${CLAUDE_SKILL_DIR}/scripts/search-images.sh` - Search and scrape images
- `references/api-details.md` - Full API documentation

## Integration Examples

### For Presentations (pptx)
```bash
curl "https://s.jina.ai/?q=unsplash+business+meeting+office" ...
```

### For Web Design
```bash
curl "https://s.jina.ai/?q=unsplash+abstract+gradient+background" ...
```

### For Visual Art
```bash
curl "https://s.jina.ai/?q=unsplash+marble+texture+minimal" ...
```
