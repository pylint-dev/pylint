# pyenchant
#
# Copyright (C) 2022, Nico Gulden, Univention GmbH
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
#
# In addition, as a special exception, you are
# given permission to link the code of this program with
# non-LGPL Spelling Provider libraries (eg: a MSFT Office
# spell checker backend) and distribute linked combinations including
# the two.  You must obey the GNU Lesser General Public License in all
# respects for all of the code used other than said providers.  If you modify
# this file, you may extend this exception to your version of the
# file, but you are not obligated to do so.  If you do not wish to
# do so, delete this exception statement from your version.
#
"""

enchant.tokenize.de:    Tokenizer for the German language

This module implements a PyEnchant text tokenizer for the German
language, based on very simple rules.

"""


from typing import Container, Optional

from enchant.tokenize.en import tokenize as tokenizer_en

from .en import _TextLike


class tokenize(tokenizer_en):  # noqa: N801
    def __init__(
        self, text: _TextLike, valid_chars: Optional[Container[str]] = ("-", ".")
    ) -> None:
        super().__init__(text, valid_chars)
