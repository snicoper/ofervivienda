from .base_accounts import BaseAccountsTest


class AccountSettingsTest(BaseAccountsTest):

    def test_settings(self):
        """Comprueba los valores de accounts.settings."""
        self.assertEqual(self.accounts_settings.ACCOUNTS_AVATAR_WIDTH, 120)
        self.assertEqual(self.accounts_settings.ACCOUNTS_AVATAR_HEIGHT, 120)
        self.assertEqual(self.accounts_settings.ACCOUNTS_AVATAR_PATH, 'accounts/avatar')
        self.assertEqual(self.accounts_settings.ACCOUNTS_AVATAR_DEFAULT, 'anonymous.png')
