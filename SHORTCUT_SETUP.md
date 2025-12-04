# iPhone Shortcut Instructions
# Create Oura NFC Tag Shortcut (Manual Setup)

## Quick Summary
This shortcut will:
1. Ask you to select a tag type
2. Get today's date
3. Send it to your backend
4. Create the tag in Oura

## Manual Steps to Create in Shortcuts App

### Step 1: Create New Shortcut
- Open Shortcuts app on iPhone
- Tap **+** button
- Tap **Create Shortcut**

### Step 2: Add "Choose from List"
1. Tap the **+** button to add action
2. Search for **"Choose from List"**
3. Add it
4. Set the title to: "What tag do you want to add?"
5. Add these items in the list:
   - workout
   - stress
   - poor_sleep
   - meditation
   - recovery
   - travel
   - sickness
   - (add any others you use)

### Step 3: Add "Get Current Date and Time"
1. Tap **+**
2. Search for **"Get Current Date and Time"**
3. Add it

### Step 4: Add "Format Date"
1. Tap **+**
2. Search for **"Format Date"**
3. Add it
4. Input: Choose the date from previous step
5. Format: "YYYY-MM-DD" (important!)

### Step 5: Add "Text"
1. Tap **+**
2. Search for **"Text"**
3. Add it
4. Paste this JSON (replace BACKEND_URL with your Render URL):

```
{
  "tag_type_code": "[result from step 2]",
  "start_time": "[result from step 4]",
  "comment": "Tagged via NFC"
}
```

### Step 6: Add "Make a POST Request"
1. Tap **+**
2. Search for **"Make a POST Request"** (or "Make a Web Request")
3. Set URL to: `https://YOUR_BACKEND_URL/create-tag`
4. Method: **POST**
5. Headers:
   - Add header
   - Key: `Content-Type`
   - Value: `application/json`
6. Body: Choose the text from step 5

### Step 7: Add "Show Result"
1. Tap **+**
2. Search for **"Show Result"** (or just "Show")
3. Add it
4. Input: Choose the web request response from step 6

### Step 8: Test It
1. Tap the **▶** play button (top right)
2. Select a tag type
3. Watch it create a tag in Oura!

---

## Important Notes

- Replace `YOUR_BACKEND_URL` with your actual Render URL (e.g., `https://oura-nfc-backend.onrender.com`)
- The date format MUST be `YYYY-MM-DD`
- Make sure `Content-Type: application/json` header is set

---

## To Use with NFC Tag

1. Once shortcut is working, save it with a name like "Create Oura Tag"
2. Go to **Shortcuts** app settings
3. Find your shortcut and share it
4. Copy the iCloud link
5. Use an NFC app like **TagWriter** to encode that link onto an NFC tag
6. Tap the tag and it will run your shortcut!

---

## Troubleshooting

**Shortcut shows error:**
- Check your backend URL is correct
- Make sure Render app is running (check Render dashboard)
- Verify JSON syntax is correct

**Tag doesn't appear in Oura:**
- Check Oura app to see if it's there
- Verify your personal access token is still valid
- Confirm tag_type_code is lowercase (e.g., "poor_sleep" not "PoorSleep")
