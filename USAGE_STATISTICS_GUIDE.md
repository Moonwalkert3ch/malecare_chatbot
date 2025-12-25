# Usage Statistics Tracking - Admin Guide

## Overview

The chatbot now tracks usage statistics to help you understand how people are using the service. This guide explains what data is collected and how to access it.

## What Data is Tracked?

For each chat session, we collect:
- **User Demographics**: Age, gender, location (state)
- **Medical Information**: Cancer type, cancer stage, comorbidities, prior treatments
- **Usage Metrics**: 
  - Number of messages sent
  - Number of clinical trials found
  - Session start and end times
  - Total session duration

## Accessing Usage Statistics

### Option 1: Admin Dashboard (Recommended for non-technical users)

1. Open your browser and visit: `http://localhost:3000/admin`
2. You'll see a dashboard with:
   - Total sessions
   - Completed sessions
   - Total messages
   - Trials found
   - Breakdowns by cancer type, location, and age group

### Option 2: Download CSV for Google Sheets

**This is the easiest way to analyze your data!**

1. Visit `http://localhost:3000/admin`
2. Click the **"Download CSV for Google Sheets"** button
3. A CSV file will download to your computer
4. Open Google Sheets in your browser
5. Go to **File → Import**
6. Click the **Upload** tab
7. Drag and drop the downloaded CSV file
8. Choose **"Create new spreadsheet"**
9. Click **"Import data"**

Your data is now in Google Sheets where you can:
- Sort and filter
- Create charts and graphs
- Share with team members
- Analyze trends over time

## Understanding the CSV Columns

| Column Name | Description |
|------------|-------------|
| User ID | Unique identifier for each session |
| Session Start | When the user started chatting |
| Session End | When the user ended or left |
| Duration (minutes) | How long the session lasted |
| Age | User's age |
| Gender | User's gender |
| Location | User's state/location |
| Cancer Type | Type of cancer they're researching |
| Cancer Stage | Stage of the cancer |
| Comorbidities | Other health conditions |
| Prior Treatments | Previous treatments received |
| Messages Sent | Number of messages in the conversation |
| Trials Found | Number of clinical trials found for them |

## How to Export Data Regularly

It's recommended to export your data weekly or monthly:

1. Visit the admin dashboard
2. Download the CSV
3. Import to Google Sheets
4. Optionally, after confirming the data is safely saved, you can click **"Clear All Data"** to start fresh (this resets the tracking)

## API Endpoints (for technical users)

If you need programmatic access:

- **Get Statistics Summary**: `GET http://localhost:8000/admin/stats`
- **Export CSV**: `GET http://localhost:8000/admin/export-csv`
- **Clear All Data**: `POST http://localhost:8000/admin/clear-stats`

## Privacy & Security

- All data is stored locally on the server
- User IDs are anonymous (no personally identifiable information)
- Data is only accessible through the admin dashboard
- We recommend exporting and clearing data regularly to maintain privacy

## Troubleshooting

**Q: I don't see any data in the dashboard**
- Make sure users have actually used the chatbot
- Check that the backend server is running
- Try refreshing the page

**Q: The CSV download isn't working**
- Make sure the backend server is running on port 8000
- Check your browser's download folder
- Try using a different browser

**Q: Can I recover data after clearing it?**
- No, clearing data is permanent. Always export before clearing!

## Support

If you need help with the usage statistics feature, please contact your development team.

## Demo/Testing

To test the system:
1. Visit `http://localhost:3000`
2. Fill out the chatbot questionnaire
3. Send a few messages
4. Check `http://localhost:3000/admin` to see your test data appear
5. Download the CSV to verify the export works
