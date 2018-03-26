python3 -c "import os; print(os.listdir(os.curdir)); import pyRpc"

python examples/server.py

TEST_EXIT_CODE=`python examples/client.py`
wait $TEST_EXIT_CODE

if [ -z ${TEST_EXIT_CODE+x} ] || [ "$TEST_EXIT_CODE" -ne 0 ] ; then
  printf "${RED}Tests Failed${NC} - Exit Code: $TEST_EXIT_CODE\n"
else
  printf "${GREEN}Tests Passed${NC}\n"
fi

exit $TEST_EXIT_CODE
