from typing import TYPE_CHECKING, Iterator, List, Optional, Union

from docling.chunking import BaseChunk, HybridChunker
from docling_core.types import DoclingDocument

from steps.convert import convert

if TYPE_CHECKING:
    from transformers import AutoTokenizer

chunker = HybridChunker()


def chunk(
    document: Union[DoclingDocument, List[DoclingDocument]],
    tokenizer: Optional["AutoTokenizer"] = None,
    max_tokens: Optional[int] = None,
    merge_peers: bool = True,
    **kwargs,
) -> Iterator[Iterator[BaseChunk]]:
    if isinstance(document, DoclingDocument):
        document = [document]
    for doc in document:
        yield chunker.chunk(
            dl_doc=doc,
            tokenizer=tokenizer,
            max_tokens=max_tokens,
            merge_peers=merge_peers,
            **kwargs,
        )


if __name__ == "__main__":
    for chunk in chunk(convert("https://arxiv.org/pdf/2408.09869")):
        print(chunk)
