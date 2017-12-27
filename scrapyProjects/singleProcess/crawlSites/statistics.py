# -*- coding: utf-8 -*-  
#!/usr/bin/python

import sys,getopt,os
import xlwt

categoryMap = {
		"51":"Women's Clothing", 
		"52":"Women's Shoes",
		"53":"Men's Clothing",
		"54":"Men's Shoes",
		"55":"Jewelry",
		"56":"Home",
		"57":"Gadgets",
		"58":"Beauty",
		"59":"Bags",
		"60":"Kids"
	}

subcategoryMap = {
	"51":{"100003141":"Hoodies", "200000783":"Sweaters", "200000775":"Jackets", "200001648":"Blouses & Shirts", "200003482":"Dresses", "200118010":"Bottoms", 
		"200000785":"Tops", "200000724":"Accessories", "200000782":"Suits & Sets", "200000777":"Sleep", "200000773":"Intimates", "200001092":"Jumpsuits", "200000781":"Socks & Hosiery", "200000784":"Swimwear"},
	"52":{"200002161":"Pumps", "100001607":"Boots", "100001611":"Sandals", "200002155":"Flats", "200002164":"Casual", "100001610":"Slippers", "200002157":"Loafers"},
	"53":{"200000662":"Jackets", "100003084":"Hoodies", "200000701":"Sweaters", "200000668":"Shirts", "100003086":"Jeans", "200118008":"Bottoms", 
		"100003088":"Shorts", "200000692":"Suits", "200000707":"Tops", "71":"Accessories", "200000706":"Swimwear", "200000708":"Underwear"},
	"54":{"200002118":"Oxfords", "200002158":"Loafers", "100001617":"Boots", "100001619":"Sandals", "100001618":"Slippers", "72":"Casual Shoes"},
	"55":{"200188001":"Fine Jewelry", "200000109":"Necklaces", "100006749":"Rings", "200132001":"Hair Accessories", "200000097":"Bracelets", "200000139":"Earrings", "200000161":"Wedding&Sets", "200154003":"Jewelry Making"},
	"56":{"78":"Bathroom", "77":"Housekeeping", "100006206":"Pet", "100002992":"Festive & Party", "81":"Bedding", "84":"Home Decoration", 
		"200020009":"Table&Sofa Linens", "200022002":"Carpets & Rugs", "200002937":"Wall Stickers", "40503":"Cushion", "82":"Curtain", "76":"Cooking Tools", "80":"Dinnerware", "83":"Drinkware", "79":"Kitchen"},
	"57":{"380230":"Phone Bags & Cases", "200002394":"Gadget Parts", "74":"Camera&photo", "1511":"Watches", "73":"Mobile Accessories", "200002361":"Tablet Accessories", "86":"Audio & Video", "85":"Electronics"},
	"58":{"660103":"Makeup", "200002458":"Hair Care & Styling", "200002547":"Nails & Tools"},
	"59":{"200100006":"Shell", "100002613":"Evening Bags", "200010057":"Men's Bags", "200092001":"Buckets", "100002612":"Crossbody Bags", 
		"200000764":"Shoulder Bags", "152405":"Wallets", "200000762":"Clutches", "200000766":"Top-Handle Bags", "152407":"Cosmetic Bags", "152401":"Backpacks"},
	"60":{"32212":"Children's Shoes", "100003199":"Girls Clothing", "100003186":"Boys Clothing", "200000528":"Baby Boys Clothing", "200000567":"Baby Girls Clothing", "200002101":"Baby Shoes", "100001118":"Baby Care"}
}
# workDir = os.getcwd()+'/'+area+'/'+categoryId+'/'

def collect_product(dir, rowNum, sheet):
	subcategory = os.listdir(dir)
	# print(subcategory)
	if subcategory is None:
		print("subcategory is empty")
		sys.exit()

	# row = row + 1
	categoryId = os.path.basename(os.path.dirname(dir))
	print('categoryDir:' + categoryId)
	categoryName = categoryMap[categoryId]
	# print('rowNum:'+str(rowNum[0]))
	
	# sheet.write_merge(rowNum[0], rowNum[0] + len(subcategory) - 1, 0, 0, categoryName+'('+categoryId+')')
	sheet.write(rowNum[0], 0, categoryName+'('+ categoryId+')')
	# print(dir)
	for subcategoryId in subcategory:
		subDir = dir + subcategoryId + '/'
		if not os.path.isdir(subDir):
			continue

		print('subcategoryDir:'+subcategoryId)
		subcategoryName = subcategoryMap[categoryId][subcategoryId]
		print('subcategoryName:' + subcategoryName)
		subcategoryFile = subDir + 'subCategoryProducts'
		# print(subcategoryFile)

		if not os.path.isfile(subcategoryFile):
			continue

		print(subcategoryFile)
		with open(subcategoryFile, "r") as f:
			productsList = f.read()
			
		#统计商品数量
		productsNum = productsList.count('\"')
		productsNum = (productsNum - 1) / 2
		print(productsNum)
		sheet.write(rowNum[0], 1, subcategoryName + '(' + subcategoryId + ')', set_style('Arial', 220, True))
		sheet.write(rowNum[0], 2, productsNum, set_style('Arial', 220, True))
		rowNum[0] += 1

	return rowNum
	#下一级目录，从下一行开始，中间不要有空行
	# rowNum -= 1

