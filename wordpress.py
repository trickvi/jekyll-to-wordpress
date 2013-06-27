from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

class WordPress(object):
    def __init__(self):
        self.wp = Client('http://thesite/xmlrpc.php',
                         'theusername', 'thepassword')

    def create(self, title, content, date):
        post = WordPressPost()
        post.title = title
        post.content = content
        post.post_date = date.strftime('%Y-%m-%d %H:%M:%S')
        post.post_status = 'publish'

        return self.wp.call(NewPost(post))
