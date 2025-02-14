from typing import Dict, Iterator, List, Optional, Union

from docling.document_converter import DocumentConverter
from docling_core.types import DoclingDocument

converter = DocumentConverter()


def convert(
    url_or_path: Union[str, List[str]],
    headers: Optional[Dict[str, str]] = None,
    raises_on_error: bool = False,
) -> Iterator[DoclingDocument]:
    if isinstance(url_or_path, str):
        url_or_path = [url_or_path]
    results = converter.convert_all(
        source=url_or_path,
        headers=headers,
        raises_on_error=raises_on_error,
    )
    for result in results:
        yield result


if __name__ == "__main__":
    for markdown in convert("https://arxiv.org/pdf/2408.09869"):
        print(markdown)
