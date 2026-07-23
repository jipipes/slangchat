import unittest

from fastapi.testclient import TestClient

from slangchat.api.app import app


class DetectEndpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_detects_known_slang(self) -> None:
        response = self.client.post("/detect", json={"text": "That explanation is SUS!"})

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["text"], "That explanation is SUS!")
        self.assertEqual([m["term"] for m in body["matches"]], ["sus"])

    def test_returns_empty_matches_for_plain_text(self) -> None:
        response = self.client.post("/detect", json={"text": "그냥 평범한 문장입니다"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["matches"], [])

    def test_rejects_empty_text(self) -> None:
        response = self.client.post("/detect", json={"text": ""})

        self.assertEqual(response.status_code, 422)

    def test_rejects_missing_text_field(self) -> None:
        response = self.client.post("/detect", json={})

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()