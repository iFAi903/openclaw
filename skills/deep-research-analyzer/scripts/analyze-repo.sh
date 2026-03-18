#!/bin/bash
# analyze-repo.sh - Quick research repository analysis script
# Usage: ./analyze-repo.sh [github-repo-url]
# Example: ./analyze-repo.sh https://github.com/google-deepmind/deepmind-research

set -e

REPO_URL=${1:-"https://github.com/google-deepmind/deepmind-research"}

echo "🔬 Deep Research Analyzer"
echo "=========================="
echo "Repository: $REPO_URL"
echo ""

# Extract org and repo name
ORG_REPO=$(echo $REPO_URL | sed 's|https://github.com/||' | sed 's|/$||')
ORG=$(echo $ORG_REPO | cut -d'/' -f1)
REPO=$(echo $ORG_REPO | cut -d'/' -f2)

echo "Organization: $ORG"
echo "Repository: $REPO"
echo ""

# Fetch README
echo "📥 Fetching README..."
README_URL="https://raw.githubusercontent.com/$ORG/$REPO/master/README.md"
README_CONTENT=$(curl -sL $README_URL 2>/dev/null || echo "")

if [ -z "$README_CONTENT" ]; then
    echo "⚠️  Could not fetch README from master branch, trying main..."
    README_URL="https://raw.githubusercontent.com/$ORG/$REPO/main/README.md"
    README_CONTENT=$(curl -sL $README_URL 2>/dev/null || echo "")
fi

if [ -n "$README_CONTENT" ]; then
    # Count projects (lines with "*   [")
    PROJECT_COUNT=$(echo "$README_CONTENT" | grep -c "^\*\s*\[" || echo "0")
    echo "✅ Found ~$PROJECT_COUNT projects in README"
    
    # Extract venues
    echo ""
    echo "📚 Venues mentioned:"
    echo "$README_CONTENT" | grep -oE "(Nature|Science|NeurIPS|ICML|ICLR|AAAI|CVPR|ICRA|RSS|CoRL)" | sort | uniq -c | sort -rn | head -10
else
    echo "❌ Could not fetch README"
fi

echo ""
echo "✅ Analysis complete!"
echo ""
echo "Next steps:"
echo "1. Review the README content for project details"
echo "2. Categorize projects by research theme"
echo "3. Identify high-impact papers (Nature/Science/top venues)"
echo "4. Extract technology stack information"
