import React from 'react';
import { PermissionItem } from '../types';
import { ShieldCheck, Mic, Eye, Settings, Bell, HardDrive, Check, AlertCircle } from 'lucide-react';

interface PermissionsScreenProps {
  permissions: PermissionItem[];
  onTogglePermission: (id: string) => void;
}

export const PermissionsScreen: React.FC<PermissionsScreenProps> = ({
  permissions,
  onTogglePermission,
}) => {
  const getIcon = (iconName: string) => {
    switch (iconName) {
      case 'mic':
        return Mic;
      case 'eye':
        return Eye;
      case 'settings':
        return Settings;
      case 'bell':
        return Bell;
      case 'storage':
      default:
        return HardDrive;
    }
  };

  const allGranted = permissions.every((p) => p.granted);

  return (
    <div id="orbit-permissions-screen" className="flex-1 flex flex-col h-full bg-slate-950 overflow-y-auto p-4 space-y-4">
      {/* Header */}
      <div className="flex items-center space-x-3 bg-slate-900/60 p-3.5 rounded-2xl border border-slate-800/80">
        <div className={`p-2.5 rounded-xl ${allGranted ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'}`}>
          <ShieldCheck className="w-6 h-6" />
        </div>
        <div>
          <h2 className="text-sm font-semibold text-slate-100">Android System Capabilities</h2>
          <p className="text-[11px] text-slate-400">
            {allGranted ? 'All autonomous services operational' : 'Some permissions required for device actions'}
          </p>
        </div>
      </div>

      {/* Permissions List */}
      <div className="space-y-2.5">
        {permissions.map((perm) => {
          const Icon = getIcon(perm.icon);

          return (
            <div
              key={perm.id}
              id={`permission-item-${perm.id}`}
              className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800/90 flex items-center justify-between space-x-3 hover:border-slate-700 transition-colors"
            >
              <div className="flex items-start space-x-3">
                <div className={`p-2 rounded-lg mt-0.5 ${perm.granted ? 'bg-cyan-500/10 text-cyan-400' : 'bg-slate-800 text-slate-500'}`}>
                  <Icon className="w-4 h-4" />
                </div>
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs font-semibold text-slate-200">{perm.name}</span>
                    {perm.critical && (
                      <span className="text-[9px] px-1.5 py-0.2 rounded bg-rose-500/20 text-rose-300 font-semibold">
                        REQUIRED
                      </span>
                    )}
                  </div>
                  <p className="text-[11px] text-slate-400 mt-0.5 leading-snug">
                    {perm.description}
                  </p>
                </div>
              </div>

              {/* Toggle Switch */}
              <button
                type="button"
                id={`toggle-perm-${perm.id}`}
                onClick={() => onTogglePermission(perm.id)}
                className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none ${
                  perm.granted ? 'bg-cyan-500' : 'bg-slate-700'
                }`}
              >
                <span
                  className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                    perm.granted ? 'translate-x-5' : 'translate-x-0'
                  }`}
                />
              </button>
            </div>
          );
        })}
      </div>

      {/* Info Card */}
      <div className="p-3 rounded-xl bg-slate-900/40 border border-slate-800 text-[11px] text-slate-400 flex items-start space-x-2">
        <AlertCircle className="w-4 h-4 text-cyan-400 flex-shrink-0 mt-0.5" />
        <span>
          Orbit runs local intent actions on Android. Permissions are stored securely in Android SharedPreferences and can be revoked at any time.
        </span>
      </div>
    </div>
  );
};
