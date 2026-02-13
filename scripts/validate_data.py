from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CsvSpec:
    path: Path
    columns: list[str]
    row_count: int


def read_header(path: Path) -> list[str]:
    with path.open(newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
    return header or []


def count_rows(path: Path) -> int:
    with path.open(newline="") as handle:
        reader = csv.reader(handle)
        next(reader, None)
        return sum(1 for _ in reader)


def main() -> int:
    specs = [
        CsvSpec(
            path=Path("data/raw/robot_churn_poc_dataset.csv"),
            columns=[
                "customer_id",
                "site_id",
                "year_month",
                "usage_volume",
                "bot_utilization",
                "bot_performance",
                "associate_performance",
                "bot_uptime",
                "upgrade_failures",
                "support_sla",
                "lack_of_rca",
                "nps",
                "churn_flag_next_6m",
            ],
            row_count=663,
        ),
        CsvSpec(
            path=Path("data/trusted/fact_churn_risk.csv"),
            columns=[
                "customer_id",
                "site_id",
                "year_month",
                "risk_category",
                "probability",
                "risk_summary",
                "primary_drivers",
                "recommended_actions",
            ],
            row_count=51,
        ),
        CsvSpec(
            path=Path("data/curated/churn_risk_scores.csv"),
            columns=[
                "customer_id",
                "site_id",
                "year_month",
                "churn_risk",
                "calibrated_probability",
                "behavior_deterioration_score",
                "usage_volume",
                "bot_utilization",
                "bot_performance",
                "bot_uptime",
                "support_sla",
                "nps",
                "usage_volume_slope_3m",
                "bot_performance_slope_3m",
                "bot_uptime_slope_3m",
                "support_sla_slope_3m",
                "nps_slope_3m",
                "nps_consec_down",
                "usage_volume_consec_down",
                "upgrade_failures_consec_up",
                "lack_of_rca_consec_up",
            ],
            row_count=51,
        ),
    ]

    errors: list[str] = []

    for spec in specs:
        if not spec.path.exists():
            errors.append(f"Missing file: {spec.path}")
            continue

        header = read_header(spec.path)
        if header != spec.columns:
            errors.append(
                f"Header mismatch for {spec.path}: expected {spec.columns} got {header}"
            )

        rows = count_rows(spec.path)
        if rows != spec.row_count:
            errors.append(
                f"Row count mismatch for {spec.path}: expected {spec.row_count} got {rows}"
            )

    if errors:
        print("Data validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print(f"Validated {len(specs)} data file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
