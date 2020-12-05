from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import copy
def patch_pl_kenny():
	known = frappe.db.sql("""select name,item_code from `tabItem Price` where item_code like "TEMP-%" """,as_list=1)
	for row in known:
		#print(row[0])
		pl_temp = frappe.get_doc("Item Price",row[0])
		new_item_parent = row[1][5:]
		item_variant= frappe.db.sql("""select * from `tabItem` where variant_of="{}" """.format(new_item_parent),as_dict=1)
		for variant in item_variant:
			new_pl = copy.copy(pl_temp)
			new_pl.item_code=variant["item_code"]
			new_pl.item_name=variant["item_name"]
			new_pl.item_description=variant["description"]
			new_pl.name=None
			new_pl.save()
def patch_item_name():
	known = frappe.db.sql("""select name from `tabItem` where item_group="Fabrics" and variant_of!="" """,as_list=1)
	for row in known:
		item = frappe.get_doc("Item",row[0])
		color = ""
		for att in item.attributes:
			if  att.attribute=="Colour":
					color = att.attribute_value
		if color in item.item_name:
			continue
		else:
			item.item_name="{} {}".format(item.item_name,color)
			item.description=item.item_name
			item.save()
			frappe.db.commit()
def patch_del_bom():
	known = frappe.db.sql("""select name,default_bom from `tabItem` where name like "TEMP-%" """,as_list=1)
	for row in known:
		print(row[0])
		bom_temp = frappe.get_doc("BOM",row[1])
		new_item_parent = row[0][5:]
		item_variant= frappe.db.sql("""select * from `tabItem` where variant_of="{}" """.format(new_item_parent),as_dict=1)
		for variant in item_variant:
			if variant["default_bom"]:
				bom_temp = frappe.get_doc("BOM",variant["default_bom"])
				if bom_temp:
					if bom_temp.docstatus ==1:
						bom_temp.cancel()
					bom_temp.delete()
					frappe.db.commit()
def patch_bom_kenny():
	known = frappe.db.sql("""select name,default_bom from `tabItem` where name like "TEMP-%" """,as_list=1)
	for row in known:
		print(row[0])
		bom_temp = frappe.get_doc("BOM",row[1])
		new_item_parent = row[0][5:]
		item_variant= frappe.db.sql("""select * from `tabItem` where variant_of="{}" """.format(new_item_parent),as_dict=1)
		for variant in item_variant:
			valid=1
			if variant["default_bom"]:
				continue
			material=[]
			item_detail = frappe.get_doc("Item",variant["item_code"])
			color = ""
			for att in item_detail.attributes:
				if  att.attribute=="Colour":
					color = att.attribute_value
			fbr_code=""
			for mat in bom_temp.items:
				item = frappe.get_doc("Item",mat.item_code)
				new_row = copy.copy(mat)
				if item.variant_of:
					#item_like = mat.item_code[:len(mat.item_code)-3]
					correct_mat = frappe.db.sql("""select parent from `tabItem Variant Attribute`
						where attribute_value="{}" and attribute="Colour" and parent IN (select name from `tabItem` where variant_of = "{}") """.format(color,item.variant_of),as_list=1)
					if len(correct_mat)>0:
						item = frappe.get_doc("Item",correct_mat[0][0])
						fbr_code=item.item_code[len(item.item_code)-6:]
						new_row.item_code = item.item_code
						new_row.item_name = item.item_name
						material.append(new_row)
					else:
						material.append(new_row)
						valid=0
				else:
					if item.item_group=="Pleats":
						if fbr_code=="":
							for x in bom_temp.items:
								if x.item_code.startswith("FBR"):
									fbr_code=x.item_code[len(x.item_code)-6:]
						if fbr_code!="":
							#try:
							#	item = frappe.get_doc("Item","{}{}".format(mat.item_code[:len(mat.item_code)-3],color_code))
							#	if item:
							#		new_row.item_code = item.item_code
							#		new_row.item_name = item.item_name
							#except:
							#	#if not found
							size = mat.item_code[1:3]
							search_simmilar = frappe.db.sql("""select name,item_name from `tabItem` where name like "P%{}" """.format(fbr_code),as_list=1)
							if len(search_simmilar)>0:
								found=0
								for p in search_simmilar:
									if p[0][1:3]==size:
										new_row.item_code = p[0]
										new_row.item_name = p[1]
										found=1
								if found==0:
									new_row.item_code = search_simmilar[0][0]
									new_row.item_name = search_simmilar[0][1]
						else:
							valid=0
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
			if valid==1:
				bom.submit()
			frappe.db.commit()
