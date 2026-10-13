#!/bin/bash
# Jina AI Image Search Script
# Usage: ./search-images.sh "search query" [source]
# Example: ./search-images.sh "mountain landscape" unsplash

QUERY="${1:-nature}"
SOURCE="${2:-unsplash}"

# API key from the JINA_API_KEY environment variable (required for Search).
# Get a free key at https://jina.ai. This script hits s.jina.ai (Search), which
# REQUIRES a key (keyless = 401). If the key 402s, mint a fresh free key, OR do the
# search with Claude Code's built-in WebSearch tool and scrape results with keyless
# r.jina.ai (Reader works no-key).
API_KEY="${JINA_API_KEY:?Set JINA_API_KEY first (get a free key at https://jina.ai)}"

# URL encode the query
ENCODED_QUERY=$(echo "$SOURCE+$QUERY" | sed 's/ /+/g')

echo "Searching for: $QUERY on $SOURCE"
echo "---"

# Step 1: Search for image pages
echo "Step 1: Searching s.jina.ai..."
SEARCH_RESULTS=$(curl -s "https://s.jina.ai/?q=$ENCODED_QUERY" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Respond-With: no-content" \
  -H "X-With-Favicons: true")

# Extract first Unsplash/Pexels URL
FIRST_URL=$(echo "$SEARCH_RESULTS" | grep -oE "https://(unsplash|pexels|pixabay)\.[^\"'\s]+" | head -1)

if [ -z "$FIRST_URL" ]; then
  echo "No image site URLs found in search results"
  echo "Raw results:"
  echo "$SEARCH_RESULTS"
  exit 1
fi

echo "Found: $FIRST_URL"
echo "---"

# Step 2: Scrape the page for actual image URLs
echo "Step 2: Scraping r.jina.ai for image URLs..."
curl -s "https://r.jina.ai/$FIRST_URL" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Engine: browser" \
  -H "X-With-Images-Summary: true" | \
  grep -oE "https://images\.(unsplash|pexels|pixabay)[^\"'\s\)]+" | \
  head -10

echo "---"
echo "Done. Above are the direct image URLs you can use."
