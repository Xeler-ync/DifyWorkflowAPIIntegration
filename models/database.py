import json
import os
import asyncio
from typing import List, Dict, Optional
import aiofiles

class Database:
    def __init__(self, data_path: str = "./data"):
        self.data_path = data_path
        self.sessions_file = os.path.join(data_path, "sessions.json")
        self.lock = asyncio.Lock()
        os.makedirs(data_path, exist_ok=True)

    def get_session_file_path(self, session_id: str) -> str:
        return os.path.join(self.data_path, f"session_{session_id}.json")

    async def save_session(self, session_id: str, session_data: dict):
        async with self.lock:
            # 保存会话信息
            sessions = await self.load_all_sessions_dict()
            sessions[session_id] = {
                "id": session_id,
                "title": session_data["title"],
                "createdAt": session_data["createdAt"],
                "updatedAt": session_data["updatedAt"],
            }

            async with aiofiles.open(self.sessions_file, "w") as f:
                await f.write(json.dumps(sessions, indent=4))

            # 保存消息
            session_file = self.get_session_file_path(session_id)
            async with aiofiles.open(session_file, "w") as f:
                await f.write(json.dumps(session_data["messages"], indent=4))

    async def load_session(self, session_id: str) -> Optional[dict]:
        async with self.lock:
            sessions = await self.load_all_sessions_dict()
            if session_id not in sessions:
                return None

            session_file = self.get_session_file_path(session_id)
            if not os.path.exists(session_file):
                return None

            async with aiofiles.open(session_file, "r") as f:
                content = await f.read()
                messages = json.loads(content)

            return {
                "id": session_id,
                "title": sessions[session_id]["title"],
                "createdAt": sessions[session_id]["createdAt"],
                "updatedAt": sessions[session_id]["updatedAt"],
                "messages": messages,
            }

    async def delete_session(self, session_id: str):
        async with self.lock:
            sessions = await self.load_all_sessions_dict()
            if session_id in sessions:
                del sessions[session_id]
                async with aiofiles.open(self.sessions_file, "w") as f:
                    await f.write(json.dumps(sessions, indent=4))

                session_file = self.get_session_file_path(session_id)
                if os.path.exists(session_file):
                    os.remove(session_file)

    async def load_all_sessions(self) -> List[dict]:
        async with self.lock:
            sessions = await self.load_all_sessions_dict()
            result = []
            for session_id in sessions:
                session_file = self.get_session_file_path(session_id)
                if os.path.exists(session_file):
                    async with aiofiles.open(session_file, "r") as f:
                        content = await f.read()
                        messages = json.loads(content)
                    result.append(
                        {
                            "id": session_id,
                            "title": sessions[session_id]["title"],
                            "createdAt": sessions[session_id]["createdAt"],
                            "updatedAt": sessions[session_id]["updatedAt"],
                            "messages": messages,
                        }
                    )
            return sorted(result, key=lambda x: x["updatedAt"], reverse=True)

    async def load_all_sessions_dict(self) -> Dict[str, dict]:
        if os.path.exists(self.sessions_file):
            async with aiofiles.open(self.sessions_file, "r") as f:
                content = await f.read()
                return json.loads(content)
        return {}
