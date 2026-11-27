"""Exercise the documented HotCRP export and the generated journal site."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class JournalPublishing(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.work = Path(scratch.name)
        self.site = self.work / "site"
        shutil.copytree(ROOT / "journalSite", self.site,
                        ignore=shutil.ignore_patterns("public", "resources", "private_data", ".hugo_build.lock"))
        config = self.site / "hugo.toml"
        config.write_text(config.read_text().replace(" -> ../..", f" -> {ROOT}"))

    def build(self, name, *flags):
        output = self.work / name
        subprocess.run(["hugo", "--panicOnWarning", "--baseURL", "https://example.org/journal/",
                        "--destination", str(output), *flags], cwd=self.site, check=True,
                       stdout=subprocess.DEVNULL)
        return output

    def test_clean_production_and_draft_preview(self):
        sample = "issues/sample/1/index.html"
        preview = self.build("preview", "-D")
        self.assertTrue((preview / sample).exists())
        self.assertIn('id="paper-1"', (preview / "issues/sample/index.html").read_text())
        live = self.build("live")
        self.assertFalse((live / "issues/sample").exists())
        self.assertIn("first issue", (live / "index.html").read_text())
        self.assertNotIn("Open HotCRP", (live / "authors/index.html").read_text())
        for file in ["index.xml", "llms.txt", "llms-full.txt", "sitemap.xml"]:
            self.assertNotIn("/sample/", (live / file).read_text())

    def test_publish_hotcrp_issue(self):
        raw = self.work / "export.json"
        raw.write_text(json.dumps([
            {"pid": 1, "title": "Pipes & paths", "decision": "Accept", "abstract": "A public abstract.",
             "authors": [{"first": "A.", "last": "Example", "affiliation": "Example Lab",
                          "email": "private@example.org"}], "reviews": ["private-review"],
             "arxiv_number_url": "2401.12345"},
            {"pid": 2, "title": "withheld-paper", "decision": "Reject"},
        ]))
        data = self.site / "data"
        subprocess.run([sys.executable, str(ROOT / "scripts/sanitize_hotcrp_json.py"), str(raw),
                        "--decision", "^Accept$", "-o", str(data / "accepted-papers-vol1.json")], check=True)
        (data / "issues.yaml").write_text(
            "- key: vol1\n  title: Volume One\n  date: '2025-04-01'\n"
            "- key: sample\n  title: Other issue\n")
        (data / "proceedings-vol1.yml").write_text('"1": "10.1234/example"\n')
        pdf = self.site / "assets/articles/vol1/1.pdf"
        pdf.parent.mkdir(parents=True)
        pdf.write_bytes(b"fixture PDF")
        config = self.site / "hugo.toml"
        config.write_text(config.read_text().replace("# hotcrpURL", "hotcrpURL"))
        live = self.build("live")
        home = (live / "index.html").read_text()
        self.assertIn('href="/journal/issues/vol1/1/"', home)
        self.assertNotIn("Documenting a civic", home)
        self.assertIn('href="https://your-submission-server.example/"', home)
        article = (live / "issues/vol1/1/index.html").read_text()
        for expected in ["A. Example", "Example Lab", "A public abstract.", "ScholarlyArticle",
                         'href="/journal/articles/vol1/1.pdf"', "https://doi.org/10.1234/example",
                         "https://arxiv.org/abs/2401.12345"]:
            self.assertIn(expected, article)
        self.assertEqual(pdf.read_bytes(), (live / "articles/vol1/1.pdf").read_bytes())
        records = json.loads((live / "issues/vol1/papers.json").read_text())["articles"]
        self.assertEqual([r["title"] for r in records], ["Pipes & paths"])
        self.assertTrue((live / "issues/sample/1/index.html").exists())
        feed = ET.parse(live / "index.xml").findall("channel/item")
        self.assertEqual([item.findtext("title") for item in feed],
                         ["Pipes & paths", "Documenting a civic software project"])
        self.assertEqual(feed[0].findtext("description"), "A public abstract.")
        self.assertIsNone(feed[1].find("pubDate"))
        self.assertIn("A public abstract.", (live / "llms-full.txt").read_text())
        for path in live.rglob("*"):
            if path.suffix in {".html", ".json", ".txt", ".xml"}:
                for private in ["private@example.org", "private-review", "withheld-paper"]:
                    self.assertNotIn(private, path.read_text(), str(path))
