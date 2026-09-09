import React from 'react';
import { ActiveScreen } from '../types';
import { Bot, MessageSquare, Activity, ShieldCheck, Settings } from 'lucide-react';

interface OrbitBottomNavProps {
  activeScreen: ActiveScreen;
  onSelectScreen: (screen: ActiveScreen) => void;
  pendingCount?: number;
}

export const OrbitBottomNav: React.FC<OrbitBottomNavProps> = ({
  activeScreen,
  onSelectScreen,
  pendingCount = 0,
}) => {
  const navItems: { id: ActiveScreen; label: string; icon: React.ComponentType<{ className?: string }> }[] = [
    { id: 'home', label: 'Orbit', icon: Bot },
    { id: 'chat', label: 'Chat', icon: MessageSquare },
    { id: 'activity', label: 'Activity', icon: Activity },
    { id: 'permissions', label: 'Security', icon: ShieldCheck },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <nav
      id="orbit-bottom-nav"
      className="bg-slate-900/90 backdrop-blur-md border-t border-slate-800/80 px-2 py-2 flex items-center justify-around z-30 select-none"
    >
      {navItems.map((item) => {
        const Icon = item.icon;
        const isActive = activeScreen === item.id;
        return (
          <button
            key={item.id}
            id={`nav-tab-${item.id}`}
            onClick={() => onSelectScreen(item.id)}
            className={`flex flex-col items-center justify-center py-1 px-3 rounded-xl transition-all duration-200 relative ${
              isActive
                ? 'text-cyan-400 font-semibold'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <div className="relative">
              <Icon className={`w-5 h-5 transition-transform duration-200 ${isActive ? 'scale-110 drop-shadow-[0_0_8px_rgba(6,182,212,0.8)]' : ''}`} />
              {item.id === 'activity' && pendingCount > 0 && (
                <span className="absolute -top-1 -right-2 bg-cyan-500 text-black text-[10px] font-bold rounded-full w-4 h-4 flex items-center justify-center animate-pulse">
                  {pendingCount}
                </span>
              )}
            </div>
            <span className="text-[11px] mt-1 tracking-tight">{item.label}</span>
            {isActive && (
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 mt-0.5 shadow-[0_0_6px_#22d3ee]" />
            )}
          </button>
        );
      })}
    </nav>
  );
};
