from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

def patch_bom_kenny():
	known = frappe.db.sql("""select name,default_bom from `tabItem` where name like "TEMP-%" """,as_list=1)
	for row in known:
		bom_temp = frappe.get_doc("BOM",row[1])
		new_item_parent = row[0][5:]
		item_variant= frappe.db.sql("""select * from `tabItem` where variant_of="{}" """.format(new_item_parent),as_dict=1)
		for variant in item_variant:
			material=[]
			item_detail = frappe.get_doc("Item",variant["item_code"])
			color = ""
			for att in item_detail.attributes:
				if  att.attribute=="Colour":
					color = att.attribute_value
			for mat in bom_temp.items:
				item = frappe.get_doc("Item",mat.item_code)
				if item.variant_of:
					correct_mat = frappe.db.sql("""select parent from `tabItem Variant Attribute`
						where attribute_value="{}" and attribute="Colour" """.format(color),as_list=1)
					if len(correct_mat)>0
						item = frappe.get_doc("Item",correct_mat[0][0])
						new_row = mat.copy()
						new_row.item_code = item.item_code
						new_row.item_name = item.item_name
						material.append(new_row)
					else:
						material.append(mat)
					# if item.item_group=="Pleats":
					# 	pass
					# elif item.item_group=="Fabrics":
					# 	pass

			bom = frappe.get_doc({
				"doctype":"BOM",
				"company" : bom_temp.company,
				"item":variant["item_code"],
				"item_name":variant["item_name"],
				"uom":variant["stock_uom"],
				"allow_alternative_item":1,
				"quantity":bom_temp.quantity,
				"with_operations":bom_temp.with_operations,
				"operations":bom_temp.operations,
				"transfer_material_against":bom_temp.transfer_material_against,
				"routing":bom_temp.routing,
				"items":material
				})
			bom.save()
			bom.submit()
			frappe.db.commit()