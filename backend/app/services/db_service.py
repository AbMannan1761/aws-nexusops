"""
In-memory and DynamoDB storage service for NexusOps.
Stores session history, service tickets, and audit dispatch logs.
"""

from typing import Dict, List, Optional
from datetime import datetime
from app.models.schemas import ServiceTicket, SystemAuditLog

class DatabaseService:
    def __init__(self):
        self.tickets: Dict[str, ServiceTicket] = {}
        self.session_history: Dict[str, List[Dict[str, str]]] = {}
        self.audit_logs: List[SystemAuditLog] = []
        self._seed_initial_data()

    def _seed_initial_data(self):
        # Sample tickets for demo
        demo_ticket = ServiceTicket(
            ticket_id="TICK-8041",
            customer_name="Sarah Jenkins (Director of Ops)",
            customer_phone="+12065550142",
            customer_email="sarah.jenkins@megacorp-logistics.com",
            category="Field Telemetry Gateway Disruption",
            priority="CRITICAL",
            status="INVESTIGATING",
            summary="Substation Node 4B lost telemetry stream during peak delivery hours.",
            details="Telemetry gateway 4B unresponsive after firmware update. Secondary backup radio online.",
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )
        self.tickets[demo_ticket.ticket_id] = demo_ticket

    def get_ticket(self, ticket_id: str) -> Optional[ServiceTicket]:
        return self.tickets.get(ticket_id)

    def list_tickets(self) -> List[ServiceTicket]:
        return list(self.tickets.values())

    def create_or_update_ticket(self, ticket: ServiceTicket) -> ServiceTicket:
        self.tickets[ticket.ticket_id] = ticket
        return ticket

    def add_audit_log(self, event_type: str, description: str, metadata: dict):
        log_entry = SystemAuditLog(
            id=f"audit-{len(self.audit_logs) + 1:04d}",
            event_type=event_type,
            description=description,
            metadata=metadata,
            timestamp=datetime.utcnow().isoformat()
        )
        self.audit_logs.append(log_entry)
        return log_entry

    def get_audit_logs(self, limit: int = 20) -> List[SystemAuditLog]:
        return sorted(self.audit_logs, key=lambda x: x.timestamp, reverse=True)[:limit]

    def append_message(self, session_id: str, role: str, content: str):
        if session_id not in self.session_history:
            self.session_history[session_id] = []
        self.session_history[session_id].append({"role": role, "content": content})

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        return self.session_history.get(session_id, [])

db = DatabaseService()
