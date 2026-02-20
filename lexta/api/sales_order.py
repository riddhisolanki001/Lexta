import frappe
from frappe.utils import flt

def validate_company_total_stock(doc, method):

    shortage = []

    for row in doc.items:

        if not row.item_code:
            continue

        row_no = row.idx

        # =======================================================
        # GET COMPANY TOTAL STOCK (Across All Warehouses)
        # =======================================================

        company_total_stock = frappe.db.sql("""
            SELECT SUM(actual_qty)
            FROM `tabBin`
            WHERE item_code = %s
        """, row.item_code)[0][0] or 0

        # =======================================================
        # VALIDATE QTY AGAINST COMPANY TOTAL STOCK
        # =======================================================

        if flt(row.qty) > flt(company_total_stock):

            shortage.append(
                f"Row {row_no} – <b>{row.item_code}</b>: "
                f"Required <b>{row.qty}</b>, "
                f"Available Company Stock <b>{company_total_stock}</b>"
            )

    # =======================================================
    # THROW ALL ERRORS TOGETHER
    # =======================================================

    if shortage:
        msg = "<br>".join(shortage)
        frappe.throw(
            msg,
            title="Insufficient Company Stock"
        )
# def validate_company_stock(doc, method):
#     for row in doc.items:
#         # print("============")
#         # print(row.qty,row.company_total_stock)
#         if not row.item_code:
#             continue

#         # Fetch total company stock for this item
#         company_total_stock = frappe.db.get_value(
#             "Bin",
#             {
#                 "item_code": row.item_code,
#                 "warehouse": row.warehouse
#             },
#             "actual_qty"
#         ) or 0

#         if row.qty > company_total_stock:
#             frappe.throw(
#                 _("Row {0}: Entered Qty {1} is greater than available stock {2} for Item {3}")
#                 .format(row.idx, row.qty, company_total_stock, row.item_code),
#                 title="Insufficient Stock"
#             )