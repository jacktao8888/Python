#encoding:utf-8
import scrapy,os,re,json,md5,logging,time
from crawlSites.items import CrawlsitesItem
from bs4 import BeautifulSoup
from scrapy.selector import Selector
import urllib2,urllib
from urllib2 import Request, urlopen, URLError

#解决问题：UnicodeEncodeError: 'ascii' codec can't encode character u'\xa0' in position 775: ordinal not in range(128)
import sys
reload(sys)

sys.setdefaultencoding( "utf-8" )

#此处配置log，文件路径只能为绝对路径，文件名不能有变量。。
#在当前目录创建log
logFile = os.getcwd() + '/tmp'
if not os.path.isdir(logFile):
	os.mkdir(logFile)
logging.basicConfig(
	format = "%(levelname)-s %(asctime)-15s %(message)s", 
	filename=os.getcwd() + '/tmp/info.log',
	level=logging.DEBUG
)

class CfSpider(scrapy.Spider):
	name = "cf"
	allowed_domains = ["xxx.com"]

	start_urls = [
		'https://xxx.com',
	]

	def __init__(self, countryCode='in', categoryId='51', *args, **kwargs):
		super(CfSpider, self).__init__(*args, **kwargs)
		self.countryCode = countryCode
		self.categoryId = categoryId

		self.cookies = {
			'gender':'F', 
			'guest_id':'e8cd0ae3a11c401eab2da485387b9b01',
			'country_code':self.countryCode,
			'experiment_status':'0',
			'_ga':'GA1.2.859894111.1511776748',
			'_gid':'GA1.2.873051111.1511776748'
		}

		#请求头部保持一致，需要带cookie信息！
		self.header = {}
		self.header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
		self.header['cookie'] = "gender=F; guest_id=e8cd0ae3a11c401eab2da485387b9b01; hide-open-app=Y; country_code="+self.countryCode+"; experiment_status=0; _ga=GA1.2.100683743.1512028084; _gid=GA1.2.227887946.1512028084"

		self.ajaxUrl = "https://xxx.com/product_list?&filter=all&limit=50&f=%7B%7D&append_page=1&list_id=0&categoryId=51"

		#跳出循环标志
		self.skipLoop = 0

		self.countryDir = os.getcwd() + '/' + self.countryCode + '/'
		if not os.path.isdir(self.countryDir):
			os.mkdir(self.countryDir)
		# os.chdir(self.countryDir)

	def start_requests(self):
		for start_url in self.start_urls:
			start_url = start_url + self.categoryId
			print(start_url)
			self.skipLoop = 0
			yield scrapy.Request(start_url, cookies=self.cookies)
			
		# if os.path.isfile(os.getcwd() + '/tmp/info.log'):
		# 	os.rename(os.getcwd() + '/tmp/info.log', os.getcwd() + '/tmp/' + str(self.categoryId) + '.log')

	def parse(self, response):
		return self.parse_start(response)

	def parse_start(self, response):
		# conurl = response.url + "&currentPage="
		#主目录提取
		self.firstDir = topDir = str((response.url.split("&")[-1])[11:])

		# print(conurl)
		#使用绝对路径
		self.topDir = self.countryDir + topDir + '/'
		# print(self.topDir)
		if not os.path.isdir(self.topDir):
			os.mkdir(self.topDir)
		# os.chdir(topDir)

		#子目录类型
		subCategoryMap = {}
		categoryRelationship = {}
		categoryList = []
		subCategory = response.xpath('//div[@class="subcateg_block"]/a').extract()
		for item in subCategory:
			sel = Selector(text=item, type="html")
			subCatName = sel.xpath('//a/text()').extract()
			# print(subCatName)	#subCatName为List--[]
			if subCatName[0] == 'All':
				continue

			subCatHref = sel.xpath('//a/@href').extract()
			# print(subCatHref)
			subCategoryMap[subCatName[0]] = subCatHref[0][25:]

			categoryList.append({"category_id":subCatHref[0][25:],"name":subCatName[0],"pId":topDir})
		# print(subCategoryMap)
		categoryRelationship[topDir] = subCategoryMap

		categoryFile = self.topDir + 'categoryRelationship'
		with open(categoryFile, "a+") as f:
			f.write(json.dumps(categoryRelationship)+"\n")
			f.write(json.dumps(categoryList))

		# productIds = []

		# print(self.allowed_domains[0]+"/product/234")

