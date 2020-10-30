from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

import logging
import webbrowser
import itertools
import string
from redminelib import Redmine

logger = logging.getLogger(__name__)

class RedmineExtension(Extension):

    def __init__(self):
        super(RedmineExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        logger.info(event.get_argument())
        logger.info(extension.preferences['redmine_url'])
        logger.info(extension.preferences['redmine_api_key'])
        redmine = Redmine(extension.preferences['redmine_url'], version='3.0.7', key=extension.preferences['redmine_api_key'])
        query = str(event.get_argument()) or str()
        if len(query) != 0:
            issue = None
            try:
                issue = redmine.issue.get(query)
            except:
                issue = None
            if issue == None:
                issue_list = list(redmine.issue.search(event.get_argument(), limit=15))
                for issue in itertools.islice(issue_list, 15):
                    issue_url = build_issue_url(extension.preferences['redmine_url'], issue)
                    items.append(ExtensionResultItem(icon='images/icon.png',
                                                name= issue.title,
                                                description='',
                                                on_enter=OpenUrlAction(issue_url)))
            else:
                issue_url = build_issue_url(extension.preferences['redmine_url'], issue)
                items.append(ExtensionResultItem(icon='images/icon.png',
                            name= '#' + query + ': ' + issue.subject,
                            description='',
                            on_enter=OpenUrlAction(issue_url)))
        return RenderResultListAction(items)

def build_issue_url(redmine_url, issue):
    issue_url = redmine_url
    if issue_url[-1] != '/':
        issue_url = issue_url + '/'
    issue_url = issue_url + 'issues/' + str(issue.id)
    return issue_url

if __name__ == '__main__':
    RedmineExtension().run()
