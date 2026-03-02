import pandas as pd
import time
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ==============================
# 1. DEFINE COLUMNS
# ==============================

columns = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes","land",
    "wrong_fragment","urgent","hot","num_failed_logins","logged_in",
    "num_compromised","root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files","num_outbound_cmds",
    "is_host_login","is_guest_login","count","srv_count","serror_rate",
    "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate","dst_host_count",
    "dst_host_srv_count","dst_host_same_srv_rate",
    "dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate",
    "dst_host_srv_serror_rate","dst_host_rerror_rate",
    "dst_host_srv_rerror_rate","label","difficulty"
]

# ==============================
# 2. LOAD TRAIN DATA
# ==============================

print("\nLoading training data...")
data = pd.read_csv("../data/KDDTrain+.txt", header=None, encoding="latin-1")
data.columns = columns

data['label'] = data['label'].apply(lambda x: 0 if x == 'normal' else 1)

# ==============================
# 3. ENCODE CATEGORICAL FEATURES (FIT ON TRAIN ONLY)
# ==============================

encoders = {}

for col in data.select_dtypes(include='object').columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    encoders[col] = le

X = data.drop(["label", "difficulty"], axis=1)
y = data["label"]

# ==============================
# 4. TRAIN TEST SPLIT
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ==============================
# 5. FULL MODEL
# ==============================

print("\n===== FULL FEATURE MODEL =====")

start = time.time()

model_full = RandomForestClassifier(n_estimators=100, random_state=42)
model_full.fit(X_train, y_train)

time_full = time.time() - start

pred_full = model_full.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred_full))
print("Training Time:", time_full, "seconds")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, pred_full))

print("\nClassification Report:")
print(classification_report(y_test, pred_full))

# ==============================
# 6. FEATURE IMPORTANCE
# ==============================

feature_importance = pd.Series(
    model_full.feature_importances_,
    index=X.columns
).sort_values(ascending=False)

print("\nTop 10 Important Features:")
print(feature_importance.head(10))

# ==============================
# 7. LIGHTWEIGHT MODEL
# ==============================

print("\n===== LIGHTWEIGHT MODEL (Top 15 Features) =====")

top_features = feature_importance.head(15).index

X_light = X[top_features]

X_train_l, X_test_l, y_train_l, y_test_l = train_test_split(
    X_light, y, test_size=0.2, random_state=42
)

start = time.time()

model_light = RandomForestClassifier(n_estimators=100, random_state=42)
model_light.fit(X_train_l, y_train_l)

time_light = time.time() - start

pred_light = model_light.predict(X_test_l)

print("Accuracy (Lightweight):", accuracy_score(y_test_l, pred_light))
print("Training Time (Lightweight):", time_light, "seconds")

print("\nConfusion Matrix (Lightweight):")
print(confusion_matrix(y_test_l, pred_light))

print("\nClassification Report (Lightweight):")
print(classification_report(y_test_l, pred_light))

# ==============================
# 8. EXTERNAL TEST VALIDATION
# ==============================

print("\n===== EXTERNAL TEST DATA VALIDATION =====")

test_data = pd.read_csv("../data/KDDTest+.txt", header=None, encoding="latin-1")
test_data.columns = columns
test_data['label'] = test_data['label'].apply(lambda x: 0 if x == 'normal' else 1)

# IMPORTANT: use same encoders from training
for col in test_data.select_dtypes(include='object').columns:
    if col in encoders:
        test_data[col] = encoders[col].transform(test_data[col])

X_external = test_data.drop(["label", "difficulty"], axis=1)
y_external = test_data["label"]

X_external_light = X_external[top_features]

pred_external = model_light.predict(X_external_light)

print("External Test Accuracy:", accuracy_score(y_external, pred_external))

print("\nExternal Confusion Matrix:")
print(confusion_matrix(y_external, pred_external))

print("\nExternal Classification Report:")
print(classification_report(y_external, pred_external))

# ==============================
# 9. SAVE MODEL + FEATURES + ENCODERS
# ==============================

joblib.dump(model_light, "../models/model.pkl")
joblib.dump(top_features.tolist(), "../models/top_features.pkl")
joblib.dump(encoders, "../models/encoders.pkl")

print("\nModel, features, and encoders saved successfully.")