import urllib2

response = urllib2.urlopen('http://placekitten.com/400/500')

image_html = response.read()

with open('output_image.jpg', 'wb') as f:
    f.write(image_html)
