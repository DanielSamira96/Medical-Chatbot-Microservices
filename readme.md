# 🏥 Medical Chatbot Microservices

A comprehensive **stateless microservice-based chatbot system** that provides personalized medical service information for Israeli health funds (Maccabi, Meuhedet, and Clalit). The system adapts responses based on user's HMO and membership tier, supporting both Hebrew and English languages.

## 🎯 Project Goal

This chatbot helps Israeli residents navigate their health insurance benefits by providing detailed, personalized information about:
- **Alternative Medicine (רפואה משלימה)** - Acupuncture, homeopathy, naturopathy and more
- **Communication Clinics (מרפאות תקשורת)** - Speech, language and swallowing disorder treatments  
- **Dental Clinics (מרפאות שיניים)** - Comprehensive dental care services
- **Optometry (אופטומטריה)** - Eye exams, glasses and contact lenses
- **Pregnancy Services (שירותי הריון)** - Pregnancy monitoring and support
- **Health Workshops (סדנאות בריאות)** - Educational health programs

## 🏗️ Architecture

### Microservice Design
- **Stateless Backend**: FastAPI-based REST API with no server-side session storage
- **Client-Side State Management**: All user data and conversation history maintained in Streamlit frontend
- **Dual Azure OpenAI Integration**: 
  - GPT-4o for complex medical Q&A
  - GPT-4o Mini for user information collection
- **Multi-language Support**: Real-time language detection and response adaptation

### Project Structure
```
Medical-Chatbot-Microservices/
├── backend/                    # FastAPI microservice
│   ├── api/                   # API endpoints
│   │   ├── health.py          # Health check endpoint
│   │   ├── user_info.py       # User information collection
│   │   └── medical_qa.py      # Medical Q&A endpoint
│   ├── models/                # Pydantic schemas
│   ├── services/              # Azure OpenAI service layer
│   └── main.py               # FastAPI application
├── frontend/                  # Streamlit web interface
│   ├── app.py                # Main Streamlit application
│   ├── user_info/            # User information collection phase
│   ├── medical_qa/           # Medical Q&A phase
│   └── utils/                # Frontend utilities and styling
├── config/                   # Configuration and prompts
│   ├── settings.py           # Environment-based configuration
│   └── prompts/              # LLM system prompts
├── preprocessing/            # Data transformation pipeline
│   ├── html_to_json.py       # HTML to structured JSON converter
│   ├── generate_user_data.py # User-specific data generator
│   └── jsons/               # Processed medical service data
├── utils/                   # Shared utilities
│   ├── helpers/             # Language detection, context loading
│   ├── logging/             # Comprehensive logging system
│   └── validators/          # User information validation
└── requirements.txt         # Python dependencies
```

## 🔄 Data Preprocessing Pipeline

The system transforms raw HTML medical service data into **personalized context files** for each user type:

### Step 1: HTML to JSON Conversion
- **Input**: Raw HTML files from `phase2_data/` containing medical service information
- **Process**: Extracts titles, descriptions, and service details using BeautifulSoup
- **Output**: Structured JSON files in `preprocessing/jsons/`

The preprocessing transforms unstructured HTML into structured JSON:
```json
{
  "title": "רפואה משלימה (רפואה אלטרנטיבית)",
  "general_description": "Overview of alternative medicine services...",
  "specific_description": {
    "מכבי": "HMO-specific service description...",
    "מאוחדת": "HMO-specific service description...", 
    "כללית": "HMO-specific service description..."
  },
  "services_descriptions": {
    "דיקור סיני": "Service-specific details...",
    "הומיאופתיה": "Service-specific details..."
  }
}
```

### Step 2: User-Specific Context Generation ⭐ **FINAL OUTPUT**
- **Input**: Structured JSON + user's HMO and membership tier
- **Process**: Creates 9 personalized context files combining all medical services tailored for each specific user type
- **Output**: **`user_specific_data/`** containing the final context files used by the chatbot:
  ```
  מכבי_זהב.txt    מכבי_כסף.txt    מכבי_ארד.txt
  מאוחדת_זהב.txt  מאוחדת_כסף.txt  מאוחדת_ארד.txt  
  כללית_זהב.txt   כללית_כסף.txt   כללית_ארד.txt
  ```

### Personalized Context Structure
Each final context file contains all medical services formatted specifically for that user type:
```text
=== נתוני שירותים רפואיים עבור מכבי - זהב ===

## רפואה משלימה (רפואה אלטרנטיבית)
### תיאור כללי: [service overview]
### פירוט שירותים:
**דיקור סיני (אקופונקטורה):**
תיאור: [service description]
הטבות: 70% הנחה, עד 20 טיפולים בשנה

## מרפאות תקשורת
[specific benefits and coverage for this HMO-tier combination]
...
```

