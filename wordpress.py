import os
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.methods.taxonomies import GetTerms
from wordpress_xmlrpc.methods.users import GetAuthors

def get_config(key, **kwargs):
    try:
        if 'default' in kwargs:
            return os.environ.get(key, kwargs['default'])
        else:
            return os.environ[key]
    except:
        raise KeyError('Please set the %s environment variable' % key)

class WordPress(object):
    def __init__(self):

        site = get_config('WORDPRESS_SITE')
        user = get_config('WORDPRESS_USER')
        password = get_config('WORDPRESS_PASSWORD')
        default_author = get_config('WORDPRESS_DEFAULT_AUTHOR', default=None)

        self.wp = Client('http://%s/xmlrpc.php' % site, user, password)

        self.authors = {a.display_name:a for a in self.wp.call(GetAuthors())}
        self.default_author = self.get_author(default_author)

        self.categories = [c.name for c in self.wp.call(GetTerms('category'))]

    def separate_tags_and_categories(self, tags):
        terms = {'category':[], 'post_tag':[]}
        for tag in tags:
            where = 'category' if tag in self.categories else 'post_tag'
            terms[where].append(tag)
        return terms

    def create(self, title, content, date, author, tags, publish):
        post = WordPressPost()
        post.title = title
        post.content = content
        post.date = date
        post.terms_names = separate_tags_and_categories(tags)

        user = self.get_author(author, self.default_author)
        if user:
            post.user = user.id
        if publish:
            post.post_status = 'publish'
        return self.wp.call(NewPost(post))

    def get_author(self, name, default=None):
        return self.authors.get(name, default)
