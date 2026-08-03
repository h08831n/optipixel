class TelemetryService:
    """Privacy-first local telemetry logger (no external tracking without opt-in)."""
    @staticmethod
    def log_event(event_name: str, payload: dict = None):
        # Privacy-conscious local logging
        pass
