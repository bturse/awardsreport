import pytest
from awardsreport.seed_helpers import get_date_ranges, generate_copy_from_sql


def test_get_date_ranges():
    # test simple default
    result = get_date_ranges(2010, 1)
    expected_result = [
        ("2009-01-01", "2009-12-31"),
        ("2010-01-01", "2010-01-31"),
    ]
    assert result == expected_result
    # test default ending on leap day
    result = get_date_ranges(2016, 2)
    expected_result = [
        ("2015-02-01", "2016-01-31"),
        ("2016-02-01", "2016-02-29"),
    ]
    assert result == expected_result

    # test < 12 months spanning across years
    result = get_date_ranges(2010, 1, 4)
    expected_result = [("2009-10-01", "2010-01-31")]
    assert result == expected_result

    # test leap year on non middle tuple
    result = get_date_ranges(2014, 2, 48, 6)
    expected_result = [
        ("2010-03-01", "2010-08-31"),
        ("2010-09-01", "2011-02-28"),
        ("2011-03-01", "2011-08-31"),
        ("2011-09-01", "2012-02-29"),
        ("2012-03-01", "2012-08-31"),
        ("2012-09-01", "2013-02-28"),
        ("2013-03-01", "2013-08-31"),
        ("2013-09-01", "2014-02-28"),
    ]
    assert result == expected_result


def test_generate_copy_from_sql():
    test_cols = {
        "asst_cols": ["asst_col1", "asst_col2"],
        "proc_cols": ["proc_col1", "proc_col2"],
    }
    result = generate_copy_from_sql("Assistance_1.csv", test_cols)
    expected_result = "COPY assistance_transactions(asst_col1, asst_col2) FROM STDIN WITH (FORMAT CSV, HEADER)"
    assert result == expected_result
    result = generate_copy_from_sql("Contract_1.csv", test_cols)
    expected_result = "COPY procurement_transactions(proc_col1, proc_col2) FROM STDIN WITH (FORMAT CSV, HEADER)"
    assert result == expected_result
    # test file name exception
    with pytest.raises(ValueError):
        generate_copy_from_sql("invalid_fname")
    # test test_cols keys exception
    with pytest.raises(ValueError):
        generate_copy_from_sql("Assistance", {"invalid_key": ["foo"]})
