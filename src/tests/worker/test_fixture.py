def test_user_payments_fixture(get_user_payments):
    users = get_user_payments(6)
    assert users[0].purpose == "subscription"
    assert users[1].id != users[2].id
    assert users[1].amount != users[2].amount
    assert users[1].created_at != users[2].created_at
