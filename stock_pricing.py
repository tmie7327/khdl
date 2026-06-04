from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DEFAULT_FILE = Path(r"C:\Users\TRA MI\Downloads\Simplize_STK_PriceHistory_20260512.xlsx")


def load_price_history(source: Any = None) -> pd.DataFrame:
    """Load the stock price history from an Excel workbook."""
    if source is None:
        source = DEFAULT_FILE
    df = pd.read_excel(source, sheet_name=0, header=5)
    df = df.iloc[:, :8]
    df.columns = [str(c).strip() for c in df.columns]
    if "NGÀY" not in df.columns:
        raise ValueError("Không tìm thấy cột NGÀY trong dữ liệu. Vui lòng kiểm tra file Excel.")
    df["NGÀY"] = pd.to_datetime(df["NGÀY"], dayfirst=True, errors="coerce")
    numeric_cols = [col for col in df.columns if col != "NGÀY"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["NGÀY", "GIÁ ĐÓNG CỬA"])
    df = df[df["GIÁ ĐÓNG CỬA"] > 0]
    return df.sort_values("NGÀY").reset_index(drop=True)


def extract_company_info(source: Any = None) -> dict[str, str]:
    """Extract company metadata from the first rows of the Excel file."""
    if source is None:
        source = DEFAULT_FILE
    header = pd.read_excel(source, sheet_name=0, header=None, nrows=5)
    company = None
    report = None
    if header.shape[1] > 1:
        company = header.iloc[1, 1]
        report = header.iloc[2, 1]
    return {
        "company": str(company).strip() if pd.notna(company) else "CTCP Sợi Thế Kỷ",
        "report": str(report).strip() if pd.notna(report) else "Lịch sử giá",
    }


def get_year_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return year-by-year summary statistics."""
    summary = (
        df.groupby(df["NGÀY"].dt.year)
        .agg(
            first_date=("NGÀY", "min"),
            last_date=("NGÀY", "max"),
            days=("NGÀY", "count"),
            avg_close=("GIÁ ĐÓNG CỬA", "mean"),
            min_close=("GIÁ ĐÓNG CỬA", "min"),
            max_close=("GIÁ ĐÓNG CỬA", "max"),
            last_close=("GIÁ ĐÓNG CỬA", "last"),
        )
        .reset_index()
    )
    summary["avg_close"] = summary["avg_close"].round(2)
    summary["min_close"] = summary["min_close"].round(2)
    summary["max_close"] = summary["max_close"].round(2)
    summary["last_close"] = summary["last_close"].round(2)
    return summary


def split_train_test(df: pd.DataFrame, test_ratio: float = 0.2) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split time series data into train/test sets preserving chronological order."""
    if not 0 < test_ratio < 1:
        raise ValueError("test_ratio phải nằm trong khoảng 0 < test_ratio < 1")
    df = df.sort_values("NGÀY").reset_index(drop=True)
    split_index = int(len(df) * (1 - test_ratio))
    train_df = df.iloc[:split_index].reset_index(drop=True)
    test_df = df.iloc[split_index:].reset_index(drop=True)
    return train_df, test_df


def build_linear_model(df: pd.DataFrame) -> tuple[LinearRegression, pd.Timestamp]:
    """Build a linear regression model for closing price over time."""
    model = LinearRegression()
    baseline = df["NGÀY"].min()
    df = df.copy()
    df["daynum"] = (df["NGÀY"] - baseline).dt.days
    X = df[["daynum"]].values
    y = df["GIÁ ĐÓNG CỬA"].values
    model.fit(X, y)
    return model, baseline


def evaluate_model(model: LinearRegression, baseline: pd.Timestamp, test_df: pd.DataFrame) -> dict[str, float]:
    """Evaluate a trained model on a test set."""
    test_df = test_df.copy()
    test_df["daynum"] = (test_df["NGÀY"] - baseline).dt.days
    X_test = test_df[["daynum"]].values
    y_true = test_df["GIÁ ĐÓNG CỬA"].values
    y_pred = model.predict(X_test)
    return {
        "mse": float(mean_squared_error(y_true, y_pred)),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "r2": float(r2_score(y_true, y_pred)),
        "test_start": test_df["NGÀY"].min(),
        "test_end": test_df["NGÀY"].max(),
        "n_test": len(test_df),
    }


def forecast_close(df: pd.DataFrame, target_date: Any) -> dict[str, float]:
    """Forecast the closing price for a target date using a linear trend."""
    if isinstance(target_date, str):
        target_date = pd.to_datetime(target_date, errors="coerce")
    elif isinstance(target_date, pd.Timestamp):
        target_date = target_date
    else:
        target_date = pd.to_datetime(target_date)
    if pd.isna(target_date):
        raise ValueError("Ngày dự báo không hợp lệ.")
    baseline = df["NGÀY"].min()
    model, baseline = build_linear_model(df)
    daynum = int((target_date - baseline).days)
    predicted = float(model.predict([[daynum]])[0])
    r2 = float(model.score((df["NGÀY"] - baseline).dt.days.to_numpy().reshape(-1, 1), df["GIÁ ĐÓNG CỬA"].to_numpy()))
    return {
        "target_date": target_date,
        "predicted_close": round(predicted, 2),
        "trend_slope": float(model.coef_[0]),
        "trend_intercept": float(model.intercept_),
        "r2_score": round(r2, 4),
    }


def get_default_file_path() -> Path:
    return DEFAULT_FILE
