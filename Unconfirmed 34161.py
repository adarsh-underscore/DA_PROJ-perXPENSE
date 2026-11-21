
import pandas as pd

INPUT_FILE = "clean_expenses.csv"
OUTPUT_FILE = "category_totals.csv"

df = pd.read_csv(INPUT_FILE, parse_dates=["date"])
df["month"] = df["date"].dt.strftime("%Y-%m")

# Optional filter: type a month like 2026-03, or press Enter for all time
month = input("Enter month (YYYY-MM) or press Enter for all time: ").strip()
if month:
    df = df[df["month"] == month]
    if df.empty:
        raise SystemExit(f"No expenses found for {month}.")
    title = f"Spending by category for {month}"
else:
    title = "Spending by category (all time)"

# Total, number of entries, average and share of total for each category
summary = (
    df.groupby("category")["amount"]
    .agg(total="sum", entries="count", average="mean")
    .sort_values("total", ascending=False)
)
summary["share_%"] = (summary["total"] / summary["total"].sum() * 100).round(1)
summary = summary.round(2)

print(f"\n{title}\n" + "-" * len(title))
print(summary.to_string())
print(f"\nGrand total : ₹{df['amount'].sum():,.2f}")
print(f"Highest     : {summary['total'].idxmax()} (₹{summary['total'].max():,.2f})")
print(f"Lowest      : {summary['total'].idxmin()} (₹{summary['total'].min():,.2f})")

# Month-by-month table: rows = category, columns = month (only for all-time view)
if not month:
    pivot = df.pivot_table(index="category", columns="month", values="amount",
                           aggfunc="sum", fill_value=0).round(2)
    print("\nCategory x Month:\n")
    print(pivot.to_string())

summary.to_csv(OUTPUT_FILE)
print(f"\nSaved: {OUTPUT_FILE}")
