from pytest_bdd import scenario

@scenario('../features/login.feature', 'Login successfully')
def test_login_successfully():
    pass

@scenario('../features/login.feature', 'Login invalid')
def test_login_invalid():
    pass