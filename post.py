from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from secrets import WP_USER, WP_PW

url = 'http://www.marsfromspace.com/xmlrpc.php'
WP = Client(url, WP_USER, WP_PW)

def post_to_wordpress(title, content, more_info_url, local_img_file):

    # first upload the image
    data = {
        'name': local_img_file.split('/')[-1],
        'type': 'image/jpg',  # mimetype
    }

    # read the binary file and let the XMLRPC library encode it into base64
    with open(local_img_file, 'rb') as img:
        data['bits'] = xmlrpc_client.Binary(img.read())
    response = WP.call(media.UploadFile(data))
    attachment_id = response['id']

    # now post the post and the image
    post = WordPressPost()
    post.post_type = 'portfolio'  # stupid effing theme
    post.title = title
    post.content = content
    post.post_status = 'publish'
    post.thumbnail = attachment_id

    WP.call(NewPost(post))
