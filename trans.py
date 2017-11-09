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
register_source(name='trans',
        priority=2,
        scoping=0,
        abbreviation='trans',
        word_pattern=r'[\w/]+',
        cm_refresh_patterns=[r'\.$'],)

import json
import os
import subprocess
import glob

logger = getLogger(__name__)


class Source(Base):

    def __init__(self, nvim):
        super(Source, self).__init__(nvim)

        '''
        # dependency check
        try:
            from distutils.spawn import find_executable
            if not find_executable("trans"):
                self.message('error', 'Can not find trans for completion, you need trans(1)')
        except Exception as ex:
            logger.exception(ex)
        '''

    def cm_refresh(self, info, ctx, *args):

        '''
        lnum = ctx['lnum']
        col = ctx['col']
        filepath = ctx['filepath']
        startcol = ctx['startcol']

        if (len(ctx['base']) < 1):
            logger.info("TRANS base: [%s]", ctx['base'])
            logger.info("TRANS bailout")
            return 0
        '''
        base = (ctx['base']).encode('utf-8')
        logger.debug("TRANS ctx['base']: [%s]", ctx['base'])
        logger.debug("TRANS len(base): [%d]", len(base))

        args = ['/home/tl/.local/bin/json_parser', ctx['base']]

        proc = subprocess.Popen(args=args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        result, errs = proc.communicate(base, timeout=4)

        logger.debug("TRANS args: [%s]", args)
        # logger.debug("TRANS errs: [%s]", errs.decode('utf-8'))
        # logger.info("args: %s, result: [%s]", args, result.decode())
        logger.info("TRANS result: [%s]", result.decode('utf-8'))


        logger.info("TRANS RESULTS: [%s]", result)
        matches = json.loads(result.decode('utf-8'))
        logger.info("TRANS matches: [%s]", matches)

        self.complete(info, ctx, ctx['startcol'], matches)
