# graphql-api-test-suite
Project written in Python 3.10
To run the tests the best option is to use a github codepsace!

Otherwise...

## Setup
1. Install Python
2. Use the provided requirements.txt file to install the dependencies:
  pip install -r requirements.txt
If you don't have pip you will need to install it: https://pypi.org/project/pip/

## Run the tests
The tests are run by the test runner Pytest.
1. Navigate to the project root
2. Run the command pytest -v (or python -m pytest -v)
3. The tests should all run and pass
4. If you want to generate a HTML report add the pytest arguments --html=report.html --self-contained-html
