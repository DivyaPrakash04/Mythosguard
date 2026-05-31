from __future__ import annotations
import random

class Planner:
    def __init__(self, weights=None):
        self.weights = weights or {"source_code": 1.0}

    def choose(self):
        # simple: pick highest weight key
        return max(self.weights.items(), key=lambda x: x[1])[0]

    def update(self, strategy: str, success: bool):
        # multiplicative update: increase if success else decrease
        if success:
            self.weights[strategy] = self.weights.get(strategy, 0.5) * 1.1
        else:
            self.weights[strategy] = self.weights.get(strategy, 0.5) * 0.9
