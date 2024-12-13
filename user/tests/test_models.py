from django.test import TestCase
from django.contrib.auth import get_user_model


def create_user(name="testName", email="user@example.com", password="testpass123"):
    """Create and return a new user."""
    return get_user_model().objects.create_user(name, email, password)


class Model_Tests(TestCase):
    """モデルをテストする"""

    def test_create_user_with_email_successful(self):
        """メールを使用してユーザーを作成して成功したかのテスト"""
        name="testName"
        email = "test@example.com"
        password = "TestPass123"
        user = get_user_model().objects.create_user(name=name,email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """新規ユーザー向けにテストメールが標準化されたかのテスト。"""
        sample_emails_and_username = [
            ["test1@EXAMPLE.com", "test1@example.com", "testUser1"],
            ["Test2@Example.com", "Test2@example.com", "testUser2"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com", "testUser3"],
            ["test4@example.COM", "test4@example.com", "testUser4"],
        ]
        for email, expected, name in sample_emails_and_username:
            user = get_user_model().objects.create_user(
                name=name, email=email, password="sample123"
            )
            self.assertEqual(user.email, expected)

