import math
from django.db import models
from django.utils.text import Truncator
from django.conf import settings
from django.utils.html import mark_safe
from markdown import markdown
from accounts.models import Account
import uuid
from django.contrib.humanize.templatetags import humanize

def generate_ticket_id():
    # generate unique ticket id
    return str(uuid.uuid4()).split("-")[-1]

status = (
    ("Open", "open"),
    ("PROGRESS", "progress"),
    ("PENDING", "pending"),
    ("CLOSED", "closed"),
)

class Ticket(models.Model):
    subject = models.CharField(max_length=255)
    description = models.TextField(max_length=4000)
    last_updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='tickets')
    objects = models.Manager()
    status = models.CharField(choices=status, max_length=155, default="open")
    ticket_id = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = 'Tickets'
        ordering = ('-last_updated', )

    def __str__(self):
        return "{} - {}".format(self.subject, self.ticket_id)

    def get_last_ten_posts(self):
        return self.replies.order_by('-created_at')[:10]

    def get_replies_count(self):
        return self.replies.count()

    def get_page_count(self):
        count = self.replies.count()
        pages = count / 10
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 5

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_date(self):
        return humanize.naturaltime(self.created)

    def save(self, *args, **kwargs):
        if len(self.ticket_id.strip(" ")) == 0:
            self.ticket_id = generate_ticket_id()

        super(Ticket, self).save(*args, **kwargs)


class Reply(models.Model):
    content = models.TextField(max_length=4000)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE,
                               related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE,
                                   related_name='replies')
    updated_by = models.ForeignKey(Account, on_delete=models.CASCADE, null=True,
                                   related_name='+')
    objects = models.Manager()

    def __str__(self):
        content = Truncator(self.content)
        return content.chars(30)

    def get_content_as_markdown(self):
        return mark_safe(markdown(self.content, safe_mode='escape'))

    def get_date(self):
        return humanize.naturaltime(self.created_at)


