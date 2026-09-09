import React, { useState, useRef, useEffect } from 'react';
import { ChatMessage } from '../types';
import { Bot, User, Send, Mic, Volume2, Sparkles, Terminal, Trash2 } from 'lucide-react';

interface ChatScreenProps {
  messages: ChatMessage[];
  onSendMessage: (text: string) => void;
  onClearChat: () => void;
  onSpeakText: (text: string) => void;
  isListening: boolean;
  onToggleListening: () => void;
}

export const ChatScreen: React.FC<ChatScreenProps> = ({
  messages,
  onSendMessage,
  onClearChat,
  onSpeakText,
  isListening,
  onToggleListening,
}) => {
  const [inputText, setInputText] = useState('');
  const [expandedToolId, setExpandedToolId] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim()) return;
    onSendMessage(inputText.trim());
    setInputText('');
  };

  return (
    <div id="orbit-chat-screen" className="flex-1 flex flex-col h-full overflow-hidden bg-slate-950">
      {/* Header bar */}
      <div className="px-4 py-2.5 bg-slate-900/60 border-b border-slate-800/80 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className="w-6 h-6 rounded-full bg-cyan-500/20 border border-cyan-500/40 flex items-center justify-center">
            <Bot className="w-3.5 h-3.5 text-cyan-400" />
          </div>
          <div>
            <h2 className="text-xs font-semibold text-slate-200">Orbit Conversation</h2>
            <p className="text-[10px] text-slate-400">OmniRoute Neural Channel Active</p>
          </div>
        </div>

        {messages.length > 0 && (
          <button
            id="clear-chat-button"
            onClick={onClearChat}
            className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-slate-800/60 transition-colors"
            title="Clear Chat History"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center text-slate-500 py-12">
            <Bot className="w-10 h-10 text-cyan-500/40 mb-3" />
            <p className="text-sm font-medium text-slate-400">Orbit Assistant Ready</p>
            <p className="text-xs text-slate-500 max-w-xs mt-1">
              Ask questions, give device commands, or test tools like web search and flashlight.
            </p>
          </div>
        ) : (
          messages.map((msg) => {
            const isOrbit = msg.sender === 'orbit';
            const isUser = msg.sender === 'user';

            return (
              <div
                key={msg.id}
                id={`chat-msg-${msg.id}`}
                className={`flex items-start space-x-2.5 ${
                  isUser ? 'flex-row-reverse space-x-reverse' : 'flex-row'
                }`}
              >
                {/* Avatar */}
                <div
                  className={`w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5 ${
                    isUser
                      ? 'bg-purple-600/30 border border-purple-500/40 text-purple-300'
                      : 'bg-cyan-500/20 border border-cyan-500/40 text-cyan-400'
                  }`}
                >
                  {isUser ? <User className="w-3.5 h-3.5" /> : <Bot className="w-3.5 h-3.5" />}
                </div>

                {/* Message Bubble */}
                <div className="flex flex-col max-w-[80%] space-y-1">
                  <div
                    className={`rounded-2xl px-4 py-2.5 text-xs sm:text-sm leading-relaxed ${
                      isUser
                        ? 'bg-purple-600/90 text-white rounded-tr-sm shadow-md'
                        : 'bg-slate-900 border border-slate-800 text-slate-200 rounded-tl-sm shadow'
                    }`}
                  >
                    {msg.text}

                    {/* Voice icon tag if sent via voice */}
                    {msg.isVoice && (
                      <span className="inline-block ml-2 text-[10px] text-purple-200/80 italic">
                        (voice)
                      </span>
                    )}

                    {/* Tool Execution Card if attached */}
                    {msg.toolExecution && (
                      <div className="mt-2.5 pt-2 border-t border-slate-700/60 text-xs">
                        <button
                          type="button"
                          onClick={() =>
                            setExpandedToolId(
                              expandedToolId === msg.id ? null : msg.id
                            )
                          }
                          className="w-full flex items-center justify-between p-2 rounded-lg bg-slate-800/80 hover:bg-slate-800 border border-slate-700 text-[11px] text-cyan-300 font-mono"
                        >
                          <div className="flex items-center space-x-1.5">
                            <Terminal className="w-3 h-3 text-emerald-400" />
                            <span>tool: {msg.toolExecution.tool}</span>
                          </div>
                          <span className="text-[10px] text-slate-400">
                            {expandedToolId === msg.id ? 'Hide output' : 'Show output'}
                          </span>
                        </button>

                        {expandedToolId === msg.id && (
                          <div className="mt-1.5 p-2 rounded bg-slate-950 font-mono text-[10px] text-slate-300 border border-slate-800 overflow-x-auto">
                            <div className="text-slate-500 mb-1">Input: {msg.toolExecution.input}</div>
                            <div className="text-emerald-400">Output: {msg.toolExecution.output}</div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>

                  {/* Bubble Footer with Timestamp & Speak Button */}
                  <div
                    className={`flex items-center space-x-2 text-[10px] text-slate-500 px-1 ${
                      isUser ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    <span>{msg.timestamp}</span>
                    {isOrbit && (
                      <button
                        onClick={() => onSpeakText(msg.text)}
                        className="p-1 rounded hover:bg-slate-800 text-slate-400 hover:text-cyan-400 transition-colors"
                        title="Read out loud"
                      >
                        <Volume2 className="w-3 h-3" />
                      </button>
                    )}
                  </div>
                </div>
              </div>
            );
          })
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input area */}
      <div className="p-3 bg-slate-900/90 border-t border-slate-800">
        <form onSubmit={handleSubmit} className="flex items-center space-x-2">
          <input
            id="chat-input-field"
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Type a message to Orbit..."
            className="flex-1 bg-slate-950 border border-slate-700 rounded-full px-4 py-2 text-xs sm:text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
          />

          <button
            type="button"
            id="chat-mic-button"
            onClick={onToggleListening}
            className={`p-2.5 rounded-full transition-colors ${
              isListening
                ? 'bg-purple-600 text-white animate-pulse'
                : 'bg-slate-800 text-slate-300 hover:text-cyan-300'
            }`}
            title={isListening ? 'Stop listening' : 'Speak'}
          >
            <Mic className="w-4 h-4" />
          </button>

          <button
            type="submit"
            id="chat-send-button"
            disabled={!inputText.trim()}
            className={`p-2.5 rounded-full transition-colors ${
              inputText.trim()
                ? 'bg-cyan-500 text-slate-950 hover:bg-cyan-400'
                : 'bg-slate-800 text-slate-600 cursor-not-allowed'
            }`}
            title="Send"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
};
