# Medical Chatbot Microservices - Project Status

## Overview
This project implements a **stateless microservice-based chatbot system** for Israeli health funds (Maccabi, Meuhedet, Clalit) that provides medical service information based on user-specific data.

## Requirements (from readme.md)
- **Stateless FastAPI microservice** with Azure OpenAI integration
- **Streamlit frontend** with two-phase user flow
- **Multi-language support** (Hebrew/English)
- **Two-prompt system**: User information collection + Medical Q&A
- **Client-side state management** (no server memory)
- **Comprehensive error handling and logging**

---

## ✅ COMPLETED TASKS

### 1. Data Preprocessing System ✅
**Location:** `preprocessing/`

**What we built:**
- `html_to_json.py` - Converts HTML files to structured JSON (6 medical service categories)
- `generate_user_data.py` - Creates user-specific text files for each HMO + tier combination (9 files total)
- `run_all.py` - Complete preprocessing pipeline

**Output:**
- `jsons/` - 6 structured JSON files (one per medical service)
- `user_specific_data/` - 9 comprehensive text files with all medical services for specific user profiles
- Each text file contains ALL medical information for a specific HMO + membership tier combination

### 2. Project Structure & Configuration ✅
**Professional folder structure:**
```
Medical-Chatbot-Microservices/
├── backend/               # FastAPI microservice
├── frontend/              # Streamlit app (pending)
├── config/                # Settings & prompts
├── utils/                 # Helper utilities
├── preprocessing/         # Data processing scripts
├── user_specific_data/    # User-specific medical context files
├── jsons/                 # Structured medical data
└── requirements.txt       # Dependencies
```

**Configuration files:**
- `.env` & `.env.example` - Environment variables
- `config/settings.py` - Settings management
- `.gitignore` - Version control exclusions

### 3. Two-Prompt System Design ✅
**Location:** `config/prompts/`

**Prompt 1 - User Information Collection:**
- `user_info_collection.py` - Conversational data collection prompt
- Validates: Name, ID (9 digits), gender, age (0-120), HMO, HMO card (9 digits), membership tier
- Returns structured JSON when complete
- **No hardcoded form logic** - purely conversational through LLM

**Prompt 2 - Medical Q&A:**
- `medical_qa.py` - Medical service Q&A with user context injection
- Uses user-specific data files for personalized responses
- Supports both Hebrew and English
- Includes safety restrictions (no personal medical advice)

### 4. Multi-Language Support ✅
**Location:** `utils/helpers/language_utils.py`

**Features:**
- **Simple language detection** from current message only
- **Validation against SUPPORTED_LANGUAGES** from config
- **Automatic fallback** to DEFAULT_LANGUAGE
- **Multilingual error messages** for consistent UX
- **Configuration-driven** (easily add new languages)

### 5. FastAPI Backend Implementation ✅
**Location:** `backend/`

**API Endpoints:**
- `GET /api/v1/health` - System health check
- `POST /api/v1/user-info-collection` - Conversational user data collection
- `POST /api/v1/medical-qa` - Medical Q&A with user context

**Key Components:**
- `models/schemas.py` - Pydantic data models with validation
- `services/azure_openai_service.py` - Azure OpenAI client with configurable parameters
- `api/` - RESTful API endpoints with comprehensive error handling
- `main.py` - FastAPI application with CORS middleware

**Azure OpenAI Integration:**
- Configurable temperatures (0.3 for user info, 0.1 for medical Q&A)
- Configurable max tokens (1500 for user info, 10000 for medical Q&A)
- Uses GPT-4o Mini for user info collection (cost-effective)
- Uses GPT-4o for medical Q&A (higher accuracy needed)

### 6. Context Loading System ✅
**Location:** `utils/helpers/context_loader.py`

**Features:**
- Loads user-specific medical context from preprocessed files
- Validates HMO + membership tier combinations
- Provides complete medical service information for user's specific profile

---

## 🚧 REMAINING TASKS

### 1. Build Streamlit Frontend (IN PROGRESS)
**Location:** `frontend/` (to be created)

**Requirements:**
- **Two-phase user interface:**
  1. User information collection phase (conversational)
  2. Medical Q&A phase (chat interface)
- **Client-side state management** (conversation history, user info)
- **Integration with FastAPI backend**
- **Multi-language support** (Hebrew/English text direction)
- **Real-time chat interface** with message history

### 2. Implement Comprehensive Error Handling and Logging System
**Location:** `utils/logging/` (to be created)

**Requirements:**
- Structured logging with timestamps
- Error tracking and monitoring
- Request/response logging for debugging
- Performance metrics logging
- Log rotation and management

### 3. Add User Information Validation
**Location:** `utils/validators/` (to be created)

**Requirements:**
- Israeli ID number validation algorithm
- Age range validation (0-120)
- HMO card number validation
- Input sanitization and security
- Field format validation

### 4. Testing and Optimization for Concurrent Users
**Location:** `tests/` (to be created)

**Requirements:**
- Unit tests for all components
- Integration tests for API endpoints
- Load testing for concurrent users
- Azure OpenAI rate limit handling
- Performance optimization
- Error recovery testing

---

## 🔧 NEXT STEPS FOR CONTINUATION

### Immediate Priority: Streamlit Frontend
1. Create `frontend/app.py` - Main Streamlit application
2. Implement two-phase user flow:
   - Phase 1: User info collection with conversational interface
   - Phase 2: Medical Q&A chat interface
3. Add session state management for conversation history
4. Integrate with FastAPI backend endpoints
5. Handle Hebrew text direction and multilingual UI

### Configuration for Next Model
The next model should:
1. **Review the existing backend** in `backend/main.py` to understand API structure
2. **Check the data structure** in `user_specific_data/` to see the medical context format
3. **Use the language utilities** in `utils/helpers/language_utils.py` for consistent language handling
4. **Follow the established patterns** for error handling and configuration management

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up Azure OpenAI credentials in .env file
# Edit AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY

# Run preprocessing (if needed)
python preprocessing/run_all.py

# Start FastAPI backend
python backend/main.py

# Start Streamlit frontend (when created)
streamlit run frontend/app.py
```

---

## 📋 Technical Decisions Made

1. **Language Detection**: Simple character counting with fallback to default (not complex NLP)
2. **Context Loading**: Pre-processed files per user profile (not real-time processing)
3. **Error Handling**: Multilingual with configuration-driven messages
4. **State Management**: Client-side only (stateless microservice architecture)
5. **Azure OpenAI Usage**: Different models for different phases (GPT-4o Mini vs GPT-4o)
6. **Data Structure**: One JSON per medical service + user-specific text files for context injection

The foundation is solid and well-structured. The remaining work focuses on frontend implementation and system hardening.