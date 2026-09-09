import React, { useState } from 'react';
import { ActionItem } from '../types';
import { CheckCircle2, Clock, AlertTriangle, Play, Trash2, Cpu, ArrowUpRight } from 'lucide-react';

interface ActivityScreenProps {
  actions: ActionItem[];
  onClearActivity: () => void;
  onRerunAction?: (action: ActionItem) => void;
}

export const ActivityScreen: React.FC<ActivityScreenProps> = ({
  actions,
  onClearActivity,
  onRerunAction,
}) => {
  const [filter, setFilter] = useState<'ALL' | 'COMPLETED' | 'IN_PROGRESS' | 'FAILED'>('ALL');
  const [selectedAction, setSelectedAction] = useState<ActionItem | null>(null);

  const filteredActions = actions.filter((a) => {
    if (filter === 'ALL') return true;
    return a.status === filter;
  });

  return (
    <div id="orbit-activity-screen" className="flex-1 flex flex-col h-full bg-slate-950 overflow-hidden">
      {/* Top Header */}
      <div className="p-4 bg-slate-900/60 border-b border-slate-800/80 flex items-center justify-between">
        <div>
          <h2 className="text-sm font-semibold text-slate-100 flex items-center space-x-2">
            <Cpu className="w-4 h-4 text-cyan-400" />
            <span>Activity & Tool Audit</span>
          </h2>
          <p className="text-[11px] text-slate-400 mt-0.5">
            Log of on-device tool calls and autonomous actions
          </p>
        </div>

        {actions.length > 0 && (
          <button
            id="clear-activity-button"
            onClick={onClearActivity}
            className="inline-flex items-center space-x-1 px-2.5 py-1 rounded-lg text-xs text-slate-400 hover:text-rose-400 hover:bg-slate-800/80 transition-colors"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>Clear Log</span>
          </button>
        )}
      </div>

      {/* Filter Tabs */}
      <div className="px-4 py-2 border-b border-slate-800/60 flex items-center space-x-2 overflow-x-auto bg-slate-900/30">
        {(['ALL', 'COMPLETED', 'IN_PROGRESS', 'FAILED'] as const).map((tab) => (
          <button
            key={tab}
            id={`filter-tab-${tab.toLowerCase()}`}
            onClick={() => setFilter(tab)}
            className={`px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap transition-colors ${
              filter === tab
                ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Actions List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {filteredActions.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center text-slate-500 py-12">
            <CheckCircle2 className="w-10 h-10 text-slate-700 mb-2" />
            <p className="text-xs text-slate-400">No actions logged yet</p>
            <p className="text-[11px] text-slate-500 max-w-xs mt-1">
              Actions executed via Orbit voice or text commands will appear here in real time.
            </p>
          </div>
        ) : (
          filteredActions.map((action) => {
            const isCompleted = action.status === 'COMPLETED';
            const isFailed = action.status === 'FAILED';
            const isInProgress = action.status === 'IN_PROGRESS';

            return (
              <div
                key={action.id}
                id={`activity-item-${action.id}`}
                onClick={() => setSelectedAction(action)}
                className="p-3 rounded-xl bg-slate-900/70 hover:bg-slate-900 border border-slate-800/80 hover:border-slate-700 transition-all cursor-pointer shadow-sm group"
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-2.5">
                    {/* Status icon */}
                    <div className="mt-0.5">
                      {isCompleted && <CheckCircle2 className="w-4 h-4 text-emerald-400" />}
                      {isInProgress && <Play className="w-4 h-4 text-amber-400 animate-spin" />}
                      {isFailed && <AlertTriangle className="w-4 h-4 text-rose-400" />}
                    </div>

                    <div>
                      <h3 className="text-xs font-semibold text-slate-200 group-hover:text-cyan-300 transition-colors">
                        {action.title}
                      </h3>
                      <p className="text-[11px] text-slate-400 mt-0.5 leading-snug line-clamp-2">
                        {action.detail}
                      </p>
                    </div>
                  </div>

                  {/* Meta: time and latency */}
                  <div className="flex flex-col items-end space-y-1 flex-shrink-0 ml-2">
                    <span className="text-[10px] text-slate-500">{action.timestamp}</span>
                    {action.durationMs && (
                      <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950/40 px-1.5 py-0.5 rounded">
                        {action.durationMs}ms
                      </span>
                    )}
                  </div>
                </div>

                {/* Footer Tag */}
                <div className="mt-2.5 pt-2 border-t border-slate-800/60 flex items-center justify-between text-[10px] text-slate-500 font-mono">
                  <span>tool: {action.toolName}</span>
                  <span className="flex items-center text-slate-400 group-hover:text-cyan-400">
                    Inspect <ArrowUpRight className="w-3 h-3 ml-0.5" />
                  </span>
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Detail Modal / Drawer if an action is clicked */}
      {selectedAction && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 max-w-sm w-full space-y-3 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <h3 className="text-sm font-semibold text-slate-100">{selectedAction.title}</h3>
              <button
                onClick={() => setSelectedAction(null)}
                className="text-slate-400 hover:text-slate-200 text-xs px-2 py-1 rounded"
              >
                ✕
              </button>
            </div>

            <div className="space-y-2 text-xs text-slate-300">
              <div>
                <span className="text-slate-500 block text-[10px]">STATUS</span>
                <span className="font-semibold text-emerald-400">{selectedAction.status}</span>
              </div>
              <div>
                <span className="text-slate-500 block text-[10px]">TOOL EXECUTED</span>
                <span className="font-mono text-cyan-300">{selectedAction.toolName}</span>
              </div>
              <div>
                <span className="text-slate-500 block text-[10px]">TIMESTAMP</span>
                <span>{selectedAction.timestamp}</span>
              </div>
              <div>
                <span className="text-slate-500 block text-[10px]">DETAILS / OUTPUT</span>
                <p className="bg-slate-950 p-2.5 rounded-lg border border-slate-800 font-mono text-[11px] text-slate-200 mt-1">
                  {selectedAction.detail}
                </p>
              </div>
            </div>

            <button
              onClick={() => setSelectedAction(null)}
              className="w-full py-2 rounded-xl bg-cyan-500 text-slate-950 font-semibold text-xs hover:bg-cyan-400 transition-colors mt-2"
            >
              Done
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
