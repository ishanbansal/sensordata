import httplib2
import urllib

print "POST REQUEST"
content = {'value':'xyz', 'size':'10'}

data = {'node_name': 'default_node', 'sensor_id': 'sensor_post', 'upload_data': content}
body = urllib.urlencode(data)
print body

h = httplib2.Http()
resp, content = h.request("https://thesistest-309000.ts.r.appspot.com/upload?", method="POST", body=body)
print resp, content


print "GET REQUEST"
data = {'node_name': 'default_node', 'data_count': '2'}
body = urllib.urlencode(data)
print body

h = httplib2.Http()
resp, content = h.request("https://thesistest-309000.ts.r.appspot.com/readdata?node_name=default_node&data_count=2&data_only=1", method="GET")
print "OUTPUT\nRESPONSE:", resp, "\nCONTENT:", content
