export type OrbitState =
  | 'IDLE'
  | 'CONNECTING'
  | 'LISTENING'
  | 'THINKING'
  | 'EXECUTING'
  | 'SPEAKING'
  | 'ERROR'
  | 'OFFLINE';

export interface ActionItem {
  id: string;
  title: string;
  detail: string;
  timestamp: string;
  status: 'COMPLETED' | 'FAILED' | 'IN_PROGRESS';
  toolName: string;
  durationMs?: number;
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'orbit' | 'system';
  text: string;
  timestamp: string;
  toolExecution?: {
    tool: string;
    input: string;
    output: string;
    status: 'success' | 'error';
  };
  isVoice?: boolean;
}

export interface SettingsState {
  omniRouteUrl: string;
  model: string;
  voicePersonality: string;
  speechSpeed: number;
  speechPitch: number;
  autoListen: boolean;
  hapticsEnabled: boolean;
  localFallback: boolean;
  wakeWordEnabled: boolean;
  themeMode: 'dark' | 'midnight' | 'neon';
}

export interface PermissionItem {
  id: string;
  name: string;
  description: string;
  granted: boolean;
  critical: boolean;
  icon: string;
}

export type ActiveScreen = 'home' | 'chat' | 'activity' | 'permissions' | 'settings';
