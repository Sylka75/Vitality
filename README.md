# Vitality - AI Calorie Tracker 🌿

Vitality is a minimalist, personal calorie-tracking application built with **Streamlit**, **Supabase**, and **AI-driven image analysis**.

## ✨ Features

- **AI Meal Analysis**: Take a photo of your food and let AI (Llava + Gemini) estimate the calories and ingredients.
- **Bento Grid Dashboard**: A clean, modular overview of your daily intake, remaining calories, and weight status.
- **Weight Tracking**: Monitor your progress with interactive trend charts.
- **Privacy First**: Built for personal use with private database integration.

## 🛠 Tech Stack

- **Frontend**: Streamlit
- **Design System**: UI/UX Pro Max (Bento Grid + Soft UI Evolution)
- **Database**: Supabase (PostgreSQL)
- **AI Vision**: Llava-1.5-7b (Hugging Face Inference API)
- **AI Parsing**: Gemini 1.5 Flash (Google AI)
- **Charts**: Plotly

## 🚀 Getting Started

1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Secrets**:
   Create `.streamlit/secrets.toml` based on `.streamlit/secrets.toml.example`.
4. **Run the app**:
   ```bash
   streamlit run app.py
   ```

## 📐 Design Philosophy

Vitality uses the **UI/UX Pro Max** guidelines:
- **Typography**: Poppins (Headings) & Open Sans (Body).
- **Colors**: Emerald Primary (#10B981) for health and trust.
- **Layout**: Modular Bento Grids for a premium, organized feel.
- **Interaction**: Smooth transitions and subtle shadows.
