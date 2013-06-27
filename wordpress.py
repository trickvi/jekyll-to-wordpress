from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

class WordPress(object):
    def __init__(self):
        self.wp = Client('http://ossandbox.wordpress.com/xmlrpc.php',
                         'ossandbox', 'openspending')

    def create(self, title, content, date):
        post = WordPressPost()
        post.title = title
        post.content = content
        post.date = date
        post.post_status = 'publish'

        return self.wp.call(NewPost(post))