def set_style(name,height,bold=False):
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = name # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height

    # borders= xlwt.Borders()
    # borders.left= 6
    # borders.right= 6
    # borders.top= 6
    # borders.bottom= 6

    style.font = font
    # style.borders = borders

    return style


def main():
	#-a area;-c category
	opts, args = getopt.getopt(sys.argv[1:], "a:c:")

	# categoryMap = {
	# 	"51":"Women's Clothing", 
	# 	"52":"Women's Shoes",
	# 	"53":"Men's Clothing",
	# 	"54":"Men's Shoes",
	# 	"55":"Jewelry",
	# 	"56":"Home",
	# 	"57":"Gadgets",
	# 	"58":"Beauty",
	# 	"59":"Bags",
	# 	"0":"Kids"
	# }

	# subcategoryMap = {
	# 	"51":{"100003141":"Hoodies", "200000783":"Sweaters", "200000775":"Jackets", "200001648":"Blouses & Shirts", "200003482":"Dresses", "200118010":"Bottoms", 
	# 		"200000785":"Tops", "200000724":"Accessories", "200000782":"Suits & Sets", "200000777":"Sleep", "200000773":"Intimates", "200001092":"Jumpsuits", "200000781":"Socks & Hosiery", "200000784":"Swimwear"},
	# 	"52":{"200002161":"Pumps", "100001607":"Boots", "100001611":"Sandals", "200002155":"Flats", "200002164":"Casual", "100001610":"Slippers", "200002157":"Loafers"},
	# 	"53":{"200000662":"Jackets", "100003084":"Hoodies", "200000701":"Sweaters", "200000668":"Shirts", "100003086":"Jeans", "200118008":"Bottoms", 
	# 		"100003088":"Shorts", "200000692":"Suits", "200000707":"Tops", "71":"Accessories", "200000706":"Swimwear", "200000708":"Underwear"},
	# 	"54":{"200002118":"Oxfords", "200002158":"Loafers", "100001617":"Boots", "100001619":"Sandals", "100001618":"Slippers", "72":"Casual Shoes"},
	# 	"55":{"200188001":"Fine Jewelry", "200000109":"Necklaces", "100006749":"Rings", "200132001":"Hair Accessories", "200000097":"Bracelets", "200000139":"Earrings", "200000161":"Wedding&Sets", "200154003":"Jewelry Making"},
	# 	"56":{"78":"Bathroom", "77":"Housekeeping", "100006206":"Pet", "100002992":"Festive & Party", "81":"Bedding", "84":"Home Decoration", 
	# 		"200020009":"Table&Sofa Linens", "200022002":"Carpets & Rugs", "200002937":"Wall Stickers", "40503":"Cushion", "82":"Curtain", "76":"Cooking Tools", "80":"Dinnerware", "83":"Drinkware", "79":"Kitchen"},
	# 	"57":{"380230":"Phone Bags & Cases", "200002394":"Gadget Parts", "74":"Camera&photo", "1511":"Watches", "73":"Mobile Accessories", "200002361":"Tablet Accessories", "86":"Audio & Video", "85":"Electronics"},
	# 	"58":{"660103":"Makeup", "200002458":"Hair Care & Styling", "200002547":"Nails & Tools"},
	# 	"59":{"200100006":"Shell", "100002613":"Evening Bags", "200010057":"Men's Bags", "200092001":"Buckets", "100002612":"Crossbody Bags", 
	# 		"200000764":"Shoulder Bags", "152405":"Wallets", "200000762":"Clutches", "200000766":"Top-Handle Bags", "152407":"Cosmetic Bags", "152401":"Backpacks"},
	# 	"60":{"32212":"Children's Shoes", "100003199":"Girls Clothing", "100003186":"Boys Clothing", "200000528":"Baby Boys Clothing", "200000567":"Baby Girls Clothing", "200002101":"Baby Shoes", "100001118":"Baby Care"}
	# }

	row = 0
	col = 0

	area = None
	categoryId = None
	for op, value in opts:
		if op == "-a":
			area = value
		elif op == "-c":
			categoryId = value
		else:
			print("please use -a/-c")
			sys.exit()

	excel = xlwt.Workbook()
	sheet1 = excel.add_sheet(u'sheet1', cell_overwrite_ok=True)#创建sheet
	outputFile = os.getcwd() + '/' + 'statistics.xls'

	row0 = [u'目录', u'子目录', u'数量']
	for i in range(0, len(row0)):
		sheet1.write(row, i, row0[i], set_style('Times New Roman',220,True))

	if area is None:
		print("please input area")
		sys.exit()

	row += 1
	if not categoryId:
		# print("please input categoryId")
		# sys.exit()
		workDir = os.getcwd()+'/'+area+'/'
		category = os.listdir(workDir)
		if category is None:
			print("category is empty")
			sys.exit()

		newRow = [row]
		for cId in category:
			topDir = workDir + cId + '/'
			if not os.path.isdir(topDir):
				print("No such directory")
				continue

			collect_product(topDir, newRow, sheet1)
			# row = newRow
			# row += 1
	else:
		topDir = os.getcwd()+'/'+area+'/'+categoryId+'/'
		if not os.path.isdir(topDir):
			print("No such directory")
			sys.exit()

		collect_product(topDir, row, sheet1)

	excel.save(outputFile)
if __name__=="__main__":
	main()
