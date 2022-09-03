from collections import defaultdict
from time import time_ns


class Timer:
    stack = []
    time_recorder = defaultdict(int)
    count_recorder = defaultdict(int)

    def __init__(self, qualname):
        self._qualname = qualname
        self._start = None

    def __enter__(self):
        self.stack.append(self._qualname)
        self.count_recorder[self._qualname] += 1
        self._start = time_ns()

    def __exit__(self, exc_type, exc_value, traceback):
        delta = time_ns() - self._start
        self.stack.pop()

        self.time_recorder[self._qualname] += delta
        if self.stack:
            caller_name = self.stack[-1]
            self.time_recorder[caller_name] -= delta

    @classmethod
    def explain_performance_by_name(cls):
        total = sum(cls.time_recorder.values())
        print(f"Overall Time: {total}ns")
        data = [("name", "sum(ns)", "count", "proportion")]
        for name in sorted(cls.time_recorder.keys(), key=cls.time_recorder.get, reverse=True):
            data.append((name, f"{cls.time_recorder[name]}", f"{cls.count_recorder[name]}", f"{cls.time_recorder[name]*100/total:.2f}%"))
        cls.__display_table(data, ('<', '>', '>', '>'))

    @staticmethod
    def __display_table(data, fmt, sep='    '):
        n = len(fmt)
        assert all(len(row) == n for row in data)
        max_len = [0] * n
        for i in range(n):
            max_len[i] = max(len(row[i]) for row in data)
        for row in data:
            print(sep.join(f"{row[i]:{fmt[i]}{max_len[i]}}" for i in range(n)))
