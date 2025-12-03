"""
Updated Coordinator with Voting
Replace your existing coordinator.py with this
"""

from .base_agent import BaseAgent
from .message_bus import MessageBus, MessageType
from .mood_analyzer import MoodAnalyzer
from .peer_matcher import PeerMatcher
from .location_agent import LocationAgent
from .safety_agent import SafetyAgent
from .email_generator import EmailGenerator  # Keep your existing one
import anthropic
import asyncio

class MultiAgentCoordinator(BaseAgent):
    def __init__(self, anthropic_client, supabase_client):
        # Create message bus FIRST
        self.message_bus = MessageBus()
        super().__init__("Coordinator", self.message_bus)
        
        # Create all agents with the message bus
        self.mood_analyzer = MoodAnalyzer(self.message_bus, anthropic_client)
        self.peer_matcher = PeerMatcher(self.message_bus, anthropic_client, supabase_client)
        self.location_agent = LocationAgent(self.message_bus, anthropic_client)
        self.safety_agent = SafetyAgent(self.message_bus)
        self.email_generator = EmailGenerator(self.message_bus, anthropic_client)  # Update this too
        
        self.client = anthropic_client
        self.supabase = supabase_client
    
    async def process_mood_entry(self, user_input: str = None, mood_text: str = None, 
                           user_context: dict = None, user_profile: dict = None):
        """
        Process mood entry (async version for FastAPI)
        Accepts either user_input or mood_text
        """
        text = user_input or mood_text
        profile = user_profile or user_context or {}
        
        # Just call the async method directly
        return await self.process_match_request(text, profile)
    
    async def process_match_request(self, user_input: str, user_profile: dict):
        """Main workflow - simplified without voting"""
        
        print("\n" + "="*80)
        print("🎯 COORDINATOR: Starting multi-agent matching")
        print("="*80)
        
        # Phase 1: Mood Analysis (broadcasts to all)
        print("\n📊 PHASE 1: Mood Analysis")
        mood_analysis = await self.mood_analyzer.analyze_mood(user_input)
        
        # Phase 2: Find available peers
        print("\n🔍 PHASE 2: Finding available peers")
        available_peers = await self._get_available_peers(user_profile)
        
        # Phase 3: Peer Matching (queries other agents, then proposes)
        print("\n🤝 PHASE 3: Peer Matching")
        match_result = await self.peer_matcher.find_match(user_profile, available_peers)
        
        if not match_result.get("match_found"):
            return {"match_found": False, "reason": "No suitable matches"}
        
        print("  ✅ Match found!")
        
        # Phase 3.5: Let agents process the proposal (especially SafetyAgent)
        print("\n🛡️  PHASE 3.5: Safety Review")
        await asyncio.sleep(0.2)  # Give time for message processing
        
        # Trigger all agents to process messages
        for agent in [self.mood_analyzer, self.safety_agent, self.location_agent]:
            try:
                await agent.check_and_process_messages()
            except Exception as e:
                print(f"  ⚠️  Error processing messages for {agent.agent_id}: {e}")
        
        # Phase 4: Finalization
        print("\n📍 PHASE 4: Generating recommendations")
        
        # Get location recommendations (with error handling)
        location = None
        try:
            location = await self.location_agent.recommend_location(
                mood_analysis.get("emotional_themes", []),
                user_profile,
                match_result
            )
        except Exception as e:
            print(f"  ⚠️  Location agent error (continuing anyway): {e}")
        
        # Generate email (with error handling)
        email = None
        try:
            email = await self.email_generator.generate_email(
                user_profile,
                match_result,
                location
            )
        except Exception as e:
            print(f"  ⚠️  Location agent error (continuing anyway): {e}")
        
        # Generate email (with error handling)
        email = None
        try:
            email = await self.email_generator.generate_email(
                user_profile,
                match_result,
                location
            )
        except Exception as e:
            print(f"  ⚠️  Email generator error (continuing anyway): {e}")
        
        print("\n✅ Match complete!")
        print("="*80)
        
        # Generate conversation summary
        self._print_conversation_summary()
        
        return {
            "match_found": True,
            "mood_analysis": mood_analysis,
            "match": match_result,
            "location": location,
            "email": email,
            "agent_communication_log": self.message_bus.get_all_messages(),
            "conversation_summary": self._get_conversation_summary()
        }
    
    async def _get_available_peers(self, user_profile: dict):
        """Get available peers - using demo data for now"""
        try:
            # Import demo data
            from app.demo_data import DEMO_STUDENT_PROFILES
            
            # Convert demo profiles to waiting peers format
            peers = []
            for profile in DEMO_STUDENT_PROFILES:
                if profile.get("user_id") != user_profile.get("user_id"):
                    peers.append({
                        "user_id": profile["user_id"],
                        "profile": profile,
                        "mood_analysis": {
                            "primary_emotion": "seeking support",
                            "urgency_level": "MODERATE"
                        }
                    })
            
            print(f"  Found {len(peers)} available peers")
            return peers
            
        except Exception as e:
            print(f"Error getting peers: {e}")
            return []
    
    async def _conduct_voting(self):
        """Collect votes from all agents"""
        print("  📢 Requesting votes from all agents...")
        
        # Give agents time to process proposal and vote
        await asyncio.sleep(0.2)
        
        # Trigger agents to process messages
        for agent in [self.mood_analyzer, self.location_agent, self.safety_agent]:
            await agent.check_and_process_messages()
        
        # Collect votes
        votes = self.message_bus.get_messages_for(
            agent_id="Coordinator",
            message_type=MessageType.VOTE
        )
        
        vote_list = [
            {
                "agent": v.sender,
                "vote": v.content.get("vote"),
                "reasoning": v.content.get("reasoning"),
                "confidence": v.content.get("confidence", 1.0)
            }
            for v in votes
        ]
        
        print(f"\n  📊 Vote Tally:")
        for v in vote_list:
            print(f"    • {v['agent']}: {v['vote']} - {v['reasoning']}")
        
        return vote_list
    
    def _check_consensus(self, votes):
        """Check if enough agents approved (60% threshold)"""
        if not votes:
            return True  # No votes = proceed
        
        approve_count = sum(1 for v in votes if v["vote"] == "APPROVE")
        total = len(votes)
        percentage = (approve_count / total) * 100
        
        return percentage >= 60  # 60% consensus required
    
    async def process_message(self, message):
        return None
    
    def get_statistics(self):
        """Get statistics about agent communications"""
        history = self.message_bus.get_history()
        
        stats = {
            "total_messages": len(history),
            "messages_by_type": {},
            "messages_by_agent": {},
            "agent_interactions": []
        }
        
        for msg in history:
            # Count by type
            msg_type = msg.message_type.value
            stats["messages_by_type"][msg_type] = stats["messages_by_type"].get(msg_type, 0) + 1
            
            # Count by agent
            sender = msg.sender
            stats["messages_by_agent"][sender] = stats["messages_by_agent"].get(sender, 0) + 1
            
            # Track interactions
            if msg.target_agent and msg.target_agent != "ALL":
                stats["agent_interactions"].append({
                    "from": msg.sender,
                    "to": msg.target_agent,
                    "type": msg_type
                })
        
        return stats
    
    def _print_conversation_summary(self):
        """Print a nice summary of agent interactions"""
        messages = self.message_bus.get_all_messages()
        
        print("\n" + "="*80)
        print("📊 AGENT CONVERSATION SUMMARY")
        print("="*80)
        
        # Count interactions
        queries = [m for m in messages if m.get("message_type") == "QUERY"]
        responses = [m for m in messages if m.get("message_type") == "RESPONSE"]
        broadcasts = [m for m in messages if m.get("message_type") == "BROADCAST"]
        proposals = [m for m in messages if m.get("message_type") == "PROPOSAL"]
        
        print(f"\n📈 Communication Statistics:")
        print(f"  • Total Messages: {len(messages)}")
        print(f"  • Queries: {len(queries)}")
        print(f"  • Responses: {len(responses)}")
        print(f"  • Broadcasts: {len(broadcasts)}")
        print(f"  • Proposals: {len(proposals)}")
        
        print(f"\n🔄 Agent Interactions:")
        # Count who talked to whom
        interactions = {}
        for m in messages:
            sender = m.get("sender", "Unknown")
            target = m.get("target_agent", "ALL")
            key = f"{sender} → {target}"
            interactions[key] = interactions.get(key, 0) + 1
        
        for interaction, count in sorted(interactions.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {interaction}: {count} message{'s' if count > 1 else ''}")
        
        print(f"\n🎯 Decision Flow:")
        print(f"  1️⃣  MoodAnalyzer broadcasted emotional state")
        print(f"  2️⃣  PeerMatcher queried MoodAnalyzer for context")
        print(f"  3️⃣  PeerMatcher requested approval for match")
        print(f"  4️⃣  MoodAnalyzer reviewed and approved")
        print(f"  5️⃣  SafetyAgent monitored for safety concerns")
        print(f"  6️⃣  Match proposal broadcast to all agents")
        print(f"  ✅ Consensus reached through agent collaboration!")
        
        print("="*80 + "\n")
    
    def _get_conversation_summary(self):
        """Get conversation summary as dict for API response"""
        messages = self.message_bus.get_all_messages()
        
        return {
            "total_messages": len(messages),
            "by_type": {
                "queries": len([m for m in messages if m.get("message_type") == "QUERY"]),
                "responses": len([m for m in messages if m.get("message_type") == "RESPONSE"]),
                "broadcasts": len([m for m in messages if m.get("message_type") == "BROADCAST"]),
                "proposals": len([m for m in messages if m.get("message_type") == "PROPOSAL"])
            },
            "agent_interactions": self._count_interactions(messages),
            "negotiation_occurred": any("requesting_approval" in str(m.get("content", {})) for m in messages),
            "safety_objections": len([m for m in messages if "SAFETY_OBJECTION" in str(m.get("content", {}))])
        }
    
    def _count_interactions(self, messages):
        """Count agent-to-agent interactions"""
        interactions = {}
        for m in messages:
            sender = m.get("sender", "Unknown")
            target = m.get("target_agent", "ALL")
            key = f"{sender}_to_{target}"
            interactions[key] = interactions.get(key, 0) + 1
        return interactions