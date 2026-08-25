const encodeSegment = (value) => encodeURIComponent(value);

async function requestJSON(path) {
  const response = await fetch(path, {
    headers: {
      Accept: "application/json",
      "Cache-Control": "no-store",
    },
  });

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok) {
    const apiError = payload?.error;
    const error = new Error(apiError?.message || "The viewer request failed.");
    error.code = apiError?.code || `http_${response.status}`;
    error.status = response.status;
    throw error;
  }
  return payload;
}

export const httpDataSource = {
  async listLanguages() {
    const payload = await requestJSON("api/languages");
    return payload.languages || [];
  },

  async listDocuments(languageId) {
    const payload = await requestJSON(
      `api/languages/${encodeSegment(languageId)}/documents`,
    );
    return payload.groups || [];
  },

  async getDocument(languageId, relativePath) {
    const encodedLanguage = encodeSegment(languageId);
    const encodedPath = relativePath
      .split("/")
      .map(encodeSegment)
      .join("/");
    return requestJSON(
      `api/languages/${encodedLanguage}/documents/${encodedPath}`,
    );
  },
};
