// Base URL for your FastAPI backend
const API_BASE_URL = 'http://localhost:8001';

/**
 * Health check endpoint
 * Tests if the backend is running and responsive
 */
export const healthCheck = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Health check error:', error);
    throw error;
  }
};

/**
 * Submit mood entry
 * @param {Object} moodData - The mood data to submit
 */
export const submitMoodEntry = async (moodData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/mood`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(moodData),
    });
    
    if (!response.ok) {
      throw new Error(`Failed to submit mood: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Mood submission error:', error);
    throw error;
  }
};

/**
 * Get mood matches
 * Retrieves potential peer matches based on mood/context
 */
export const getMoodMatches = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/matches`);
    if (!response.ok) {
      throw new Error(`Failed to get matches: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Get matches error:', error);
    throw error;
  }
};

// Add more API functions as you build out your backend endpoints