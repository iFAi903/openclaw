#!/bin/bash
# RSS Source Diagnostic Script
# Tests all RSS sources from rss-sources.md

echo "=========================================="
echo "RSS Source Diagnostic Report"
echo "Time: $(date)"
echo "=========================================="

# Test function
test_rss() {
    local name="$1"
    local url="$2"
    echo ""
    echo "--- Testing: $name ---"
    echo "URL: $url"
    
    # Test with curl
    response=$(curl -s -L -A "Mozilla/5.0 (compatible; RSS Bot/1.0)" \
        --max-time 15 \
        -w "\nHTTP_CODE:%{http_code}\nSIZE:%{size_download}\n" \
        "$url" 2>&1)
    
    http_code=$(echo "$response" | grep "HTTP_CODE:" | cut -d: -f2)
    size=$(echo "$response" | grep "SIZE:" | cut -d: -f2)
    content=$(echo "$response" | grep -v "HTTP_CODE:" | grep -v "SIZE:")
    
    echo "Status: $http_code"
    echo "Size: ${size} bytes"
    
    if [ "$http_code" = "200" ] && [ "$size" -gt 100 ]; then
        # Check content type
        if echo "$content" | grep -q "<?xml"; then
            echo "✅ Valid XML found"
            # Check format
            if echo "$content" | grep -q "<rss"; then
                echo "Format: RSS 2.0"
            elif echo "$content" | grep -q "<feed"; then
                echo "Format: Atom"
            else
                echo "Format: Unknown XML"
            fi
            # Count items
            item_count=$(echo "$content" | grep -o "<item>" | wc -l)
            entry_count=$(echo "$content" | grep -o "<entry>" | wc -l)
            total=$((item_count + entry_count))
            echo "Items found: $total"
        else
            echo "⚠️ No XML found - may be HTML or error page"
            echo "First 200 chars:"
            echo "$content" | head -c 200
        fi
    else
        echo "❌ Failed - HTTP $http_code or empty response"
    fi
}

# Main sources from rss-sources.md (13 sources)
echo ""
echo "========== MAIN AI NEWS SOURCES =========="

test_rss "TheVerge AI" "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"
test_rss "TechCrunch AI" "https://techcrunch.com/category/artificial-intelligence/feed/"
test_rss "MIT Technology Review AI" "https://www.technologyreview.com/topic/artificial-intelligence/feed"
test_rss "Wired AI" "https://www.wired.com/feed/tag/ai/latest/rss"
test_rss "VentureBeat AI" "https://venturebeat.com/category/ai/feed/"
test_rss "The Guardian AI" "https://www.theguardian.com/technology/artificialintelligenceai/rss"
test_rss "ScienceDaily AI" "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml"
test_rss "AI News" "https://www.artificialintelligence-news.com/feed/"
test_rss "MarkTechPost" "https://www.marktechpost.com/feed/"
test_rss "MIT News AI" "https://news.mit.edu/rss/topic/artificial-intelligence2"
test_rss "Google Research Blog" "https://research.google/blog/rss/"
test_rss "Microsoft AI Blog" "https://news.microsoft.com/source/topics/ai/feed/"
test_rss "BAIR Berkeley" "https://bair.berkeley.edu/blog/feed.xml"

echo ""
echo "========== PRODUCT SOURCES =========="

test_rss "ProductHunt" "https://www.producthunt.com/feed"
test_rss "HackerNews" "https://news.ycombinator.com/rss"
test_rss "Toolify" "https://www.toolify.ai/rss"
test_rss "Reddit r/artificial" "https://www.reddit.com/r/artificial/.rss"
test_rss "Reddit r/MachineLearning" "https://www.reddit.com/r/MachineLearning/.rss"

echo ""
echo "=========================================="
echo "Diagnostic Complete"
echo "=========================================="
