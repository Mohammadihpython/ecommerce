def test_model_str(db, user_factory):
    user = user_factory.create()
    assert str(user) == user.phone_number
