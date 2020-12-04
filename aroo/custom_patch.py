from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import copy
def patch_pl_kenny():
	known = frappe.db.sql("""select name,item_code from `tabItem Price` where item_code like "TEMP-%" """,as_list=1)
	for row in known:
		pl_temp = frappe.get_doc("Item Price",row[0])
		new_item_parent = row[1][5:]
		item_variant= frappe.db.sql("""select * from `tabItem` where variant_of="{}" """.format(new_item_parent),as_dict=1)
		for variant in item_variant:
			new_pl = copy.copy(pl_temp)
			new_pl.item_code=item_variant["item_code"]
			new_pl.item_code=item_variant["item_name"]
			new_pl.item_description=item_variant["description"]
			new_pl.name=None
			new_pl.save()
def patch_del_bom():
	known = frappe.db.sql("""select name,default_bom from `tabItem` where name like "TEMP-%" """,as_list=1)
	for row in known:
		bom_temp = frappe.get_doc("BOM",row[1])
		new_item_parent = row[0][5:]
		item_variant= frappe.db.sql("""select * from `tabItem` where variant_of="{}" """.format(new_item_parent),as_dict=1)
		for variant in item_variant:
			bom_temp = frappe.get_doc("BOM",variant["default_bom"])
			if bom_temp:
				bom_temp.cancel()
				bom_temp.delete()
def patch_bom_kenny():
	known = frappe.db.sql("""select name,default_bom from `tabItem` where name like "TEMP-%" """,as_list=1)
	for row in known:
		print(row[0])
		bom_temp = frappe.get_doc("BOM",row[1])
		new_item_parent = row[0][5:]
		item_variant= frappe.db.sql("""select * from `tabItem` where variant_of="{}" """.format(new_item_parent),as_dict=1)
		for variant in item_variant:
			if variant["default_bom"]:
				continue
			material=[]
			item_detail = frappe.get_doc("Item",variant["item_code"])
			color = ""
			for att in item_detail.attributes:
				if  att.attribute=="Colour":
					color = att.attribute_value
			color_code=variant["item_code"][len(variant["item_code"])-3:]
			for mat in bom_temp.items:
				item = frappe.get_doc("Item",mat.item_code)
				new_row = copy.copy(mat)
				if item.variant_of:
					item_like = mat.item_code[:len(mat.item_code)-3]
					correct_mat = frappe.db.sql("""select parent from `tabItem Variant Attribute`
						where attribute_value="{}" and attribute="Colour" and parent like "{}%" """.format(color,item_like),as_list=1)
					if len(correct_mat)>0:
						item = frappe.get_doc("Item",correct_mat[0][0])
						new_row.item_code = item.item_code
						new_row.item_name = item.item_name
						material.append(new_row)
					else:
						material.append(new_row)
				else:
					if item.item_group=="Pleats":
						item = frappe.get_doc("Item",mat.item_code[mat.item_code[:len(mat.item_code)-3]]+color_code)
						if item:
							new_row.item_code = item.item_code
							new_row.item_name = item.item_name
					material.append(new_row)
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
