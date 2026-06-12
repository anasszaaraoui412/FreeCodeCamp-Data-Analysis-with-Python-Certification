"use client";

import React, { useState } from "react";
import { LiveKitRoom, RoomAudioRenderer, ControlBar } from "@livekit/components-react";
import "@livekit/components-styles";
import { motion, AnimatePresence } from "framer-motion";
import { Mic, MicOff, Video, VideoOff } from "lucide-react";

export default function TotemPage() {
  const [token, setToken] = useState<string | null>(null);
  const [url, setUrl] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  // Mock function to "connect" for the UI demo
  const startSession = () => {
     setIsConnected(true);
  };

  return (
    <div className="h-screen w-full bg-slate-950 flex flex-col items-center justify-center text-white overflow-hidden relative">
      {/* Background Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-500/10 rounded-full blur-[120px]" />

      <AnimatePresence mode="wait">
        {!isConnected ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="z-10 flex flex-col items-center gap-8"
          >
            <div className="text-center">
              <h1 className="text-5xl font-bold mb-4 tracking-tighter">UNOYA</h1>
              <p className="text-slate-400 text-xl">Your AI Workplace Concierge</p>
            </div>

            <button
              onClick={startSession}
              className="px-8 py-4 bg-white text-black rounded-full font-bold text-lg hover:bg-blue-50 transition-all hover:scale-105 active:scale-95"
            >
              Start Conversation
            </button>
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="z-10 flex flex-col items-center gap-12 w-full max-w-4xl px-4"
          >
             {/* Audio Visualizer Mock */}
             <div className="relative flex items-center justify-center">
                <motion.div
                    animate={{
                        scale: [1, 1.1, 1],
                        opacity: [0.3, 0.6, 0.3]
                    }}
                    transition={{ repeat: Infinity, duration: 3 }}
                    className="absolute w-64 h-64 bg-blue-500/20 rounded-full blur-2xl"
                />
                <div className="relative w-48 h-48 border-4 border-blue-500/30 rounded-full flex items-center justify-center overflow-hidden bg-slate-900 shadow-2xl">
                    <motion.div
                        animate={{
                            height: ["20%", "60%", "30%", "80%", "40%"]
                        }}
                        transition={{ repeat: Infinity, duration: 1.5, ease: "easeInOut" }}
                        className="w-1 bg-blue-400 mx-1 rounded-full"
                    />
                    <motion.div
                        animate={{
                            height: ["40%", "20%", "70%", "40%", "90%"]
                        }}
                        transition={{ repeat: Infinity, duration: 1.2, ease: "easeInOut" }}
                        className="w-1 bg-blue-400 mx-1 rounded-full"
                    />
                    <motion.div
                        animate={{
                            height: ["60%", "90%", "40%", "20%", "60%"]
                        }}
                        transition={{ repeat: Infinity, duration: 1.8, ease: "easeInOut" }}
                        className="w-1 bg-blue-400 mx-1 rounded-full"
                    />
                </div>
             </div>

             <div className="text-center">
                <h2 className="text-3xl font-medium text-blue-100">Listening...</h2>
                <p className="text-slate-500 mt-2">&quot;Hi, I&apos;m looking for Sarah from Marketing.&quot;</p>
             </div>

             <div className="grid grid-cols-3 gap-6 w-full">
                <div className="p-4 bg-slate-900/50 border border-slate-800 rounded-2xl">
                    <div className="text-xs text-slate-500 uppercase tracking-widest mb-1">Status</div>
                    <div className="font-semibold">AI Agent Online</div>
                </div>
                <div className="p-4 bg-slate-900/50 border border-slate-800 rounded-2xl">
                    <div className="text-xs text-slate-500 uppercase tracking-widest mb-1">Latency</div>
                    <div className="font-semibold">142ms</div>
                </div>
                <div className="p-4 bg-slate-900/50 border border-slate-800 rounded-2xl">
                    <div className="text-xs text-slate-500 uppercase tracking-widest mb-1">Model</div>
                    <div className="font-semibold">GPT-4o Realtime</div>
                </div>
             </div>

             <button
                onClick={() => setIsConnected(false)}
                className="mt-8 text-slate-500 hover:text-white transition-colors"
             >
                End Session
             </button>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="absolute bottom-8 text-slate-700 text-sm">
        Powered by UNOYA AI & LiveKit
      </div>
    </div>
  );
}
