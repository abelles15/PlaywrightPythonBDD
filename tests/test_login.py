from pytest_bdd import scenario # pyright: ignore[reportMissingImports]

@scenario('../features/login.feature', 'Login successfully')
def test_login_successfully():
    pass

@scenario('../features/login.feature', 'Login invalid')
def test_login_invalid():
    pass

@scenario('../features/login.feature', 'Logout')
def test_logout():
    pass