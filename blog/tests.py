from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from blog.models import Post
from django.core.urlresolvers import reverse
import logging
logger = logging.getLogger(__name__)

def create_post(create=True):
    args = {}
    args["creator"] = User.objects.get(username="bob")
    args["title"] = "onion"
    args["tease"] = "yep onions"
    args["text"] = "now I need chewing gum"
    post = Post(**args)
    if create:
        post.save()
    return post


def get_post_args():
    return {
            "title": "some title",
            "tease": "some tease",
            "text": "some description"
        }


def post_update(username):
    post = create_post()
    c = Client()
    c.login(username=username, password="secret")
    url = reverse("blog_update", kwargs={"slug": post.slug})
    return c.post(url, get_post_args())


def post_delete(username):
    post = create_post()
    c = Client()
    c.login(username=username, password="secret")
    url = reverse("blog_delete", kwargs={"slug": post.slug})
    return c.delete(url)


class BlogFunctionalityTest(TestCase):
    def setUp(self):
        User.objects.create_user('bob', 'bob@thebuilder.com', 'secret')
        User.objects.create_user('dave', 'dave@youknowdave.com', 'secret')
        User.objects.create_superuser('fred', 'fred@fred.com', 'secret')


    def test_create_for_user(self):
        c = Client()
        args = get_post_args()
        User.objects.get(username="bob")

        c.login(username="bob", password="secret")
        c.post("/add/", args)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.all()[0]
        for k, v in args.iteritems():
            self.assertEqual(getattr(post, k), v)

    def test_update_for_non_permissioned_user(self):
        response = post_update("dave")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Post.objects.count(), 1)
        original_post = create_post(create=False)
        changed_post = Post.objects.all()[0]
        for i in ["title", "tease", "text"]:
            self.assertEqual(getattr(original_post, i), getattr(changed_post, i))

    def test_update_for_permissioned_user(self):
        response = post_update("bob")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)
        changed_post = Post.objects.all()[0]
        args = get_post_args()

        for k, v in args.iteritems():
            self.assertEqual(v, getattr(changed_post, k))

    def test_update_for_super_user(self):
        response = post_update("fred")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)
        changed_post = Post.objects.all()[0]
        args = get_post_args()

        for k, v in args.iteritems():
            self.assertEqual(v, getattr(changed_post, k))


    def test_delete_for_non_permissioned_user(self):
        response = post_delete("dave")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Post.objects.all().count(), 1)

    def test_delete_for_permissioned_user(self):
        response = post_delete("bob")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.all().count(), 0)

    def test_delete_for_super_user(self):
        response = post_delete("fred")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.all().count(), 0)

