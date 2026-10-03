import pytest

from inventory import Inventory

# --- Tests สำหรับ low_stock_items ---

def test_low_stock_all_items_above_threshold():
    inv = Inventory()
    inv.add_item("Apple", 10, 2.0)
    inv.add_item("Banana", 5, 3.0)
    assert inv.low_stock_items(3) == []


def test_low_stock_includes_equal_threshold():
    inv = Inventory()
    inv.add_item("Apple", 3, 2.0)
    inv.add_item("Banana", 5, 3.0)
    assert inv.low_stock_items(3) == ["Apple"]


def test_low_stock_sorted_by_name():
    inv = Inventory()
    inv.add_item("Orange", 2, 2.0)
    inv.add_item("Apple", 2, 2.0)
    inv.add_item("Banana", 1, 2.0)
    assert inv.low_stock_items(2) == ["Apple", "Banana", "Orange"]


def test_low_stock_empty_inventory():
    inv = Inventory()
    assert inv.low_stock_items(5) == []


def test_low_stock_threshold_zero():
    inv = Inventory()
    inv.add_item("Apple", 0, 2.0)
    inv.add_item("Banana", 1, 2.0)
    assert inv.low_stock_items(0) == ["Apple"]


def test_low_stock_negative_threshold():
    inv = Inventory()
    inv.add_item("Apple", 0, 2.0)
    assert inv.low_stock_items(-1) == []


# --- Tests สำหรับ sell ---

def test_sell_exact_remaining_quantity():
    inv = Inventory()
    inv.add_item("Apple", 5, 2.0)
    assert inv.sell("Apple", 5) == 0


def test_sell_zero_should_raise():
    inv = Inventory()
    inv.add_item("Apple", 5, 2.0)
    with pytest.raises(ValueError):
        inv.sell("Apple", 0)


def test_sell_negative_should_raise():
    inv = Inventory()
    inv.add_item("Apple", 5, 2.0)
    with pytest.raises(ValueError):
        inv.sell("Apple", -1)


def test_sell_over_quantity_should_raise():
    inv = Inventory()
    inv.add_item("Apple", 5, 2.0)
    with pytest.raises(ValueError):
        inv.sell("Apple", 6)


def test_sell_missing_item_should_raise():
    inv = Inventory()
    with pytest.raises(KeyError):
        inv.sell("Apple", 1)

from inventory import InventoryItem

# --- Tests สำหรับ InventoryItem (Validation Errors) ---

def test_inventory_item_empty_name_raises():
    with pytest.raises(ValueError, match="ชื่อสินค้าต้องไม่ว่างเปล่า"):
        InventoryItem("", 5, 10.0)
    with pytest.raises(ValueError, match="ชื่อสินค้าต้องไม่ว่างเปล่า"):
        InventoryItem("   ", 5, 10.0)


def test_inventory_item_negative_quantity_raises():
    with pytest.raises(ValueError, match="จำนวนสินค้าต้องไม่ติดลบ"):
        InventoryItem("Apple", -1, 10.0)


def test_inventory_item_invalid_price_raises():
    with pytest.raises(ValueError, match="ราคาต้องมากกว่าศูนย์"):
        InventoryItem("Apple", 5, 0.0)
    with pytest.raises(ValueError, match="ราคาต้องมากกว่าศูนย์"):
        InventoryItem("Apple", 5, -5.0)


# --- Tests สำหรับ add_item ชื่อซ้ำ ---

def test_add_duplicate_item_raises():
    inv = Inventory()
    inv.add_item("Apple", 5, 2.0)
    with pytest.raises(ValueError, match="มีอยู่ในระบบแล้ว"):
        inv.add_item("Apple", 3, 2.0)


# --- Tests สำหรับ restock ---

def test_restock_success():
    inv = Inventory()
    inv.add_item("Apple", 5, 2.0)
    assert inv.restock("Apple", 5) == 10


def test_restock_missing_item_raises():
    inv = Inventory()
    with pytest.raises(KeyError, match="ไม่พบสินค้า"):
        inv.restock("Unknown", 5)


def test_restock_invalid_amount_raises():
    inv = Inventory()
    inv.add_item("Apple", 5, 2.0)
    with pytest.raises(ValueError, match="จำนวนที่เติมต้องมากกว่าศูนย์"):
        inv.restock("Apple", 0)


# --- Tests สำหรับ get_total_value ---

def test_get_total_value():
    inv = Inventory()
    assert inv.get_total_value() == 0.0
    inv.add_item("Apple", 2, 10.0)
    inv.add_item("Banana", 3, 20.0)
    assert inv.get_total_value() == 80.0