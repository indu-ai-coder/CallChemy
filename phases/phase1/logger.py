import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Any, Optional
import traceback

class CallChemyLogger:
    def __init__(
        self,
        log_dir: str = "logs",
        log_file: str = "backend.log",
        data_file: str = "requests.jsonl",
        retention_days: int = 30
    ):
        # Create log directory if it doesn't exist
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup paths
        self.log_file = self.log_dir / log_file
        self.data_file = self.log_dir / data_file
        self.retention_days = retention_days
    
        # Configure logging
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)

    def _write_jsonl(self, data: Dict[str, Any]) -> None:
        """Write a single JSON line to the data file"""
        with open(self.data_file, 'a', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
            f.write('\n')

    def log_request(
        self,
        conversation_id: str,
        request_data: Dict[str, Any],
        response_data: Optional[Dict[str, Any]] = None,
        error: Optional[Exception] = None
    ) -> None:
        """Log request, response and any errors"""
        timestamp = datetime.now(timezone.utc).isoformat()
        
        log_entry = {
            "timestamp": timestamp,
            "conversation_id": conversation_id,
            "request": request_data,
            "response": response_data,
            "status": "success" if not error else "error"
        }

        if error:
            log_entry["error"] = {
                "type": type(error).__name__,
                "message": str(error),
                "traceback": traceback.format_exc()
            }
            self.logger.error(
                f"Error processing conversation {conversation_id}: {str(error)}"
            )
        else:
            self.logger.info(
                f"Successfully processed conversation {conversation_id}"
            )

        self._write_jsonl(log_entry)

    def cleanup_old_logs(self) -> None:
        """Remove log entries older than retention_days"""
        if not self.data_file.exists():
            return
            
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=self.retention_days)
        temp_file = self.data_file.with_suffix('.temp')
        
        with open(self.data_file, 'r', encoding='utf-8') as source, \
             open(temp_file, 'w', encoding='utf-8') as target:
            for line in source:
                try:
                    entry = json.loads(line)
                    entry_time = datetime.fromisoformat(entry['timestamp']).replace(tzinfo=timezone.utc)
                    if entry_time > cutoff_date:
                        target.write(line)
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue
        
        # Replace original file with filtered content
        temp_file.replace(self.data_file)