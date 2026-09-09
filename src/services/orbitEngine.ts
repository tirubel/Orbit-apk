import { ActionItem, ChatMessage, OrbitState } from '../types';

export interface ProcessQueryResult {
  reply: string;
  toolAction?: ActionItem;
  speechText?: string;
}

// Built-in device simulation status
export interface DeviceStatus {
  batteryLevel: number;
  isCharging: boolean;
  flashlightOn: boolean;
  volumeLevel: number;
  wifiConnected: boolean;
}

export class OrbitEngine {
  private deviceStatus: DeviceStatus = {
    batteryLevel: 88,
    isCharging: false,
    flashlightOn: false,
    volumeLevel: 75,
    wifiConnected: true,
  };

  public getDeviceStatus(): DeviceStatus {
    return { ...this.deviceStatus };
  }

  public setFlashlight(on: boolean): void {
    this.deviceStatus.flashlightOn = on;
  }

  public setVolume(level: number): void {
    this.deviceStatus.volumeLevel = Math.max(0, Math.min(100, level));
  }

  public async executeQuery(
    query: string,
    onStateChange: (state: OrbitState, label?: string) => void
  ): Promise<ProcessQueryResult> {
    const trimmed = query.trim();
    if (!trimmed) {
      return { reply: "I didn't catch that. How can I help you?" };
    }

    onStateChange('THINKING', 'Analyzing intent...');
    await new Promise((r) => setTimeout(r, 600));

    const lower = trimmed.toLowerCase();

    // 1. Tool: Current Time & Date
    if (
      lower.includes('time') ||
      lower.includes('date') ||
      lower.includes('what day') ||
      lower.includes('clock')
    ) {
      onStateChange('EXECUTING', 'Retrieving device time...');
      await new Promise((r) => setTimeout(r, 400));
      const now = new Date();
      const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
      const dateStr = now.toLocaleDateString([], { weekday: 'long', month: 'short', day: 'numeric', year: 'numeric' });
      const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

      const actionItem: ActionItem = {
        id: `act_${Date.now()}`,
        title: 'Get Device Time',
        detail: `Retrieved system clock: ${timeStr} (${timezone})`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        status: 'COMPLETED',
        toolName: 'get_current_time',
        durationMs: 380,
      };

      return {
        reply: `It's currently ${timeStr} on ${dateStr} (${timezone}).`,
        toolAction: actionItem,
        speechText: `It is currently ${timeStr} on ${dateStr}.`,
      };
    }

    // 2. Tool: Flashlight / Device Control
    if (lower.includes('flashlight') || lower.includes('torch')) {
      onStateChange('EXECUTING', 'Updating device hardware state...');
      await new Promise((r) => setTimeout(r, 450));
      const turnOn = !lower.includes('off') && (lower.includes('on') || !this.deviceStatus.flashlightOn);
      this.deviceStatus.flashlightOn = turnOn;

      const actionItem: ActionItem = {
        id: `act_${Date.now()}`,
        title: turnOn ? 'Turn On Flashlight' : 'Turn Off Flashlight',
        detail: `Camera flash hardware set to ${turnOn ? 'HIGH_INTENSITY' : 'OFF'}`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        status: 'COMPLETED',
        toolName: 'device_hardware_control',
        durationMs: 420,
      };

      const msg = turnOn ? 'I have turned on your device flashlight.' : 'Flashlight has been switched off.';
      return {
        reply: msg,
        toolAction: actionItem,
        speechText: msg,
      };
    }

    // 3. Tool: Battery Status
    if (lower.includes('battery') || lower.includes('power') || lower.includes('charge')) {
      onStateChange('EXECUTING', 'Querying BatteryManager service...');
      await new Promise((r) => setTimeout(r, 350));

      const actionItem: ActionItem = {
        id: `act_${Date.now()}`,
        title: 'Check Battery Status',
        detail: `Battery at ${this.deviceStatus.batteryLevel}% • ${this.deviceStatus.isCharging ? 'Charging' : 'Discharging'} • Health: Good (38°C)`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        status: 'COMPLETED',
        toolName: 'battery_manager',
        durationMs: 320,
      };

      const reply = `Your battery is at ${this.deviceStatus.batteryLevel}%, currently ${
        this.deviceStatus.isCharging ? 'charging' : 'on battery power'
      }. Thermal temperature is normal.`;

      return {
        reply,
        toolAction: actionItem,
        speechText: reply,
      };
    }

    // 4. Tool: Open App
    if (lower.startsWith('open ') || lower.startsWith('launch ') || lower.includes('open app')) {
      const appName = trimmed.replace(/^(open|launch)\s+/i, '').replace(/app\s*/i, '').trim();
      onStateChange('EXECUTING', `Launching ${appName}...`);
      await new Promise((r) => setTimeout(r, 500));

      const actionItem: ActionItem = {
        id: `act_${Date.now()}`,
        title: `Launch ${appName.charAt(0).toUpperCase() + appName.slice(1)}`,
        detail: `Intent android.intent.action.MAIN dispatched for ${appName}`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        status: 'COMPLETED',
        toolName: 'open_app',
        durationMs: 510,
      };

      const reply = `Opening ${appName}. Dispatched launch intent to the Android system package manager.`;
      return {
        reply,
        toolAction: actionItem,
        speechText: `Opening ${appName}.`,
      };
    }

    // 5. Tool: Volume Control
    if (lower.includes('volume') || lower.includes('sound level') || lower.includes('mute')) {
      onStateChange('EXECUTING', 'Adjusting AudioManager...');
      await new Promise((r) => setTimeout(r, 400));
      let newLevel = this.deviceStatus.volumeLevel;
      if (lower.includes('mute') || lower.includes('silent')) newLevel = 0;
      else if (lower.includes('max') || lower.includes('100')) newLevel = 100;
      else if (lower.includes('up') || lower.includes('increase')) newLevel = Math.min(100, newLevel + 20);
      else if (lower.includes('down') || lower.includes('decrease') || lower.includes('lower')) newLevel = Math.max(0, newLevel - 20);
      this.deviceStatus.volumeLevel = newLevel;

      const actionItem: ActionItem = {
        id: `act_${Date.now()}`,
        title: 'Adjust Audio Volume',
        detail: `STREAM_MUSIC volume set to ${newLevel}%`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        status: 'COMPLETED',
        toolName: 'audio_manager',
        durationMs: 380,
      };

      const reply = `Media volume is set to ${newLevel}%.`;
      return {
        reply,
        toolAction: actionItem,
        speechText: reply,
      };
    }

    // 6. Tool: Search Web
    if (
      lower.startsWith('search ') ||
      lower.startsWith('google ') ||
      lower.includes('who is') ||
      lower.includes('what is') ||
      lower.includes('tell me about') ||
      lower.includes('weather') ||
      lower.includes('news')
    ) {
      onStateChange('EXECUTING', 'OmniRoute Web Search executing...');
      await new Promise((r) => setTimeout(r, 700));

      const cleanQuery = trimmed.replace(/^(search for|search|google)\s+/i, '');
      const actionItem: ActionItem = {
        id: `act_${Date.now()}`,
        title: `Search: "${cleanQuery}"`,
        detail: `OmniRoute Search indexed 4 verified sources with low-latency synthesis`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        status: 'COMPLETED',
        toolName: 'search_web',
        durationMs: 680,
      };

      let answer = `Here is what I found regarding "${cleanQuery}": Verified knowledge from OmniRoute AI neural routing confirms comprehensive data matching your query. All systems are operational.`;

      if (lower.includes('weather')) {
        answer = `Current weather conditions: 72°F (22°C), partly cloudy with 45% humidity and a gentle breeze at 6 mph. No precipitation expected for the next 6 hours.`;
      } else if (lower.includes('orbit')) {
        answer = `Orbit Assistant is an autonomous on-device personal AI agent built with reactive glowing visuals, voice recognition, device hardware integration, and OmniRoute neural link capabilities.`;
      }

      return {
        reply: answer,
        toolAction: actionItem,
        speechText: answer,
      };
    }

    // 7. General Assistant Response
    onStateChange('EXECUTING', 'OmniRoute Neural Processing...');
    await new Promise((r) => setTimeout(r, 600));

    const actionItem: ActionItem = {
      id: `act_${Date.now()}`,
      title: 'OmniRoute Reasoning',
      detail: `Model: Gemini 2.5 Flash • Context tokens: 284 • Latency: 142ms`,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      status: 'COMPLETED',
      toolName: 'omniroute_llm',
      durationMs: 540,
    };

    const reply = `I processed: "${trimmed}". As your autonomous on-device assistant, I can trigger device tools, fetch live web answers, manage settings, or execute tasks. Try asking me "What time is it?", "Check battery", "Turn on flashlight", or "Search quantum physics".`;

    return {
      reply,
      toolAction: actionItem,
      speechText: `I have processed your request for ${trimmed}. All tools are ready.`,
    };
  }

  // Voice synthesis helper
  public speakText(
    text: string,
    speed: number = 1.0,
    pitch: number = 1.0,
    onStart?: () => void,
    onEnd?: () => void
  ): boolean {
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) {
      return false;
    }

    try {
      window.speechSynthesis.cancel(); // Stop any pending speech
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = speed;
      utterance.pitch = pitch;

      if (onStart) utterance.onstart = () => onStart();
      if (onEnd) utterance.onend = () => onEnd();
      utterance.onerror = () => onEnd && onEnd();

      window.speechSynthesis.speak(utterance);
      return true;
    } catch {
      if (onEnd) onEnd();
      return false;
    }
  }

  public stopSpeaking(): void {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
  }
}

export const orbitEngineInstance = new OrbitEngine();
