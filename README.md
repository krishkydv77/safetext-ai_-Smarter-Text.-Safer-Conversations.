# SafeText AI — Smarter Text. Safer Conversations.

**An AI-powered text moderation mini-project for safer digital conversations.**

SafeText AI is a text moderation API built with Python and FastAPI. It combines rule-based filtering, Hinglish profanity detection, URL-pattern detection, Redis caching, and Google Gemini integration to explore practical text safety workflows.

##  Project Overview

SafeText AI analyzes user-submitted text and returns a structured moderation result indicating whether the content has been flagged, its category, a cleaned version of the text, and an explanation.

The project demonstrates how backend APIs, rule-based text processing, caching, and generative AI integration can be combined in a modular application.

##  Key Features

- **Rule-Based Moderation:** Detect configured profanity terms and URL patterns.
- **Hinglish Text Filtering:** Apply configured profanity rules to Hindi-English mixed text.
- **Profanity Masking:** Replace detected terms with masking characters.
- **URL Pattern Detection:** Flag text containing matching HTTP or HTTPS URL patterns.
- **Structured JSON Responses:** Return moderation status, category, cleaned text, explanation, source, and confidence label.
- **Redis Caching:** Cache moderation results for repeated text inputs with a one-hour expiration.
- **Gemini API Integration:** Includes a Google Gemini service for text classification.
- **FastAPI Backend:** Expose the moderation functionality through a REST API.
- **Pydantic Validation:** Validate incoming request data and structure API responses.
- **Interactive API Documentation:** Explore and test the endpoint through Swagger UI.

> **Implementation note:** The current rule-based function returns a result for every input category (`clean`, `spam`, or `profanity`). Consequently, the Gemini fallback in the current pipeline is not reached. The Gemini service is integrated into the codebase, but the fallback routing needs an update to make it operational.

##  Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.12+ | Core development |
| FastAPI | REST API development |
| Google Gemini API | AI-based text classification integration |
| Redis | Moderation-result caching |
| Pydantic | Request and response validation |
| Uvicorn | ASGI application server |
| SlowAPI | Rate-limiting dependency |
| uv | Python project and dependency management |
| Git & GitHub | Version control |

##  How It Works

1. **Receive Input:** The API accepts text, a user ID, and optional context.
2. **Check Cache:** Redis checks whether a result is already cached for the input text.
3. **Apply Rules:** The rule-based filter checks for URL patterns and configured profanity terms.
4. **Generate Result:** The filter returns a moderation category and associated metadata.
5. **Cache Result:** The moderation result is stored in Redis for one hour.
6. **Return Response:** FastAPI returns the structured JSON result to the client.

### Architecture

```text
Client Request
      |
      v
FastAPI Endpoint
/api/v1/moderate
      |
      v
Request Validation
(Pydantic)
      |
      v
Redis Cache Check
      |
      +---- Cache Hit ----> Cached Result
      |
      v
Rule-Based Filter
      |
      +---- URL Pattern
      |
      +---- Profanity Match
      |
      +---- No Match
      |
      v
Moderation Result
      |
      v
Redis Cache
      |
      v
Structured JSON Response
```

**Gemini integration:** A Gemini classification service and fallback branch are present in the code. The fallback requires a routing fix because the current rule-based function already returns a result for every input.


##  Getting Started

### Prerequisites

- Python 3.12 or later
- Redis server
- Google Gemini API key
- Git
- uv package manager (recommended)

### 1. Clone the Repository

If your GitHub repository has been renamed to `safetext-ai`:

```bash
git clone https://github.com/krishkydv77/safetext-ai.git
cd safetext-ai
```

If you have not renamed the repository, use its current GitHub clone URL instead.

### 2. Create a Virtual Environment

