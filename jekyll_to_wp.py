# -*- coding: utf-8 -*-
import os

import markdown
import yaml
import datetime
from wordpress import WordPress


class jekyll_to_wp():
    def __init__(self):
        wp = WordPress()
        blogs = self.parse_blogs()
        for blog in blogs:
            print "Creating:", blog['front_matter']['title'], '...',
            blog_id = wp.create(blog['front_matter']['title'],
                                blog['html'],
                                blog['date'])
            print 'done (%s)' % blog_id

    # parse all blogs in a given directory
    def parse_blogs(self, directory="_posts"):
        blogs = []
        blog_fullpaths = ['%s/%s' % (directory, blog_filename) for blog_filename in os.listdir(directory)]
        for blog_fullpath in blog_fullpaths:
            blog = self.parse_blog(blog_fullpath)
            if blog is not False:
                blogs.append(blog)
        return blogs

    # parse the specified blog file
    def parse_blog(self, blog_fullpath):
        # get the creation date
        date = datetime.datetime.strptime(os.path.basename(blog_fullpath)[:10],
                                                           '%Y-%m-%d')

        # fetch the file into memory
        with open(blog_fullpath) as blogfile:
            lines = blogfile.readlines()

        # find the bounds of the front matter
        front_matter_bounds = [ind for ind in range(len(lines)) if lines[ind].startswith('---')]
        if len(front_matter_bounds) < 2:
            # sanity check - front matter isn't properly formatted
            return False
        front_matter_raw = ''.join(lines[front_matter_bounds[0]+1:front_matter_bounds[1]])
        markdown_raw = ''.join(lines[front_matter_bounds[1]+1:]).decode('utf8')

        # parse front matter yaml
        front_matter = yaml.load(front_matter_raw)

        # parse blog markdown
        m = markdown.Markdown()
        html = m.convert(markdown_raw)

        return {"front_matter": front_matter, "html": html, "date":date}

jekyll_to_wp()
