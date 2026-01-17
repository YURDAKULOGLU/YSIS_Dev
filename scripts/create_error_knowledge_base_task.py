#!/usr/bin/env python3
"""
Create task for Error Knowledge Base implementation.
"""

import sys
import asyncio
from pathlib import Path

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def create_task():
    """Create Error Knowledge Base task."""
    print("=" * 60)
    print("Creating Error Knowledge Base Task")
    print("=" * 60)
    print()
    
    server_params = StdioServerParameters(
        command="python",
        args=["scripts/ybis_mcp_server.py"],
        env=None,
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("Creating Task: Error Knowledge Base...")
            result = await session.call_tool(
                "task_create",
                arguments={
                    "title": "Feature: Error Knowledge Base (Task Hataları Ortak Toplama)",
                    "objective": """Implement centralized error knowledge base for cross-task learning.

Problem:
- Task hataları şu an her task'ta ayrı ayrı kayboluyor
- Bir task'ta yapılan hata, diğer task'larda tekrar yapılıyor
- Hangi hataların nerede nasıl yapıldığı bilinmiyor

Solution:
Task hatalarını ortak bir yerde topla, analiz et, pattern'ları çıkar.

Requirements:
1. Error Knowledge Base Service:
   - src/ybis/services/error_knowledge_base.py (✅ Already created)
   - TaskError dataclass (error_type, error_message, error_location, step)
   - ErrorPattern dataclass (pattern extraction)
   - ErrorKnowledgeBase class (storage, analysis, query)
   
2. Error Collection:
   - record_error() - Tek bir hata kaydet
   - record_from_verifier_report() - Verifier report'tan hataları kaydet
   - record_from_gate_report() - Gate block'ları kaydet
   - record_from_executor_report() - Execution hatalarını kaydet
   
3. Pattern Analysis:
   - Benzer hataları grupla
   - Pattern'ları çıkar (2+ occurrence)
   - Common context'i bul
   - Suggested fix öner
   
4. Integration:
   - verifier_node'da: verifier_report'tan hataları kaydet
   - gate_node'da: block'ları kaydet
   - repair_node'da: repair attempt'leri kaydet
   - spec_node'da: Benzer hataları sorgula ve prompt'a ekle
   - plan_node'da: Benzer hataları sorgula ve prompt'a ekle
   
5. Storage:
   - platform_data/error_kb/errors.jsonl (her hata bir satır)
   - platform_data/error_kb/patterns.json (pattern'lar)
   - platform_data/error_kb/stats.json (istatistikler)
   
6. Query API:
   - get_similar_errors() - Benzer hataları bul
   - get_error_patterns() - Pattern'ları listele
   - get_insights_for_task() - Task için insight'lar
   - get_statistics() - Genel istatistikler

Success Criteria:
- Tüm task hataları ortak yerde toplanıyor
- Pattern'lar otomatik çıkarılıyor
- Benzer hatalar sorgulanabiliyor
- spec_node ve plan_node benzer hataları görüyor
- Cross-task learning çalışıyor""",
                    "priority": "HIGH",
                }
            )
            task_data = eval(result.content[0].text)
            print(f"  ✅ Created: {task_data['task_id']}")
            print()
            print("=" * 60)
            print("✅ Task Created!")
            print("=" * 60)
            print()
            print(f"To run:")
            print(f"  python scripts/ybis_run.py {task_data['task_id']} --workflow self_develop")
            print("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(create_task())
    except KeyboardInterrupt:
        print("\n⚠️  Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

