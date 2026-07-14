from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
import matplotlib as mpl
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, RidgeCV, LassoCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import textwrap
# =====================================================
# Load data
# =====================================================

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "fuel_seal_swell_data.xlsx"

df = pd.read_excel(DATA_PATH)

# Rename these if your spreadsheet uses different column names
target_col = "O-ring Swell (% v/v)"

feature_cols = [
    "Aromatic content (%v)",
    "N-, Iso-paraffin content (%v)",
    "Cyclo-paraffin content (%v)",
]

# =====================================================
# Clean data
# =====================================================

# Keep only rows with swell and at least one composition feature
df_model = df[feature_cols + [target_col]].copy()

for col in feature_cols + [target_col]:
    df_model[col] = pd.to_numeric(df_model[col], errors="coerce")

df_model = df_model.dropna(subset=[target_col])
df_model[feature_cols] = df_model[feature_cols].fillna(0)

X = df_model[feature_cols]
y = df_model[target_col]


import matplotlib.pyplot as plt
import numpy as np

# =====================================================
# Plot settings: unique color by Source, marker by Class
# =====================================================

source_col = "Source"
class_col = "Class"

# Keep source/class columns in plotting dataframe
plot_cols = feature_cols + [target_col, source_col, class_col]
df_plot = df[plot_cols].copy()

for col in feature_cols + [target_col]:
    df_plot[col] = pd.to_numeric(df_plot[col], errors="coerce")

df_plot = df_plot.dropna(subset=[target_col])
df_plot[feature_cols] = df_plot[feature_cols].fillna(0)

df_plot[source_col] = df_plot[source_col].fillna("Unknown source")
df_plot[class_col] = df_plot[class_col].fillna("Unknown class")

sources = sorted(df_plot[source_col].unique())
classes = sorted(df_plot[class_col].unique())

# Color map for sources
cmap = mpl.colormaps["tab20"]
fuel_colors = {
    source: cmap(i)
    for i, source in enumerate(classes)
}

# Marker map for fuel classes
marker_list = ["o", "s", "^", "D", "P", "X", "v", "<", ">", "*", "h"]
source_markers = {
    source: marker_list[i % len(marker_list)]
    for i, source in enumerate(sources)
}

# =====================================================
# Train/test split
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42
)

# =====================================================
# Models
# =====================================================

models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": RidgeCV(alphas=np.logspace(-4, 4, 50)),
    "Lasso Regression": LassoCV(alphas=np.logspace(-4, 2, 50), max_iter=10000),
    "Random Forest": RandomForestRegressor(
        n_estimators=500,
        random_state=42,
        min_samples_leaf=2
    ),
}

# =====================================================
# Fit and evaluate
# =====================================================

results = []

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5

    results.append({
        "model": name,
        "R2": r2,
        "MAE": mae,
        "RMSE": rmse,
    })

results_df = pd.DataFrame(results)
print(results_df)
# =====================================================
# Print all model equations / parameters
# =====================================================

print("\n" + "="*70)
print("MODEL EQUATIONS / PARAMETERS")
print("="*70)

for name, model in models.items():

    print(f"\n{name}")
    print("-" * len(name))

    # Linear-style models: Linear, Ridge, Lasso
    if hasattr(model, "coef_"):
        equation = f"Swell = {model.intercept_:.3f}"

        for col, coef in zip(feature_cols, model.coef_):
            equation += f" + ({coef:.3f})*{col}"

        print(equation)

        coef_df = pd.DataFrame({
            "Feature": feature_cols,
            "Coefficient": model.coef_
        })

        print("\nCoefficients:")
        print(coef_df.to_string(index=False))

    # Random forest does not have a simple equation
    elif hasattr(model, "feature_importances_"):
        importance_df = pd.DataFrame({
            "Feature": feature_cols,
            "Importance": model.feature_importances_
        }).sort_values("Importance", ascending=False)

        print("Random Forest does not produce a simple linear equation.")
        print("Feature importances:")
        print(importance_df.to_string(index=False))




# =====================================================
# Plot settings: unique color by Source, marker by Class
# =====================================================

source_col = "Source"
class_col = "Class"

# Keep source/class columns in plotting dataframe
plot_cols = feature_cols + [target_col, source_col, class_col]
df_plot = df[plot_cols].copy()

for col in feature_cols + [target_col]:
    df_plot[col] = pd.to_numeric(df_plot[col], errors="coerce")

df_plot = df_plot.dropna(subset=[target_col])
df_plot[feature_cols] = df_plot[feature_cols].fillna(0)

df_plot[source_col] = df_plot[source_col].fillna("Unknown source")
df_plot[class_col] = df_plot[class_col].fillna("Unknown class")

sources = sorted(df_plot[source_col].unique())
classes = sorted(df_plot[class_col].unique())


# Marker map for fuel classes
marker_list = ["o", "s", "^", "D", "P", "X", "v", "<", ">", "*", "h"]
class_markers = {
    fuel_class: marker_list[i % len(marker_list)]
    for i, fuel_class in enumerate(classes)
}
import matplotlib.pyplot as plt
import matplotlib as mpl

