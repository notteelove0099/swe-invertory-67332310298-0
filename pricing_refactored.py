# pricing_legacy.py
# โมดูลคำนวณราคาและส่วนลดของระบบ Inventory (Refactored)

import datetime

TAX_RATE = 0.07
member_points = {}
LOG = []


def _calculate_item_subtotal(quantity, unit_price):
    """คำนวณราคาย่อยของสินค้าแต่ละรายการพร้อมส่วนลดตามจำนวนชิ้น (Bulk Discount)"""
    if quantity <= 0:
        return 0.0

    subtotal = quantity * unit_price
    if quantity >= 100:
        subtotal *= 0.90
    elif quantity >= 50:
        subtotal *= 0.95

    return subtotal


def _apply_member_benefits(total, member):
    """คำนวณส่วนลดสมาชิก 5% และสะสมแต้ม 1 แต้มต่อ 100 บาท"""
    if member is None:
        return total

    if member not in member_points:
        member_points[member] = 0

    discounted_total = total * 0.95
    earned_points = int(discounted_total / 100)
    member_points[member] += earned_points

    return discounted_total


def _apply_coupon(total, coupon, today):
    """คำนวณส่วนลดจากคูปองโปรโมชัน"""
    if coupon is None:
        return total

    if coupon == "SAVE50":
        return total - 50
    elif coupon == "HALF":
        return total * 0.5
    elif coupon == "NEWYEAR":
        current_date = (
            datetime.datetime.now(datetime.timezone.utc).date()
            if today is None
            else today
        )
        if current_date.month == 1:
            return total * 0.8

    return total


def calc(items, member=None, coupon=None, today=None):
    """คำนวณราคาสุทธิรวมภาษี บันทึกประวัติ และอัปเดตแต้มสมาชิก"""
    # 1. รวมยอดสินค้าพร้อมส่วนลดจำนวนซื้อ
    total = sum(_calculate_item_subtotal(qty, price) for _, qty, price in items)

    # 2. คำนวณส่วนลดสมาชิกและสะสมแต้ม
    total = _apply_member_benefits(total, member)

    # 3. คำนวณส่วนลดจากคูปอง
    total = _apply_coupon(total, coupon, today)

    # 4. ตรวจสอบไม่ให้ยอดติดลบ
    total = max(total, 0)

    # 5. บวกภาษีและปัดเศษ 2 ตำแหน่ง
    total = total + (total * TAX_RATE)
    total = round(total, 2)

    # 6. บันทึก Transaction Log
    LOG.append((member, total))

    return total