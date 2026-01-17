const asyncRetry = require('async-retry');
const rateLimit = require('express-rate-limit');

// Configurable settings for exponential backoff and retry logic
const maxAttempts = process.env.MAX_ATTEMPTS ? parseInt(process.env.MAX_ATTEMPTS, 10) : 5; // Maximum number of attempts
const initialWaitTime = process.env.INITIAL_WAIT_TIME ? parseInt(process.env.INITIAL_WAIT_TIME, 10) : 1000; // Initial wait time in milliseconds
const growthFactor = process.env.GROWTH_FACTOR ? parseFloat(process.env.GROWTH_FACTOR) : 2; // Exponential growth factor

// Create rate limiter middleware to prevent abuse of the retry mechanism
const apiRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: process.env.MAX_REQUESTS ? parseInt(process.env.MAX_REQUESTS, 10) : 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again after 15 minutes'
});

// Function to perform a request with exponential backoff and retry logic
async function performRequestWithRetry(requestFn) {
  return asyncRetry(
    async (bail) => {
      try {
        const response = await requestFn();
        if (!response.ok) {
          // If the response is not ok, throw an error to trigger a retry
          throw new Error(`Request failed with status ${response.status}`);
        }
        return response;
      } catch (error) {
        console.error('Request failed:', error.message);
        bail(error); // If you want to stop trying on certain errors
        throw error; // Re-throw the error to trigger a retry
      }
    },
    {
      retries: maxAttempts,
      factor: growthFactor,
      minTimeout: initialWaitTime,
      randomize: false,
      onRetry: (error, attempt) => {
        const nextAttemptIn = Math.min(
          initialWaitTime * Math.pow(growthFactor, attempt - 1),
          Number.MAX_SAFE_INTEGER
        );
        console.log(`Request failed. Retrying in ${nextAttemptIn}ms...`);
      }
    }
  );
}

module.exports = {
  performRequestWithRetry,
  apiRateLimiter
};