# Copyright (C) 2022 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

from importlib.resources import files
from unittest import TestCase
from unittest.mock import patch

from resolve_march_native._gcc.target_help_parser import (
    _parse_gcc_output, get_flags_implied_by_march)


class GetFlagsImpliedByMarchTest(TestCase):
    def test(self):
        stdout_mock_filename = (files('resolve_march_native._gcc.test')
                                / 'data' /
                                'sandybridge--11-3-0-gentoo--target-help.txt')
        with open(stdout_mock_filename, 'rb') as f:
            stdout_mock_bytes = f.read()
        expected_flags = [
            '-m128bit-long-double',
            '-mno-16',
            '-mno-32',
            '-mno-3dnow',
            '-mno-3dnowa',
            '-m64',
            '-m80387',
            '-mno-8bit-idiv',
            '-mno-96bit-long-double',
            '-mabi=sysv',
            '-mno-abm',
            '-mno-accumulate-outgoing-args',
            '-maddress-mode=long',
            '-mno-adx',
            '-mno-aes',
            '-malign-data=compat',
            '-mno-align-double',
            '-malign-functions=0',
            '-malign-jumps=0',
            '-malign-loops=0',
            '-malign-stringops',
            '-mno-amx-bf16',
            '-mno-amx-int8',
            '-mno-amx-tile',
            '-mno-android',
            '-march=sandybridge',
            '-masm=att',
            '-mavx',
            '-mno-avx2',
            '-mavx256-split-unaligned-load',
            '-mavx256-split-unaligned-store',
            '-mno-avx5124fmaps',
            '-mno-avx5124vnniw',
            '-mno-avx512bf16',
            '-mno-avx512bitalg',
            '-mno-avx512bw',
            '-mno-avx512cd',
            '-mno-avx512dq',
            '-mno-avx512er',
            '-mno-avx512f',
            '-mno-avx512ifma',
            '-mno-avx512pf',
            '-mno-avx512vbmi',
            '-mno-avx512vbmi2',
            '-mno-avx512vl',
            '-mno-avx512vnni',
            '-mno-avx512vp2intersect',
            '-mno-avx512vpopcntdq',
            '-mno-avxvnni',
            '-mno-bionic',
            '-mno-bmi',
            '-mno-bmi2',
            '-mbranch-cost=3',
            '-mno-call-ms2sysv-xlogues',
            '-mno-cet-switch',
            '-mno-cld',
            '-mno-cldemote',
            '-mno-clflushopt',
            '-mno-clwb',
            '-mno-clzero',
            '-mcpu=',
            '-mcrc32',
            '-mcx16',
            '-mno-dispatch-scheduler',
            '-mno-dump-tune-features',
            '-mno-enqcmd',
            '-mno-f16c',
            '-mfancy-math-387',
            '-mno-fentry',
            '-mfentry-name=',
            '-mfentry-section=',
            '-mno-fma',
            '-mno-fma4',
            '-mno-force-drap',
            '-mno-force-indirect-call',
            '-mfp-ret-in-387',
            '-mfpmath=sse',
            '-mno-fsgsbase',
            '-mfunction-return=keep',
            '-mfxsr',
            '-mno-general-regs-only',
            '-mno-gfni',
            '-mglibc',
            '-mhard-float',
            '-mharden-sls=none',
            '-mno-hle',
            '-mno-hreset',
            '-mno-iamcu',
            '-mieee-fp',
            '-mincoming-stack-boundary=0',
            '-mno-indirect-branch-cs-prefix',
            '-mno-indirect-branch-register',
            '-mindirect-branch=keep',
            '-mno-inline-all-stringops',
            '-mno-inline-stringops-dynamically',
            '-minstrument-return=none',
            '-mno-kl',
            '-mlarge-data-threshold=65536',
            '-mno-long-double-128',
            '-mno-long-double-64',
            '-mlong-double-80',
            '-mno-lwp',
            '-mno-lzcnt',
            '-mno-manual-endbr',
            '-mmemcpy-strategy=',
            '-mmemset-strategy=',
            '-mno-mitigate-rop',
            '-mmmx',
            '-mno-movbe',
            '-mno-movdir64b',
            '-mno-movdiri',
            '-mno-mpx',
            '-mno-ms-bitfields',
            '-mno-musl',
            '-mmwait',
            '-mno-mwaitx',
            '-mno-needed',
            '-malign-stringops',
            '-mdefault',
            '-mfancy-math-387',
            '-mpush-args',
            '-mred-zone',
            '-msse4',
            '-mno-nop-mcount',
            '-mno-omit-leaf-frame-pointer',
            '-mno-pc32',
            '-mno-pc64',
            '-mno-pc80',
            '-mpclmul',
            '-mno-pcommit',
            '-mno-pconfig',
            '-mno-pku',
            '-mpopcnt',
            '-mprefer-vector-width=none',
            '-mpreferred-stack-boundary=0',
            '-mno-prefetchwt1',
            '-mno-prfchw',
            '-mno-ptwrite',
            '-mpush-args',
            '-mno-rdpid',
            '-mno-rdrnd',
            '-mno-rdseed',
            '-mno-recip',
            '-mrecip=',
            '-mno-record-mcount',
            '-mno-record-return',
            '-mred-zone',
            '-mregparm=6',
            '-mno-rtd',
            '-mno-rtm',
            '-msahf',
            '-mno-serialize',
            '-mno-sgx',
            '-mno-sha',
            '-mno-shstk',
            '-mno-skip-rax-setup',
            '-mno-soft-float',
            '-msse',
            '-msse2',
            '-mno-sse2avx',
            '-msse3',
            '-msse4',
            '-msse4.1',
            '-msse4.2',
            '-mno-sse4a',
            '-mno-sseregparm',
            '-mssse3',
            '-mno-stack-arg-probe',
            '-mstack-protector-guard-offset=',
            '-mstack-protector-guard-reg=',
            '-mstack-protector-guard-symbol=',
            '-mstack-protector-guard=tls',
            '-mno-stackrealign',
            '-mstv',
            '-mno-tbm',
            '-mtls-dialect=gnu',
            '-mtls-direct-seg-refs',
            '-mno-tsxldtrk',
            '-mtune-ctrl=',
            '-mtune=sandybridge',
            '-mno-uclibc',
            '-mno-uintr',
            '-mno-vaes',
            '-mno-vect8-ret-in-mem',
            '-mno-vpclmulqdq',
            '-mvzeroupper',
            '-mno-waitpkg',
            '-mno-wbnoinvd',
            '-mno-widekl',
            '-mno-x32',
            '-mno-xop',
            '-mxsave',
            '-mno-xsavec',
            '-mxsaveopt',
            '-mno-xsaves',
        ]
        with patch('subprocess.check_output', return_value=stdout_mock_bytes):
            actual_flags = get_flags_implied_by_march('sandybridge', debug=False)
        self.assertEqual(actual_flags, expected_flags)

    def test_macos(self):
        stdout_mock_filename = (files('resolve_march_native._gcc.test')
                                / 'data'
                                / 'native-ivybridge--10-4-0-macos-homebrew--target-help.txt')
        with open(stdout_mock_filename, 'rb') as f:
            stdout_mock_bytes = f.read()
        expected_flags = [
            '-Wnonportable-cfstrings',
            '-m128bit-long-double',
            '-mno-16',
            '-mno-32',
            '-mno-3dnow',
            '-mno-3dnowa',
            '-m64',
            '-m80387',
            '-mno-8bit-idiv',
            '-mno-96bit-long-double',
            '-mabi=sysv',
            '-mno-abm',
            '-mno-accumulate-outgoing-args',
            '-maddress-mode=long',
            '-mno-adx',
            '-maes',
            '-malign-data=compat',
            '-mno-align-double',
            '-malign-functions=0',
            '-malign-jumps=0',
            '-malign-loops=0',
            '-malign-stringops',
            '-march=ivybridge',
            '-masm=att',
            '-matt-stubs',
            '-mavx',
            '-mno-avx2',
            '-mavx256-split-unaligned-load',
            '-mavx256-split-unaligned-store',
            '-mno-avx5124fmaps',
            '-mno-avx5124vnniw',
            '-mno-avx512bf16',
            '-mno-avx512bitalg',
            '-mno-avx512bw',
            '-mno-avx512cd',
            '-mno-avx512dq',
            '-mno-avx512er',
            '-mno-avx512f',
            '-mno-avx512ifma',
            '-mno-avx512pf',
            '-mno-avx512vbmi',
            '-mno-avx512vbmi2',
            '-mno-avx512vl',
            '-mno-avx512vnni',
            '-mno-avx512vp2intersect',
            '-mno-avx512vpopcntdq',
            '-mno-bmi',
            '-mno-bmi2',
            '-mbranch-cost=3',
            '-mno-call-ms2sysv-xlogues',
            '-mno-cet-switch',
            '-mno-cld',
            '-mno-cldemote',
            '-mno-clflushopt',
            '-mno-clwb',
            '-mno-clzero',
            '-mconstant-cfstrings',
            '-mcpu=',
            '-mno-crc32',
            '-mcx16',
            '-mno-dispatch-scheduler',
            '-mno-dump-tune-features',
            '-mno-dynamic-no-pic',
            '-mno-enqcmd',
            '-mf16c',
            '-mfancy-math-387',
            '-mno-fentry',
            '-mfentry-name=',
            '-mfentry-section=',
            '-mno-fix-and-continue',
            '-mno-fma',
            '-mno-fma4',
            '-mno-force-drap',
            '-mno-force-indirect-call',
            '-mfp-ret-in-387',
            '-mfpmath=sse',
            '-mfsgsbase',
            '-mfunction-return=keep',
            '-mfxsr',
            '-mno-general-regs-only',
            '-mno-gfni',
            '-mhard-float',
            '-mno-hle',
            '-mno-iamcu',
            '-mieee-fp',
            '-mincoming-stack-boundary=0',
            '-mno-indirect-branch-register',
            '-mindirect-branch=keep',
            '-mno-inline-all-stringops',
            '-mno-inline-stringops-dynamically',
            '-minstrument-return=none',
            '-mno-kernel',
            '-mlarge-data-threshold=65536',
            '-mno-long-double-128',
            '-mno-long-double-64',
            '-mlong-double-80',
            '-mno-lwp',
            '-mno-lzcnt',
            '-mmacosx-version-min=11.0.0',
            '-mno-manual-endbr',
            '-mmemcpy-strategy=',
            '-mmemset-strategy=',
            '-mno-mitigate-rop',
            '-mmmx',
            '-mno-movbe',
            '-mno-movdir64b',
            '-mno-movdiri',
            '-mno-mpx',
            '-mno-ms-bitfields',
            '-mno-mwaitx',
            '-malign-stringops',
            '-mdefault',
            '-mfancy-math-387',
            '-mpush-args',
            '-mred-zone',
            '-msse4',
            '-mno-nop-mcount',
            '-mno-omit-leaf-frame-pointer',
            '-mno-one-byte-bool',
            '-mno-pc32',
            '-mno-pc64',
            '-mno-pc80',
            '-mpclmul',
            '-mno-pcommit',
            '-mno-pconfig',
            '-mno-pku',
            '-mpopcnt',
            '-mprefer-vector-width=none',
            '-mpreferred-stack-boundary=0',
            '-mno-prefetchwt1',
            '-mno-prfchw',
            '-mno-ptwrite',
            '-mpush-args',
            '-mno-rdpid',
            '-mrdrnd',
            '-mno-rdseed',
            '-mno-recip',
            '-mrecip=',
            '-mno-record-mcount',
            '-mno-record-return',
            '-mred-zone',
            '-mregparm=6',
            '-mno-rtd',
            '-mno-rtm',
            '-msahf',
            '-mno-sgx',
            '-mno-sha',
            '-mno-shstk',
            '-mno-skip-rax-setup',
            '-mno-soft-float',
            '-msse',
            '-msse2',
            '-mno-sse2avx',
            '-msse3',
            '-msse4',
            '-msse4.1',
            '-msse4.2',
            '-mno-sse4a',
            '-mno-sseregparm',
            '-mssse3',
            '-mno-stack-arg-probe',
            '-mstack-protector-guard-offset=',
            '-mstack-protector-guard-reg=',
            '-mstack-protector-guard-symbol=',
            '-mstack-protector-guard=global',
            '-mno-stackrealign',
            '-mstv',
            '-mno-symbol-stubs',
            '-mtarget-linker 711',
            '-mtarget-linker=',
            '-mno-tbm',
            '-mtls-dialect=gnu',
            '-mno-tls-direct-seg-refs',
            '-mtune-ctrl=',
            '-mtune=ivybridge',
            '-mno-vaes',
            '-mno-vect8-ret-in-mem',
            '-mno-vpclmulqdq',
            '-mvzeroupper',
            '-mno-waitpkg',
            '-mno-wbnoinvd',
            '-mno-x32',
            '-mno-xop',
            '-mxsave',
            '-mno-xsavec',
            '-mno-xsaveopt',
            '-mno-xsaves',
        ]
        with patch('subprocess.check_output', return_value=stdout_mock_bytes):
            actual_flags = get_flags_implied_by_march('native', debug=False)
        self.assertEqual(actual_flags, expected_flags)

    def test_sandybridge_celeron_without_avx__native(self):
        stdout_mock_filename = (files('resolve_march_native._gcc.test')
                                / 'data'
                                / 'sandybridge-celeron--target-help--native.txt')
        with open(stdout_mock_filename, 'rb') as f:
            stdout_mock_bytes = f.read()

        with patch('subprocess.check_output', return_value=stdout_mock_bytes):
            actual_flags = get_flags_implied_by_march('native', debug=False)

        self.assertIn('-mno-avx', actual_flags)
        self.assertNotIn('-mavx', actual_flags)

    def test_sandybridge_celeron_without_avx__explicit(self):
        stdout_mock_filename = (files('resolve_march_native._gcc.test')
                                / 'data'
                                / 'sandybridge-celeron--target-help--explicit.txt')
        with open(stdout_mock_filename, 'rb') as f:
            stdout_mock_bytes = f.read()

        with patch('subprocess.check_output', return_value=stdout_mock_bytes):
            actual_flags = get_flags_implied_by_march('native', debug=False)

        self.assertIn('-mavx', actual_flags)
        self.assertNotIn('-mno-avx', actual_flags)


