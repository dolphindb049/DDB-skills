import os
import time
from pathlib import Path
from openai import OpenAI
from tqdm import tqdm
import fitz

API_KEY = "sk-MDQLUXvVuVESXdTSPfaH2PJE4uaXdC54YHpiXuKkTmwVxD8J"
BASE_URL = "https://hk.n1n.ai/v1/"
MODEL = "gpt-5-nano"

INPUT_PDF = Path("originfiles") / "The-Complete-Guide-to-Building-Skill-for-Claude.pdf"
OUTPUT_MD = Path("finishfiles") / "The-Complete-Guide-to-Building-Skill-for-Claude.zh.md"

MAX_CHARS_PER_CHUNK = 2600


def split_chunks(text: str, max_chars: int):
    text = text.strip()
    if not text:
        return []
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) + 1 <= max_chars:
            current = f"{current}\n{para}".strip()
        else:
            if current:
                chunks.append(current)
            if len(para) <= max_chars:
                current = para
            else:
                start = 0
                while start < len(para):
                    end = start + max_chars
                    chunks.append(para[start:end])
                    start = end
                current = ""
    if current:
        chunks.append(current)
    return chunks


def translate_chunk(client: OpenAI, text: str) -> str:
    if not text.strip():
        return ""
    last_error = None
    for _ in range(3):
        try:
            rsp = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "你是专业技术编辑。请将输入英文内容准确翻译为中文，保留标题层级、项目符号、术语和代码块，不要额外解释。",
                    },
                    {"role": "user", "content": text},
                ],
                temperature=0.1,
            )
            return (rsp.choices[0].message.content or "").strip()
        except Exception as exc:
            last_error = exc
            time.sleep(1)
    if last_error:
        return text
    return text


def main():
    os.makedirs("finishfiles", exist_ok=True)
    if not INPUT_PDF.exists():
        raise FileNotFoundError(f"Input PDF not found: {INPUT_PDF}")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    doc = fitz.open(str(INPUT_PDF))

    all_sections = []
    for page_idx in tqdm(range(len(doc)), desc="Extract+Translate", unit="page"):
        page = doc[page_idx]
        text = page.get_text("text")
        chunks = split_chunks(text, MAX_CHARS_PER_CHUNK)
        zh_chunks = []
        for chunk in chunks:
            zh_chunks.append(translate_chunk(client, chunk))

        section = [f"## 第 {page_idx + 1} 页", ""]
        if zh_chunks:
            section.append("\n\n".join(zh_chunks))
        else:
            section.append("（本页未提取到可翻译文本）")
        section.append("")
        all_sections.append("\n".join(section))

        OUTPUT_MD.write_text(
            "# The Complete Guide to Building Skill for Claude（中文翻译）\n\n" + "\n".join(all_sections),
            encoding="utf-8",
        )

    print(f"Saved translation to: {OUTPUT_MD}")


if __name__ == "__main__":
    main()
