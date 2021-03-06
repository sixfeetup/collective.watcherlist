from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from collective.watcherlist.browser import BaseMail
from collective.watcherlist.interfaces import IWatcherList


class NewsItemMail(BaseMail):

    @property
    def subject(self):
        return u'Newsflash: ' + self.context.Title()

    @property
    def html(self):
        return self.context.getRawText()


class InternationalMail(BaseMail):

    @property
    def plain(self):
        # This says: Breaking international news
        return u'Breaking \xefnt\xe9rn\xe4ti\xf3nal news: %s' % (
            self.context.Title())


class SubscriptionForm(BrowserView):

    def __call__(self):
        context = aq_inner(self.context)
        watchers = IWatcherList(context)
        email = self.request.form.get('email')
        if email:
            watchers.watchers.append(email)
        if self.request.form.get('toggle'):
            watchers.toggle_watching()
        # Return the rendered form.
        return self.index()

    def is_watching(self):
        context = aq_inner(self.context)
        watchers = IWatcherList(context)
        return watchers.isWatching()


class SubscriptionOverview(BrowserView):

    def __call__(self):
        context = aq_inner(self.context)
        watchers = IWatcherList(context)
        return '\n'.join(watchers.addresses)
