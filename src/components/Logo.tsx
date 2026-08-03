import React from "react";

interface LogoProps {
  className?: string;
  size?: number;
}

export const Logo: React.FC<LogoProps> = ({ className = "w-8 h-8", size = 32 }) => {
  return (
    <div className={`relative inline-flex items-center justify-center shrink-0 ${className}`}>
      <img
        src="/logo.svg"
        alt="OptiPixel Logo"
        width={size}
        height={size}
        className="w-full h-full object-contain filter drop-shadow-sm transition-transform hover:scale-105"
      />
    </div>
  );
};
