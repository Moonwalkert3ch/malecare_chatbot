import { NextRequest, NextResponse } from 'next/server';
import { google } from 'googleapis';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Only track if Google Sheets credentials are configured
    if (!process.env.GOOGLE_SHEETS_PRIVATE_KEY || !process.env.GOOGLE_SHEETS_CLIENT_EMAIL || !process.env.GOOGLE_SHEET_ID) {
      console.log('Google Sheets not configured - skipping tracking');
      return NextResponse.json({ ok: true, message: 'Tracking skipped (not configured)' });
    }

    // Set up Google Sheets API authentication
    const auth = new google.auth.GoogleAuth({
      credentials: {
        client_email: process.env.GOOGLE_SHEETS_CLIENT_EMAIL,
        private_key: process.env.GOOGLE_SHEETS_PRIVATE_KEY?.replace(/\\n/g, '\n'),
      },
      scopes: ['https://www.googleapis.com/auth/spreadsheets'],
    });

    const sheets = google.sheets({ version: 'v4', auth });
    const spreadsheetId = process.env.GOOGLE_SHEET_ID;

    // Prepare row data
    const timestamp = new Date().toLocaleString('en-US', { timeZone: 'America/New_York' });
    const row = [
      timestamp,
      body.userId || 'unknown',
      body.eventType || 'unknown', // 'questionnaire_submit', 'message_sent', 'chat_started'
      body.age || '',
      body.gender || '',
      body.state || '',
      body.cancerType || '',
      body.cancerStage || '',
      body.comorbidities || '',
      body.priorTreatments || '',
      body.message || '',
      body.sessionId || '',
    ];

    // Append row to the sheet
    await sheets.spreadsheets.values.append({
      spreadsheetId,
      range: 'Sheet1!A:L', // Adjust sheet name if needed
      valueInputOption: 'USER_ENTERED',
      requestBody: {
        values: [row],
      },
    });

    return NextResponse.json({ ok: true, message: 'Usage tracked successfully' });
  } catch (error) {
    console.error('Error tracking usage:', error);
    // Don't fail the request if tracking fails
    return NextResponse.json({ ok: false, error: (error as Error).message }, { status: 200 });
  }
}
