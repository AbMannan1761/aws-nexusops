/**
 * AWS NexusOps Frontend Application Controller
 * Manages WhatsApp phone simulator, Bedrock Agent reasoning visualizer, and CDS dispatch monitors.
 */

document.addEventListener("DOMContentLoaded", () => {
  const waForm = document.getElementById("wa-form");
  const waInput = document.getElementById("wa-input");
  const waChatBody = document.getElementById("wa-chat-body");
  const traceFeed = document.getElementById("trace-feed");
  const emptyTraceState = document.getElementById("empty-trace-state");
  const btnRefresh = document.getElementById("btn-refresh");

  // CDS monitors
  const sesSender = document.getElementById("ses-sender");
  const sesRecipient = document.getElementById("ses-recipient");
  const sesSubject = document.getElementById("ses-subject");
  const sesBodyContainer = document.getElementById("ses-body-container");
  const smsFeed = document.getElementById("sms-feed");
  const ticketsContainer = document.getElementById("tickets-container");

  // Tab switching
  const tabBtns = document.querySelectorAll(".tab-btn");
  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      tabBtns.forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".tab-content").forEach(tc => tc.classList.remove("active"));
      btn.classList.add("active");
      const targetId = btn.getAttribute("data-tab");
      document.getElementById(targetId).classList.add("active");
    });
  });

  // Quick Scenarios Chips
  document.querySelectorAll(".qp-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      const prompt = chip.getAttribute("data-prompt");
      waInput.value = prompt;
      waForm.dispatchEvent(new Event("submit"));
    });
  });

  // Reset / Refresh button
  btnRefresh.addEventListener("click", () => {
    fetchTickets();
    loadStatus();
  });

  // Handle Form Submission
  waForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const userText = waInput.value.trim();
    if (!userText) return;

    // 1. Append User WhatsApp Bubble
    appendWhatsAppMessage(userText, "outgoing");
    waInput.value = "";

    // 2. Show Agent Thinking State
    showAgentThinking();

    const startTime = performance.now();

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: "demo-session-wa-01",
          user_phone: "+12065550142",
          user_name: "Sarah Jenkins (Director of Ops)",
          message: userText,
          channel: "WHATSAPP"
        })
      });

      const data = await response.json();
      const duration = Math.round(performance.now() - startTime);
      document.getElementById("metric-latency").textContent = `${duration}ms`;

      // 3. Render Bedrock Traces
      renderTraces(data.traces);

      // 4. Render WhatsApp Incoming Response
      appendWhatsAppMessage(data.response_text, "incoming");

      // 5. Update CDS Dispatches (SES, SMS, Tickets)
      handleCdsDispatches(data.cds_dispatches);

      // 6. Refresh Tickets
      fetchTickets();

    } catch (err) {
      console.error("Agent chat failed:", err);
      appendWhatsAppMessage("⚠️ Connection error reaching Amazon Bedrock Agent. Check console.", "incoming");
    } finally {
      removeAgentThinking();
    }
  });

  function appendWhatsAppMessage(text, direction) {
    const bubble = document.createElement("div");
    bubble.className = `wa-bubble wa-${direction}`;

    const now = new Date();
    const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    // Format bold markdown (*text*)
    const formattedText = text.replace(/\*(.*?)\*/g, "<strong>$1</strong>").replace(/\n/g, "<br>");

    bubble.innerHTML = `
      <div class="wa-msg-content">${formattedText}</div>
      <span class="wa-msg-time">${timeStr}</span>
    `;

    waChatBody.appendChild(bubble);
    waChatBody.scrollTop = waChatBody.scrollHeight;
  }

  function showAgentThinking() {
    const thinkingBubble = document.createElement("div");
    thinkingBubble.id = "wa-thinking-bubble";
    thinkingBubble.className = "wa-bubble wa-incoming";
    thinkingBubble.innerHTML = `<span style="color:#94a3b8; font-style:italic;">Bedrock Agent reasoning & dispatching CDS...</span>`;
    waChatBody.appendChild(thinkingBubble);
    waChatBody.scrollTop = waChatBody.scrollHeight;
  }

  function removeAgentThinking() {
    const bubble = document.getElementById("wa-thinking-bubble");
    if (bubble) bubble.remove();
  }

  function renderTraces(traces) {
    if (!traces || traces.length === 0) return;
    if (emptyTraceState) emptyTraceState.style.display = "none";

    // Clear previous traces
    traceFeed.innerHTML = "";

    traces.forEach(trace => {
      const card = document.createElement("div");
      card.className = "trace-card active-step";

      let toolCallsHtml = "";
      if (trace.tool_calls && trace.tool_calls.length > 0) {
        trace.tool_calls.forEach(tc => {
          let badgeClass = "db";
          if (tc.tool_name.includes("whatsapp")) badgeClass = "whatsapp";
          else if (tc.tool_name.includes("ses")) badgeClass = "ses";
          else if (tc.tool_name.includes("sms")) badgeClass = "sms";

          toolCallsHtml += `
            <div class="tool-invocation-box" style="margin-top: 8px;">
              <span class="tool-badge ${badgeClass}">${tc.tool_name}</span>
              <div class="tool-json"><strong>Arguments:</strong> ${JSON.stringify(tc.arguments, null, 2)}</div>
              <div class="tool-json" style="margin-top: 4px; color: #34d399;"><strong>Result:</strong> ${JSON.stringify(tc.result, null, 2)}</div>
            </div>
          `;
        });
      }

      card.innerHTML = `
        <div class="trace-step-header">
          <span class="step-badge">STEP ${trace.step_number}</span>
          <span style="font-size: 0.68rem; color: #94a3b8;">${new Date(trace.timestamp).toLocaleTimeString()}</span>
        </div>
        <div class="step-thought">${trace.thought}</div>
        ${toolCallsHtml}
      `;

      traceFeed.appendChild(card);
    });

    traceFeed.scrollTop = traceFeed.scrollHeight;
  }

  function handleCdsDispatches(dispatches) {
    if (!dispatches || dispatches.length === 0) return;

    dispatches.forEach(item => {
      const tool = item.tool;
      const res = item.result;

      if (tool === "send_ses_audit_email") {
        sesSubject.textContent = res.subject || "Incident Resolution Notice";
        sesRecipient.textContent = (res.recipients || ["ops-director@megacorp-logistics.com"]).join(", ");
        sesSender.textContent = `${res.sender || "ops-concierge@nexusops.aws"} (Amazon SES v2)`;
        sesBodyContainer.innerHTML = res.htmlBody || `<p>Audit email dispatched successfully.</p>`;
      }

      if (tool === "send_sms_urgent_alert") {
        const smsCard = document.createElement("div");
        smsCard.className = "sms-card";
        smsCard.innerHTML = `
          <div class="sms-header">
            <span>AWS PINPOINT SMS v2</span>
            <span>${new Date().toLocaleTimeString()}</span>
          </div>
          <div class="sms-text">${res.message || "Alert dispatched"}</div>
          <div style="font-size: 0.68rem; color: #64748b; margin-top: 4px;">To: ${res.destinationPhoneNumber} | ID: ${res.messageId}</div>
        `;
        const emptyPrompt = smsFeed.querySelector(".empty-sms-prompt");
        if (emptyPrompt) emptyPrompt.remove();
        smsFeed.prepend(smsCard);
      }
    });
  }

  async function fetchTickets() {
    try {
      const res = await fetch("/api/tickets");
      const tickets = await res.json();
      ticketsContainer.innerHTML = "";

      tickets.forEach(t => {
        const item = document.createElement("div");
        item.className = "ticket-item";
        item.innerHTML = `
          <div class="ticket-header">
            <span class="ticket-tag">${t.ticket_id}</span>
            <span class="ticket-status status-${t.status}">${t.status}</span>
          </div>
          <div class="ticket-summary"><strong>${t.category}</strong>: ${t.summary}</div>
          <div class="ticket-details">${t.details}</div>
          <div style="font-size: 0.65rem; color: #64748b; margin-top: 6px;">Client: ${t.customer_name} (${t.customer_phone})</div>
        `;
        ticketsContainer.appendChild(item);
      });
    } catch (e) {
      console.warn("Could not fetch tickets:", e);
    }
  }

  async function loadStatus() {
    try {
      const res = await fetch("/api/status");
      const data = await res.json();
      console.log("NexusOps Engine Status:", data);
    } catch (e) {
      console.warn("Could not load engine status:", e);
    }
  }

  // Initial loads
  fetchTickets();
  loadStatus();
});
