"""Local adapter. Reference text and annotation labels never enter this module."""
from pathlib import Path
from time import perf_counter


class FasterWhisperAdapter:
    def __init__(self, config):
        from faster_whisper import WhisperModel
        model_path = Path(config["model_path"])
        if not model_path.is_dir():
            raise ValueError("Local model is missing; use the explicit download script")
        start = perf_counter()
        self.model = WhisperModel(str(model_path), device="cpu", compute_type="int8",
                                  cpu_threads=config.get("cpu_threads", 4), num_workers=1,
                                  local_files_only=True)
        self.load_s = perf_counter()-start

    def transcribe(self, audio_path, config):
        start = perf_counter()
        segments, _ = self.model.transcribe(str(audio_path), language="fr", task="transcribe",
                                           beam_size=config.get("beam_size", 1), temperature=0,
                                           condition_on_previous_text=False, vad_filter=False)
        # Inference is lazy: time the full generator consumption.
        text = "".join(segment.text for segment in segments).strip()
        return {"text": text, "elapsed_s": perf_counter()-start}
