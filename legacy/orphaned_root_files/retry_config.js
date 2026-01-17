retry_config.js
utils/retry_logic.js

utils/retry_logic.js
const asyncRetry = require('async-retry');
const rateLimit = require('express-rate-limit');

// Configure rate limiting to prevent abuse of the retry mechanism
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests, please try again later.'
});

// Exponential backoff and retry logic
const retryLogic = async (fn, options) => {
  const { maxAttempts, initialWaitTime, growthFactor, maxWaitTime } = options;

  return await asyncRetry(
    async (bail) => {
      try {
        return await fn();
      } catch (error) {
        // If you want to bail out of retries, you can do so by throwing an error that is not instance of Error
        if (error.bail) {
          bail(error);
        }
        throw error;
      }
    },
    {
      retries: maxAttempts - 1,
      factor: growthFactor,
      minTimeout: initialWaitTime * 1000, // Convert seconds to milliseconds
      onRetry: (err, attemptNumber) => {
        const nextAttemptDelay = Math.min(
          maxWaitTime * 1000,
          initialWaitTime * Math.pow(growthFactor, attemptNumber - 1)
        );
        console.log(`Attempt ${attemptNumber} failed with error: ${err.message}. Retrying in ${nextAttemptDelay / 1000} seconds.`);
      }
    }
  );
};

module.exports = { retryLogic, limiter };