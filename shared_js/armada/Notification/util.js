export const createSuccessMessage = (message) => ({
  type: "success",
  text: message
});

export const createWarningMessage = (message) => ({
  type: "warning",
  text: message
});

export const createErrorMessage = (message) => ({
  type: "error",
  text: message
});
