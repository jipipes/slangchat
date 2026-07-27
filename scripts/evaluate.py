from __future__ import annotations

import argparse
import time

from slangchat.data.loader import load_entries
from slangchat.detection.hybrid import HybridSlangDetector


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate SlangChat detection accuracy and latency"
    )
    parser.add_argument("path", nargs="?", default="data/slang.json")
    args = parser.parse_args()

    entries = load_entries(args.path)
    detector = HybridSlangDetector(entries)

    true_positives = 0
    false_positives = 0
    false_negatives = 0
    latencies_ms: list[float] = []

    for entry in entries:
        started = time.perf_counter()
        results = detector.detect(entry.example)
        latencies_ms.append((time.perf_counter() - started) * 1000)

        predicted_terms = [result.term for result in results]
        if entry.term in predicted_terms:
            true_positives += 1
            predicted_terms.remove(entry.term)
        else:
            false_negatives += 1
        false_positives += len(predicted_terms)

    precision = true_positives / (true_positives + false_positives) if true_positives + false_positives else 0.0
    recall = true_positives / (true_positives + false_negatives) if true_positives + false_negatives else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    avg_latency_ms = sum(latencies_ms) / len(latencies_ms) if latencies_ms else 0.0

    print(f"precision={precision:.3f} recall={recall:.3f} f1={f1:.3f}")
    print(f"avg_latency_ms={avg_latency_ms:.2f} over {len(entries)} examples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())