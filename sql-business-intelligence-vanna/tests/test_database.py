from src.database import is_safe_read_query

def test_select_is_allowed():
    assert is_safe_read_query("SELECT COUNT(*) FROM orders")

def test_with_query_is_allowed():
    assert is_safe_read_query("WITH totals AS (SELECT SUM(sales) AS s FROM orders) SELECT s FROM totals")

def test_delete_is_rejected():
    assert not is_safe_read_query("DELETE FROM orders")

def test_multiple_statements_are_rejected():
    assert not is_safe_read_query("SELECT * FROM orders; DROP TABLE orders;")
