import datetime
import hashlib
import http.client
import json
import math
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

import numpy
from sklearn.base import BaseEstimator, ClassifierMixin

from orchestra.data import LABELS, file_sha256

MODEL = "jev-1.14.0"
URL = "https://api.typesafe.ai/v1/systemone"
QUESTION = "first_action"
KEY_VARIABLE = "TYPESAFE_API_KEY"
# Wording follows annotation guide v2 and the M3.5 lookup rules, written before
# any API call. The criteria carry the guide's multi-action rule because a
# calculation over figures in a document or record is the usual confusion.
INSTRUCTIONS = (
    "Which action must the assistant take first to handle `query`? When `query` "
    "needs several actions, the first is the one whose output another action needs."
)
CRITERIA = {
    "document_retrieval": (
        "Read a document or passage that `query` identifies, such as a named "
        "report, article or attached text."
    ),
    "knowledge_lookup": (
        "Look up a record in a structured source that `query` identifies, such as "
        "a database, catalog, table, dataset or the user's own account."
    ),
    "calculation": (
        "Compute a numeric result from values stated in `query` itself. Figures "
        "that must first be read from a document or record are not stated in it."
    ),
    "direct_answer": (
        "Explain, answer or rewrite from general knowledge, with no document, "
        "record or calculation needed."
    ),
}


def request_body(text):
    return {
        "model": MODEL,
        "state": {"query": text},
        "questions": {
            QUESTION: {
                "type": "choice",
                "instructions": INSTRUCTIONS,
                "criteria": dict(CRITERIA),
            }
        },
    }


def parse(payload):
    try:
        answer = payload["answers"][QUESTION]
        model = payload.get("model")
    except (KeyError, TypeError, AttributeError):
        raise ValueError(f"no {QUESTION} answer") from None
    if model != MODEL:
        raise ValueError(f"answered by model {model}, not {MODEL}")
    if not isinstance(answer, dict) or answer.get("type") != "choice":
        raise ValueError(f"{QUESTION} answer is not a choice")
    choice = answer.get("choice")
    if choice not in LABELS:
        raise ValueError(f"choice {choice!r} is not a label")
    raw = answer.get("probabilities")
    if not isinstance(raw, dict) or set(raw) != set(LABELS):
        raise ValueError("probability keys differ from the labels")
    probabilities = [raw[label] for label in LABELS]
    for value in probabilities:
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or not 0 <= value <= 1
        ):
            raise ValueError(f"probability {value!r} is not a number in [0, 1]")
    if abs(sum(probabilities) - 1) > 1e-3:
        raise ValueError("probabilities do not sum to 1")
    return {
        "model": payload.get("model"),
        "choice": choice,
        "probabilities": [float(p) for p in probabilities],
        "confidence": answer.get("confidence"),
        "usage": payload.get("usage"),
    }


