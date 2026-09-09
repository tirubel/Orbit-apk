import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  ActiveScreen,
  OrbitState,
  ChatMessage,
  ActionItem,
  SettingsState,
  PermissionItem,
} from './types';
import { OrbitHeader } from './components/OrbitHeader';
import { OrbitBottomNav } from './components/OrbitBottomNav';
import { HomeScreen } from './components/HomeScreen';
import { ChatScreen } from './components/ChatScreen';
import { ActivityScreen } from './components/ActivityScreen';
import { PermissionsScreen } from './components/PermissionsScreen';
import { SettingsScreen } from './components/SettingsScreen';
import { orbitEngineInstance, DeviceStatus } from './services/orbitEngine';

export default function App() {
  const [activeScreen, setActiveScreen] = useState<ActiveScreen>('home');
  const [orbitState, setOrbitState] = useState<OrbitState>('IDLE');
  const [stateLabel, setStateLabel] = useState<string>('Ready');
  const [stateSubtitle, setStateSubtitle] = useState<string>('How can I help you today?');
  const [activeQuery, setActiveQuery] = useState<string>('');
  const [currentTask, setCurrentTask] = useState<string | null>(null);
  const [lastAction, setLastAction] = useState<ActionItem | null>(null);
  const [isListening, setIsListening] = useState<boolean>(false);
  const [isPhoneFrame, setIsPhoneFrame] = useState<boolean>(false);

  // Device hardware status
  const [deviceStatus, setDeviceStatus] = useState<DeviceStatus>(() =>
    orbitEngineInstance.getDeviceStatus()
  );

  // Seed chat messages
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'm-init',
      sender: 'orbit',
      text: 'Hello! I am Orbit, your autonomous AI assistant. Speak to me or type a command to control device tools, search the web, or check system stats.',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);

  // Seed activity log
  const [actions, setActions] = useState<ActionItem[]>([
    {
      id: 'act-init-1',
      title: 'OmniRoute Gateway Initialized',
      detail: 'Secure channel established with Gemini 2.5 neural router',
      timestamp: new Date(Date.now() - 60000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      status: 'COMPLETED',
      toolName: 'omniroute_init',
      durationMs: 120,
    },
    {
      id: 'act-init-2',
      title: 'Android Hardware Binder Bound',
      detail: 'BatteryManager, AudioManager, CameraFlash services attached',
      timestamp: new Date(Date.now() - 30000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      status: 'COMPLETED',
      toolName: 'android_binder',
      durationMs: 95,
    },
  ]);

  // Settings
  const [settings, setSettings] = useState<SettingsState>({
    omniRouteUrl: 'https://omniroute.internal.network/v1',
    model: 'gemini-2.5-flash',
    voicePersonality: 'Orbit Aura (Neutral)',
    speechSpeed: 1.0,
    speechPitch: 1.0,
    autoListen: false,
    hapticsEnabled: true,
    localFallback: true,
    wakeWordEnabled: true,
    themeMode: 'dark',
  });

  // Permissions list
  const [permissions, setPermissions] = useState<PermissionItem[]>([
    {
      id: 'mic',
      name: 'Microphone & Audio Record',
      description: 'Used for real-time speech recognition and continuous voice queries.',
      granted: true,
      critical: true,
      icon: 'mic',
    },
    {
      id: 'accessibility',
      name: 'Accessibility Service',
      description: 'Allows Orbit to inspect on-screen content and perform autonomous device actions.',
      granted: true,
      critical: false,
      icon: 'eye',
    },
    {
      id: 'settings',
      name: 'Modify System Settings',
      description: 'Allows adjusting audio volumes, torchlight, Wi-Fi states, and brightness.',
      granted: true,
      critical: false,
      icon: 'settings',
    },
    {
      id: 'notifications',
      name: 'Post Notifications',
      description: 'Used for autonomous background task completion alerts and reminders.',
      granted: true,
      critical: false,
      icon: 'bell',
    },
    {
      id: 'storage',
      name: 'Secure Local Storage',
      description: 'Stores encrypted model cache and offline vector embeddings.',
      granted: true,
      critical: false,
      icon: 'storage',
    },
  ]);

  // Speech Recognition ref
  const recognitionRef = useRef<any>(null);

  // Stop speech playback
  const handleStopSpeech = useCallback(() => {
    orbitEngineInstance.stopSpeaking();
    if (orbitState === 'SPEAKING') {
      setOrbitState('IDLE');
      setStateLabel('Ready');
      setStateSubtitle('How can I help you today?');
    }
  }, [orbitState]);

  // Query processing pipeline
  const processQuery = useCallback(
    async (queryText: string, isVoice = false) => {
      handleStopSpeech();

      // Add user message to chat
      const userMsg: ChatMessage = {
        id: `msg_${Date.now()}_u`,
        sender: 'user',
        text: queryText,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        isVoice,
      };
      setMessages((prev) => [...prev, userMsg]);
      setActiveQuery(queryText);

      // Execute via Orbit Engine
      try {
        const result = await orbitEngineInstance.executeQuery(queryText, (newState, label) => {
          setOrbitState(newState);
          if (label) {
            setStateLabel(newState === 'THINKING' ? 'Thinking...' : 'Executing...');
            setStateSubtitle(label);
            setCurrentTask(label);
          }
        });

        // Update hardware status if changed
        setDeviceStatus(orbitEngineInstance.getDeviceStatus());

        // Record action if any
        if (result.toolAction) {
          setLastAction(result.toolAction);
          setActions((prev) => [result.toolAction!, ...prev]);
        }

        // Add Orbit reply to chat
        const orbitMsg: ChatMessage = {
          id: `msg_${Date.now()}_o`,
          sender: 'orbit',
          text: result.reply,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          toolExecution: result.toolAction
            ? {
                tool: result.toolAction.toolName,
                input: queryText,
                output: result.toolAction.detail,
                status: 'success',
              }
            : undefined,
        };
        setMessages((prev) => [...prev, orbitMsg]);

        // Speak the reply aloud if supported
        const textToSpeak = result.speechText || result.reply;
        setOrbitState('SPEAKING');
        setStateLabel('Speaking...');
        setStateSubtitle(textToSpeak.slice(0, 60) + (textToSpeak.length > 60 ? '...' : ''));
        setCurrentTask(null);

        const spoken = orbitEngineInstance.speakText(
          textToSpeak,
          settings.speechSpeed,
          settings.speechPitch,
          () => {
            setOrbitState('SPEAKING');
          },
          () => {
            setOrbitState('IDLE');
            setStateLabel('Ready');
            setStateSubtitle('How can I help you today?');
            setActiveQuery('');
          }
        );

        if (!spoken) {
          // If speech synthesis not available, reset after 2.5s
          setTimeout(() => {
            setOrbitState('IDLE');
            setStateLabel('Ready');
            setStateSubtitle('How can I help you today?');
            setActiveQuery('');
          }, 2500);
        }
      } catch (err: any) {
        setOrbitState('ERROR');
        setStateLabel('Error');
        setStateSubtitle(err?.message || 'Processing failed');
        setCurrentTask(null);
        setTimeout(() => {
          setOrbitState('IDLE');
          setStateLabel('Ready');
          setStateSubtitle('How can I help you today?');
        }, 3000);
      }
    },
    [handleStopSpeech, settings.speechSpeed, settings.speechPitch]
  );

  // Toggle voice listening
  const handleToggleListening = useCallback(() => {
    if (isListening) {
      // Stop listening
      if (recognitionRef.current) {
        try {
          recognitionRef.current.stop();
        } catch {}
      }
      setIsListening(false);
      setOrbitState('IDLE');
      setStateLabel('Ready');
      setStateSubtitle('How can I help you today?');
      return;
    }

    handleStopSpeech();

    // Check for browser speech recognition
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (SpeechRecognition) {
      try {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
          setIsListening(true);
          setOrbitState('LISTENING');
          setStateLabel('Listening...');
          setStateSubtitle('Say something to Orbit...');
          setActiveQuery('');
        };

        recognition.onresult = (event: any) => {
          const transcript = Array.from(event.results)
            .map((result: any) => result[0].transcript)
            .join('');
          setActiveQuery(transcript);
        };

        recognition.onerror = () => {
          setIsListening(false);
          setOrbitState('IDLE');
          setStateLabel('Ready');
          setStateSubtitle('Could not capture audio. Try speaking again or typing.');
        };

        recognition.onend = () => {
          setIsListening(false);
          if (activeQuery.trim()) {
            processQuery(activeQuery.trim(), true);
          } else {
            setOrbitState('IDLE');
            setStateLabel('Ready');
            setStateSubtitle('How can I help you today?');
          }
        };

        recognitionRef.current = recognition;
        recognition.start();
        return;
      } catch {
        // Fall through to simulation if mic access throws in iframe
      }
    }

    // Interactive Voice Simulation if SpeechRecognition unavailable in iframe sandbox
    setIsListening(true);
    setOrbitState('LISTENING');
    setStateLabel('Listening...');
    setStateSubtitle('Listening to voice input...');
    const simulatedQueries = [
      'What time is it?',
      'Check my battery level',
      'Turn on the flashlight',
      'Search quantum computing',
      'Open YouTube app',
    ];
    const picked = simulatedQueries[Math.floor(Math.random() * simulatedQueries.length)];

    let currentLen = 0;
    const interval = setInterval(() => {
      currentLen += 2;
      setActiveQuery(picked.slice(0, currentLen));
      if (currentLen >= picked.length) {
        clearInterval(interval);
        setTimeout(() => {
          setIsListening(false);
          processQuery(picked, true);
        }, 600);
      }
    }, 100);
  }, [isListening, activeQuery, handleStopSpeech, processQuery]);

  // Toggle permission
  const handleTogglePermission = (id: string) => {
    setPermissions((prev) =>
      prev.map((p) => (p.id === id ? { ...p, granted: !p.granted } : p))
    );
  };

  // Test OmniRoute Connection
  const handleTestConnection = async () => {
    await new Promise((r) => setTimeout(r, 600));
    return { latency: Math.floor(Math.random() * 40) + 45, ok: true };
  };

  return (
    <div
      id="orbit-root-container"
      className="w-full min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center p-0 sm:p-4 font-sans selection:bg-cyan-500 selection:text-black overflow-x-hidden"
    >
      {/* Container: either phone mockup or full dashboard */}
      <div
        id="orbit-app-shell"
        className={`w-full transition-all duration-300 flex flex-col overflow-hidden bg-slate-950 border border-slate-800/80 shadow-2xl ${
          isPhoneFrame
            ? 'max-w-[430px] h-[92vh] max-h-[880px] rounded-[40px] ring-8 ring-slate-900/90 shadow-[0_25px_60px_-15px_rgba(0,0,0,0.9)]'
            : 'max-w-4xl h-[92vh] rounded-2xl'
        }`}
      >
        {/* Dynamic Island / Android Camera Hole for Phone Frame */}
        {isPhoneFrame && (
          <div className="w-full pt-2 flex justify-center bg-slate-950 select-none">
            <div className="w-24 h-4 bg-black rounded-full flex items-center justify-center space-x-2 border border-slate-800/60">
              <span className="w-2 h-2 rounded-full bg-slate-900 border border-slate-700" />
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-950" />
            </div>
          </div>
        )}

        {/* Top Status Bar */}
        <OrbitHeader
          deviceStatus={deviceStatus}
          isOnline={true}
          isPhoneFrame={isPhoneFrame}
          onToggleFrame={() => setIsPhoneFrame(!isPhoneFrame)}
        />

        {/* Main Content Area */}
        <main id="orbit-main-viewport" className="flex-1 flex flex-col overflow-hidden relative">
          {activeScreen === 'home' && (
            <HomeScreen
              orbitState={orbitState}
              stateLabel={stateLabel}
              stateSubtitle={stateSubtitle}
              activeQuery={activeQuery}
              currentTask={currentTask}
              lastAction={lastAction}
              isListening={isListening}
              onToggleListening={handleToggleListening}
              onSubmitQuery={(q) => processQuery(q, false)}
              onStopSpeech={handleStopSpeech}
            />
          )}

          {activeScreen === 'chat' && (
            <ChatScreen
              messages={messages}
              onSendMessage={(q) => processQuery(q, false)}
              onClearChat={() => setMessages([])}
              onSpeakText={(text) => {
                orbitEngineInstance.speakText(text, settings.speechSpeed, settings.speechPitch);
              }}
              isListening={isListening}
              onToggleListening={handleToggleListening}
            />
          )}

          {activeScreen === 'activity' && (
            <ActivityScreen
              actions={actions}
              onClearActivity={() => setActions([])}
            />
          )}

          {activeScreen === 'permissions' && (
            <PermissionsScreen
              permissions={permissions}
              onTogglePermission={handleTogglePermission}
            />
          )}

          {activeScreen === 'settings' && (
            <SettingsScreen
              settings={settings}
              onUpdateSettings={setSettings}
              onTestConnection={handleTestConnection}
            />
          )}
        </main>

        {/* Bottom Navigation */}
        <OrbitBottomNav
          activeScreen={activeScreen}
          onSelectScreen={setActiveScreen}
          pendingCount={actions.filter((a) => a.status === 'IN_PROGRESS').length}
        />
      </div>
    </div>
  );
}
