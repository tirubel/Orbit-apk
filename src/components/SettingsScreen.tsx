import React, { useState } from 'react';
import { SettingsState } from '../types';
import { Sliders, Cpu, Volume2, Globe, Check, RefreshCw, Smartphone } from 'lucide-react';

interface SettingsScreenProps {
  settings: SettingsState;
  onUpdateSettings: (updater: (prev: SettingsState) => SettingsState) => void;
  onTestConnection: () => Promise<{ latency: number; ok: boolean }>;
}

export const SettingsScreen: React.FC<SettingsScreenProps> = ({
  settings,
  onUpdateSettings,
  onTestConnection,
}) => {
  const [testingPing, setTestingPing] = useState(false);
  const [pingResult, setPingResult] = useState<{ latency: number; ok: boolean } | null>(null);

  const handlePing = async () => {
    setTestingPing(true);
    setPingResult(null);
    try {
      const res = await onTestConnection();
      setPingResult(res);
    } catch {
      setPingResult({ latency: 0, ok: false });
    } finally {
      setTestingPing(false);
    }
  };

  return (
    <div id="orbit-settings-screen" className="flex-1 flex flex-col h-full bg-slate-950 overflow-y-auto p-4 space-y-5">
      {/* OmniRoute Neural Service */}
      <section className="space-y-3">
        <div className="flex items-center space-x-2 text-slate-200">
          <Globe className="w-4 h-4 text-cyan-400" />
          <h3 className="text-xs font-semibold uppercase tracking-wider">OmniRoute AI Gateway</h3>
        </div>

        <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-3">
          <div>
            <label className="text-[11px] text-slate-400 block mb-1">Server Endpoint URL</label>
            <input
              id="settings-omniroute-url"
              type="text"
              value={settings.omniRouteUrl}
              onChange={(e) =>
                onUpdateSettings((s) => ({ ...s, omniRouteUrl: e.target.value }))
              }
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 font-mono focus:outline-none focus:border-cyan-500"
            />
          </div>

          <div className="flex items-center justify-between pt-1">
            <button
              id="test-omniroute-button"
              type="button"
              onClick={handlePing}
              disabled={testingPing}
              className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs text-cyan-400 transition-colors"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${testingPing ? 'animate-spin' : ''}`} />
              <span>{testingPing ? 'Pinging Gateway...' : 'Test Connection'}</span>
            </button>

            {pingResult && (
              <span className={`text-xs font-mono ${pingResult.ok ? 'text-emerald-400' : 'text-rose-400'}`}>
                {pingResult.ok ? `Connected • ${pingResult.latency}ms latency` : 'Connection Failed'}
              </span>
            )}
          </div>
        </div>
      </section>

      {/* Model Selection */}
      <section className="space-y-3">
        <div className="flex items-center space-x-2 text-slate-200">
          <Cpu className="w-4 h-4 text-cyan-400" />
          <h3 className="text-xs font-semibold uppercase tracking-wider">AI Reasoning Model</h3>
        </div>

        <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
          {[
            { id: 'gemini-2.5-flash', name: 'Gemini 2.5 Flash', desc: 'Fastest response time, optimized for device tools' },
            { id: 'gemini-2.5-pro', name: 'Gemini 2.5 Pro', desc: 'Deep contextual reasoning and multi-step workflows' },
            { id: 'omniroute-edge', name: 'OmniRoute Hybrid Edge', desc: 'Local model routing with cloud failover' },
          ].map((m) => (
            <div
              key={m.id}
              onClick={() => onUpdateSettings((s) => ({ ...s, model: m.id }))}
              className={`p-2.5 rounded-lg border cursor-pointer transition-all flex items-center justify-between ${
                settings.model === m.id
                  ? 'bg-cyan-950/40 border-cyan-500/60 text-slate-100'
                  : 'bg-slate-950 border-slate-800/80 text-slate-400 hover:border-slate-700'
              }`}
            >
              <div>
                <div className="text-xs font-semibold">{m.name}</div>
                <div className="text-[10px] text-slate-500">{m.desc}</div>
              </div>
              {settings.model === m.id && <Check className="w-4 h-4 text-cyan-400 flex-shrink-0" />}
            </div>
          ))}
        </div>
      </section>

      {/* Voice & Speech Tuning */}
      <section className="space-y-3">
        <div className="flex items-center space-x-2 text-slate-200">
          <Volume2 className="w-4 h-4 text-cyan-400" />
          <h3 className="text-xs font-semibold uppercase tracking-wider">Voice & Audio</h3>
        </div>

        <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-3">
          <div>
            <div className="flex justify-between text-[11px] text-slate-400 mb-1">
              <span>Speech Rate</span>
              <span className="font-mono text-cyan-400">{settings.speechSpeed}x</span>
            </div>
            <input
              type="range"
              min="0.7"
              max="1.5"
              step="0.1"
              value={settings.speechSpeed}
              onChange={(e) =>
                onUpdateSettings((s) => ({ ...s, speechSpeed: parseFloat(e.target.value) }))
              }
              className="w-full accent-cyan-400"
            />
          </div>

          <div className="flex items-center justify-between pt-1 border-t border-slate-800/60">
            <span className="text-xs text-slate-300">Continuous Auto-Listen</span>
            <button
              type="button"
              onClick={() =>
                onUpdateSettings((s) => ({ ...s, autoListen: !s.autoListen }))
              }
              className={`relative inline-flex h-5 w-9 rounded-full transition-colors ${
                settings.autoListen ? 'bg-cyan-500' : 'bg-slate-700'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                  settings.autoListen ? 'translate-x-4' : 'translate-x-0.5'
                } mt-0.5`}
              />
            </button>
          </div>
        </div>
      </section>

      {/* Device Integration */}
      <section className="space-y-3">
        <div className="flex items-center space-x-2 text-slate-200">
          <Smartphone className="w-4 h-4 text-cyan-400" />
          <h3 className="text-xs font-semibold uppercase tracking-wider">Device System</h3>
        </div>

        <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between py-1">
            <span className="text-xs text-slate-300">Haptic Feedback on Action</span>
            <button
              type="button"
              onClick={() =>
                onUpdateSettings((s) => ({ ...s, hapticsEnabled: !s.hapticsEnabled }))
              }
              className={`relative inline-flex h-5 w-9 rounded-full transition-colors ${
                settings.hapticsEnabled ? 'bg-cyan-500' : 'bg-slate-700'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                  settings.hapticsEnabled ? 'translate-x-4' : 'translate-x-0.5'
                } mt-0.5`}
              />
            </button>
          </div>

          <div className="flex items-center justify-between py-1 border-t border-slate-800/60">
            <span className="text-xs text-slate-300">Offline Fallback Engine</span>
            <button
              type="button"
              onClick={() =>
                onUpdateSettings((s) => ({ ...s, localFallback: !s.localFallback }))
              }
              className={`relative inline-flex h-5 w-9 rounded-full transition-colors ${
                settings.localFallback ? 'bg-cyan-500' : 'bg-slate-700'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                  settings.localFallback ? 'translate-x-4' : 'translate-x-0.5'
                } mt-0.5`}
              />
            </button>
          </div>
        </div>
      </section>
    </div>
  );
};
