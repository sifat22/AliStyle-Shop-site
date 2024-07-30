from django.apps import AppConfig


class AppAdminAccountConfig(AppConfig):
    name = 'app_admin_account'

    def ready(self):
        import app_admin_account.signals
