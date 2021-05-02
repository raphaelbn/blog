from unittest import mock
from user.authentication import SystemAuthUser


class UserMock():
    id = 401465483996
    displayName = 'Brett Wiltshire'
    email = 'brett@email.com'
    image = 'http://4.bp.blogspot.com/_YA50adQ-7vQ/S1gfR_6ufpI/AAAAAAAAAAk/1ErJGgRWZDg/S45/brett.png'


def mock_authenticate_credentials_success():
    user = UserMock()
    token = 'gfdgfdgdfhdfhdfh'
    return mock.MagicMock(return_value=(SystemAuthUser(user), token))
