import pytest

import pricing_refactored as p


@pytest.fixture(autouse=True)
def reset_globals():
    p.member_points.clear()
    p.LOG.clear()


def test_calc_normal_price():
    assert p.calc([("Apple", 2, 10)]) == 21.4


def test_calc_bulk_discount_50():
    assert p.calc([("Apple", 50, 10)]) == 508.25


def test_calc_bulk_discount_100():
    assert p.calc([("Apple", 100, 10)]) == 963.0


def test_calc_zero_quantity_is_ignored():
    assert p.calc([("Apple", 0, 10)]) == 0.0


def test_calc_member_updates_points():
    assert p.calc([("Apple", 2, 10)], member="A") == 20.33
    assert p.member_points["A"] == 0


def test_calc_coupon_save50():
    assert p.calc([("Apple", 10, 10)], coupon="SAVE50") == 53.5

import datetime


def test_calc_coupon_half():
    # ทดสอบคูปอง HALF (ลด 50%)
    # ยอด 10 * 10 = 100 -> เหลือ 50 -> บวก VAT 7% = 53.5
    assert p.calc([("Apple", 10, 10)], coupon="HALF") == 53.5


def test_calc_coupon_newyear_in_january():
    # ทดสอบคูปอง NEWYEAR ในเดือนมกราคม (ลด 20%)
    # ยอด 10 * 10 = 100 -> เหลือ 80 -> บวก VAT 7% = 85.6
    jan_date = datetime.date(2026, 1, 15)
    assert p.calc([("Apple", 10, 10)], coupon="NEWYEAR", today=jan_date) == 85.6


def test_calc_coupon_newyear_outside_january_and_default_today():
    # 1. ทดสอบ NEWYEAR นอกเดือนมกราคม (ไม่ลด)
    feb_date = datetime.date(2026, 2, 1)
    assert p.calc([("Apple", 10, 10)], coupon="NEWYEAR", today=feb_date) == 107.0

    # 2. ทดสอบ NEWYEAR แบบไม่ส่ง today (โค้ดจะดึง datetime.date.today() มาใช้)
    res = p.calc([("Apple", 10, 10)], coupon="NEWYEAR")
    assert isinstance(res, float)


def test_calc_negative_total_floors_to_zero():
    # ทดสอบกรณียอดติดลบจากคูปอง SAVE50 (ซื้อ 10 บาท แต่ลด 50 บาท -> ติดลบ -> ปรับเป็น 0)
    assert p.calc([("Apple", 1, 10)], coupon="SAVE50") == 0.0