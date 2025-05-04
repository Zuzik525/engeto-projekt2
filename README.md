# Pytest + Playwright automatic tests

## Authors
- [@Zuzana Frankova](https://www.github.com/zuzik525)

## Requirements: 
- Playwright installed
- Pytest installed
  - By default uses chromium.

## Configuration and run: 
- File tests/conftest.py contains configuration options
  - SITE_URL directs base project link. Change for directing to test environment
  - CART_SAVE_MAIL is mail address used for save/load cart tests. 
  - Browser() fixture can be edited for browser options.
    - There are prepared options
      - Headless (default)
      - With browser displayed (commented out)
Tests are run by simply runing pytest.

Note: When tests are run with debug on (pytest -v or PWDEBUG=1), each test run has to be started in playwright debug window.

## Documentation:
- Each test_* file has tests purpose in the first commented line (general tested area)
- Each individual test has comment as to what functionality is tested

## Known bugs:
- Tests may randomly fail due to page not loading in time 
  - Timeout while waiting for page load. 
  - Issue is not in tests, but in the site tested. 
  - Issue has been reported.