class ParseGccOutputTest(TestCase):
    def test_deprecated_lines(self):
        self.assertEqual(_parse_gcc_output('  -mfused-madd                \t\t'), [])

    def test_ignore_lines(self):
        self.assertEqual(_parse_gcc_output('  -fapple-kext                \t\t[available in C++]'),
                         [])

    def test_equal_value_default_lines(self):
        # https://github.com/hartwork/resolve-march-native/issues/72
        self.assertEqual(_parse_gcc_output('  -mabi=ABI                   \t\tlp64'),
                         ['-mabi=lp64'])

    def test_value_default_lines(self):
        # On cfarm29 (ppc64le)
        self.assertEqual(_parse_gcc_output('  -G<number>                  \t\t8'),
                         ['-G8'])

    def test_concat_arg_lines(self):
        # On cfarm29 (ppc64le)
        self.assertEqual(_parse_gcc_output('  -malign-                    \t\tnatural'),
                         ['-malign-natural'])

    def test_concat_var_lines(self):
        # On cfarm29 (ppc64le)
        self.assertEqual(_parse_gcc_output('  -mcall-ABI                  \t\tlinux'),
                         ['-mcall-linux'])

    def test_ignore_marked_lines(self):
        # On cfarm29 (ppc64le)
        self.assertEqual(_parse_gcc_output('  -mgen-cell-microcode        \t\t[ignored]'),
                         ['-mgen-cell-microcode'])

    def test_array_value_lines(self):
        # On cfarm29 (ppc64le)
        self.assertEqual(_parse_gcc_output('  -msdata=[none,data,sysv,eabi] \tnone'),
                         ['-msdata=none'])

    def test_disabled_m_lines(self):
        self.assertEqual(_parse_gcc_output('  -mno-align-stringops        \t\t[disabled]'),
                         ['-malign-stringops'])
        self.assertEqual(_parse_gcc_output('  -mavx                                 [disabled]'),
                         ['-mno-avx'])

    def test_assign_no_lines(self):
        self.assertEqual(_parse_gcc_output('  -misel=no                   \t\t'),
                         ['-mno-isel'])

    def test_assign_yes_lines(self):
        self.assertEqual(_parse_gcc_output('  -misel=yes                  \t\t'),
                         ['-misel'])

    def test_upper_value_lines(self):
        self.assertEqual(_parse_gcc_output('  -mipsN                      \t\t1'),
                         ['-mips1'])
