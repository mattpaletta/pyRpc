#!/usr/bin/env bash
if command -v python3 &>/dev/null; then
    echo "Using Python3"
    python3 server.py &

    python3 client.py &
    wait $!
    TEST_EXIT_CODE=$?
else
    echo "Using Python 2"
    python server.py &

    python client.py &
    wait $!
    TEST_EXIT_CODE=$?
fi

if [ -z ${TEST_EXIT_CODE+x} ] || [ "$TEST_EXIT_CODE" -ne 0 ] ; then
  printf "${RED}Tests Failed${NC} - Exit Code: $TEST_EXIT_CODE\n"
else
  printf "${GREEN}Tests Passed${NC}\n"
fi

exit $TEST_EXIT_CODE
