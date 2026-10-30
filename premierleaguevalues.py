import pandas as pd

players = pd.DataFrame({
    "player_id": [1, 2],
    "name": ["Player X", "Player Y"],
    "DOB": pd.to_datetime(["2001-03-10", "1995-08-22"]),
    "position": ["FWD", "DEF"],
})

valuations = pd.DataFrame({
    "player_id": [1, 1, 1, 2, 2],
    "date": pd.to_datetime(["2023-06-20", "2024-01-15", "2024-07-20",
                            "2023-06-20", "2024-03-10"]),
    "value_m": [35, 40, 50, 20, 18],
})

snapshots = pd.DataFrame({"snapshot": pd.to_datetime(["2023-07-01", "2024-07-01"])})

spine = players.merge(snapshots, how="cross")
print(spine.columns.tolist())
spine["age"] = (spine["snapshot"] - spine["DOB"]).dt.days / 365.25

target = valuations.rename(columns={"date": "target_date", "value_m": "target_value"})

spine = pd.merge_asof(spine.sort_values("snapshot"), target.sort_values("target_date"), left_on="snapshot", right_on="target_date", by="player_id", direction="forward", tolerance=pd.Timedelta(days=120),)
spine["lag_date"] = spine["snapshot"] - pd.Timedelta(days=365)
prior = valuations.rename(columns={"date": "prior_date", "value_m": "value_1yr_ago"})

spine = pd.merge_asof(spine.sort_values("lag_date"), prior.sort_values("prior_date"), left_on="lag_date", right_on="prior_date", by="player_id", direction="backward",)
print(spine.sort_values(["player_id", "snapshot"]))