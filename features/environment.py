import logging
import os
import uuid

from allure_behave.hooks import (  # noqa: F401  # used by the commented-out reporting hook below
    allure_report,
)
from behave.runner import Context

from features.seed import SCENARIO_STATE_ROOT, ensure_seed, provision, release

# Caps on the thread pools the numeric stack creates when it is imported.
#
# `import partcad` reaches build123d, which reaches scipy, which asks its BLAS
# for one thread per core at import time. On an idle workstation that hides in
# the spare cores, but it is ~8s of CPU on every `pc` invocation against ~1.4s
# with these set, and the suite starts hundreds of them. It matters most exactly
# where there is no headroom: a 2-core CI runner, and any run under
# `--parallel-processes`, where the workers would otherwise each try to fill the
# whole machine.
THREAD_LIMIT_ENV = {
    "OMP_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
    "VECLIB_MAXIMUM_THREADS": "1",
}

# Scenarios carrying this tag assert on PartCAD's shipped telemetry behaviour -
# that it defaults to Sentry, and that `pc system set telemetry` changes it.
# Forcing a value through the environment would decide the answer before the
# command ran, so they are the one place the default is left alone.
TELEMETRY_TAG = "pc-system-telemetry"

# Scenarios carrying this tag are left entirely alone: no seed copy, and
# PC_INTERNAL_STATE_DIR unset, so PartCAD falls back to `$HOME/.partcad` and
# finds it empty because the scenario's `$HOME` is a fresh temporary directory.
# Two kinds of assertion need that. Some assert on cache-miss behaviour -
# `pc install` reports "Cloning the GIT repo:", which it does not do for a
# repository the seed already cloned. Others assert on the default location
# itself, which pointing PC_INTERNAL_STATE_DIR elsewhere would change. They pay
# the cold-start cost the rest of the suite no longer does, which is the point.
COLD_STATE_TAG = "cold-state"


# def before_all(context: Context) -> None:
#     import steps

#     allure_report("allure-results")


def subprocess_env() -> dict:
    """The environment the suite's `pc` invocations inherit."""
    env = dict(os.environ)
    env.update(THREAD_LIMIT_ENV)
    return env


def before_all(context: Context) -> None:
    # Applied to this process rather than handed to each subprocess, so that
    # anything the suite starts inherits them, including the seed build below.
    os.environ.update(THREAD_LIMIT_ENV)

    # Building here rather than in a fixture keeps `behave` usable on its own.
    # Under behavex every worker reaches this line; `ensure_seed` locks so only
    # the first one builds. CI builds it in an earlier step, and then all of
    # them find the marker already written and return immediately.
    context.seed_state_dir = ensure_seed(subprocess_env())


def before_scenario(context: Context, scenario) -> None:
    if not hasattr(context, "env"):
        context.env = {}

    # Every `pc` invocation in this scenario reads and writes its own copy of
    # the seed instead of `$HOME/.partcad`. A step that sets
    # PC_INTERNAL_STATE_DIR explicitly runs after this hook and overwrites it,
    # which is what the scenarios exercising `--internal-state-dir` rely on.
    if COLD_STATE_TAG not in scenario.effective_tags:
        state_dir = os.path.join(SCENARIO_STATE_ROOT, f"state-{os.getpid()}-{uuid.uuid4().hex[:8]}")
        provision(state_dir)
        context.state_dir = state_dir
        context.env["PC_INTERNAL_STATE_DIR"] = state_dir

    # Left unset for the telemetry scenarios; see TELEMETRY_TAG. Everywhere else
    # this stops each invocation from opening a connection to Sentry and
    # flushing it on exit, which the suite was doing several times per command.
    if TELEMETRY_TAG not in scenario.effective_tags:
        context.env["PC_TELEMETRY_TYPE"] = "none"


def after_scenario(context: Context, scenario) -> None:
    state_dir = getattr(context, "state_dir", None)
    if state_dir:
        release(state_dir)
        logging.debug("Removed scenario state directory: %s", state_dir)