```bash
uv venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

Using uv:

```bash
uv sync
```

Alternatively, install the listed dependencies using pip:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root containing:

```env
GEMINI_API_KEY=your_gemini_api_key
REDIS_URL=redis://localhost:6379
RATE_LIMIT=30
```

Replace the placeholder with your own Gemini API key.

The application settings require `GEMINI_API_KEY` during initialization. Never commit your `.env` file or expose API keys in source code.

### 5. Start Redis

Ensure Redis is installed and running at the URL configured in `.env`.

Test the Redis connection:

```bash
redis-cli ping
```

Expected output:

```text
PONG
```

Redis must be reachable because the current moderation pipeline accesses the cache for requests.

### 6. Run the API

From the project root:

```bash
uvicorn app.main:app --reload
```

The local API will be available at:

```text
http://127.0.0.1:8000
```

##  API Testing

### Interactive API Documentation

Open Swagger UI in your browser:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Use the `POST /api/v1/moderate` endpoint to submit moderation requests.

### Request Format

The `text` and `user_id` fields are required. The `context` field is optional.

```json
{
  "text": "Hello, how can I help you today?",
  "user_id": "demo_user_01",
  "context": "customer_support"
}
```

### Example 1: Clean Text

**Request:**

```json
{
  {
  "text": "yaar ye class bakwas thi",
  "user_id": "user_10432",
  "context": "course_review"      // optional: chat | course_review | comment
}

}
```

**Expected response with the current rule-based implementation:**

```json
{
  "is_flagged": true,
  "category": "profanity",        // clean | profanity | spam | harassment | other
  "cleaned_text": "yaar ye class ****** thi",
  "explanation": "Contains a Hinglish profanity term",
  "source": "rule_based",         // cache | rule_based | gemini_llm
  "confidence": "high"
}
```

### Example 2: URL Pattern Detection

**Request:**

```json
{
  "text": "Please visit https://example.com",
  "user_id": "demo_user_02"
}
```

**Expected response:**

```json
{
  "is_flagged": true,
  "category": "spam",
  "cleaned_text": "Please visit https://example.com",
  "explanation": "Contains a URL pattern",
  "source": "rule_based",
  "confidence": "high"
}
```

### Example 3: Profanity Detection

Submit a message containing a term configured in `app/data/profanity_wordlist.py`.

The current implementation returns a response with:

- `is_flagged`: `true`
- `category`: `profanity`
- `cleaned_text`: text with the matched term masked
- `explanation`: a message describing the matched term
- `source`: `rule_based`
- `confidence`: `high`

Actual detection depends on the configured wordlist and matching logic.

> **Note:** These examples reflect the current rule-based response structure. Results depend on the input and configured rules. The confidence field is a categorical label (`high`), not a calibrated numerical probability.

##  Security and Reliability

- Keep API keys and other secrets in environment variables.
- Add `.env`, `.venv/`, `__pycache__/`, and compiled Python files to `.gitignore`.
- Avoid logging sensitive user messages or credentials.
- Handle Redis connection failures and Gemini API errors appropriately.
- Review profanity matching and masking behavior before using real user content.
- Add request size limits and enforce rate limiting before exposing the API publicly.
- Treat moderation decisions as signals for review, not guaranteed proof that content is safe or unsafe.

**Rate-limiting status:** SlowAPI is included and a limiter is configured in the project, but the current endpoint does not apply the rate-limit decorator and the application does not register the SlowAPI exception handler. Rate limiting should not be considered active until those pieces are implemented and tested.

##  Potential Use Cases

- Chat application moderation experiments
- Customer support text filtering
- Hinglish profanity detection
- API-based text safety checks
- Exploring rule-based and LLM-based moderation architectures


##  Learning Outcomes

This mini-project explores:

- REST API development with FastAPI
- Request and response validation with Pydantic
- Rule-based text processing
- Google Gemini API integration
- Redis caching and expiration
- Environment-based configuration
- Modular backend architecture
- API testing and responsible moderation design



- GitHub: [@krishkydv77](https://github.com/krishkydv77)
- LinkedIn: [Krishan Kumar Yadav](https://www.linkedin.com/in/krishan-kumar7/)



**SafeText AI — Smarter Text. Safer Conversations.**

*A mini-project exploring text moderation, AI integration, caching, and backend engineering.*
