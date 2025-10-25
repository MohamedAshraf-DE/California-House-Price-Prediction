# 🏡 California House Price Predictor

![House App Screenshot](https://github.com/MohamedAshraf-DE/California-House-Price-Prediction/blob/main/house.jpg?raw=true)

A **live-data web app** that predicts **median house prices in California** using machine learning.  
This project bridges the gap between **real estate analytics** and **practical decision-making**, helping homeowners, investors, and enthusiasts explore how different features impact property prices.

---

## 🌟 Why This Project Matters

### 🏠 For Homebuyers & Investors
- Estimate house prices based on key features such as location, rooms, and square footage.  
- Make **data-driven buying or investment decisions**.  
- Compare properties quickly to identify undervalued opportunities.  

### 👥 For Real Estate Professionals
- Understand the impact of property features on price.  
- Provide **clients with accurate, data-backed insights**.  
- Reduce the risk of mispricing and improve strategic planning for sales or investments.

### 💼 Business Value
- Helps real estate agencies **maximize profits** with better pricing strategies.  
- Encourages **efficient resource allocation** and investment planning.  
- Makes **property analytics accessible** to everyone, from beginners to experts.

---

## ✨ Features & Highlights

| Feature | Description |
|---------|-------------|
| 🔍 Interactive Predictions | Input property features and get estimated median house price. |
| 📊 Model Comparison | Linear, Lasso, and Ridge Regression models included. |
| 🖌️ Custom UI | Streamlit interactive dashboard for user-friendly experience. |
| 💻 End-to-End Pipeline | Data cleaning, feature engineering, skew correction, scaling, and model training. |
| 🤖 ML-Powered | Ridge Regression chosen as the final model for best performance. |

---

## 🚀 How to Run This App Locally

1. **Prerequisites**  
   - Python 3.9+  

2. **Clone & Install Dependencies**
```bash
git clone https://github.com/MohamedAshraf-DE/California-House-Price-Prediction.git
cd California-House-Price-Prediction
pip install -r requirements.txt
Run the Streamlit App

bash
Copy code
streamlit run app.py
Open your browser & explore the interactive app! 🎉

🛠️ Technical Details
Best Model: Ridge Regression

Target Transform: Log1p (to reduce skewness)

Evaluation Metrics: R² ≈ 0.75, RMSE, MAE

Feature Scaling: StandardScaler

Libraries: scikit-learn, pandas, numpy, seaborn, matplotlib, Streamlit

Files Included:

feature_scaler_california.pkl — Scaler for normalization

power_transformer.pkl — Skewness transformer

ridge_model_california.pkl — Trained Ridge model

skewed_cols_list.pkl — Skewed columns list

target_transform_info.pkl — Target variable transformation info

📞 Contact & Portfolio
Connect or check out my work:

🌐 Portfolio: https://mohamed-ashraf-github-io.vercel.app/

🔗 LinkedIn: https://www.linkedin.com/in/mohamed--ashraff

🐙 GitHub: https://github.com/MohamedAshraf-DE/MohamedAshraf.github.io
