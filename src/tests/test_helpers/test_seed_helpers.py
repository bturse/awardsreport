from awardsreport.helpers.seed_helpers import get_date_ranges


def test_get_date_ranges(db_session):
    result = get_date_ranges(2016, 2, 1)
    expected_result = [("2016-02-01", "2016-02-29")]
    assert result == expected_result

    result = get_date_ranges(2016, 2, 12)
    expected_result = [("2015-03-01", "2016-02-29")]
    assert result == expected_result

    result = get_date_ranges(2016, 3, 13)
    expected_result = [
        ("2015-03-01", "2016-02-29"),
        ("2016-03-01", "2016-03-31"),
    ]
    assert result == expected_result
