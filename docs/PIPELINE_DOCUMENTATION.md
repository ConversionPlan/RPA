# CI/CD Pipeline Documentation - GitHub Actions

## Overview

This pipeline automates the execution of RPA (Robotic Process Automation) tests using Selenium WebDriver and Behave/BehaveX. Results are automatically sent to Slack and stored in MinIO S3.

**File:** `.github/workflows/github-actions.yml`

---

## When the Pipeline Runs

The pipeline has two triggers:

### 1. Push to main branch
```yaml
on:
  push:
    branches:
      - main
```
Whenever there is a commit to the `main` branch, the pipeline runs automatically.

### 2. Daily schedule
```yaml
schedule:
  - cron: "0 6 * * *"
```
Automatic execution **every day at 6:00 AM UTC** (3:00 AM Brasília time during daylight saving, 2:00 AM otherwise).

---

## Execution Environment

**Operating System:** Ubuntu Latest
```yaml
runs-on: ubuntu-latest
```

---

## Pipeline Steps

### 1️⃣ Disable GOPROXY
```yaml
- name: Disable GOPROXY
  run: echo "GOPROXY=off" >> $GITHUB_ENV
```
**Purpose:** Disables Go proxy to avoid network conflicts.

---

### 2️⃣ Check out repository code
```yaml
- name: Check out repository code
  uses: actions/checkout@v4
```
**Purpose:** Clones the repository into the GitHub Actions execution environment.

**Action used:** `actions/checkout@v4`

---

### 3️⃣ Set up Python 3.13
```yaml
- name: Set up Python 3.13
  uses: actions/setup-python@v5
  with:
    python-version: 3.13
```
**Purpose:** Installs and configures Python 3.13 in the environment.

**Action used:** `actions/setup-python@v5`

---

### 4️⃣ Set up NPM
```yaml
- name: Set up NPM
  uses: actions/setup-node@v4
```
**Purpose:** Installs Node.js and NPM to allow Lighthouse installation.

**Action used:** `actions/setup-node@v4`

---

### 5️⃣ Set up Chrome
```yaml
- name: Set up Chrome
  uses: browser-actions/setup-chrome@v1
- run: chrome --version
```
**Purpose:**
- Installs Google Chrome in the environment
- Verifies the installed version

**Action used:** `browser-actions/setup-chrome@v1`

**Why Chrome?** Selenium tests automate Chrome browser in headless mode.

---

### 6️⃣ Install dependencies
```yaml
- name: Install dependencies
  run: pip install -r requirements.txt
```
**Purpose:** Installs all Python dependencies listed in `requirements.txt`:
- `selenium`: Browser automation
- `behave` / `behavex`: BDD testing framework
- `webdriver-manager`: Automatic ChromeDriver management
- Other required libraries

---

### 7️⃣ Install Lighthouse
```yaml
- name: Install Lighthouse
  run: npm i -g lighthouse
```
**Purpose:** Installs Lighthouse globally for web performance analysis.

**Note:** Lighthouse is used to measure performance metrics of tested pages.

---

### 8️⃣ Run tests
```yaml
- name: Run tests
  run: |
    mkdir -p report/output
    HEADLESS=True behavex --parallel-processes 1 --parallel-scheme scenario -o report/output
```
**Purpose:** **MAIN STEP** - Executes RPA tests.

**Details:**
- `mkdir -p report/output`: Creates output directory
- `HEADLESS=True`: Runs Chrome without graphical interface
- `behavex`: Extended BDD testing framework
- `--parallel-processes 1`: Executes 1 process (sequential execution)
- `--parallel-scheme scenario`: Parallelizes by scenario
- `-o report/output`: Output directory for results

**Estimated duration:** 20-25 minutes

**Recent change:** Changed from 4 parallel processes to 1 sequential process for improved stability.

---

### 9️⃣ Print errors
```yaml
- name: Print errors
  if: failure()
  run: python report/print_errors.py
```
**Purpose:** If tests fail, runs script that prints detailed errors to the log.

**Condition:** Only runs if previous step fails (`if: failure()`)

