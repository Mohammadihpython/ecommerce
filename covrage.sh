
COVERAGE_REPORT=$(pytest --cov )
COVERAGE_PERCENTAGE=$(echo "$COVERAGE_REPORT" | awk '/TOTAL/{print substr($NF, 1, length($NF)-1)}')
if [ -n "$COVERAGE_PERCENTAGE" ]; then
    echo "Coverage Percentage: $COVERAGE_PERCENTAGE"
    sed -i "s|!\[Coverage\].*|![Coverage](https://img.shields.io/badge/coverage-${COVERAGE_PERCENTAGE}%25-brightgreen)|g" README.md
else
    echo "Failed to retrieve coverage percentage."
fi
