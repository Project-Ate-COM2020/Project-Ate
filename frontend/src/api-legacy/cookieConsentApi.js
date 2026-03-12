export async function sendCookieConsent(choice) {
    try {
      const response = await fetch("/api/cookie-consent", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          consent: choice,
          consentVersion: "1.0",
          timestamp: new Date().toISOString(),
        }),
      });
  
      if (!response.ok) {
        throw new Error("Failed to record cookie consent");
      }
  
      return await response.json();
  
    } catch (error) {
      console.error("Cookie consent API error:", error);
      throw error;
    }
  }