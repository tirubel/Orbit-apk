import React, { useState } from 'react';
import { OrbitCore } from './OrbitCore';
import { OrbitState, ActionItem } from '../types';
import { Mic, MicOff, Send, Sparkles, Volume2, Clock, Battery, Search, Smartphone } from 'lucide-react';

interface HomeScreenProps {
  orbitState: OrbitState;
  stateLabel: string;
  stateSubtitle: string;
  activeQuery: string;
  currentTask?: string | null;
  lastAction?: ActionItem | null;
  isListening: boolean;
  onToggleListening: () => void;
  onSubmitQuery: (text: string) => void;
  onStopSpeech: () => void;
}

export const HomeScreen: React.FC<HomeScreenProps> = ({
  orbitState,
  stateLabel,
  stateSubtitle,
  activeQuery,
  currentTask,
  lastAction,
  isListening,
  onToggleListening,
  onSubmitQuery,
  onStopSpeech,
}) => {
  const [inputText, setInputText] = useState('');

  const handleSend = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!inputText.trim()) return;
    onSubmitQuery(inputText.trim());
    setInputText('');
  };

  const samplePrompts = [
    { label: 'What time is it?', icon: Clock },
    { label: 'Check battery status', icon: Battery },
    { label: 'Search quantum computing', icon: Search },
    { label: 'Turn on flashlight', icon: Sparkles },
    { label: 'Open YouTube', icon: Smartphone },
  ];

  return (
    <div
      id="orbit-home-screen"
      className="flex-1 flex flex-col items-center justify-between p-4 sm:p-6 overflow-y-auto max-w-lg mx-auto w-full select-none"
    >
      {/* Top: Status Badges */}
      <div className="w-full flex flex-col items-center pt-2 text-center">
        <div className="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-slate-800/80 border border-slate-700/60 shadow-inner">
          <span
            className={`w-2 h-2 rounded-full ${
              orbitState === 'IDLE'
                ? 'bg-cyan-400'
                : orbitState === 'LISTENING'
                ? 'bg-purple-400 animate-pulse'
                : orbitState === 'THINKING'
                ? 'bg-amber-400 animate-spin'
                : orbitState === 'EXECUTING'
                ? 'bg-emerald-400 animate-ping'
                : orbitState === 'SPEAKING'
                ? 'bg-blue-400 animate-bounce'
                : 'bg-rose-500'
            }`}
          />
          <span className="text-xs font-semibold tracking-wider uppercase text-slate-200">
            {stateLabel}
          </span>
        </div>
        <p className="text-xs text-slate-400 mt-1.5 max-w-xs">{stateSubtitle}</p>
      </div>

      {/* Middle: Reactive Glowing Core */}
      <div className="my-auto flex flex-col items-center justify-center py-4 relative">
        <OrbitCore
          state={orbitState}
          size={250}
          audioLevel={isListening || orbitState === 'SPEAKING' ? 0.8 : 0.15}
          onClick={onToggleListening}
        />

        {/* Live Audio Visualizer ripples during Voice active */}
        {(isListening || orbitState === 'SPEAKING') && (
          <div className="flex items-center space-x-1 mt-4 h-6">
            <span className="w-1 h-3 rounded-full bg-cyan-400/80 animate-pulse" />
            <span className="w-1 h-5 rounded-full bg-cyan-400/80 animate-pulse" />
            <span className="w-1 h-6 rounded-full bg-cyan-400/80 animate-pulse" />
            <span className="w-1 h-4 rounded-full bg-cyan-400/80 animate-pulse" />
            <span className="w-1 h-6 rounded-full bg-cyan-400/80 animate-pulse" />
            <span className="w-1 h-3 rounded-full bg-cyan-400/80 animate-pulse" />
            <span className="w-1 h-5 rounded-full bg-cyan-400/80 animate-pulse" />
            <span className="w-1 h-4 rounded-full bg-cyan-400/80 animate-pulse" />
            <span className="w-1 h-5 rounded-full bg-cyan-400/80 animate-pulse" />
            <span className="w-1 h-2 rounded-full bg-cyan-400/80 animate-pulse" />
          </div>
        )}

        {/* Live speech feedback if active query is being recognized */}
        {activeQuery && (
          <div className="mt-3 px-4 py-1.5 rounded-xl bg-slate-800/90 border border-slate-700 max-w-xs text-center">
            <span className="text-xs text-slate-400">Heard: </span>
            <span className="text-xs text-cyan-300 font-medium">"{activeQuery}"</span>
          </div>
        )}

        {/* Active Task Banner if working */}
        {currentTask && (
          <div className="mt-3 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs flex items-center space-x-2">
            <Sparkles className="w-3 h-3 animate-spin" />
            <span>{currentTask}</span>
          </div>
        )}

        {/* Speaking controller if assistant is vocalizing */}
        {orbitState === 'SPEAKING' && (
          <button
            id="stop-speaking-button"
            onClick={onStopSpeech}
            className="mt-3 inline-flex items-center space-x-1 px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 border border-blue-500/40 text-xs hover:bg-blue-500/30 transition-colors"
          >
            <Volume2 className="w-3 h-3" />
            <span>Stop Voice</span>
          </button>
        )}
      </div>

      {/* Bottom Area: Sample Prompts & Controls */}
      <div className="w-full space-y-4 pb-2">
        {/* Quick prompt pills */}
        <div className="flex flex-wrap items-center justify-center gap-2">
          {samplePrompts.map((p, idx) => {
            const Icon = p.icon;
            return (
              <button
                key={idx}
                id={`quick-prompt-${idx}`}
                onClick={() => onSubmitQuery(p.label)}
                className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-full bg-slate-800/60 hover:bg-slate-700/80 border border-slate-700/50 text-slate-300 hover:text-cyan-300 text-xs transition-colors shadow-sm active:scale-95"
              >
                <Icon className="w-3 h-3 text-cyan-400" />
                <span>{p.label}</span>
              </button>
            );
          })}
        </div>

        {/* Last Action Notification Card (if any) */}
        {lastAction && (
          <div
            id="last-action-summary-card"
            className="w-full p-2.5 rounded-xl bg-slate-900/80 border border-slate-800 flex items-center justify-between text-xs"
          >
            <div className="flex items-center space-x-2 truncate">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 flex-shrink-0" />
              <span className="font-semibold text-slate-200 truncate">{lastAction.title}</span>
              <span className="text-slate-500 text-[10px]">({lastAction.timestamp})</span>
            </div>
            <span className="text-[10px] text-cyan-400 font-mono flex-shrink-0 ml-2">
              {lastAction.status}
            </span>
          </div>
        )}

        {/* Query Input Bar & Mic Trigger */}
        <form
          id="orbit-query-form"
          onSubmit={handleSend}
          className="flex items-center space-x-2 w-full"
        >
          <div className="relative flex-1">
            <input
              id="orbit-query-input"
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder={isListening ? 'Listening to your voice...' : 'Ask Orbit anything...'}
              className="w-full bg-slate-900/90 border border-slate-700 rounded-full px-4 py-2.5 text-xs sm:text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all shadow-inner"
            />
            {inputText.trim() && (
              <button
                type="submit"
                id="orbit-submit-button"
                className="absolute right-1.5 top-1.5 p-1.5 rounded-full bg-cyan-500 text-black hover:bg-cyan-400 transition-colors shadow"
                title="Send query"
              >
                <Send className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

          {/* Big Mic Button */}
          <button
            type="button"
            id="orbit-mic-button"
            onClick={onToggleListening}
            className={`p-3 rounded-full transition-all duration-300 relative shadow-lg ${
              isListening
                ? 'bg-purple-600 text-white ring-4 ring-purple-500/40 animate-pulse scale-105'
                : 'bg-cyan-500 text-slate-950 hover:bg-cyan-400 active:scale-95'
            }`}
            title={isListening ? 'Tap to stop listening' : 'Tap to speak to Orbit'}
          >
            {isListening ? (
              <MicOff className="w-5 h-5" />
            ) : (
              <Mic className="w-5 h-5" />
            )}
          </button>
        </form>
      </div>
    </div>
  );
};