# 		logging.basicConfig(
# 	format = "%(levelname)-s %(asctime)-15s %(message)s", 
# 	filename='/tmp/'+topDir+'.log',
# 	level=logging.DEBUG
# )

		for k,v in subCategoryMap.items():
			#categoryId替换
			subCatReq = self.ajaxUrl[0:-2] + v
			# print(subCatReq)
			self.secondDir = v
			logging.info("[process_start] category:%s,subCategory:%s", self.firstDir, v)
			# yield scrapy.Request(subCatReq, cookies=self.cookies, callback=self.save_subcategory, dont_filter=True)

			req = urllib2.Request(subCatReq, None, self.header)
			
			try:
				response = urllib2.urlopen(req)
			except Exception, e:
				print(e.code)
				print(e.reason)
				logging.error("error code:%s,error reason:%s", e.code, e.reason)
				time.sleep(1)
				try:
					response = urllib2.urlopen(req)
				except Exception, e:
					print(e.code)
					print(e.reason)
					logging.error("error code:%s,error reason:%s", e.code, e.reason)
					time.sleep(1)
					continue
				else:
					self.save_subcategory(response)
			else:
				self.save_subcategory(response) 
			# html = res.read()
			

	def save_subcategory(self, response):
		html = response.read()
		#这里面不能用self.secondDir，只能用response.url提取
		subDir = str(response.url.split("&")[-1])[11:]
		self.subDir = self.countryDir + self.categoryId + '/' + subDir + '/'
		if not os.path.isdir(self.subDir):
			os.mkdir(self.subDir)
		# os.chdir(subDir)

		#处理默认请求页面，即第一页
		# print(response.read())
		productIds = Selector(text=html).xpath('//div[@class="image_region"]/@id').extract()
		# print(type(productIds))
		# print(response.read())
		t0 = time.clock()
		if not productIds:
			# os.chdir("..")
			return
		# print(productIds)
		# print(response.read())
		
		self.save_product(productIds, html)

		pageNum = 1	#初始页1
		while (1):
			tn = time.clock()
			# print("000000")
			# output = "%(levelname)-s %(asctime)-15s %(message)s"+" [process] category:%s,pageNum:%s"
			# print(output)

			#保存子目录中所有商品ID
			productsFile = self.subDir + 'subCategoryProducts'
			with open(productsFile, "a+") as f:
				f.write(json.dumps(productIds))

			logging.info("[process_end] category:%s,subcategory:%s,pageNum:%s", self.firstDir, self.subDir, str(pageNum))
			logging.info("[process_intval] pageNo:%s intval time: %ss", str(pageNum), str(tn - t0))

			# if self.skipLoop == 1:
			# 	break
			
			pageNum += 1
			#调试终止条件
			# if pageNum == 5:
			# 	break
			
			t0 = time.clock()
			# print(response.url+"&currentPage="+str(pageNum))
			# try:
			# 	yield scrapy.Request(response.url+"&currentPage="+str(pageNum), cookies=self.cookies, callback=self.save_product, dont_filter=True)
			# except StopIteration:
			# 	break

			pageUrl = response.url+"&currentPage="+str(pageNum)
			req = urllib2.Request(pageUrl, None, self.header)
			try:
				res = urllib2.urlopen(req) 
			except Exception, e:
				print(e.code)
				print(e.reason)
				logging.error("error code:%s,error reason:%s", e.code, e.reason)
				time.sleep(1)
				try:
					res = urllib2.urlopen(req) 
				except Exception, e:
					print(e.code)
					print(e.reason)
					logging.error("error code:%s,error reason:%s", e.code, e.reason)
					time.sleep(1)
					continue
				else:
					html = res.read()
					productIds = Selector(text=html).xpath('//div[@class="image_region"]/@id').extract()
					# print(type(productIds))
					#页面没有更多产品，即浏览完子目录所有商品了
					if not productIds:
						break
					else:
						self.save_product(productIds, html)
			else:
				html = res.read()
				productIds = Selector(text=html).xpath('//div[@class="image_region"]/@id').extract()
				# print(type(productIds))
				#页面没有更多产品，即浏览完子目录所有商品了
				if not productIds:
					break
				else:
					self.save_product(productIds, html)

		# os.chdir("..")

	def save_product(self, productIds, html):
		# print(html)
		print(productIds)
		for pId in productIds:
			# print(pId)
			logging.info("[process detail] productId:%s", pId)
			#md5序列化取前8bit位，2个0~f字符作为目录
			m1 = md5.new()
			m1.update(pId)
			hashIdDir = m1.hexdigest()[0:2]

			pId = str(pId)

			hashIdDir = self.subDir + '/' + hashIdDir + '/'
			if not os.path.isdir(hashIdDir):
				os.mkdir(hashIdDir)
			# os.chdir(hashIdDir)

			pIdDir = hashIdDir + pId + '/'
			if not os.path.isdir(pIdDir):
				os.mkdir(pIdDir)
				# os.chdir(pId)
			else:
				# os.chdir(pId)
				repeatFile = pIdDir + 'repeat.log'
				with open(repeatFile, "a+") as f:
					f.write("repeat-tag:1")

			#数据是否取到了？
			listItem = Selector(text=html).xpath('//div[@id='+pId+']/..').extract()
			# print(listItem)
			# listItem[] = response.xpath('//div[@id='+pId+']/following-sibling::div[position()=1]').extract()
			# print(listItem)
			listFile = pIdDir + 'list.html'
			with open(listFile, "wb") as f:
				f.write(listItem[0])

			#保存详情页
			detailUrl = "https://" + self.allowed_domains[0]+"/product/"+pId
			# print(detailUrl)
			#cookies是否区分了国家？
			#回调不成功，保存文件的路径变了，回调函数中的detail.html存在/in/51/中
			# request_with_cookies = scrapy.Request(detailUrl, callback=self.download_details, cookies=self.cookies, dont_filter=True)

			req = urllib2.Request(detailUrl, None, self.header)
			
			detailFile = pIdDir + 'detail.html'
			try:
				res = urllib2.urlopen(req)
			except Exception, e:
				print(e)
				# print(e.reason)
				logging.error("error code:%s,error reason:%s", e.code, e.reason)
				time.sleep(1)
				try:
					res = urllib2.urlopen(req)
				except Exception, e:
					print(e)
					# print(e.reason)
					logging.error("error code:%s,error reason:%s", e.code, e.reason)
					time.sleep(1)
					# os.chdir("..")
					# os.chdir("..")
					continue
				else:
					with open(detailFile, "wb") as f:
						f.write(res.read())
					# print(os.curdir)
					#使用绝对路径，不需要跳转
					# os.chdir("..")
					# os.chdir("..")
			else:
				with open(detailFile, "wb") as f:
					f.write(res.read())
				# print(os.curdir)
				# os.chdir("..")
				# os.chdir("..")

		return
			# return {"status":"success"}

	def download_details(self, response):
		# print("download_details???")
		with open("detail.html","wb") as f:
			f.write(response.body)

	def list_items(self, response):
		# print("\nbbbbbbb\n")
		os.mkdir("page1")

		item = CrawlsitesItem()
		# print(response)
		products = response.xpath('//div[@class="oe_product"]').extract()
		# print(products)

	
