stripe-mock api testing project
============================

- this is a QA automation project for the stripe API using stripe-mock
- it uses pytest for automated tests, and postman for manual/collection-based tests
- the goal: get as close as possible to real-world stripe QA, but with a mock server

How to run it
-------------
- install requirements: `pip install -r requirements.txt`
- start stripe-mock (download from github, run the binary, listens on localhost:12111)
- run tests: `pytest` (or use markers like `pytest -m charges`)
- you can also open the postman collection for manual poking

Project structure
-----------------
- `src/` - the api client and helpers
- `tests/` - all the pytest files, organized by endpoint (payment_intents, customers, refunds, charges, etc)
- `conftest.py` - fixtures for reusable test data and setup
- `config/` - constants, settings, etc

Stripe-mock is not a full stripe clone. it sometimes returns errors for things that would work on real stripe, or ignores some params. For some update or invalid id tests, it might return an error instead of a mock object. So, some tests check for either "id" or "error" in the response.

Test coverage
--------------
- payment intents: create, retrieve, update, confirm, cancel, list
- customers: create, retrieve, update, delete, list
- refunds: create, retrieve, update, cancel, list
- charges: create, retrieve, update, capture, list
- auth and error handling: missing/invalid api key, invalid endpoints, bad requests, etc
+ postman collection covers some tests for manual testing