def post(body, key, timeout=60):
    request = urllib.request.Request(
        URL,
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        text = error.read().decode("utf-8", errors="replace")
        try:
            return error.code, json.loads(text)
        except json.JSONDecodeError:
            return error.code, text
    except (
        urllib.error.URLError,
        http.client.HTTPException,
        TimeoutError,
        OSError,
        ValueError,
    ) as error:
        return None, str(getattr(error, "reason", error))


def text_digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def valid_answer(line):
    """The parsed answer, only if it was given under the current model and prompt
    for the very text its digest names."""
    if line.get("status") != 200:
        return None
    try:
        query = line["request"]["state"]["query"]
        if line["request"] != request_body(query):
            return None
        if text_digest(query) != line["text_sha256"]:
            return None
        return parse(line["response"])
    except (ValueError, KeyError, TypeError):
        return None


def read_log(path):
    lines = []
    if Path(path).exists():
        with open(path, encoding="utf-8") as file:
            for raw in file:
                try:
                    line = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                if isinstance(line, dict):
                    lines.append(line)
    return lines


def answered_keys(log_path):
    return {
        (line["query_id"], line["text_sha256"])
        for line in read_log(log_path)
        if valid_answer(line) and "query_id" in line
    }


def collect(rows, log_path, max_requests, send):
    answered = answered_keys(log_path)
    requests = 0
    with open(log_path, "a", encoding="utf-8") as log:
        for row in rows:
            if requests >= max_requests:
                break
            digest = text_digest(row["text"])
            if (row["query_id"], digest) in answered:
                continue
            body = request_body(row["text"])
            requested = datetime.datetime.now(datetime.UTC).isoformat()
            started = time.perf_counter()
            status, response = send(body)
            latency = time.perf_counter() - started
            requests += 1
            line = {
                "query_id": row["query_id"],
                "text_sha256": digest,
                "requested_utc": requested,
                "latency_seconds": latency,
                "request": body,
                "status": status,
                "response": response,
                "error": None,
            }
            if status != 200:
                line["error"] = f"HTTP status {status}"
            else:
                try:
                    parse(response)
                except ValueError as error:
                    line["error"] = str(error)
            log.write(json.dumps(line) + "\n")
            log.flush()
    valid = [(line, valid_answer(line)) for line in read_log(log_path)]
    done = answered_keys(log_path)
    tokens = sum(
        (answer["usage"] or {}).get("input_tokens", 0) for _, answer in valid if answer
    )
    keys = {
        row["query_id"]: (row["query_id"], text_digest(row["text"])) for row in rows
    }
    return {
        "requests": requests,
        "answered": len([k for k in keys.values() if k in done]),
        "missing": sorted(i for i, k in keys.items() if k not in done),
        "input_tokens": tokens,
    }


class Replay(ClassifierMixin, BaseEstimator):
    def __init__(self, responses=None, responses_sha256=None):
        self.responses = responses
        self.responses_sha256 = responses_sha256

    def fit(self, X, y=None):
        path = Path(self.responses)
        found = file_sha256(path)
        if found != self.responses_sha256:
            raise ValueError(
                f"Jev responses changed: {path} hashes to {found}, "
                f"expected {self.responses_sha256}"
            )
        answers = {}
        for line in read_log(path):
            answer = valid_answer(line)
            if answer and line.get("text_sha256") not in answers:
                answers[line["text_sha256"]] = answer
        self.answers_ = answers
        self.classes_ = numpy.array(LABELS)
        return self

    def lookup(self, X):
        found = [self.answers_.get(text_digest(text)) for text in X]
        missing = found.count(None)
        if missing:
            raise ValueError(f"{missing} queries have no valid Jev answer")
        return found

    def predict_proba(self, X):
        return numpy.array([a["probabilities"] for a in self.lookup(X)])

    def predict(self, X):
        return numpy.array([a["choice"] for a in self.lookup(X)])


def log_is_unsafe(path):
    # Logs hold query text, which must stay out of Git.
    root = Path(__file__).resolve().parents[2]
    resolved = Path(path).resolve()
    if root not in resolved.parents:
        return False
    from orchestra.experiment import git

    return git("check-ignore", "-q", str(resolved)) is None


def run_jev(args):
    from orchestra.experiment import check_inputs, load_rows

    if args.max_requests < 1:
        print("ERROR: --max-requests must be a positive integer")
        return 1
    if log_is_unsafe(args.log):
        print(f"ERROR: {args.log} is inside the repository and not ignored by Git")
        return 1
    with open(args.config, encoding="utf-8") as file:
        config = json.load(file)
    train = load_rows(config["train"], "train")
    validation = load_rows(config["validation"], "validation")
    check_inputs(config, train, validation)
    if args.dry_run:
        done = answered_keys(args.log)
        pending = sum(
            (r["query_id"], text_digest(r["text"])) not in done for r in validation
        )
        example = request_body("<query text>")
        print(
            json.dumps(
                {
                    "validation_rows": len(validation),
                    "pending": pending,
                    "example_request": example,
                },
                indent=2,
            )
        )
        return 0
    key = os.environ.get(KEY_VARIABLE)
    if not key:
        print(f"ERROR: {KEY_VARIABLE} is not set")
        return 1
    summary = collect(
        validation, args.log, args.max_requests, lambda body: post(body, key)
    )
    print(json.dumps(summary, indent=2))
    print(f"log sha256: {file_sha256(args.log)}")
    return 1 if summary["missing"] else 0
