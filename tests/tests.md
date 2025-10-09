Brief Summary of Test Code


A test script that checks each logical block without actually downloading heavy data or making live HTTP/TAP requests:

-Uses pytest.

-Mocks external services (TapPlus, requests, etc.).

-Creates temporary test data using tmp_path.

-Verifies that key steps (loading, filtering, saving) work and produce expected outputs.
