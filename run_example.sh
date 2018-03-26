RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'


python server.py &

TEST_EXIT_CODE=`python client.py`
wait $TEST_EXIT_CODE

if [ -z ${TEST_EXIT_CODE+x} ] || [ "$TEST_EXIT_CODE" -ne 0 ] ; then
  printf "${RED}Tests Failed${NC} - Exit Code: $TEST_EXIT_CODE\n"
else
  printf "${GREEN}Tests Passed${NC}\n"
fi

exit "$TEST_EXIT_CODE"
