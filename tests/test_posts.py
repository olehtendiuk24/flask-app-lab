import unittest
from datetime import datetime
from app import create_app, db
from app.posts.models import Post


class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_post(self):
        with self.app.app_context():
            response = self.client.post(
                "/post/create",
                data={
                    "title": "My first post",
                    "content": "This is TDD content!",
                    "is_active": "y",
                    "publish_date": "2026-11-24T20:00",
                    "category": "tech"
                },
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Post &#39;My first post&#39; added successfully!", response.data)

            post = db.session.scalar(db.select(Post).where(Post.title == "My first post"))
            self.assertIsNotNone(post)
            self.assertEqual(post.content, "This is TDD content!")

    def test_list_posts(self):
        with self.app.app_context():
            p = Post(title="Visible Post", content="Some content", category="news", is_active=True)
            db.session.add(p)
            db.session.commit()

            response = self.client.get("/post/")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Visible Post", response.data)

    def test_view_post_detail(self):
        with self.app.app_context():
            p = Post(title="Detail Title", content="Full detailed text", category="publication")
            db.session.add(p)
            db.session.commit()
            post_id = p.id

            response = self.client.get(f"/post/{post_id}")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Detail Title", response.data)
            self.assertIn(b"Full detailed text", response.data)

    def test_update_post(self):
        with self.app.app_context():
            p = Post(title="Old Title", content="Old text", category="other")
            db.session.add(p)
            db.session.commit()
            post_id = p.id

            response = self.client.post(
                f"/post/{post_id}/update",
                data={
                    "title": "Updated Title",
                    "content": "Updated text",
                    "is_active": "y",
                    "publish_date": "2026-11-24T21:00",
                    "category": "tech"
                },
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Updated Title", response.data)

    def test_delete_post(self):
        with self.app.app_context():
            p = Post(title="Post To Delete", content="Delete me", category="news")
            db.session.add(p)
            db.session.commit()
            post_id = p.id

            response = self.client.post(f"/post/{post_id}/delete", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            deleted = db.session.get(Post, post_id)
            self.assertIsNone(deleted)

    def test_404_not_found(self):
        response = self.client.get("/post/9999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()