---

### 🔟 Archive production artifacts
```yaml
- name: Archive production artifacts
  if: success() || failure()
  uses: actions/upload-artifact@v4
  with:
    name: dist-without-markdown
    path: report/output
```
**Purpose:** Uploads test results as GitHub Actions artifact.

**Condition:** Always runs (`if: success() || failure()`)

**Action used:** `actions/upload-artifact@v4`

**Artifacts included:**
- JSON files with results
- Failure screenshots
- Execution logs

---

### 1️⃣1️⃣ Run bot
```yaml
- name: Run bot
  if: success() || failure()
  env:
    SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
    GITHUB_REPOSITORY: ${{ github.repository }}
    GITHUB_RUN_ID: ${{ github.run_id }}
    GITHUB_RUN_NUMBER: ${{ github.run_number }}
    GITHUB_ACTOR: ${{ github.actor }}
    GITHUB_SHA: ${{ github.sha }}
    GITHUB_REF: ${{ github.ref }}
    GITHUB_WORKFLOW: ${{ github.workflow }}
    GITHUB_SERVER_URL: ${{ github.server_url }}
    GITHUB_EVENT_NAME: ${{ github.event_name }}
    MINIO_ENDPOINT: ${{ secrets.MINIO_ENDPOINT }}
    MINIO_BUCKET: ${{ secrets.MINIO_BUCKET }}
  run: |
    echo "[INFO] Running Slack bot..."
    python report/bot.py
```
**Purpose:** **Sends notification to Slack** with test summary.

**Condition:** Always runs

**Secrets required:**
- `SLACK_BOT_TOKEN`: Slack bot authentication token
- `MINIO_ENDPOINT`: MinIO server URL
- `MINIO_BUCKET`: MinIO bucket name

**What the bot sends:**
- Number of passed/failed scenarios
- Success rate
- Detailed statistics per feature
- Links to artifacts and MinIO
- Failure details in thread (if any)
- GitHub context information

---

### 1️⃣2️⃣ Generate PDF file
```yaml
- name: Generate PDF file
  if: success() || failure()
  run: python report/generate_pdf.py
```
**Purpose:** Generates PDF report with test results.

**Condition:** Always runs

**File generated:** `report/output/Track_Validation.pdf`

---

### 1️⃣3️⃣ Get current date
```yaml
- name: Get current date
  if: success() || failure()
  id: DATE
  run: echo "DATE=$(date +'%m%d%YT%H%M%S')" >> $GITHUB_ENV
```
**Purpose:** Captures current date/time to name files with timestamp.

**Format:** `MMDDYYYYTHHmmss` (e.g., `10292025T143025`)

**Environment variable:** `${{ env.DATE }}`

---

### 1️⃣4️⃣ Rename PDF
```yaml
- name: Rename PDF
  if: success() || failure()
  run: |
    if [ -f report/output/Track_Validation.pdf ]; then
      mv report/output/Track_Validation.pdf report/output/Track_Validation_${{ env.DATE }}.pdf
    fi
```
**Purpose:** Renames PDF by adding timestamp to the name.

**Example:** `Track_Validation.pdf` → `Track_Validation_10292025T143025.pdf`

---

### 1️⃣5️⃣ Rename and copy JSON files
```yaml
- name: Rename and copy JSON files
  if: success() || failure()
  run: |
    if [ -f report/output/report.json ]; then
      cp report/output/report.json report/output/report_${{ env.DATE }}.json
    fi
    if [ -f report/output/results.json ]; then
      cp report/output/results.json report/output/results_${{ env.DATE }}.json
    fi
```
**Purpose:** Creates copies of JSON files with timestamp.

**Files:**
- `report.json` → `report_10292025T143025.json`
- `results.json` → `results_10292025T143025.json`

**Why copy instead of move?** Keeps original files for immediate reference.

---

