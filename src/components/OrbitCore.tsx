import React, { useEffect, useRef } from 'react';
import { OrbitState } from '../types';

interface OrbitCoreProps {
  state: OrbitState;
  size?: number;
  audioLevel?: number; // 0 to 1
  onClick?: () => void;
}

export const OrbitCore: React.FC<OrbitCoreProps> = ({
  state,
  size = 240,
  audioLevel = 0,
  onClick,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // State color palettes
  const getColorScheme = (st: OrbitState) => {
    switch (st) {
      case 'LISTENING':
        return {
          primary: 'rgba(168, 85, 247, 0.9)', // Purple
          secondary: 'rgba(236, 72, 153, 0.6)', // Pink
          glow: 'rgba(168, 85, 247, 0.5)',
          core: '#e879f9',
        };
      case 'THINKING':
        return {
          primary: 'rgba(245, 158, 11, 0.9)', // Amber
          secondary: 'rgba(234, 88, 12, 0.6)', // Orange
          glow: 'rgba(245, 158, 11, 0.5)',
          core: '#fde047',
        };
      case 'EXECUTING':
        return {
          primary: 'rgba(16, 185, 129, 0.9)', // Emerald
          secondary: 'rgba(6, 182, 212, 0.6)', // Cyan
          glow: 'rgba(16, 185, 129, 0.5)',
          core: '#6ee7b7',
        };
      case 'SPEAKING':
        return {
          primary: 'rgba(59, 130, 246, 0.9)', // Blue
          secondary: 'rgba(147, 51, 234, 0.6)', // Indigo
          glow: 'rgba(59, 130, 246, 0.6)',
          core: '#93c5fd',
        };
      case 'ERROR':
        return {
          primary: 'rgba(239, 68, 68, 0.9)', // Red
          secondary: 'rgba(244, 63, 94, 0.6)',
          glow: 'rgba(239, 68, 68, 0.6)',
          core: '#fca5a5',
        };
      case 'OFFLINE':
        return {
          primary: 'rgba(100, 116, 139, 0.6)', // Slate
          secondary: 'rgba(71, 85, 105, 0.4)',
          glow: 'rgba(71, 85, 105, 0.3)',
          core: '#94a3b8',
        };
      case 'IDLE':
      case 'CONNECTING':
      default:
        return {
          primary: 'rgba(6, 182, 212, 0.85)', // Cyan
          secondary: 'rgba(59, 130, 246, 0.5)', // Electric Blue
          glow: 'rgba(6, 182, 212, 0.45)',
          core: '#67e8f9',
        };
    }
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let time = 0;

    const render = () => {
      time += 0.035;
      const w = canvas.width;
      const h = canvas.height;
      const cx = w / 2;
      const cy = h / 2;
      const colors = getColorScheme(state);

      ctx.clearRect(0, 0, w, h);

      // Pulse calculations based on state and audio
      const baseRadius = (size * 0.28);
      const pulseMultiplier = state === 'LISTENING' || state === 'SPEAKING'
        ? 1 + audioLevel * 0.45 + Math.sin(time * 3) * 0.08
        : state === 'THINKING'
        ? 1 + Math.sin(time * 5) * 0.12
        : 1 + Math.sin(time * 1.5) * 0.04;

      const currentRadius = baseRadius * pulseMultiplier;

      // 1. Outermost Diffused Nebula Glow
      const outerGlow = ctx.createRadialGradient(cx, cy, currentRadius * 0.2, cx, cy, currentRadius * 2.2);
      outerGlow.addColorStop(0, colors.glow);
      outerGlow.addColorStop(0.5, colors.secondary);
      outerGlow.addColorStop(1, 'rgba(0, 0, 0, 0)');
      ctx.fillStyle = outerGlow;
      ctx.beginPath();
      ctx.arc(cx, cy, currentRadius * 2.2, 0, Math.PI * 2);
      ctx.fill();

      // 2. Multi-orbital planetary rings
      const ringCount = 3;
      for (let i = 0; i < ringCount; i++) {
        const ringRadius = currentRadius * (1.25 + i * 0.35);
        const rot = time * (0.8 - i * 0.3) * (i % 2 === 0 ? 1 : -1);

        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(rot);

        ctx.beginPath();
        ctx.ellipse(0, 0, ringRadius, ringRadius * 0.55, rot * 0.2, 0, Math.PI * 2);
        ctx.strokeStyle = i === 0 ? colors.primary : colors.secondary;
        ctx.lineWidth = 1.8;
        ctx.shadowColor = colors.glow;
        ctx.shadowBlur = 10;
        ctx.stroke();

        // Orbiting particles on the rings
        const particleAngle = time * (1.2 + i * 0.4);
        const px = Math.cos(particleAngle) * ringRadius;
        const py = Math.sin(particleAngle) * (ringRadius * 0.55);
        ctx.beginPath();
        ctx.arc(px, py, 3.5, 0, Math.PI * 2);
        ctx.fillStyle = colors.core;
        ctx.shadowBlur = 12;
        ctx.fill();

        ctx.restore();
      }

      // 3. Central Core Plasma Sphere
      const coreGradient = ctx.createRadialGradient(
        cx - currentRadius * 0.25,
        cy - currentRadius * 0.25,
        currentRadius * 0.05,
        cx,
        cy,
        currentRadius
      );
      coreGradient.addColorStop(0, '#ffffff');
      coreGradient.addColorStop(0.3, colors.core);
      coreGradient.addColorStop(0.7, colors.primary);
      coreGradient.addColorStop(1, colors.secondary);

      ctx.save();
      ctx.shadowColor = colors.glow;
      ctx.shadowBlur = 24;
      ctx.fillStyle = coreGradient;
      ctx.beginPath();
      ctx.arc(cx, cy, currentRadius, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();

      // 4. Subtle Inner Highlight / Specular
      ctx.beginPath();
      ctx.ellipse(
        cx - currentRadius * 0.3,
        cy - currentRadius * 0.3,
        currentRadius * 0.35,
        currentRadius * 0.18,
        -Math.PI / 4,
        0,
        Math.PI * 2
      );
      ctx.fillStyle = 'rgba(255, 255, 255, 0.45)';
      ctx.fill();

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, [state, size, audioLevel]);

  return (
    <div
      id="orbit-core-container"
      onClick={onClick}
      className="relative flex items-center justify-center cursor-pointer transition-transform duration-300 hover:scale-105 active:scale-95 select-none w-[250px] h-[250px]"
      title={`Orbit Status: ${state}. Click to interact.`}
    >
      <canvas
        id="orbit-core-canvas"
        ref={canvasRef}
        width={size}
        height={size}
        className="block"
      />
    </div>
  );
};
