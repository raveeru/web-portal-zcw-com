from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    keyword: str
    url: str
    description: str
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def summary(self) -> str:
        return f"[{self.keyword}] {self.url} — {self.description[:50]}..."

    def tag_list(self) -> str:
        return ", ".join(self.tags) if self.tags else "无标签"


@dataclass
class NoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag.lower() in [t.lower() for t in n.tags]]

    def format_all(self) -> str:
        lines = ["=== 关键词笔记列表 ==="]
        for i, note in enumerate(self.notes, 1):
            lines.append(f"{i}. {note.summary()}")
            lines.append(f"   标签: {note.tag_list()}")
            lines.append(f"   时间: {note.created_at}")
        return "\n".join(lines)

    def format_markdown(self) -> str:
        lines = ["# 关键词笔记\n"]
        for note in self.notes:
            lines.append(f"## {note.keyword}")
            lines.append(f"- **URL**: [{note.url}]({note.url})")
            lines.append(f"- **描述**: {note.description}")
            lines.append(f"- **标签**: {note.tag_list()}")
            lines.append(f"- **创建时间**: {note.created_at}")
            lines.append("")
        return "\n".join(lines)


def demo_usage():
    sample_url = "https://web-portal-zcw.com"
    sample_keyword = "足彩网"

    note1 = KeywordNote(
        keyword="足彩网",
        url=sample_url,
        description="一个专业的足球彩票信息门户网站",
        tags=["足球", "彩票", "体育"],
    )
    note2 = KeywordNote(
        keyword="足球资讯",
        url="https://web-portal-zcw.com/news",
        description="最新足球比赛新闻和赛事分析",
        tags=["足球", "新闻"],
    )
    note3 = KeywordNote(
        keyword="彩票分析",
        url="https://web-portal-zcw.com/analysis",
        description="提供专业足彩数据分析和预测",
        tags=["彩票", "数据分析"],
    )

    collection = NoteCollection()
    collection.add(note1)
    collection.add(note2)
    collection.add(note3)

    print(collection.format_all())
    print("\n")
    print(collection.format_markdown())

    print("--- 搜索 '足彩网' ---")
    results = collection.find_by_keyword(sample_keyword)
    for r in results:
        print(r.summary())

    print("\n--- 搜索标签 '足球' ---")
    tagged = collection.find_by_tag("足球")
    for r in tagged:
        print(r.summary())


if __name__ == "__main__":
    demo_usage()