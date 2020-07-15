import platform
from collections import defaultdict, namedtuple
import inspect
import os
import json
import random
import time
import re
from pathlib import Path

from benchmark.base import Test
import benchmark.simple
import benchmark.test_random
import benchmark.repeated
import benchmark.holey

from tqdm import tqdm
import psutil


TestCase = namedtuple('TestCase', ['cls', 'variant', 'method'])
Result = namedtuple('Result', ['case', 'result', 'took'])


def try_get_cpuid():
    cpuinfo_path = Path('/proc/cpuinfo')
    if cpuinfo_path.exists():
        cpuinfo = cpuinfo_path.read_text()
        matches = set(re.findall("model name\s*: (.*)", cpuinfo))
        return ', '.join(matches)

def get_mem_info():
    meminfo = psutil.virtual_memory()
    return {'total': meminfo.total, 'available': meminfo.available}


def plat_info():
    info = {'memory': get_mem_info()}
    for fn_name in [
        'release', 'system', 'processor', 'python_compiler', 
        'python_build', 'python_implementation', 'python_revision',
    ]:
        info[fn_name] = getattr(platform, fn_name)()
    cpuid = try_get_cpuid()
    if cpuid:
        info['processor'] = cpuid 
    return info


def main():
    testers = []
    warmups = []

    tester_info = {}
    output = {
        'time': time.time(),
        'platform': plat_info(),
        'tests': tester_info,
    }

    for test_class in Test.all_test_classes():
        cls_info = {
            'name': test_class.NAME,
            'num_runs': test_class.NUM_RUNS,
            'methods': {},
            'variants': [],
        }
        tester_info[test_class.__name__] = cls_info

        first_variant = True
        for variant in test_class.variants():
            cls_info['variants'].append(variant)

            for method in test_class.test_methods():
                if method.__name__ not in cls_info['methods']:
                    cls_info['methods'][method.__name__] = inspect.getsource(method)

                for _ in range(test_class.NUM_RUNS):
                    testers.append(TestCase(test_class, variant, method))
                if first_variant:
                    warmups.append(TestCase(test_class, variant, method))
            first_variant = False

    random.shuffle(warmups)
    random.shuffle(testers)

    for warmup in tqdm(warmups):
        warmup.cls.run_test(warmup.variant, warmup.method)

    results = []

    for test in tqdm(testers):
        result, took = test.cls.run_test(test.variant, test.method)
        results.append(Result(test, result, took))

    nested_times = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    nested_results = defaultdict(dict)

    for result in results:
        cls_name = result.case.cls.__name__
        fn_name = result.case.method.__name__
        variant = result.case.variant
        nested_times[cls_name][fn_name][variant].append(result.took)
        if result.case.cls.CHECK_RESULTS:
            current_result = nested_results[cls_name].setdefault(variant, result.result)
            if current_result != result.result:
                raise AssertionError(f'Result mismatch: {cls_name}({variant}).{fn_name} returned {result.result}, previous: {current_result}')

    output['results'] = nested_times
        

    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
