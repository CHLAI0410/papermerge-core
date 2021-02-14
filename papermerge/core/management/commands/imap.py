import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from papermerge.core.importers.imap import import_attachment
from papermerge.core.importers.imap import login as imap_login


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """Helper command to troubleshoot IMAP account.

    It can:

        * check if Papermerge is able to connect to IMAP account
        * count number of UNSEEN email messages
        * fetch/import documents from IMAP account
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            '--connect',
            action='store_true',
            help="Check if can connect to IMAP account"
        )
        parser.add_argument(
            '--count',
            action='store_true',
            help="Counts total number of UNSEED email messages"
        )
        parser.add_argument(
            '--import',
            action='store_true',
            help="Imports documents from email attachments. "
            "Does not run in a loop i.e. imports currently 'UNSEED'"
            " messages and quit."
        )

    def handle(self, *args, **options):

        connect_action = options.get('connect', False)
        count_action = options.get('count', False)
        import_action = options.get('import', False)

        # options used across all actions (i.e. connect, count, import)
        self._imap_server = settings.PAPERMERGE_IMPORT_MAIL_HOST
        self._username = settings.PAPERMERGE_IMPORT_MAIL_USER
        self._password = settings.PAPERMERGE_IMPORT_MAIL_PASS
        self._delete = settings.PAPERMERGE_IMPORT_MAIL_DELETE
        self._by_user = settings.PAPERMERGE_IMPORT_MAIL_BY_USER
        self._by_secret = settings.PAPERMERGE_IMPORT_MAIL_BY_SECRET
        self._inbox_name = settings.PAPERMERGE_IMPORT_MAIL_INBOX

        if connect_action:
            self._connect_action()
        elif count_action:
            self._count_action()
        elif import_action:
            self._import_action()

    def _connect_action(self):
        server = imap_login(
            imap_server=self._imap_server,
            username=self._username,
            password=self._password,
        )
        if server:
            print("Connection to IMAP server: OK")
        else:
            print("Connection to IMAP server: FAIL")

    def _count_action(self):
        pass

    def _import_action(self):

        if self._all_credentials_provided():
            import_attachment(
                imap_server=self._imap_server,
                username=self._username,
                password=self._password,
                delete=self._delete,
                inbox_name=self._inbox_name,
                by_user=self._by_user,
                by_secret=self._by_secret
            )
        else:
            print("Not all credentials are provided.")

    def _all_credentials_provided(self):
        """
        Returns True only if all IMAP host, username and password
        are non-empty.
        Returns False if at least one of imap host, username or password
        is empty.
        """

        if not self._imap_server:
            print("IMPORT_MAIL_HOST is empty.")
            return False

        if not self._username:
            print("IMPORT_MAIL_USER is empty.")
            return False

        if not self._password:
            print("IMPORT_MAIL_PASS is empty.")
            return False

        return True