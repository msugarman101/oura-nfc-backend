# Oura NFC Tag Creator - Deployment Guide

## Step 1: Get Your Oura Personal Access Token

1. Go to: https://cloud.ouraring.com/personal-access-tokens
2. Click **"Create a new personal access token"**
3. Name it: `NFC Tag Creator`
4. Click **Create**
5. **Copy the token** (you'll only see it once!) and save it somewhere safe

---

## Step 2: Deploy on Render (Free)

### 2a. Create a GitHub Repository (2 minutes)

1. Go to https://github.com/new
2. Repository name: `oura-nfc-backend`
3. Description: `Oura NFC Tag Creator`
4. Choose **Public** (easier for Render)
5. Click **Create repository**

### 2b. Upload Files to GitHub

1. Click **"Add file"** → **"Upload files"**
2. Drag and drop these 3 files:
   - `oura_nfc_backend.py`
   - `requirements.txt`
   - Create a new file called `Procfile` with this content:
     ```
     web: gunicorn oura_nfc_backend:app
     ```

3. Click **"Commit changes"**

### 2c. Deploy to Render

1. Go to https://render.com
2. Sign up (free, no credit card needed)
3. Click **New +** (top right)
4. Select **Web Service**
5. Choose **Deploy existing code from a repository**
6. Paste your GitHub repo URL from Step 2a
7. Click **Connect**
8. Fill in the form:
   - **Name**: `oura-nfc-backend`
   - **Runtime**: Python 3
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `gunicorn oura_nfc_backend:app`
9. Scroll down to **Environment**
10. Click **Add Environment Variable**
11. Add your Oura token:
    - **Key**: `OURA_TOKEN`
    - **Value**: Paste your token from Step 1
12. Click **Create Web Service**

**Wait 2-3 minutes for it to build and deploy.**

Once it's live, you'll see a URL like: `https://oura-nfc-backend.onrender.com`

**Save this URL** — you need it for your iPhone Shortcut!

---

## Step 3: Test Your Backend (Optional but Recommended)

1. Go to your Render URL (e.g., `https://oura-nfc-backend.onrender.com`)
2. You should see a JSON response with instructions

To test tag creation:
- Open Postman or a similar tool
- **POST** to: `https://YOUR_RENDER_URL/create-tag`
- **Body** (JSON):
  ```json
  {
    "tag_type_code": "workout",
    "start_time": "2025-12-03",
    "comment": "Test tag"
  }
  ```
- You should see a success response!

---

## Step 4: Create Your iPhone Shortcut

### 4a. Create the Shortcut

1. On iPhone, open **Shortcuts** app
2. Click **+** to create new shortcut
3. Add these steps:

**Step 1: Choose from List**
- Title: "Select tag type"
- Options:
  - workout
  - stress
  - poor_sleep
  - meditation
  - recovery
  - travel
  - sickness
- (Add any other tags you use in Oura)

**Step 2: Get Current Date**
- Add action: **Get Current Date and Time**

**Step 3: Send Request**
- Add action: **Make a POST Request**
- URL: `https://YOUR_RENDER_URL/create-tag` (replace with your actual URL)
- Method: **POST**
- Headers: 
  - Key: `Content-Type`
  - Value: `application/json`
- Body: **Text**
  ```json
  {
    "tag_type_code": "[first result]",
    "start_time": "[second result in YYYY-MM-DD format]",
    "comment": "Tagged via NFC"
  }
  ```

**Step 4: Show Result**
- Add action: **Show Result**

### 4b. Link to NFC Tag

1. In Shortcuts, tap the three dots on your shortcut
2. Add to Home Screen or keep in app
3. You can then create an NFC tag that opens this shortcut

Alternatively:
- Use an app like **TagWriter** to encode an NFC tag
- Set the URL to your Shortcut's iCloud link

---

## Step 5: Use It!

1. Tap NFC tag
2. Shortcut runs
3. Select tag type from list
4. Shortcut sends to your backend
5. Backend creates tag in Oura
6. Check Oura app — tag appears! ✅

---

## Troubleshooting

### Backend won't start
- Check Render logs for errors
- Make sure `OURA_TOKEN` environment variable is set
- Verify token is valid (hasn't expired)

### Tag not appearing in Oura
- Check that tag_type_code is valid (use lowercase with underscores)
- Verify start_time is in YYYY-MM-DD format
- Make sure your Oura account has an active membership (Gen3/Ring 4 requirement)

### Shortcut shows error
- Double-check the URL is correct (no typos)
- Verify JSON format in the body step
- Check that Content-Type header is set to `application/json`

---

## Valid Tag Types in Oura

- `workout`
- `stress`
- `poor_sleep`
- `meditation`
- `recovery`
- `travel`
- `sickness`
- `menstruation`
- `alcohol`
- `caffeine`

---

## Need Help?

1. Check Render logs: Go to your service on Render and click "Logs"
2. Test the backend: Visit your URL in a browser
3. Check Oura API docs: https://developer.ouraring.com/docs

Enjoy your NFC-powered Oura tagging! 🎉
