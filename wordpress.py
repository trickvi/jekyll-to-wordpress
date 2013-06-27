from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.methods.users import GetAuthors

class WordPress(object):
    def __init__(self, site='thesite.wordpress.com', user='theuser',
                 password='thepassword', default_author='Joe Bloggs'):
        self.wp = Client('http://%s/xmlrpc.php' % site, user, password)
        self.default_author = default_author
        self.authors = {a.display_name:a for a in self.wp.call(GetAuthors())}

    def create(self, title, content, date):
        post = WordPressPost()
        post.title = title
        post.content = content
        post.date = date
        post.post_status = 'publish'

        return self.wp.call(NewPost(post))

    def get_author_id(self, name):
        return self.authors.get(name, self.authors[self.default_author])