# =====================================================
# Plot settings
# Color = Fuel Class
# Marker = Source
# =====================================================

source_col = "Source"
class_col = "Class"

plot_cols = feature_cols + [target_col, source_col, class_col]
df_plot = df[plot_cols].copy()

for col in feature_cols + [target_col]:
    df_plot[col] = pd.to_numeric(df_plot[col], errors="coerce")

df_plot = df_plot.dropna(subset=[target_col])
df_plot[feature_cols] = df_plot[feature_cols].fillna(0)

df_plot[source_col] = df_plot[source_col].fillna("Unknown source")
df_plot[class_col] = df_plot[class_col].fillna("Unknown class")

sources = sorted(df_plot[source_col].unique())
classes = sorted(df_plot[class_col].unique())

# Colors for fuel classes
base_cmap = mpl.colormaps["tab20"]
fuel_colors = {
    fuel_class: base_cmap(i / max(len(classes) - 1, 1))
    for i, fuel_class in enumerate(classes)
}

# Markers for sources
marker_list = ["o", "s", "^", "D", "P", "X", "v", "<", ">", "*", "h"]
source_markers = {
    source: marker_list[i % len(marker_list)]
    for i, source in enumerate(sources)
}

# Legend handles
class_handles = [
    plt.Line2D(
        [0], [0],
        marker="o",
        color="w",
        label="\n".join(textwrap.wrap(fuel_class, width=30)),
        markerfacecolor=fuel_colors[fuel_class],
        markeredgecolor="black",
        markersize=8
    )
    for fuel_class in classes
]

source_handles = [
    plt.Line2D(
        [0], [0],
        marker=source_markers[source],
        color="black",
        label="\n".join(textwrap.wrap(source, width=30)),
        linestyle="None",
        markersize=8
    )
    for source in sources
]

# =====================================================
# Raw composition-property plots
# =====================================================

for feature in feature_cols:

    plt.figure(figsize=(9, 6))

    for source in sources:
        for fuel_class in classes:

            subset = df_plot[
                (df_plot[source_col] == source) &
                (df_plot[class_col] == fuel_class)
            ]

            if subset.empty:
                continue

            plt.scatter(
                subset[feature],
                subset[target_col],
                color=fuel_colors[fuel_class],
                marker=source_markers[source],
                alpha=0.8,
                edgecolor="black",
                linewidth=0.5,
                s=70
            )

    plt.xlabel(feature)
    plt.ylabel("O-ring swell (% v/v)")
    plt.title(f"O-ring swell vs {feature}")

    class_legend = plt.legend(
        handles=class_handles,
        title="Fuel class",
        loc="upper left",
        bbox_to_anchor=(1.02, 1)
    )

    plt.gca().add_artist(class_legend)

    plt.legend(
        handles=source_handles,
        title="Source",
        loc="lower left",
        bbox_to_anchor=(1.02, 0)
    )

    plt.tight_layout()
    plt.show()

# =====================================================
# Actual vs predicted plots
# =====================================================

metadata = df_model.copy()
metadata[source_col] = df.loc[df_model.index, source_col].fillna("Unknown source")
metadata[class_col] = df.loc[df_model.index, class_col].fillna("Unknown class")

X = df_model[feature_cols]
y = df_model[target_col]

X_train, X_test, y_train, y_test, meta_train, meta_test = train_test_split(
    X,
    y,
    metadata[[source_col, class_col]],
    test_size=0.25,
    random_state=42
)

for name, model in models.items():

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    plot_test = meta_test.copy()
    plot_test["Measured"] = y_test
    plot_test["Predicted"] = y_pred

    plt.figure(figsize=(9, 6))

    for source in sources:
        for fuel_class in classes:

            subset = plot_test[
                (plot_test[source_col] == source) &
                (plot_test[class_col] == fuel_class)
            ]

            if subset.empty:
                continue

            plt.scatter(
                subset["Measured"],
                subset["Predicted"],
                color=fuel_colors[fuel_class],
                marker=source_markers[source],
                alpha=0.85,
                edgecolor="black",
                linewidth=0.5,
                s=80
            )

    min_val = min(plot_test["Measured"].min(), plot_test["Predicted"].min())
    max_val = max(plot_test["Measured"].max(), plot_test["Predicted"].max())

    plt.plot(
        [min_val, max_val],
        [min_val, max_val],
        linestyle="--",
        color="black",
        linewidth=1
    )

    plt.xlabel("Measured O-ring swell (% v/v)")
    plt.ylabel("Predicted O-ring swell (% v/v)")
    plt.title(f"Actual vs predicted swell: {name}")

    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    plt.text(
        0.05,
        0.95,
        f"R² = {r2:.3f}\nMAE = {mae:.2f}",
        transform=plt.gca().transAxes,
        verticalalignment="top"
    )

    class_legend = plt.legend(
        handles=class_handles,
        title="Fuel class",
        loc="upper left",
        bbox_to_anchor=(1.02, 1)
    )

    plt.gca().add_artist(class_legend)

    plt.legend(
        handles=source_handles,
        title="Source",
        loc="lower left",
        bbox_to_anchor=(1.02, 0)
    )

    plt.tight_layout()
    plt.show()