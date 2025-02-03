# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

import subprocess
import sys
from contextlib import suppress

from resolve_march_native._gcc.parser import extract_flags
from resolve_march_native._gcc.runner import run
from resolve_march_native._gcc.target_help_parser import \
    get_flags_implied_by_march
from resolve_march_native.messenger import announce_flags


class NoTunePresentError(Exception):
    pass


class Engine:
    def __init__(self, gcc_command, debug):
        self._gcc_command = gcc_command
        self._debug = debug

    @staticmethod
    def _extract_arch_from_flags(flags):
        for prefix in ('-march=', '-mcpu='):
            for flag in flags:
                if flag.startswith(prefix):
                    arch = flag[len(prefix):]
                    if arch:
                        return arch
        raise ValueError('No entry -m(arch|cpu)=.. found in: %s' %
                         ' '.join(sorted(flags)))

    @staticmethod
    def _extract_tune_from_flags(flags):
        prefix = '-mtune='
        for flag in flags:
            if flag.startswith(prefix):
                return (flag, flag[len(prefix):])
        raise NoTunePresentError(
            'No entry -mtune=.. found in: %s' % ' '.join(sorted(flags)))

    def _resolve_mtune(self, flag_set, arch):
        try:
            flag, tune = self._extract_tune_from_flags(flag_set)
            if tune == arch:
                flag_set.remove(flag)
        except NoTunePresentError:
            pass

    @staticmethod
    def _resolve_mno_flags(flag_set):
        for flag in list(flag_set):
            if flag.startswith('-mno-'):
                flag_set.remove(flag)

    def _get_march_native_flag_set(self):
        try:
            output = run(self._gcc_command, ['-march=native'], self._debug)
        except subprocess.CalledProcessError:
            output = run(self._gcc_command, ['-mcpu=native'], self._debug)
        march_native_flag_set = set(extract_flags(output))
        if self._debug:
            announce_flags(march_native_flag_set)
        march_native_flag_set |= set(get_flags_implied_by_march('native', gcc=self._gcc_command,
                                                                debug=self._debug))
        if self._debug:
            announce_flags(march_native_flag_set)
        return march_native_flag_set

    def _get_march_explicit_flag_set(self, arch):
        try:
            output = run(self._gcc_command, ['-march=%s' % arch], self._debug)
        except subprocess.CalledProcessError:
            output = run(self._gcc_command, ['-mcpu=%s' % arch], self._debug)
        march_explicit_flag_set = set(extract_flags(output))
        if self._debug:
            announce_flags(march_explicit_flag_set)
        march_explicit_flag_set |= set(get_flags_implied_by_march(arch, gcc=self._gcc_command,
                                                                  debug=self._debug))
        if self._debug:
            announce_flags(march_explicit_flag_set)
        return march_explicit_flag_set

    def _process_flags_explicit_has_more(self, target_set,
                                         march_native_flag_set,
                                         march_explicit_flag_set):
        PREFIX_NO = '-mno-'
        PREFIX_YES = '-m'
        PREFIX_MTUNE = '-mtune='

        explicit_more_flag_set = march_explicit_flag_set - march_native_flag_set
        for flag in explicit_more_flag_set:
            if not flag.startswith('-m'):
                print('Unsure what to do about flag %s, please report this as a bug.' %
                      flag, file=sys.stderr)
                continue

            if not flag.startswith(PREFIX_NO) and flag.startswith(PREFIX_YES) \
                    and not flag.startswith(PREFIX_MTUNE) and '=' not in flag:
                # march=<explicit> enabled something (too much) that march=native disabled
                opposite_flag = PREFIX_NO + flag[len(PREFIX_YES):]
                target_set.add(opposite_flag)

    def _resolve(self, march_native_flag_set, march_explicit_flag_set, arch, options,
                 march_wanted):
        if options.keep_identical_mtune:
            # NOTE: Set ``march_explicit_flag_set`` will be subtracted below and it may contain
            #       ``-mtune={arch}``.  So by removing mtune from the remove list, it survives.
            self._resolve_mtune(march_explicit_flag_set, arch)

        native_unrolled_flag_set = march_native_flag_set - march_explicit_flag_set
        if march_wanted:
            native_unrolled_flag_set.add('-march=%s' % arch)
        else:
            native_unrolled_flag_set.add('-mcpu=%s' % arch)

        if not options.keep_identical_mtune:
            self._resolve_mtune(native_unrolled_flag_set, arch)
        if not options.keep_mno_flags:
            self._resolve_mno_flags(native_unrolled_flag_set)

        # NOTE: The next step needs to go after resolution of -mno-* flags
        #       since it may add new -mno-* flags
        self._process_flags_explicit_has_more(native_unrolled_flag_set,
                                              march_native_flag_set, march_explicit_flag_set)

        # Workaround issues with tribool for machines with e.g. SSE4.1 but not SSE4.2
        for flag_prefix in ('-m', '-mno-'):
            with suppress(KeyError):
                native_unrolled_flag_set.remove(f"{flag_prefix}sse4")

        return native_unrolled_flag_set

    def run(self, options):
        march_native_flag_set = self._get_march_native_flag_set()
        march_wanted = ('-march=' in repr(march_native_flag_set)
                        and '-march=' not in march_native_flag_set)
        arch = self._extract_arch_from_flags(march_native_flag_set)
        march_explicit_flag_set = self._get_march_explicit_flag_set(
            arch)

        return self._resolve(march_native_flag_set, march_explicit_flag_set, arch, options,
                             march_wanted)
