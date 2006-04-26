# Copyright (c) 2002-2004 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""functional tests using the sample configuration file, should behave exactly
as with the default configuration
"""
__revision__ = '$Id: func_test_sample_config.py,v 1.3 2005-04-15 10:40:24 syt Exp $'

from func_test import *

from os.path import join

import pylint
sample_config = join(pylint.__path__[0], 'examples', 'pylintrc')
linter.load_file_configuration(sample_config)

if __name__=='__main__':
    unittest.main(defaultTest='suite')
