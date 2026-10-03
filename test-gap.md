| กรณีที่ AI ให้มา | กรณีที่ขาด | test ที่เราเขียนเสริม |
|---|---|---|
| ขายปกติ 1 รายการ | ขายเท่ากับจำนวนที่เหลือทั้งหมด | `test_sell_exact_remaining_quantity` |
| ขายปกติ 1 รายการ | ขาย 0 | `test_sell_zero_should_raise` |
| ขายปกติ 1 รายการ | ขายติดลบ | `test_sell_negative_should_raise` |
| ขายปกติ 1 รายการ | ขายเกินจำนวน | `test_sell_over_quantity_should_raise` |
| ขายปกติ 1 รายการ | ขายสินค้าที่ไม่มีในคลัง | `test_sell_missing_item_should_raise` |