const alertsTableBody = document.getElementById("alerts-body");
const statusElement = document.getElementById("status");
const popup = document.getElementById("alert-popup");
const popupSender = document.getElementById("popup-sender");
const popupSubject = document.getElementById("popup-subject");
const popupClose = document.getElementById("popup-close");

let lastSeen = new Date().toISOString();
let knownAlertIds = new Set();

async function fetchAlerts() {
  try {
    const response = await fetch("/api/alerts");
    if (!response.ok) {
      throw new Error(`Failed to load alerts: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(error);
    statusElement.textContent = "Unable to load alerts. Check the server.";
    return { alerts: [] };
  }
}

async function fetchRecentAlerts() {
  const url = `/api/alerts/recent?since=${encodeURIComponent(lastSeen)}`;
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to load recent alerts: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(error);
    return { alerts: [] };
  }
}

function renderAlerts(alerts) {
  alertsTableBody.innerHTML = "";

  if (!alerts.length) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.setAttribute("colspan", "4");
    cell.className = "empty";
    cell.textContent = "No phishing threats have been detected yet.";
    row.appendChild(cell);
    alertsTableBody.appendChild(row);
    return;
  }

  alerts.sort((a, b) => new Date(b.detected_at) - new Date(a.detected_at));
  knownAlertIds.clear();

  alerts.forEach((alert) => {
    knownAlertIds.add(alert.id || alert.message_id);

    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${alert.sender || "Unknown sender"}</td>
      <td>${alert.subject || "No subject"}</td>
      <td>${new Date(alert.detected_at).toLocaleString()}</td>
      <td>${alert.reason || "Phishing detected"}</td>
    `;
    alertsTableBody.appendChild(row);
  });
}

function showPopup(alert) {
  popupSender.textContent = `Sender: ${alert.sender || "Unknown sender"}`;
  popupSubject.textContent = `Subject: ${alert.subject || "No subject"}`;
  popup.classList.remove("hidden");
}

function hidePopup() {
  popup.classList.add("hidden");
}

popupClose.addEventListener("click", hidePopup);

async function loadInitialAlerts() {
  const payload = await fetchAlerts();
  renderAlerts(payload.alerts || []);
  if (payload.alerts && payload.alerts.length) {
    statusElement.textContent = `Loaded ${payload.alerts.length} detected phishing alert(s).`;
  } else {
    statusElement.textContent = "No phishing alerts detected yet.";
  }
  lastSeen = new Date().toISOString();
}

async function pollForAlerts() {
  const payload = await fetchRecentAlerts();
  const newAlerts = (payload.alerts || []).filter(
    (alert) => !knownAlertIds.has(alert.id || alert.message_id)
  );

  if (newAlerts.length) {
    const allAlerts = await fetchAlerts();
    renderAlerts(allAlerts.alerts || []);
    newAlerts.forEach((alert) => showPopup(alert));
    statusElement.textContent = `Received ${newAlerts.length} new phishing alert(s).`;
  }

  lastSeen = new Date().toISOString();
}

window.addEventListener("load", async () => {
  await loadInitialAlerts();
  setInterval(pollForAlerts, 10000);
});
