import React, { useState, useEffect } from 'react';
import { Wifi, Battery, BatteryCharging, Zap, Smartphone, Monitor } from 'lucide-react';
import { DeviceStatus } from '../services/orbitEngine';

interface OrbitHeaderProps {
  deviceStatus: DeviceStatus;
  isOnline: boolean;
  isPhoneFrame: boolean;
  onToggleFrame: () => void;
}

export const OrbitHeader: React.FC<OrbitHeaderProps> = ({
  deviceStatus,
  isOnline,
  isPhoneFrame,
  onToggleFrame,
}) => {
  const [timeStr, setTimeStr] = useState<string>('');

  useEffect(() => {
    const update = () => {
      const now = new Date();
      setTimeStr(
        now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      );
    };
    update();
    const interval = setInterval(update, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header
      id="orbit-status-bar"
      className="w-full bg-slate-950/80 backdrop-blur-sm border-b border-slate-800/60 px-4 py-2 flex items-center justify-between text-xs text-slate-300 select-none z-30"
    >
      {/* Left: Time & Brand */}
      <div className="flex items-center space-x-2">
        <span className="font-semibold text-slate-100 tracking-wider">{timeStr}</span>
        <span className="hidden sm:inline-block text-slate-500">•</span>
        <div className="flex items-center space-x-1.5">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
          <span className="text-[11px] font-mono font-medium text-emerald-400">
            {isOnline ? 'OmniRoute' : 'Offline'}
          </span>
        </div>
      </div>

      {/* Center: Device Features pill */}
      <div className="flex items-center space-x-2 text-[11px]">
        {deviceStatus.flashlightOn && (
          <span className="inline-flex items-center space-x-1 px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/40 animate-pulse">
            <Zap className="w-3 h-3" />
            <span>Torch ON</span>
          </span>
        )}
      </div>

      {/* Right: Phone frame switch, Wi-Fi, Battery */}
      <div className="flex items-center space-x-3">
        <button
          id="toggle-view-frame-button"
          onClick={onToggleFrame}
          className="p-1 rounded hover:bg-slate-800 text-slate-400 hover:text-cyan-400 transition-colors"
          title={isPhoneFrame ? 'Switch to Full Screen View' : 'Switch to Phone View'}
        >
          {isPhoneFrame ? (
            <Monitor className="w-3.5 h-3.5" />
          ) : (
            <Smartphone className="w-3.5 h-3.5" />
          )}
        </button>

        <div className="flex items-center space-x-1 text-slate-400" title="Wi-Fi: Connected (5GHz)">
          <Wifi className="w-3.5 h-3.5 text-cyan-400" />
        </div>

        <div
          className="flex items-center space-x-1 text-slate-300"
          title={`Battery: ${deviceStatus.batteryLevel}%`}
        >
          <span className="font-mono text-[10px]">{deviceStatus.batteryLevel}%</span>
          {deviceStatus.isCharging ? (
            <BatteryCharging className="w-4 h-4 text-emerald-400" />
          ) : (
            <Battery className="w-4 h-4 text-slate-300" />
          )}
        </div>
      </div>
    </header>
  );
};
