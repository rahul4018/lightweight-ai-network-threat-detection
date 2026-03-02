import pandas as pd
import shap
import joblib
import matplotlib.pyplot as plt

# Load model and features
model = joblib.load("../models/model.pkl")
top_features = joblib.load("../models/top_features.pkl")
encoders = joblib.load("../models/encoders.pkl")

# Load dataset
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

data = pd.read_csv("../data/KDDTrain+.txt", header=None, encoding="latin-1")
data.columns = columns

data['label'] = data['label'].apply(lambda x: 0 if x == 'normal' else 1)

for col in data.select_dtypes(include='object').columns:
    data[col] = encoders[col].transform(data[col])

X = data[top_features]

# Use small sample (SHAP is heavy)
X_sample = X.sample(500, random_state=42)

# SHAP explanation
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_sample)

# Plot
shap.summary_plot(shap_values, X_sample, show=False)

plt.savefig("../models/shap_summary.png")
print("SHAP plot saved.")