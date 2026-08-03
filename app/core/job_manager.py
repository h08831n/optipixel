import csv
import json
from pathlib import Path
from typing import List
from app.core.processor import ProcessingResult

class JobReportExporter:
    @staticmethod
    def export_csv(results: List[ProcessingResult], export_path: Path):
        fieldnames = [
            "Source Path",
            "Output Path",
            "Original Format",
            "Output Format",
            "Original Size (Bytes)",
            "New Size (Bytes)",
            "Saved Bytes",
            "Reduction (%)",
            "Width",
            "Height",
            "Duration (s)",
            "Status",
            "Message",
            "Backup Path"
        ]

        with open(export_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in results:
                writer.writerow({
                    "Source Path": str(r.source_path),
                    "Output Path": str(r.output_path),
                    "Original Format": r.original_format.value,
                    "Output Format": r.output_format.value,
                    "Original Size (Bytes)": r.original_size_bytes,
                    "New Size (Bytes)": r.new_size_bytes,
                    "Saved Bytes": r.saved_bytes,
                    "Reduction (%)": f"{r.reduction_percentage:.2f}",
                    "Width": r.width,
                    "Height": r.height,
                    "Duration (s)": f"{r.duration_seconds:.3f}",
                    "Status": r.status,
                    "Message": r.message,
                    "Backup Path": str(r.backup_path) if r.backup_path else ""
                })

    @staticmethod
    def export_json(results: List[ProcessingResult], export_path: Path):
        data = []
        for r in results:
            data.append({
                "source_path": str(r.source_path),
                "output_path": str(r.output_path),
                "original_format": r.original_format.value,
                "output_format": r.output_format.value,
                "original_size_bytes": r.original_size_bytes,
                "new_size_bytes": r.new_size_bytes,
                "saved_bytes": r.saved_bytes,
                "reduction_percentage": round(r.reduction_percentage, 2),
                "width": r.width,
                "height": r.height,
                "duration_seconds": round(r.duration_seconds, 3),
                "status": r.status,
                "message": r.message,
                "backup_path": str(r.backup_path) if r.backup_path else None
            })

        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
