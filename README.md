# SolarGreen

## 🌍 Overview
**SolarGreen** is a web-based platform that allows users to upload utility bills. The system extracts the user's name and address using **Ollama**, fetches a satellite image of their house, and calculates the rooftop area suitable for solar panel installation. A custom proposal is then generated, offering the user rental income from leasing their roof for solar energy production.

## 🚀 Features
- 📂 **Bill Upload**: Upload utility bills for processing.
- 🔎 **Information Extraction**: Extracts user name and address using Ollama.
- 🌍 **Satellite Imaging**: Retrieves satellite imagery of user property.
- 🛍️ **Rooftop Analysis**: Calculates usable rooftop area for solar panels.
- 📋 **Proposal Generation**: Offers a leasing proposal with shared energy profits.
- 🔗 **SAM Integration**: Uses Meta's Segment Anything Model (SAM) for precise rooftop segmentation.

## 💻 Tech Stack
- **Backend**: Python (FastAPI)
- **Database**: MongoDB
- **Machine Learning**: Ollama (OCR), Segment Anything by Meta (SAM)
- **APIs**: Google Maps/Satellite imagery providers
- **DevOps**: Docker & Docker Compose

## 📂 Project Structure
```bash
.
├── README.md
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── endpoints
│   │       ├── __init.py
│   │       ├── bill_upload.py
│   │       ├── moderate_user.py
│   │       ├── sam_process.py
│   │       └── user
│   │           ├── __init__.py
│   │           ├── get.py
│   │           └── validate.py
│   └── core
│       ├── __init__.py
│       └── config.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └── user_schema.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── googlemaps
│   │   ├── mongo
│   │   │   ├── __init__.py
│   │   │   └── user.py
│   │   ├── ollama
│   │   │   ├── __init__.py
│   │   │   ├── handler.py
│   │   │   └── prompts.py
│   │   ├── segment_anything
│   │   │   ├── __init__.py
│   │   │   ├── model
│   │   │   │   ├── sam_vit_h.pth
│   │   │   │   └── sam_vit_h_4b8939.pth:Zone.Identifier
│   │   │   └── sam.py
│   │   └── supabase
│   │       ├── __init__.py
│   │       └── service.py
│   └── utils
│       ├── __init__.py
│       ├── db.py
│       └── url_to_text.py
├── main.py
├── pytest.ini
├── requirements.txt
├── scripts
└── test
    └── services
        └── test_sam.py
```

## 🚧 Installation & Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/solargreen.git
   cd solargreen
   ```
2. **Create conda environment**:
    ```bash
    conda env create -f requirements.yaml
    conda activate solar-rooftop
    ```
   ```

3. **Run the server**:
   ```bash
   uvicorn main:app --reload
   ```

## 🗓️ API Endpoints
| Method | Endpoint                  | Description                        |
|--------|---------------------------|------------------------------------|
| POST   | /upload-bill              | Upload a utility bill              |
| POST   | /user/validate            | Validate user details              |
| POST   | /user/get_by_id           | Fetch user by ID                   |
| GET    | /user/get_all             | Retrieve all users                 |
| POST   | /user/get_by_moderation_status | Get users by moderation status  |
| POST   | /admin/moderate           | Moderate a user profile            |
| POST   | /sam/process              | Process satellite image with SAM   |

## 🚀 Future Enhancements
- AI optimization for solar panel placement
- Real-time energy pricing integration
- User dashboard for analytics and earnings tracking

## 📄 License
This project is licensed under the [MIT License](LICENSE).

## 👤 Contributors
- **[kapeeshkaul]**
- **[satilog]**

