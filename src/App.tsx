import React, { useState } from 'react';

const cardStyle: React.CSSProperties = {
  background: 'rgba(255,255,255,0.10)',
  borderRadius: 22,
  boxShadow: '0 12px 40px 0 rgba(31, 38, 135, 0.22)',
  padding: '2.5rem 2rem 2rem 2rem',
  maxWidth: 370,
  width: '100%',
  margin: '0 auto',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  border: '1.5px solid rgba(255,255,255,0.18)',
  backdropFilter: 'blur(16px)',
  transition: 'box-shadow 0.3s, transform 0.3s',
};

const titleStyle: React.CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  width: '100%',
  marginBottom: '0.5rem',
};

const ytLogoStyle: React.CSSProperties = {
  width: 56,
  height: 56,
  background: '#ff0000',
  borderRadius: 16,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  marginBottom: 0,
  boxShadow: '0 2px 12px 0 rgba(255,0,0,0.18)',
};

const h1Style: React.CSSProperties = {
  marginBottom: 0,
  marginLeft: '0.75rem',
  fontSize: '2.1rem',
  fontWeight: 700,
  letterSpacing: '1px',
  textAlign: 'left',
  background: 'linear-gradient(90deg,#6366f1,#93333ea,#2563eb)',
  WebkitBackgroundClip: 'text',
  backgroundClip: 'text',
  color: 'transparent',
};

const subtitleStyle: React.CSSProperties = {
  color: '#fff',
  fontSize: '1.08rem',
  marginBottom: '1.2rem',
  textAlign: 'center',
  fontWeight: 500,
  opacity: 0.85,
  letterSpacing: '0.5px',
};

const helperStyle: React.CSSProperties = {
  color: '#888',
  fontSize: '0.95rem',
  marginBottom: '1.2rem',
  textAlign: 'center',
  letterSpacing: '0.2px',
};

const inputRowStyle: React.CSSProperties = {
  width: '100%',
  display: 'flex',
  flexDirection: 'column',
  gap: '0.5rem',
  marginBottom: '1.2rem',
};

const inputStyle: React.CSSProperties = {
  width: '100%',
  padding: '0.85rem 1.1rem',
  borderRadius: 10,
  border: '1.5px solid #e5e7eb',
  fontSize: '1.08rem',
  outline: 'none',
  background: 'rgba(255,255,255,0.18)',
  color: '#222',
  transition: 'border 0.2s, box-shadow 0.2s, background 0.2s',
  marginBottom: '1rem',
  boxShadow: '0 2px 8px 0 rgba(80, 0, 120, 0.07)',
  fontFamily: 'inherit',
  appearance: 'none',
  boxSizing: 'border-box',
};

const selectStyle: React.CSSProperties = {
  ...inputStyle,
  cursor: 'pointer',
  backgroundImage:
    "url(\"data:image/svg+xml,%3Csvg width='18' height='18' viewBox='0 0 20 20' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M6 8L10 12L14 8' stroke='%236366f1' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E\")",
  backgroundRepeat: 'no-repeat',
  backgroundPosition: 'right 1rem center',
  backgroundSize: '1.2em',
  paddingRight: '2.5rem',
};

const buttonStyle: React.CSSProperties = {
  width: '100%',
  padding: '0.85rem 1.1rem',
  borderRadius: 10,
  border: 'none',
  background: 'linear-gradient(90deg, #6366f1 0%, #9333ea 100%)',
  color: '#fff',
  fontSize: '1.15rem',
  fontWeight: 600,
  cursor: 'pointer',
  transition: 'background 0.2s, box-shadow 0.2s, transform 0.2s',
  marginBottom: '0.5rem',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  gap: '0.7rem',
  boxShadow: '0 2px 12px 0 rgba(99,51,234,0.13)',
  fontFamily: 'inherit',
};

const footerStyle: React.CSSProperties = {
  marginTop: '1.5rem',
  fontSize: '0.95rem',
  color: '#888',
  textAlign: 'center',
};

export default function App() {
  const [url, setUrl] = useState('');
  const [format, setFormat] = useState('mp4');
  const [quality, setQuality] = useState('720p');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDownload = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!url || !format || !quality) {
      setError('Please fill all fields.');
      return;
    }

    setIsLoading(true);

    try {
      // Change the backendUrl to your local network IP
      const backendUrl = 'http://YOUR_LOCAL_IP:5000/download';

      const response = await fetch(backendUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, format, quality }),
      });

      const contentType = response.headers.get('Content-Type') || '';

      if (!response.ok) {
        if (contentType.includes('application/json')) {
          const errorData = await response.json();
          setError(errorData.error || 'Something went wrong');
        } else {
          const text = await response.text();
          setError(`Error: ${text}`);
        }
        return;
      }

      if (contentType.includes('application/json')) {
        const json = await response.json();
        setError(json.error || 'Unexpected response format.');
        return;
      }

      const blob = await response.blob();
      const filename = `download.${format}`;
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(link.href);

    } catch (err: any) {
      setError(
        'Could not connect to the backend. Please ensure the Flask server is running on http://127.0.0.1:5000'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      width: '100vw',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'none'
    }}>
      <form
        style={cardStyle}
        onSubmit={handleDownload}
      >
        <div style={titleStyle}>
          <div style={ytLogoStyle}>
            <svg viewBox="0 0 32 32" fill="none" width={32} height={32}>
              <rect width="32" height="32" rx="8" fill="#FF0000"/>
              <polygon points="12,10 24,16 12,22" fill="#fff"/>
            </svg>
          </div>
          <h1 style={h1Style}>
            UTube Video Downloader
          </h1>
        </div>
        <div style={subtitleStyle}>Download YouTube videos instantly in HD</div>
        <div style={helperStyle}>No registration required. Free forever.</div>
        <div style={inputRowStyle}>
          <input
            type="url"
            placeholder="Paste YouTube video URL"
            required
            style={inputStyle}
            value={url}
            onChange={e => setUrl(e.target.value)}
          />
          <select
            required
            style={selectStyle}
            value={quality}
            onChange={e => setQuality(e.target.value)}
          >
            <option value="360p">360p</option>
            <option value="720p">720p</option>
            <option value="1080p">1080p (Full HD)</option>
          </select>
          <select
            required
            style={selectStyle}
            value={format}
            onChange={e => setFormat(e.target.value)}
          >
            <option value="mp4">MP4 (Video)</option>
            <option value="mp3">MP3 (Audio)</option>
          </select>
          <button
            type="submit"
            style={buttonStyle}
            disabled={isLoading}
          >
            <svg width="22" height="22" fill="none" viewBox="0 0 24 24">
              <path d="M12 3v12m0 0l-4-4m4 4l4-4M4 17v2a2 2 0 002 2h12a2 2 0 002-2v-2" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            {isLoading ? 'Downloading...' : 'Download'}
          </button>
        </div>
        {error && (
          <div style={{
            color: '#b91c1c',
            background: '#fee2e2',
            borderRadius: 8,
            padding: '0.75rem 1rem',
            marginTop: '0.5rem',
            textAlign: 'center',
            fontWeight: 500,
          }}>
            {error}
          </div>
        )}
        <div style={footerStyle}>
          @ NISHANT KUMAR all rights reserved
        </div>
      </form>
    </div>
  );
}