🎯 **These 9 context files are the actual knowledge base used by the chatbot** - each user gets their specific file loaded based on their HMO and membership tier, ensuring 100% personalized and accurate responses.

## 🌟 Key Features

### Two-Phase Conversation Flow
1. **User Information Collection**
   - Natural language conversation (no forms!)
   - Validates Israeli ID numbers (9 digits)
   - Collects: Name, age, gender, HMO, membership tier
   - Automatic language detection and adaptation
   - English-to-Hebrew translation for standardization

2. **Medical Q&A**
   - Personalized responses based on user's HMO and tier
   - Real-time language switching support
   - Comprehensive logging for monitoring and analytics

### Advanced Language Support
- **Automatic Language Detection**: Analyzes Hebrew vs English characters
- **Dynamic Response Language**: Adapts to user's current message language
- **UI Language Selection**: Persistent language preference with CSS RTL support
- **Translation Pipeline**: Converts English inputs (Clalit/Silver) to Hebrew (כללית/כסף)

### Robust Validation System
- **User Information**: ID validation, age ranges, HMO verification
- **Input Sanitization**: Comprehensive data cleaning and validation
- **Error Handling**: Multilingual error messages with graceful fallbacks

## 🚀 Setup and Installation

### Prerequisites
- Python 3.9+
- Azure OpenAI API access (dual endpoints: GPT-4o and GPT-4o Mini)

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Medical-Chatbot-Microservices
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Copy the example configuration file and update with your Azure credentials:
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` with your actual Azure OpenAI credentials:
   ```env
   # Azure OpenAI Configuration - GPT-4o (for Medical Q&A)
   AZURE_OPENAI_ENDPOINT=https://your-gpt4o-resource-name.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-gpt4o-api-key-here
   AZURE_OPENAI_API_VERSION=2024-02-01

   # Azure OpenAI Configuration - GPT-4o-mini (for User Info Collection)
   AZURE_OPENAI_MINI_ENDPOINT=https://your-gpt4o-mini-resource-name.openai.azure.com/
   AZURE_OPENAI_MINI_API_KEY=your-gpt4o-mini-api-key-here
   AZURE_OPENAI_MINI_API_VERSION=2024-02-01

   # Model Configuration
   GPT_4O_DEPLOYMENT_NAME=gpt-4o
   GPT_4O_MINI_DEPLOYMENT_NAME=gpt-4o-mini

   # Application Configuration
   APP_HOST=localhost
   APP_PORT=8000
   DEFAULT_LANGUAGE=he
   SUPPORTED_LANGUAGES=he,en
   
   # Additional settings available in .env.example...
   ```

### Data Preprocessing

Before running the application, process the medical service data:

```bash
# Run the complete preprocessing pipeline
python preprocessing/run_all.py
```

This will:
1. Convert HTML files to structured JSON
2. Generate user-specific data files for all HMO-tier combinations
3. Create the knowledge base for personalized responses

## 🏃‍♂️ Running the Application

### Start the Backend (FastAPI)
```bash
python backend/main.py
```
Backend will be available at: `http://localhost:8000`

### Start the Frontend (Streamlit)
```bash
streamlit run frontend/app.py
```
Frontend will be available at: `http://localhost:8501`

### Health Check
Verify the system is running:
```bash
curl http://localhost:8000/api/v1/health
```

## 🔧 Configuration

### Environment Variables
All configuration is handled through environment variables in `.env`:

- **Azure OpenAI Settings**: Dual endpoint configuration for different models
- **Application Ports**: Customizable backend and frontend ports  
- **Language Settings**: Default language and supported languages
- **Logging Configuration**: Log levels, file paths, and rotation settings

### Model Parameters
- **User Info Collection**: Lower temperature (0.3) for consistent data collection
- **Medical Q&A**: Very low temperature (0.1) for factual medical information
- **Token Limits**: Optimized for each phase (1500 for user info, 8000 for medical Q&A)

## 📝 API Documentation

### User Information Collection
```
POST /api/v1/user-info-collection
```
Manages conversational user information collection with validation.

### Medical Q&A
```
POST /api/v1/medical-qa  
```
Provides personalized medical service information based on user context.

### Health Check
```
GET /api/v1/health
```
System health and configuration validation.

## 🎨 User Experience

### Seamless Flow
1. **Language Selection**: Choose Hebrew or English (changeable anytime)
2. **Natural Conversation**: Chat-based information collection (no forms!)
3. **Automatic Transition**: Smooth flow from data collection to Q&A
4. **Personalized Responses**: All answers tailored to user's HMO and membership tier

### Multi-language Support
- **RTL Support**: Proper Hebrew text rendering
- **Dynamic Language Switching**: Change language mid-conversation
- **Consistent Translations**: Standardized medical terminology
