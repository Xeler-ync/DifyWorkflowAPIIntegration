import json
import os
import asyncio
from typing import List, Dict, Optional
import aiofiles
from models.chat import ChatSession


class Database:
    def __init__(self, data_path: str = "./data"):
        self.data_path = data_path
        self.sessions_file = os.path.join(data_path, "sessions.json")
        self.lock = asyncio.Lock()
        os.makedirs(data_path, exist_ok=True)

    def get_session_file_path(self, session_id: str) -> str:
        return os.path.join(self.data_path, f"session_{session_id}.json")

    async def save_session(self, session_id: str, session_data: ChatSession):
        async with self.lock:
            # 保存会话信息
            sessions = await self.load_all_sessions_dict()
            sessions[session_id] = {
                "id": session_id,
                "title": session_data.title,
                "created_at": session_data.created_at,
                "updated_at": session_data.updated_at,
                "repository_types": list(session_data.repository_types),
            }

            async with aiofiles.open(self.sessions_file, "w") as f:
                await f.write(json.dumps(sessions, indent=4))

            # 保存消息
            session_file = self.get_session_file_path(session_id)
            async with aiofiles.open(session_file, "w") as f:
                await f.write(
                    json.dumps(
                        [msg.to_dict() for msg in session_data.messages], indent=4
                    )
                )

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
                            "created_at": sessions[session_id]["created_at"],
                            "updated_at": sessions[session_id]["updated_at"],
                            "messages": messages,
                            "repository_types": sessions[session_id][
                                "repository_types"
                            ],
                        }
                    )
            return sorted(result, key=lambda x: x["updated_at"], reverse=True)

    async def load_all_sessions_dict(self) -> Dict[str, dict]:
        if os.path.exists(self.sessions_file):
            async with aiofiles.open(self.sessions_file, "r") as f:
                content = await f.read()
                if content:
                    return json.loads(content)
        return {}
