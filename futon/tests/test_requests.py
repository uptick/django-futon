from django.test import SimpleTestCase, TestCase


class MakeUrlTestCase(SimpleTestCase):

    def test_absolute_path(self):
        pass

    def test_relative_path(self):
        pass

    def test_empty_path(self):
        pass

    def test_empty_site_domain(self):
        pass


class GetTokenTestCase(TestCase):

    def test_uses_existing_token(self):
        pass

    def test_force_skips_existing_token(self):
        pass

    def test_failed_authentication_raises_error(self):
        pass

    def test_old_tokens_are_deleted(self):
        pass

    def test_new_token_inserted(self):
        pass

    def test_valid_authentication(self):
        pass


class AuthoriseTestCase(TestCase):

    def test_valid_authorisation(self):
        pass


class ExecuteTestCase(TestCase):

    def test_returns_json(self):
        pass

    def test_reauthentication(self):
        pass


class FetchTestCase(TestCase):

    def test_fetch(self):
        pass


class CreateTestCase(TestCase):

    def test_create(self):
        pass


class UpdateTestCase(TestCase):

    def test_update(self):
        pass
