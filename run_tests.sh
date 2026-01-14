#!/bin/bash

# Default values
TEST_PATH="examples/poc_saucedemo/tests"
ALLURE_DIR="reports/allure-results"
OPEN_REPORT=false

# Help Function
show_help() {
    echo "Usage: ./run_tests.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -t, --tests PATH      Path to test directory or file (default: $TEST_PATH)"
    echo "  -o, --open            Open Allure report after execution"
    echo "  -c, --clean           Clean allure-results before running"
    echo "  -h, --help            Show this help message"
}

# Parse Arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -t|--tests) TEST_PATH="$2"; shift ;;
        -o|--open) OPEN_REPORT=true ;;
        -c|--clean) rm -rf "$ALLURE_DIR"; echo "Cleaned $ALLURE_DIR" ;;
        -h|--help) show_help; exit 0 ;;
        *) echo "Unknown parameter passed: $1"; show_help; exit 1 ;;
    esac
    shift
done

# Run Pytest
echo "🚀 Running tests in: $TEST_PATH"
.venv/bin/pytest "$TEST_PATH" --alluredir="$ALLURE_DIR"

EXIT_CODE=$?

# Report Generation
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Tests Passed!"
else
    echo "❌ Tests Failed!"
fi

echo "📊 Allure results saved to: $ALLURE_DIR"

if [ "$OPEN_REPORT" = true ]; then
    if command -v allure &> /dev/null; then
        echo "Opening Allure Report..."
        allure serve "$ALLURE_DIR"
    else
        echo "⚠️  Allure CLI not found. Install it to view reports (e.g., brew install allure)."
    fi
fi

exit $EXIT_CODE
