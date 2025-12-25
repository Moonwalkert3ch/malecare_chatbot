// Helper function to track usage to Google Sheets
export async function trackUsage(data: {
  userId: string;
  eventType: 'chat_started' | 'questionnaire_submit' | 'message_sent';
  age?: string;
  gender?: string;
  state?: string;
  cancerType?: string;
  cancerStage?: string;
  comorbidities?: string;
  priorTreatments?: string;
  message?: string;
  sessionId?: string;
}) {
  try {
    await fetch('/api/track-usage', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    // Don't wait for response, don't block user experience
  } catch (error) {
    console.error('Failed to track usage:', error);
    // Silently fail - don't disrupt user experience
  }
}
