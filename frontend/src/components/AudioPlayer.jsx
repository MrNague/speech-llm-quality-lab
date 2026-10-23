import { useEffect, useRef, useState } from "react";
import WaveSurfer from "wavesurfer.js";
import { Play, Pause } from "lucide-react";

export function AudioPlayer({ audioUrl }) {
  const containerRef = useRef(null);
  const wsRef = useRef(null);
  const [playing, setPlaying] = useState(false);
  const [duration, setDuration] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    if (!containerRef.current || !audioUrl) return;

    const ws = WaveSurfer.create({
      container: containerRef.current,
      waveColor: "#c7d2fe",
      progressColor: "#4f46e5",
      height: 48,
      barWidth: 2,
      barGap: 1,
      cursorWidth: 0,
    });

    ws.load(audioUrl);

    ws.on("ready", () => setDuration(ws.getDuration()));
    ws.on("audioprocess", () => setCurrentTime(ws.getCurrentTime()));
    ws.on("finish", () => setPlaying(false));

    wsRef.current = ws;

    return () => ws.destroy();
  }, [audioUrl]);

  const togglePlay = () => {
    wsRef.current?.playPause();
    setPlaying((p) => !p);
  };

  const fmt = (s) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}`;

  return (
    <div className="flex items-center gap-3">
      <button
        onClick={togglePlay}
        className="flex h-9 w-9 items-center justify-center rounded-full bg-indigo-600 text-white"
      >
        {playing ? <Pause size={16} /> : <Play size={16} />}
      </button>
      <div ref={containerRef} className="flex-1" />
      <span className="w-20 text-right text-xs text-slate-500">
        {fmt(currentTime)} / {fmt(duration)}
      </span>
    </div>
  );
}