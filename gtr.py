# -*- coding: utf-8 -*-

# For debugging, use this command to start neovim:
#
# NVIM_PYTHON_LOG_FILE=nvim.log NVIM_PYTHON_LOG_LEVEL=INFO nvim
#
#
# Please register source before executing any other code, this allow cm_core to
# read basic information about the source without loading the whole module, and
# modules required by this module
from cm import register_source, getLogger, Base
register_source(name='gtr',
        priority=4,
        scoping=0,
        abbreviation='gtr',
        word_pattern=r'[\w\s]+',
        cm_refresh_patterns=[r'(\.|^)?.*?$\.'])
        # cm_completeopt="menu,menuone,insert,select",

import json
import os
import subprocess
import glob

logger = getLogger(__name__)


class Source(Base):
    def __init__(self, nvim):
        super(Source, self).__init__(nvim)

    def cm_refresh(self, info, ctx, *args):

        base = (ctx['base']).encode('utf-8')
        logger.info("TRANS base: [%s]", base)

        args = ['json_parser', base]

        proc = subprocess.Popen(args=args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        result, errs = proc.communicate(base, timeout=4)

        logger.info("TRANS result: [%s]", result.decode('utf-8'))
        matches = json.loads(result.decode('utf-8'))
        logger.info("TRANS matches: [%s]", matches)

        # startcol = ctx['startcol'] - result[0]
        self.complete(info, ctx, ctx['startcol'], matches)
