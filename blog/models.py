from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(_('title'), max_length=100)
    tease = models.CharField(_('tease'), max_length=200)
    text = models.TextField(_('text'), max_length=500)
    slug = models.SlugField(_('slug'))
    publish = models.DateTimeField(_('publish'), default=datetime.datetime.now)
    creator = models.ForeignKey(User)

    def save(self, *args, **kwargs):
        ''' add the slug but only on the first save, to preserver urls '''
        if not self.id:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-publish']