### 1️⃣6️⃣ Upload Folder (MinIO S3)
```yaml
- name: Upload Folder
  if: success() || failure()
  uses: yakubique/minio-upload@v1.1.3
  with:
    endpoint: ${{ secrets.MINIO_ENDPOINT }}
    access_key: ${{ secrets.MINIO_ACCESS_KEY }}
    secret_key: ${{ secrets.MINIO_SECRET_KEY }}
    bucket: ${{ secrets.MINIO_BUCKET }}
    source: 'report/output'
    target: '/'
    recursive: true
```
**Purpose:** **Uploads all results to MinIO S3** (object storage).

**Condition:** Always runs

**Action used:** `yakubique/minio-upload@v1.1.3`

**Secrets required:**
- `MINIO_ENDPOINT`: MinIO server URL (e.g., `https://minio.example.com`)
- `MINIO_ACCESS_KEY`: Access key
- `MINIO_SECRET_KEY`: Secret key
- `MINIO_BUCKET`: Bucket name (e.g., `rpa-test-results`)

**Configuration:**
- `source: 'report/output'`: Local folder to be sent
- `target: '/'`: Bucket root folder
- `recursive: true`: Recursively sends all subdirectories

**Files uploaded:**
- PDFs with timestamp
- JSONs with timestamp
- Screenshots
- Logs
- Feature files

---

## Configured Secrets

Secrets are sensitive environment variables configured in GitHub:

| Secret | Purpose | Example |
|--------|---------|---------|
| `SLACK_BOT_TOKEN` | Slack bot authentication token | `xoxb-...` |
| `MINIO_ENDPOINT` | MinIO server URL | `https://s3.example.com` |
| `MINIO_ACCESS_KEY` | MinIO access key | `minioadmin` |
| `MINIO_SECRET_KEY` | MinIO secret key | `minioadmin123` |
| `MINIO_BUCKET` | MinIO bucket name | `rpa-results` |

**How to configure:** `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

---

## Generated Artifacts

### GitHub Actions Artifacts
- Name: `dist-without-markdown`
- Content: Complete `report/output` folder
- Retention: 90 days (default)

### MinIO S3
- Location: `<MINIO_BUCKET>/`
- Files with timestamp for history
- Retention: Permanent (until manual removal)

### Slack
- Message with test summary
- Link to GitHub Actions artifacts
- Link to MinIO storage
- Failure details in thread

---

## Complete Pipeline Flow

```
┌─────────────────────────────────────────────────────────────┐
│  TRIGGER: Push to main OR Daily cron at 6:00 AM UTC        │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  1. Setup: Python 3.13 + NPM + Chrome + Dependencies       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  2. Run Tests (behavex --parallel-processes 1)             │
│     Duration: ~20-25 minutes                                │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  3. Generate Reports (PDF + JSON)                          │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  4. Add Timestamp to Files                                 │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  5. Distribute Results                                      │
│     ├─ GitHub Actions Artifacts                            │
│     ├─ Slack Notification                                  │
│     └─ MinIO S3 Upload                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Recent Improvements Applied

### Commit: deb0e54 (Latest)
**Date:** October 29, 2025

**Changes:**
- ✅ Fixed dict append error in auth.py for test_times.json
- ✅ Added type checking to ensure test_times.json is always a list
- ✅ Converts corrupted dict to empty list
- ✅ Resolves 'dict' object has no attribute 'append' error that caused failures in all tests

**Problem solved:**
- Tests failing with AttributeError when test_times.json contained dict instead of list
- Improved error handling and logging

### Commit: 4157025
**Date:** October 29, 2025

**Changes:**
- ✅ Changed test execution from parallel to sequential mode
- ✅ `--parallel-processes 4` → `--parallel-processes 1`
- ✅ `--parallel-scheme feature` → `--parallel-scheme scenario`

**Problem solved:**
- Improved test stability
- Reduced resource contention
- Decreased Chrome/Selenium session errors

### Commit: 0337d4b
**Date:** October 29, 2025

**Changes:**
- ✅ Added complete failure details in Slack thread
- ✅ Chunked messages when more than 5 failures
- ✅ Added quick actions in separate thread message

**Problem solved:**
- Slack 50-block limit exceeded
- Better visibility of detailed failure information

