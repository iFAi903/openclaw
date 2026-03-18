#!/bin/bash
# Test connection to CRO and CTO agents

echo "Testing connection to CRO (18766)..."
curl -s -o /dev/null -w "%{http_code}" http://localhost:18766/status
echo ""

echo "Testing connection to CTO (18793)..."
curl -s -o /dev/null -w "%{http_code}" http://localhost:18793/status
echo ""
