"""
Message Bus System for Multi-Agent Communication
Enables agents to send/receive messages asynchronously
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
import json


class MessageType(Enum):
    """Types of messages agents can send"""
    BROADCAST = "broadcast"           # To all agents
    QUERY = "query"                   # Request for information
    RESPONSE = "response"             # Answer to a query
    PROPOSAL = "proposal"             # Suggest an action
    VOTE = "vote"                     # Vote on a proposal
    NOTIFICATION = "notification"     # Inform about an event
    FEEDBACK = "feedback"             # Comment on another agent's output


@dataclass
class AgentMessage:
    """Standard message format for inter-agent communication"""
    sender: str                       # Agent who sent the message
    receiver: str                     # Target agent or "ALL" for broadcast
    message_type: MessageType
    content: Dict[str, Any]           # Message payload
    timestamp: datetime = field(default_factory=datetime.now)
    message_id: str = field(default_factory=lambda: f"msg_{datetime.now().timestamp()}")
    in_reply_to: Optional[str] = None  # For threading conversations
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "message_id": self.message_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "message_type": self.message_type.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "in_reply_to": self.in_reply_to
        }
    
    def __repr__(self):
        return f"[{self.sender} → {self.receiver}] {self.message_type.value}: {self.content.get('summary', '')}"


class MessageBus:
    """Central communication hub for all agents"""
    
    def __init__(self):
        self.messages: List[AgentMessage] = []
        self.subscribers: Dict[str, List[str]] = {}  # agent_id -> [message_types]
        
    def send(self, message: AgentMessage) -> None:
        """Post a message to the bus"""
        self.messages.append(message)
        print(f"📨 {message}")
        
    def broadcast(self, sender: str, message_type: MessageType, content: Dict[str, Any]) -> AgentMessage:
        """Send a message to all agents"""
        message = AgentMessage(
            sender=sender,
            receiver="ALL",
            message_type=message_type,
            content=content
        )
        self.send(message)
        return message
    
    def send_to(self, sender: str, receiver: str, message_type: MessageType, 
                content: Dict[str, Any], in_reply_to: Optional[str] = None) -> AgentMessage:
        """Send a direct message to a specific agent"""
        message = AgentMessage(
            sender=sender,
            receiver=receiver,
            message_type=message_type,
            content=content,
            in_reply_to=in_reply_to
        )
        self.send(message)
        return message
    
    def get_messages_for(self, agent_id: str, 
                         message_type: Optional[MessageType] = None,
                         unread_only: bool = False,
                         since: Optional[datetime] = None) -> List[AgentMessage]:
        """Retrieve messages for a specific agent"""
        messages = [
            m for m in self.messages
            if (m.receiver == agent_id or m.receiver == "ALL")
            and (message_type is None or m.message_type == message_type)
            and (since is None or m.timestamp > since)
        ]
        return messages
    
    def get_conversation_thread(self, message_id: str) -> List[AgentMessage]:
        """Get all messages in a conversation thread"""
        thread = []
        for msg in self.messages:
            if msg.message_id == message_id or msg.in_reply_to == message_id:
                thread.append(msg)
        return sorted(thread, key=lambda m: m.timestamp)
    
    def get_all_messages(self) -> List[Dict[str, Any]]:
        """Get all messages as dictionaries (for UI display)"""
        return [m.to_dict() for m in self.messages]
    
    def clear(self) -> None:
        """Clear all messages (useful for testing)"""
        self.messages = []
        
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of communication activity"""
        return {
            "total_messages": len(self.messages),
            "by_sender": self._count_by_field("sender"),
            "by_type": self._count_by_field("message_type"),
            "timeline": [
                {
                    "time": m.timestamp.isoformat(),
                    "sender": m.sender,
                    "type": m.message_type.value,
                    "summary": m.content.get("summary", "")
                }
                for m in self.messages[-10:]  # Last 10 messages
            ]
        }
    
    def _count_by_field(self, field: str) -> Dict[str, int]:
        """Helper to count messages by a field"""
        counts = {}
        for msg in self.messages:
            value = getattr(msg, field)
            if isinstance(value, Enum):
                value = value.value
            counts[value] = counts.get(value, 0) + 1
        return counts


# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing Message Bus System\n")
    
    bus = MessageBus()
    
    # Example 1: Broadcast
    print("1️⃣ MoodAnalyzer broadcasts findings:")
    bus.broadcast(
        sender="MoodAnalyzer",
        message_type=MessageType.BROADCAST,
        content={
            "summary": "User shows HIGH career anxiety",
            "primary_emotion": "overwhelmed",
            "urgency": "MODERATE",
            "themes": ["career stress", "self-doubt"]
        }
    )
    
    print("\n2️⃣ PeerMatcher queries LocationAgent:")
    query_msg = bus.send_to(
        sender="PeerMatcher",
        receiver="LocationAgent",
        message_type=MessageType.QUERY,
        content={
            "summary": "Need location preferences for anxious user",
            "question": "What type of environment works best for career anxiety?"
        }
    )
    
    print("\n3️⃣ LocationAgent responds:")
    bus.send_to(
        sender="LocationAgent",
        receiver="PeerMatcher",
        message_type=MessageType.RESPONSE,
        content={
            "summary": "Quiet study spaces recommended",
            "answer": "For career anxiety, recommend quiet spaces like Mugar 5th floor",
            "reasoning": "Anxious users prefer low-stimulation environments"
        },
        in_reply_to=query_msg.message_id
    )
    
    print("\n4️⃣ PeerMatcher proposes a match:")
    proposal_msg = bus.broadcast(
        sender="PeerMatcher",
        message_type=MessageType.PROPOSAL,
        content={
            "summary": "Proposing match: Ananya ↔ Marcus (87% score)",
            "match_id": "match_001",
            "user_a": "student_ananya",
            "user_b": "student_marcus",
            "score": 87,
            "rationale": "Both experiencing career anxiety and self-doubt"
        }
    )
    
    print("\n5️⃣ Agents vote on the proposal:")
    for agent, vote, reason in [
        ("MoodAnalyzer", "APPROVE", "Anxiety levels compatible"),
        ("LocationAgent", "APPROVE", "Good environment match available"),
        ("SafetyAgent", "APPROVE", "Both users emotionally stable")
    ]:
        bus.send_to(
            sender=agent,
            receiver="Coordinator",
            message_type=MessageType.VOTE,
            content={
                "summary": f"{agent} votes {vote}",
                "proposal_id": proposal_msg.message_id,
                "vote": vote,
                "reasoning": reason,
                "confidence": 0.9
            },
            in_reply_to=proposal_msg.message_id
        )
    
    print("\n" + "="*60)
    print("📊 Communication Summary:")
    print("="*60)
    summary = bus.get_summary()
    print(f"Total messages: {summary['total_messages']}")
    print(f"\nBy sender: {json.dumps(summary['by_sender'], indent=2)}")
    print(f"\nBy type: {json.dumps(summary['by_type'], indent=2)}")
    
    print("\n" + "="*60)
    print("🔍 Messages for Coordinator:")
    print("="*60)
    coordinator_msgs = bus.get_messages_for("Coordinator")
    for msg in coordinator_msgs:
        print(f"  • {msg}")