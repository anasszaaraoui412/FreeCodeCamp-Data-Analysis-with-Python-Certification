"use client";

import React, { useState } from "react";
import {
  LiveKitRoom,
  RoomAudioRenderer,
  ControlBar,
  VideoConference,
  ParticipantTile,
  useParticipants,
  TrackReference,
  ParticipantLoop,
  ParticipantContext,
  useRemoteParticipants,
  useTracks,
  useIsSpeaking,
  useLocalParticipant
} from "@livekit/components-react";
import { Track, Participant } from "livekit-client";
import "@livekit/components-styles";
import { motion, AnimatePresence } from "framer-motion";

function AnamAvatar() {
  const tracks = useTracks([Track.Source.Camera]);
  const anamTrack = tracks.find(t => t.participant.identity.includes("anam") || t.participant.identity.includes("agent"));
  const isSpeaking = useIsSpeaking(anamTrack?.participant);

  if (!anamTrack) return (
    <div className="w-full h-full flex items-center justify-center relative">
       <div className="absolute inset-0 bg-gradient-to-b from-transparent to-slate-950/50 z-10" />
       <img
          src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=1200"
          alt="AI Avatar Placeholder"
          className="w-full h-full object-cover opacity-80"
       />
       <div className="absolute z-20 bottom-8 text-center w-full">
          <div className="text-2xl font-semibold text-white drop-shadow-lg">Anam Virtual Assistant</div>
          <div className="text-blue-400 text-sm mt-1">Connecting to neural stream...</div>
       </div>
    </div>
  );

  return (
    <div className="relative w-full h-full flex items-center justify-center">
      <AnimatePresence>
        {isSpeaking && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1.05 }}
            exit={{ opacity: 0, scale: 1.1 }}
            transition={{
              duration: 0.8,
              repeat: Infinity,
              repeatType: "reverse"
            }}
            className="absolute inset-4 rounded-[2rem] border-4 border-blue-500/40 blur-xl z-0"
          />
        )}
      </AnimatePresence>
      <div className="z-10 w-full h-full rounded-3xl overflow-hidden border border-white/10 shadow-2xl">
        <ParticipantTile trackRef={anamTrack} />
      </div>
    </div>
  );
}

function ListeningIndicator() {
  const { localParticipant } = useLocalParticipant();
  const isSpeaking = useIsSpeaking(localParticipant);

  return (
    <div className="flex items-center justify-center gap-2 mt-4 h-6">
      <AnimatePresence mode="wait">
        {isSpeaking ? (
          <motion.div
            key="listening"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="flex gap-1 items-end h-4"
          >
            {[0, 1, 2, 3, 4].map((i) => (
              <motion.div
                key={i}
                animate={{ height: [4, 16, 4] }}
                transition={{
                  repeat: Infinity,
                  duration: 0.5,
                  delay: i * 0.1
                }}
                className="w-1 bg-blue-400 rounded-full"
              />
            ))}
          </motion.div>
        ) : (
          <motion.div
            key="idle"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="flex items-center gap-2"
          >
            <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ repeat: Infinity, duration: 2 }}
                className="w-2 h-2 bg-blue-500 rounded-full"
            />
            <span className="text-slate-500 uppercase tracking-widest text-[10px]">AI Processing</span>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default function TotemPage() {
  const [token, setToken] = useState<string | null>(null);
  const [url, setUrl] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const startSession = async () => {
     setIsConnected(true);
     setError(null);

     try {
       const resp = await fetch("http://localhost:8000/api/v1/livekit-token", {
         headers: {
           "X-Mock-Role": "employee",
           "X-Mock-User-Email": "totem@unoya.ai"
         }
       });

       if (!resp.ok) {
         throw new Error("Failed to get token");
       }

       const data = await resp.json();
       setToken(data.token);
       setUrl("ws://localhost:7880");
     } catch (err) {
       console.error(err);
       setError("Failed to connect to AI server. Please try again.");
       setIsConnected(false);
     }
  };

  return (
    <div className="h-screen w-full bg-slate-950 flex flex-col items-center justify-center text-white overflow-hidden relative">
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

            {error && (
              <div className="bg-red-500/20 border border-red-500 text-red-200 px-4 py-2 rounded-lg text-sm">
                {error}
              </div>
            )}

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
            className="z-10 flex flex-col items-center gap-12 w-full max-w-6xl px-4"
          >
             {/* Avatar Display Area */}
             <div className="relative w-full aspect-video max-h-[60vh] rounded-3xl overflow-hidden border border-slate-800 bg-slate-900 shadow-2xl">
                {token && url ? (
                  <LiveKitRoom
                    video={true}
                    audio={true}
                    token={token}
                    serverUrl={url}
                    data-lk-theme="default"
                    style={{ height: '100%' }}
                  >
                    <AnamAvatar />
                    <RoomAudioRenderer />
                  </LiveKitRoom>
                ) : (
                  <div className="w-full h-full flex items-center justify-center relative">
                     <div className="absolute inset-0 bg-gradient-to-b from-transparent to-slate-950/50 z-10" />
                     {/* Placeholder for Anam Avatar Video */}
                     <img
                        src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=1200"
                        alt="AI Avatar Placeholder"
                        className="w-full h-full object-cover opacity-80"
                     />
                     <div className="absolute z-20 bottom-8 text-center w-full">
                        <div className="text-2xl font-semibold text-white drop-shadow-lg">Anam Virtual Assistant</div>
                        <div className="text-blue-400 text-sm mt-1">Connecting to neural stream...</div>
                     </div>
                  </div>
                )}
             </div>

             <div className="text-center">
                <h2 className="text-3xl font-medium text-blue-100">How can I help you today?</h2>
                <ListeningIndicator />
             </div>

             <div className="grid grid-cols-3 gap-6 w-full max-w-4xl">
                <div className="p-4 bg-slate-900/50 border border-slate-800 rounded-2xl backdrop-blur-sm">
                    <div className="text-xs text-slate-500 uppercase tracking-widest mb-1">Avatar Status</div>
                    <div className="font-semibold text-green-400">Lifelike Sync Active</div>
                </div>
                <div className="p-4 bg-slate-900/50 border border-slate-800 rounded-2xl backdrop-blur-sm">
                    <div className="text-xs text-slate-500 uppercase tracking-widest mb-1">Interaction</div>
                    <div className="font-semibold text-blue-100">Voice & Vision</div>
                </div>
                <div className="p-4 bg-slate-900/50 border border-slate-800 rounded-2xl backdrop-blur-sm">
                    <div className="text-xs text-slate-500 uppercase tracking-widest mb-1">Emotion</div>
                    <div className="font-semibold text-blue-100">Professional</div>
                </div>
             </div>

             <button
                onClick={() => setIsConnected(false)}
                className="mt-4 text-slate-500 hover:text-white transition-colors underline underline-offset-4 decoration-slate-800"
             >
                End Session
             </button>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="absolute bottom-8 text-slate-700 text-xs tracking-widest uppercase">
        UNOYA Virtual Intelligence × Anam AI × LiveKit
      </div>
    </div>
  );
}
