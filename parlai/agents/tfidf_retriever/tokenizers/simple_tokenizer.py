#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""
Basic tokenizer that splits text into alpha-numeric tokens and non-whitespace tokens.
"""

import regex
from .tokenizer import Tokens, Tokenizer
from parlai.utils.logging import logger


class SimpleTokenizer(Tokenizer):
    ALPHA_NUM = r'[\p{L}\p{N}\p{M}]+'
    NON_WS = r'[^\p{Z}\p{C}]'

    def __init__(self, **kwargs):
        """
        Args:
            annotators: None or empty set (only tokenizes).
        """
        self._regexp = regex.compile(
            f'({self.ALPHA_NUM})|({self.NON_WS})',
            flags=regex.IGNORECASE + regex.UNICODE + regex.MULTILINE,
        )
        if len(kwargs.get('annotators', {})) > 0:
            logger.warning(
                f"{type(self).__name__} only tokenizes! Skipping annotators: {kwargs.get('annotators')}"
            )
        self.annotators = set()

    def tokenize(self, text):
        data = []
        matches = list(self._regexp.finditer(text))
        for i in range(len(matches)):
            # Get text
            token = matches[i].group()

            # Get whitespace
            span = matches[i].span()
            start_ws = span[0]
            end_ws = matches[i + 1].span()[0] if i + 1 < len(matches) else span[1]
            # Format data
            data.append((token, text[start_ws:end_ws], span))
        return Tokens(data, self.annotators)
