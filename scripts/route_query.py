"""Route a new query through the frozen logistic system, raw and calibrated.

For oral practice. The frozen configuration is refit on the training rows
exactly as final-test refit it, so a saved row's text reproduces its saved
probabilities. Jev is not routed; that would send the query to TypeSafe.
"""

import argparse
import sys

from orchestra import confidence
from orchestra.data import LABELS


def route(freeze_path, text, top=6):
    frozen = confidence._json(freeze_path)
    config = frozen["config"]
    confidence._verify_hashes(config["hashes"])
    _, _, train, _, _, _, entry = confidence._context(
        config["run"], config["selection"]
    )
    if entry != config["logistic"]:
        raise ValueError("frozen logistic system changed")
    rows = [{"text": text}]
    raw = confidence._fit(entry, train, rows)
    calibrated = confidence._calibrate(
        entry, train, rows, confidence.calibration_folds(train)
    )
    vectorizer = raw["pipeline"].named_steps["vec"]
    classifier = raw["pipeline"].named_steps["clf"]
    weights = classifier.coef_[list(classifier.classes_).index(raw["predictions"][0])]
    features = vectorizer.transform([text]).tocoo()
    names = vectorizer.get_feature_names_out()
    evidence = sorted(
        (
            (str(names[j]), float(value * weights[j]))
            for j, value in zip(features.col, features.data, strict=True)
        ),
        key=lambda item: -item[1],
    )
    return {
        "system": entry["id"],
        "training_rows": len(train),
        "threshold": frozen["fallback"]["chosen"],
        "raw": {"prediction": raw["predictions"][0], "probabilities": raw["scores"][0]},
        "calibrated": {
            "prediction": calibrated["predictions"][0],
            "probabilities": calibrated["scores"][0],
        },
        "evidence": evidence[:top],
        "unseen": [
            token
            for token in vectorizer.build_analyzer()(text)
            if " " not in token and token not in vectorizer.vocabulary_
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", default="results/frozen-study-m3-5.json")
    parser.add_argument("query")
    args = parser.parse_args(argv)
    result = route(args.freeze, args.query)
    print(f"Query: {args.query}")
    print(
        f"System: {result['system']}, refit on {result['training_rows']} "
        "training rows as in the final test"
    )
    print(f"{'':12}" + "".join(f"{label:>20}" for label in LABELS))
    for kind in ("raw", "calibrated"):
        values = result[kind]["probabilities"]
        print(f"{kind:12}" + "".join(f"{v:>20.4f}" for v in values))
        print(f"{'':12}prediction: {result[kind]['prediction']}")
    top = max(result["calibrated"]["probabilities"])
    threshold = result["threshold"]
    if threshold is None:
        print("Fallback: none frozen")
    else:
        decision = "route it" if top >= threshold else "hand it to the fallback"
        print(f"Fallback threshold {threshold}: top calibrated {top:.4f}, {decision}")
    print(f"Strongest n-grams for {result['raw']['prediction']} (TF-IDF x weight):")
    for name, value in result["evidence"]:
        print(f"  {name!r}: {value:+.4f}")
    print(f"Words never seen in training: {', '.join(result['unseen']) or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
